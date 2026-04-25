#!/usr/bin/env python3
"""
Generate an interactive story graph dashboard from markdown lore files.

Usage:
  python3 scripts/build_story_dashboard.py
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "dashboard" / "story-dashboard.html"
SKIP_DIRS = {"assets", "ref", ".git", ".cursor", ".agents", "dashboard", "scripts"}

FIELD_KEYS = ["region", "parent_region", "culture", "based_on"]
ASSET_REGEX = re.compile(r"(?:\./)?(assets/[^\s`)\]]+\.(?:png|jpg|jpeg|gif|webp))", re.IGNORECASE)


@dataclass
class Entry:
    id: str
    slug: str
    title: str
    category: str
    path: str
    status: str
    themes: List[str]
    related: List[str]
    raw_links: List[str]
    asset_path: str


def slugify(text: str) -> str:
    value = text.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def parse_frontmatter(text: str) -> Optional[Dict[str, object]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    i = 1
    data: Dict[str, object] = {}
    current_key: Optional[str] = None
    list_mode = False
    list_values: List[str] = []

    while i < len(lines):
        line = lines[i]
        i += 1
        stripped = line.strip()

        if stripped == "---":
            if current_key and list_mode:
                data[current_key] = list_values
            break

        if not stripped:
            continue

        if line.startswith("  - ") and current_key and list_mode:
            list_values.append(line.split("-", 1)[1].strip())
            continue

        # finalize previous list key when moving on
        if current_key and list_mode:
            data[current_key] = list_values
            list_values = []
            list_mode = False

        if ":" not in line:
            continue

        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()

        if value == "":
            current_key = key
            list_mode = True
            list_values = []
            continue

        current_key = key
        if value.startswith("[") and value.endswith("]"):
            maybe_items = [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
            data[key] = maybe_items
        else:
            data[key] = value

    return data


def extract_asset_path(text: str) -> str:
    match = ASSET_REGEX.search(text)
    if not match:
        return ""
    candidate = match.group(1).strip()
    normalized = candidate.replace("\\", "/")
    asset_file = ROOT / normalized
    if asset_file.exists():
        return normalized
    return ""


def extract_entry(path: Path) -> Optional[Entry]:
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    if not frontmatter:
        return None

    title = str(frontmatter.get("name") or path.stem.replace("-", " ").title()).strip()
    category = str(frontmatter.get("category") or path.parent.name.rstrip("s")).strip() or "unknown"
    status = str(frontmatter.get("status") or "").strip()

    related = frontmatter.get("related") or []
    if isinstance(related, str):
        related = [related]
    related_values = [str(v).strip() for v in related if str(v).strip()]

    themes = frontmatter.get("themes") or []
    if isinstance(themes, str):
        themes = [themes]
    theme_values = [str(v).strip() for v in themes if str(v).strip()]

    raw_links: List[str] = []
    for key in FIELD_KEYS:
        val = frontmatter.get(key)
        if not val:
            continue
        if isinstance(val, list):
            raw_links.extend([str(v).strip() for v in val if str(v).strip()])
        else:
            raw_links.append(str(val).strip())

    ident = f"{category}:{slugify(title)}"
    rel_path = path.relative_to(ROOT).as_posix()
    return Entry(
        id=ident,
        slug=slugify(title),
        title=title,
        category=category,
        path=rel_path,
        status=status,
        themes=theme_values,
        related=related_values,
        raw_links=raw_links,
        asset_path=extract_asset_path(text),
    )


def discover_entries() -> List[Entry]:
    entries: List[Entry] = []
    for md_file in ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in md_file.parts):
            continue
        entry = extract_entry(md_file)
        if entry:
            entries.append(entry)
    entries.sort(key=lambda e: (e.category, e.title))
    return entries


def build_graph_payload(entries: List[Entry]) -> Dict[str, object]:
    title_index = {e.title.lower(): e.id for e in entries}
    slug_index = {e.slug: e.id for e in entries}
    nodes = []
    edges = []
    edge_keys = set()

    for e in entries:
        nodes.append(
            {
                "id": e.id,
                "label": e.title,
                "category": e.category,
                "status": e.status or "unspecified",
                "themes": e.themes,
                "path": e.path,
                "asset_path": e.asset_path,
            }
        )

    for e in entries:
        candidates = e.related + e.raw_links
        for raw_target in candidates:
            key = raw_target.lower().strip()
            target = title_index.get(key) or slug_index.get(slugify(raw_target))
            if not target or target == e.id:
                continue
            dedupe_key = tuple(sorted((e.id, target)))
            if dedupe_key in edge_keys:
                continue
            edge_keys.add(dedupe_key)
            edges.append(
                {
                    "source": e.id,
                    "target": target,
                }
            )

    return {"nodes": nodes, "edges": edges}


def render_html(payload: Dict[str, object]) -> str:
    data_json = json.dumps(payload, ensure_ascii=True)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Story Graph</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #0b1020;
      --panel: #111833;
      --ink: #e7ecff;
      --muted: #9da7cc;
      --line: #3b4b85;
      --accent: #86a8ff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
      color: var(--ink);
      background: radial-gradient(circle at 20% 10%, #1a2451 0%, var(--bg) 45%);
      height: 100vh;
      display: grid;
      grid-template-columns: 320px 1fr;
      gap: 12px;
      padding: 12px;
      overflow: hidden;
    }}
    aside, main {{
      background: color-mix(in srgb, var(--panel) 92%, black);
      border: 1px solid color-mix(in srgb, var(--line) 55%, black);
      border-radius: 12px;
      min-height: 0;
    }}
    aside {{
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    h1 {{ margin: 0; font-size: 1.05rem; }}
    .muted {{ color: var(--muted); font-size: 0.88rem; margin-top: 4px; }}
    label {{ display: grid; gap: 6px; font-size: 0.85rem; color: var(--muted); }}
    label.tight {{ gap: 1px; }}
    input, select {{
      width: 100%;
      border: 1px solid #3b4b85;
      border-radius: 8px;
      background: #0f1430;
      color: var(--ink);
      padding: 8px 10px;
      outline: none;
    }}
    input[type="range"] {{
      margin: 0;
      padding: 0;
      height: 22px;
    }}
    .category-tools {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: var(--muted);
      font-size: 0.85rem;
    }}
    .category-actions {{
      display: flex;
      gap: 6px;
    }}
    .tiny-btn {{
      border: 1px solid #3b4b85;
      border-radius: 7px;
      background: #121a3f;
      color: var(--ink);
      padding: 4px 8px;
      font-size: 0.75rem;
      cursor: pointer;
    }}
    .tiny-btn:hover {{
      background: #1a2755;
    }}
    #category-list {{
      max-height: 160px;
      overflow: auto;
      border: 1px solid #384574;
      border-radius: 8px;
      background: #101735;
      padding: 6px;
      display: grid;
      gap: 4px;
    }}
    .cat-item {{
      display: flex;
      align-items: center;
      gap: 8px;
      color: #d8e0ff;
      font-size: 0.82rem;
      justify-content: space-between;
    }}
    .cat-item-left {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .cat-item input[type="checkbox"] {{
      width: auto;
      padding: 0;
      margin: 0;
      accent-color: #86a8ff;
    }}
    .cat-color-dot {{
      width: 10px;
      height: 10px;
      border-radius: 999px;
      border: 1px solid rgba(255, 255, 255, 0.45);
      flex: 0 0 auto;
    }}
    #selected {{
      border: 1px solid #384574;
      border-radius: 10px;
      padding: 10px;
      font-size: 0.86rem;
      background: #101735;
      overflow: auto;
      flex: 1;
      min-height: 140px;
    }}
    #artwork-preview {{
      border: 1px solid #384574;
      border-radius: 10px;
      background: #101735;
      overflow: hidden;
      display: none;
    }}
    #artwork-preview.visible {{ display: block; }}
    #artwork-preview-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 10px;
      border-bottom: 1px solid #2b3a68;
      color: #dbe4ff;
      font-size: 0.8rem;
    }}
    #artwork-preview-close {{
      border: 1px solid #4b5e9d;
      background: #1a2755;
      color: #fff;
      border-radius: 6px;
      width: 22px;
      height: 22px;
      line-height: 18px;
      cursor: pointer;
      font-size: 0.85rem;
      padding: 0;
    }}
    #artwork-preview-media {{
      width: 100%;
      max-height: 190px;
      object-fit: contain;
      display: block;
      background: #0c1230;
    }}
    .k {{ color: var(--muted); display: block; font-size: 0.75rem; }}
    .v {{ display: block; margin-bottom: 8px; }}
    #stats {{ color: var(--muted); font-size: 0.8rem; }}
    main {{ position: relative; overflow: hidden; }}
    #graph {{ width: 100%; height: 100%; display: block; }}
    #graph.panning {{ cursor: grabbing; }}
    #graph.pan-ready {{ cursor: grab; }}
    .node {{ cursor: pointer; stroke: #0a102b; stroke-width: 1.25px; }}
    .node.dim {{ opacity: 0.08; }}
    .node.selected {{ stroke: #f2f5ff; stroke-width: 2.2px; opacity: 1; }}
    .node.connected {{ opacity: 0.95; }}
    .edge {{ stroke: #425393; stroke-opacity: 0.65; stroke-width: 1.1; }}
    .edge.dim {{ opacity: 0.05; }}
    .edge.connected {{ stroke: #8fa9ff; stroke-opacity: 0.9; stroke-width: 1.45; }}
    .label {{
      font-size: 10px;
      fill: #dbe4ff;
      pointer-events: auto;
      cursor: pointer;
      text-shadow: 0 0 4px #000;
    }}
    .label.dim {{ opacity: 0.06; }}
    .label.selected {{ opacity: 1; fill: #ffffff; }}
    .label.connected {{ opacity: 0.95; }}
    .sub-label {{
      font-size: 8px;
      fill: #9da7cc;
      pointer-events: auto;
      cursor: pointer;
      letter-spacing: 0.02em;
      text-transform: uppercase;
    }}
    .sub-label.dim {{ opacity: 0.08; }}
    .sub-label.selected {{ opacity: 1; fill: #cfd8ff; }}
    .sub-label.connected {{ opacity: 0.9; }}
  </style>
</head>
<body>
  <aside>
    <div>
      <h1>Story Graph</h1>
      <div class="muted">Generated from lore markdown frontmatter.</div>
    </div>
    <label>
      Search
      <input id="search" placeholder="name, theme, path..." />
    </label>
    <div class="category-tools">
      <span>Categories</span>
      <div class="category-actions">
        <button id="select-all-categories" class="tiny-btn" type="button">Select All</button>
        <button id="deselect-all-categories" class="tiny-btn" type="button">Deselect All</button>
      </div>
    </div>
    <div id="category-list"></div>
    <label class="tight">
      Node spacing
      <input id="spacing" type="range" min="70" max="340" step="1" value="130" />
    </label>
    <div id="artwork-preview">
      <div id="artwork-preview-header">
        <span id="artwork-preview-title">Artwork Preview</span>
        <button id="artwork-preview-close" type="button" aria-label="Close artwork preview">x</button>
      </div>
      <img id="artwork-preview-media" alt="Artwork preview" />
    </div>
    <div id="selected">Click a node to inspect details.</div>
    <div id="stats"></div>
  </aside>
  <main>
    <svg id="graph" viewBox="0 0 2200 1600" preserveAspectRatio="xMidYMid meet"></svg>
  </main>
  <script>
    const graph = {data_json};
    const svg = document.getElementById('graph');
    const searchInput = document.getElementById('search');
    const categoryList = document.getElementById('category-list');
    const selectAllCategoriesBtn = document.getElementById('select-all-categories');
    const deselectAllCategoriesBtn = document.getElementById('deselect-all-categories');
    const selectedEl = document.getElementById('selected');
    const statsEl = document.getElementById('stats');
    const spacingInput = document.getElementById('spacing');
    const artworkPreviewEl = document.getElementById('artwork-preview');
    const artworkPreviewTitleEl = document.getElementById('artwork-preview-title');
    const artworkPreviewMediaEl = document.getElementById('artwork-preview-media');
    const artworkPreviewCloseEl = document.getElementById('artwork-preview-close');

    // Canonical Story Architect categories + defaults.
    const canonicalColors = {{
      world: '#6ea8ff',
      region: '#f48fb1',
      rule: '#8dd3c7',
      culture: '#80cbc4',
      inhabitant: '#ffd180',
      artifact: '#ce93d8',
      symbol: '#ffcc80',
      myth: '#b0bec5',
      story: '#90caf9',
      artwork: '#ffab91',
      phenomenon: '#a5d6a7',
      unknown: '#90a4ae',
    }};

    function fallbackColorForCategory(category) {{
      // Deterministic HSL so unknown/new categories always get a stable color.
      let hash = 0;
      for (let i = 0; i < category.length; i += 1) {{
        hash = (hash * 31 + category.charCodeAt(i)) | 0;
      }}
      const hue = Math.abs(hash) % 360;
      return `hsl(${{hue}} 70% 70%)`;
    }}

    function colorForCategory(category) {{
      return canonicalColors[category] || fallbackColorForCategory(category || 'unknown');
    }}

    const categories = [...new Set(graph.nodes.map(n => n.category))].sort();
    const selectedCategories = new Set(categories);
    for (const c of categories) {{
      const row = document.createElement('label');
      row.className = 'cat-item';
      const left = document.createElement('span');
      left.className = 'cat-item-left';
      const box = document.createElement('input');
      box.type = 'checkbox';
      box.value = c;
      box.checked = true;
      box.addEventListener('change', () => {{
        if (box.checked) selectedCategories.add(c);
        else selectedCategories.delete(c);
        applyFilters();
      }});
      const text = document.createElement('span');
      text.textContent = c;
      const dot = document.createElement('span');
      dot.className = 'cat-color-dot';
      dot.style.background = colorForCategory(c);
      left.append(box, text);
      row.append(left, dot);
      categoryList.appendChild(row);
    }}

    const width = 2200;
    const height = 1600;
    const radiusByCategory = (c) => (c === 'world' ? 9 : c === 'region' ? 7.5 : 6);
    const nodeById = new Map(graph.nodes.map(n => [n.id, n]));
    const graphRoot = document.createElementNS('http://www.w3.org/2000/svg', 'g');

    const startRadius = Math.max(500, Math.min(820, graph.nodes.length * 5.1));
    graph.nodes.forEach((n, i) => {{
      const angle = (i / graph.nodes.length) * Math.PI * 2;
      n.x = width / 2 + Math.cos(angle) * startRadius + (Math.random() - 0.5) * 70;
      n.y = height / 2 + Math.sin(angle) * startRadius + (Math.random() - 0.5) * 70;
      n.vx = 0;
      n.vy = 0;
      n.r = radiusByCategory(n.category);
      n.color = colorForCategory(n.category);
    }});

    const edgeGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    const nodeGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    const labelGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    graphRoot.append(edgeGroup, nodeGroup, labelGroup);
    svg.append(graphRoot);

    const edgeEls = [];
    for (const e of graph.edges) {{
      const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      line.setAttribute('class', 'edge');
      edgeGroup.appendChild(line);
      edgeEls.push([e, line]);
    }}

    const nodeEls = [];
    const labelEls = [];
    const subLabelEls = [];
    for (const n of graph.nodes) {{
      const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circle.setAttribute('class', 'node');
      circle.setAttribute('r', String(n.r));
      circle.setAttribute('fill', n.color);
      circle.setAttribute('data-node-id', n.id);
      nodeGroup.appendChild(circle);
      nodeEls.push([n, circle]);

      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('class', 'label');
      text.textContent = n.label;
      text.setAttribute('data-node-id', n.id);
      labelGroup.appendChild(text);
      labelEls.push([n, text]);

      const sub = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      sub.setAttribute('class', 'sub-label');
      sub.textContent = n.category;
      sub.setAttribute('data-node-id', n.id);
      labelGroup.appendChild(sub);
      subLabelEls.push([n, sub]);
    }}

    let selectedNodeId = null;
    let dragPan = null;
    let isSpacePressed = false;
    let suppressBackgroundClickOnce = false;
    let hiddenArtworkForNodeId = null;
    let filterText = '';
    let spacingStrength = Number(spacingInput.value);
    let scale = 1;
    let offsetX = 0;
    let offsetY = 0;
    const MIN_SCALE = 0.34;
    const MAX_SCALE = 2.8;
    let simulationEnergy = 1.0;
    const MIN_SIM_ENERGY = 0.012;
    let settledFrames = 0;
    const SETTLE_FRAMES_REQUIRED = 20;

    function clamp(v, min, max) {{
      return Math.max(min, Math.min(max, v));
    }}

    function neighbors(id) {{
      const ids = new Set([id]);
      for (const e of graph.edges) {{
        if (e.source === id) ids.add(e.target);
        if (e.target === id) ids.add(e.source);
      }}
      return ids;
    }}

    function setSelected(id) {{
      selectedNodeId = id;
      const n = nodeById.get(id);
      if (hiddenArtworkForNodeId !== id) {{
        renderArtworkPreview(n);
      }}
      const themeText = n.themes.length ? n.themes.join(', ') : 'none';
      selectedEl.innerHTML = `
        <span class="k">Name</span><span class="v">${{n.label}}</span>
        <span class="k">Category</span><span class="v">${{n.category}}</span>
        <span class="k">Status</span><span class="v">${{n.status}}</span>
        <span class="k">Themes</span><span class="v">${{themeText}}</span>
        <span class="k">File</span><span class="v"><code>${{n.path}}</code></span>
      `;
      applyFilters();
    }}

    function clearSelection() {{
      selectedNodeId = null;
      selectedEl.innerHTML = 'Click a node to inspect details.';
      hideArtworkPreview();
      applyFilters();
    }}

    function assetUrlFromPath(assetPath) {{
      if (!assetPath) return '';
      return `../${{assetPath}}`;
    }}

    function hideArtworkPreview() {{
      artworkPreviewEl.classList.remove('visible');
      artworkPreviewMediaEl.removeAttribute('src');
    }}

    function renderArtworkPreview(node) {{
      if (!node || node.category !== 'artwork' || !node.asset_path) {{
        hideArtworkPreview();
        return;
      }}
      artworkPreviewTitleEl.textContent = node.label;
      artworkPreviewMediaEl.src = assetUrlFromPath(node.asset_path);
      artworkPreviewEl.classList.add('visible');
    }}

    function matchNode(n) {{
      if (!selectedCategories.has(n.category)) return false;
      if (!filterText) return true;
      const hay = `${{n.label}} ${{n.category}} ${{n.path}} ${{n.themes.join(' ')}}`.toLowerCase();
      return hay.includes(filterText);
    }}

    function applyFilters() {{
      const visibleNodeIds = new Set(graph.nodes.filter(matchNode).map(n => n.id));
      const neighborIds = selectedNodeId ? neighbors(selectedNodeId) : null;

      for (const [n, el] of nodeEls) {{
        const isVisible = visibleNodeIds.has(n.id);
        const shouldDim = !isVisible || (neighborIds && !neighborIds.has(n.id));
        const isSelected = selectedNodeId === n.id;
        const isConnected = !!(neighborIds && !isSelected && neighborIds.has(n.id));
        el.classList.toggle('dim', shouldDim);
        el.classList.toggle('selected', isSelected && isVisible);
        el.classList.toggle('connected', isConnected && isVisible);
        el.style.display = isVisible ? 'block' : 'none';
      }}

      for (const [n, el] of labelEls) {{
        const isVisible = visibleNodeIds.has(n.id);
        const shouldDim = !isVisible || (neighborIds && !neighborIds.has(n.id));
        const isSelected = selectedNodeId === n.id;
        const isConnected = !!(neighborIds && !isSelected && neighborIds.has(n.id));
        el.classList.toggle('dim', shouldDim);
        el.classList.toggle('selected', isSelected && isVisible);
        el.classList.toggle('connected', isConnected && isVisible);
        el.style.display = isVisible ? 'block' : 'none';
      }}
      for (const [n, el] of subLabelEls) {{
        const isVisible = visibleNodeIds.has(n.id);
        const shouldDim = !isVisible || (neighborIds && !neighborIds.has(n.id));
        const isSelected = selectedNodeId === n.id;
        const isConnected = !!(neighborIds && !isSelected && neighborIds.has(n.id));
        el.classList.toggle('dim', shouldDim);
        el.classList.toggle('selected', isSelected && isVisible);
        el.classList.toggle('connected', isConnected && isVisible);
        el.style.display = isVisible ? 'block' : 'none';
      }}

      let visibleEdges = 0;
      for (const [e, el] of edgeEls) {{
        const sourceVisible = visibleNodeIds.has(e.source);
        const targetVisible = visibleNodeIds.has(e.target);
        const visible = sourceVisible && targetVisible;
        if (visible) visibleEdges += 1;
        const isConnected = !!(selectedNodeId && visible && (e.source === selectedNodeId || e.target === selectedNodeId));
        const shouldDim = !visible || (selectedNodeId && !isConnected);
        el.classList.toggle('dim', shouldDim);
        el.classList.toggle('connected', isConnected);
        el.style.display = visible ? 'block' : 'none';
      }}

      statsEl.textContent = `${{visibleNodeIds.size}} visible nodes, ${{visibleEdges}} visible links`;
    }}

    function applyTransform() {{
      graphRoot.setAttribute('transform', `translate(${{offsetX}} ${{offsetY}}) scale(${{scale}})`);
    }}

    function toWorld(screenX, screenY) {{
      return {{
        x: (screenX - offsetX) / scale,
        y: (screenY - offsetY) / scale,
      }};
    }}

    function zoomAt(factor, sx, sy) {{
      const nextScale = clamp(scale * factor, MIN_SCALE, MAX_SCALE);
      if (nextScale === scale) return;
      const wx = (sx - offsetX) / scale;
      const wy = (sy - offsetY) / scale;
      scale = nextScale;
      offsetX = sx - wx * scale;
      offsetY = sy - wy * scale;
      applyTransform();
    }}

    function tick() {{
      if (simulationEnergy <= MIN_SIM_ENERGY) return;
      let totalMotion = 0;

      for (const e of graph.edges) {{
        const a = nodeById.get(e.source);
        const b = nodeById.get(e.target);
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const dist = Math.max(1, Math.hypot(dx, dy));
        const ideal = spacingStrength;
        const force = (dist - ideal) * (0.0028 * simulationEnergy);
        const fx = (dx / dist) * force;
        const fy = (dy / dist) * force;
        a.vx += fx; a.vy += fy;
        b.vx -= fx; b.vy -= fy;
      }}

      for (let i = 0; i < graph.nodes.length; i++) {{
        for (let j = i + 1; j < graph.nodes.length; j++) {{
          const a = graph.nodes[i];
          const b = graph.nodes[j];
          const dx = b.x - a.x;
          const dy = b.y - a.y;
          const dist = Math.max(1, Math.hypot(dx, dy));
          const minDist = a.r + b.r + (spacingStrength * 0.5);
          if (dist < minDist) {{
            const push = (minDist - dist) * (0.06 * simulationEnergy);
            const px = (dx / dist) * push;
            const py = (dy / dist) * push;
            a.vx -= px; a.vy -= py;
            b.vx += px; b.vy += py;
          }}
        }}
      }}

      for (const n of graph.nodes) {{
        const dx = width / 2 - n.x;
        const dy = height / 2 - n.y;
        n.vx += dx * (0.00013 * simulationEnergy);
        n.vy += dy * (0.00013 * simulationEnergy);
        n.vx *= 0.82;
        n.vy *= 0.82;
        if (Math.abs(n.vx) < 0.003) n.vx = 0;
        if (Math.abs(n.vy) < 0.003) n.vy = 0;
        n.x += n.vx;
        n.y += n.vy;
        n.x = clamp(n.x, n.r + 16, width - n.r - 16);
        n.y = clamp(n.y, n.r + 16, height - n.r - 16);
        totalMotion += Math.abs(n.vx) + Math.abs(n.vy);
      }}

      // Cool the simulation so nodes settle and stop jiggling.
      simulationEnergy *= 0.992;
      if (simulationEnergy < MIN_SIM_ENERGY) simulationEnergy = MIN_SIM_ENERGY;

      if (totalMotion < graph.nodes.length * 0.01) {{
        settledFrames += 1;
      }} else {{
        settledFrames = 0;
      }}

      // Hard-stop micro motion once layout is stable.
      if (settledFrames >= SETTLE_FRAMES_REQUIRED) {{
        simulationEnergy = MIN_SIM_ENERGY;
        for (const n of graph.nodes) {{
          n.vx = 0;
          n.vy = 0;
        }}
      }}
    }}

    function render() {{
      for (const [e, line] of edgeEls) {{
        const a = nodeById.get(e.source);
        const b = nodeById.get(e.target);
        line.setAttribute('x1', a.x);
        line.setAttribute('y1', a.y);
        line.setAttribute('x2', b.x);
        line.setAttribute('y2', b.y);
      }}
      for (const [n, circle] of nodeEls) {{
        circle.setAttribute('cx', n.x);
        circle.setAttribute('cy', n.y);
      }}
      for (const [n, text] of labelEls) {{
        text.setAttribute('x', n.x + n.r + 2);
        text.setAttribute('y', n.y + 3);
      }}
      for (const [n, text] of subLabelEls) {{
        text.setAttribute('x', n.x + n.r + 2);
        text.setAttribute('y', n.y + 12);
      }}
    }}

    function frame() {{
      tick();
      render();
      requestAnimationFrame(frame);
    }}

    function pickNodeFromPoint(x, y) {{
      for (const n of graph.nodes) {{
        const dx = n.x - x;
        const dy = n.y - y;
        if (Math.hypot(dx, dy) <= n.r + 9) return n;
      }}
      return null;
    }}

    const toLocal = (evt) => {{
      const rect = svg.getBoundingClientRect();
      const sx = width / rect.width;
      const sy = height / rect.height;
      const screenX = (evt.clientX - rect.left) * sx;
      const screenY = (evt.clientY - rect.top) * sy;
      return toWorld(screenX, screenY);
    }};

    svg.addEventListener('pointerdown', (evt) => {{
      simulationEnergy = 1.0;
      settledFrames = 0;
      const wantsPan = evt.button === 1 || (evt.button === 0 && isSpacePressed);
      if (!wantsPan) return;
      const clickedNodeId = evt.target && evt.target.getAttribute ? evt.target.getAttribute('data-node-id') : null;
      if (!clickedNodeId) {{
        evt.preventDefault();
        dragPan = {{ x: evt.clientX, y: evt.clientY }};
        svg.classList.add('panning');
        svg.setPointerCapture(evt.pointerId);
      }}
    }});

    svg.addEventListener('pointermove', (evt) => {{
      if (dragPan) {{
        const rect = svg.getBoundingClientRect();
        const sx = width / rect.width;
        const sy = height / rect.height;
        offsetX += (evt.clientX - dragPan.x) * sx;
        offsetY += (evt.clientY - dragPan.y) * sy;
        dragPan = {{ x: evt.clientX, y: evt.clientY }};
        suppressBackgroundClickOnce = true;
        applyTransform();
      }}
    }});

    svg.addEventListener('pointerup', (evt) => {{
      dragPan = null;
      svg.classList.remove('panning');
      try {{ svg.releasePointerCapture(evt.pointerId); }} catch (_err) {{}}
    }});

    svg.addEventListener('pointercancel', () => {{
      dragPan = null;
      svg.classList.remove('panning');
    }});

    svg.addEventListener('wheel', (evt) => {{
      evt.preventDefault();
      const rect = svg.getBoundingClientRect();
      const sx = width / rect.width;
      const sy = height / rect.height;
      const cx = (evt.clientX - rect.left) * sx;
      const cy = (evt.clientY - rect.top) * sy;
      const factor = evt.deltaY < 0 ? 1.1 : 0.9;
      zoomAt(factor, cx, cy);
    }}, {{ passive: false }});

    function centerView() {{
      // Start with the graph centered in the viewport.
      scale = 1;
      offsetX = 0;
      offsetY = 0;
      applyTransform();
    }}

    spacingInput.addEventListener('input', (evt) => {{
      spacingStrength = Number(evt.target.value);
      simulationEnergy = 1.0;
      settledFrames = 0;
    }});

    svg.addEventListener('click', (evt) => {{
      const clickedNodeId = evt.target && evt.target.getAttribute ? evt.target.getAttribute('data-node-id') : null;
      if (clickedNodeId) {{
        hiddenArtworkForNodeId = null;
        setSelected(clickedNodeId);
        return;
      }}
      if (suppressBackgroundClickOnce) {{
        suppressBackgroundClickOnce = false;
        return;
      }}
      clearSelection();
    }});

    window.addEventListener('keydown', (evt) => {{
      if (evt.code === 'Space') {{
        isSpacePressed = true;
        svg.classList.add('pan-ready');
        evt.preventDefault();
      }}
    }});

    window.addEventListener('keyup', (evt) => {{
      if (evt.code === 'Space') {{
        isSpacePressed = false;
        svg.classList.remove('pan-ready');
      }}
    }});

    artworkPreviewCloseEl.addEventListener('click', () => {{
      hideArtworkPreview();
      hiddenArtworkForNodeId = selectedNodeId;
    }});

    selectAllCategoriesBtn.addEventListener('click', () => {{
      selectedCategories.clear();
      for (const c of categories) selectedCategories.add(c);
      for (const box of categoryList.querySelectorAll('input[type="checkbox"]')) {{
        box.checked = true;
      }}
      applyFilters();
    }});

    deselectAllCategoriesBtn.addEventListener('click', () => {{
      selectedCategories.clear();
      for (const box of categoryList.querySelectorAll('input[type="checkbox"]')) {{
        box.checked = false;
      }}
      applyFilters();
    }});

    searchInput.addEventListener('input', (evt) => {{
      filterText = evt.target.value.trim().toLowerCase();
      applyFilters();
    }});

    centerView();
    applyFilters();
    frame();
  </script>
</body>
</html>
"""


def main() -> None:
    entries = discover_entries()
    payload = build_graph_payload(entries)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render_html(payload), encoding="utf-8")
    print(f"Generated {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Nodes: {len(payload['nodes'])} | Edges: {len(payload['edges'])}")


if __name__ == "__main__":
    main()
