#!/usr/bin/env python3
"""
Generate an interactive world atlas dashboard from markdown lore files.

Extracts full frontmatter metadata, document sections, summaries, assets and
typed relationships from every lore entry, then renders a self-contained
multi-tab HTML dashboard (graph, map, explorer, gallery, themes, hierarchy,
insights) with a rich detail panel per entry.

Map positions are authored in dashboard/map-registry.yaml and compiled in.

Usage:
  python3 scripts/build_story_dashboard.py
"""

from __future__ import annotations

import datetime
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dias_map import compile_map_payload, load_map_registry  # noqa: E402

OUTPUT_PATH = ROOT / "dashboard" / "story-dashboard.html"
SKIP_DIRS = {"assets", "ref", ".git", ".cursor", ".agents", "dashboard", "scripts", ".venv"}

# Frontmatter fields that create typed links to other entries.
LINK_FIELD_KINDS = {
    "region": "region",
    "parent_region": "parent region",
    "culture": "culture",
    "based_on": "based on",
}

# Frontmatter fields surfaced as metadata in the detail panel.
META_KEYS = [
    "region",
    "parent_region",
    "place_type",
    "culture",
    "scope",
    "artifact_type",
    "nature",
    "story_type",
    "medium",
    "edition",
    "year",
    "based_on",
]

ASSET_REGEX = re.compile(
    r"(?:\./)?(assets/[^\s`)\]]+\.(?:png|jpg|jpeg|gif|webp))", re.IGNORECASE
)


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
    meta: Dict[str, str]
    assets: List[str]
    sections: List[Dict[str, str]]
    summary: str
    words: int
    link_refs: List[Tuple[str, str]] = field(default_factory=list)


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


def split_body(text: str) -> List[str]:
    """Return the markdown body lines after the closing frontmatter fence."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return lines
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return lines[idx + 1:]
    return []


def parse_sections(body_lines: List[str]) -> List[Dict[str, str]]:
    sections: List[Dict[str, str]] = []
    current: Optional[Dict[str, object]] = None

    for line in body_lines:
        if line.startswith("# ") and not line.startswith("## "):
            continue  # the H1 repeats the entry name
        if line.startswith("## "):
            current = {"h": line[3:].strip(), "t": []}
            sections.append(current)  # type: ignore[arg-type]
            continue
        if current is None:
            if not line.strip():
                continue
            current = {"h": "", "t": []}
            sections.append(current)  # type: ignore[arg-type]
        current["t"].append(line)  # type: ignore[index]

    cleaned: List[Dict[str, str]] = []
    for sec in sections:
        text = "\n".join(sec["t"]).strip()  # type: ignore[arg-type]
        if not text and not sec["h"]:
            continue
        cleaned.append({"h": str(sec["h"]), "t": text})
    return cleaned


MD_CLEAN_REGEX = re.compile(r"[*_`#]+")


def make_summary(sections: List[Dict[str, str]]) -> str:
    for sec in sections:
        for paragraph in sec["t"].split("\n\n"):
            candidate = paragraph.strip()
            if not candidate or candidate.startswith(("-", ">", "|", "!")):
                continue
            plain = MD_CLEAN_REGEX.sub("", candidate)
            plain = re.sub(r"\s+", " ", plain).strip()
            if len(plain) > 260:
                plain = plain[:257].rstrip() + "..."
            return plain
    return ""


def count_words(body_lines: List[str]) -> int:
    text = " ".join(body_lines)
    text = MD_CLEAN_REGEX.sub(" ", text)
    return len([w for w in text.split() if w])


def extract_assets(text: str) -> List[str]:
    seen: List[str] = []
    for match in ASSET_REGEX.finditer(text):
        normalized = match.group(1).strip().replace("\\", "/")
        if normalized in seen:
            continue
        if (ROOT / normalized).exists():
            seen.append(normalized)
    return seen


def as_list(value: object) -> List[str]:
    if not value:
        return []
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    return [str(v).strip() for v in value if str(v).strip()]


def extract_entry(path: Path) -> Optional[Entry]:
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    if not frontmatter:
        return None

    title = str(frontmatter.get("name") or path.stem.replace("-", " ").title()).strip()
    category = str(frontmatter.get("category") or path.parent.name.rstrip("s")).strip() or "unknown"
    status = str(frontmatter.get("status") or "unspecified").strip() or "unspecified"

    related = as_list(frontmatter.get("related"))
    themes = as_list(frontmatter.get("themes"))

    meta: Dict[str, str] = {}
    for key in META_KEYS:
        value = frontmatter.get(key)
        if isinstance(value, list):
            joined = ", ".join(str(v).strip() for v in value if str(v).strip())
            if joined:
                meta[key] = joined
        elif value and str(value).strip():
            meta[key] = str(value).strip()

    link_refs: List[Tuple[str, str]] = [(r, "related") for r in related]
    for key, kind in LINK_FIELD_KINDS.items():
        for v in as_list(frontmatter.get(key)):
            link_refs.append((v, kind))

    body_lines = split_body(text)
    sections = parse_sections(body_lines)

    return Entry(
        id=f"{category}:{slugify(title)}",
        slug=slugify(title),
        title=title,
        category=category,
        path=path.relative_to(ROOT).as_posix(),
        status=status,
        themes=themes,
        related=related,
        meta=meta,
        assets=extract_assets(text),
        sections=sections,
        summary=make_summary(sections),
        words=count_words(body_lines),
        link_refs=link_refs,
    )


def discover_entries() -> List[Entry]:
    entries: List[Entry] = []
    for md_file in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in md_file.parts):
            continue
        if md_file.parent == ROOT:
            continue  # README, START-HERE, etc.
        entry = extract_entry(md_file)
        if entry:
            entries.append(entry)
    entries.sort(key=lambda e: (e.category, e.title.lower()))
    return entries


def build_payload(entries: List[Entry]) -> Dict[str, object]:
    title_index = {e.title.lower(): e.id for e in entries}
    slug_index = {e.slug: e.id for e in entries}

    def resolve(ref: str) -> Optional[str]:
        key = ref.lower().strip()
        return title_index.get(key) or slug_index.get(slugify(ref))

    nodes = []
    edge_map: Dict[Tuple[str, str], Dict[str, object]] = {}

    for e in entries:
        unresolved: List[str] = []
        for ref, kind in e.link_refs:
            target = resolve(ref)
            if target and target != e.id:
                pair = tuple(sorted((e.id, target)))
                record = edge_map.get(pair)
                if record is None:
                    record = {"source": e.id, "target": target, "kinds": set()}
                    edge_map[pair] = record
                record["kinds"].add(kind)  # type: ignore[union-attr]
            elif not target and kind == "related":
                unresolved.append(ref)

        nodes.append(
            {
                "id": e.id,
                "slug": e.slug,
                "label": e.title,
                "category": e.category,
                "status": e.status,
                "themes": e.themes,
                "path": e.path,
                "region": e.meta.get("region", ""),
                "parent_region": e.meta.get("parent_region", ""),
                "meta": e.meta,
                "assets": e.assets,
                "summary": e.summary,
                "words": e.words,
                "sections": e.sections,
                "unresolved": unresolved,
            }
        )

    edges = [
        {"source": rec["source"], "target": rec["target"], "kinds": sorted(rec["kinds"])}  # type: ignore[arg-type]
        for rec in edge_map.values()
    ]

    map_payload, _map_warnings = compile_map_payload(
        load_map_registry(),
        title_index,
        slug_index,
        slugify,
        entries=entries,
    )

    return {
        "generated": datetime.date.today().isoformat(),
        "nodes": nodes,
        "edges": edges,
        "map": map_payload,
    }


def world_title(entries: List[Entry]) -> Optional[str]:
    """Name of the world entry with the most outgoing references, if any."""
    worlds = [e for e in entries if e.category == "world"]
    if not worlds:
        return None
    return max(worlds, key=lambda e: len(e.link_refs)).title


def html_escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_html(payload: Dict[str, object], title: Optional[str]) -> str:
    data_json = json.dumps(payload, ensure_ascii=True).replace("</", "<\\/")
    brand = html_escape(title) if title else "World Atlas"
    subtitle = "World Atlas" if title else "Story Dashboard"
    page_title = f"{brand} - World Atlas" if title else "World Atlas"
    return (
        TEMPLATE.replace("__DATA__", data_json)
        .replace("__PAGE_TITLE__", page_title)
        .replace("__BRAND__", brand)
        .replace("__SUBTITLE__", subtitle)
    )


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>__PAGE_TITLE__</title>
<style>
  :root {
    color-scheme: dark;
    --bg: #07070b;
    --bg-soft: #0d0e14;
    --panel: #12141c;
    --panel-2: #181b25;
    --line: #262a38;
    --line-soft: #1d2030;
    --ink: #e9ebf2;
    --muted: #9aa1b4;
    --faint: #6b7186;
    --accent: #8fa9ff;
    --radius: 14px;
    --header-h: 58px;
  }
  * { box-sizing: border-box; }
  html, body { height: 100%; }
  body {
    margin: 0;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    background:
      radial-gradient(1200px 600px at 75% -10%, rgba(70, 90, 160, 0.16), transparent 60%),
      radial-gradient(900px 500px at 10% 110%, rgba(120, 80, 160, 0.10), transparent 60%),
      var(--bg);
    color: var(--ink);
    overflow: hidden;
  }
  button { font-family: inherit; }

  /* ---------- header ---------- */
  header {
    height: var(--header-h);
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 0 16px;
    border-bottom: 1px solid var(--line-soft);
    background: rgba(10, 11, 16, 0.82);
    backdrop-filter: blur(10px);
    position: relative;
    z-index: 30;
  }
  .brand { display: flex; flex-direction: column; line-height: 1.15; min-width: 130px; }
  .brand b { font-size: 0.98rem; letter-spacing: 0.04em; }
  .brand span { font-size: 0.68rem; color: var(--faint); letter-spacing: 0.12em; text-transform: uppercase; }
  nav { display: flex; gap: 4px; }
  nav button {
    border: 1px solid transparent;
    background: transparent;
    color: var(--muted);
    padding: 7px 13px;
    border-radius: 9px;
    font-size: 0.84rem;
    cursor: pointer;
    transition: color .15s, background .15s;
  }
  nav button:hover { color: var(--ink); background: rgba(255,255,255,0.05); }
  nav button.active {
    color: var(--ink);
    background: rgba(143, 169, 255, 0.13);
    border-color: rgba(143, 169, 255, 0.32);
  }
  .header-search { margin-left: auto; position: relative; width: min(330px, 30vw); }
  .header-search input {
    width: 100%;
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 10px;
    color: var(--ink);
    padding: 8px 12px;
    font-size: 0.85rem;
    outline: none;
  }
  .header-search input:focus { border-color: rgba(143,169,255,0.5); }
  #search-results {
    position: absolute;
    top: calc(100% + 6px);
    left: 0; right: 0;
    background: var(--panel-2);
    border: 1px solid var(--line);
    border-radius: 12px;
    max-height: 380px;
    overflow: auto;
    display: none;
    box-shadow: 0 18px 48px rgba(0,0,0,0.55);
  }
  #search-results.open { display: block; }
  .search-item {
    display: flex; align-items: center; gap: 9px;
    padding: 8px 12px;
    cursor: pointer;
    font-size: 0.84rem;
  }
  .search-item:hover { background: rgba(143,169,255,0.10); }
  .search-item .cat-mini { margin-left: auto; color: var(--faint); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.06em; }
  .header-stats { display: flex; gap: 14px; color: var(--faint); font-size: 0.74rem; white-space: nowrap; }
  .header-stats b { color: var(--muted); font-weight: 600; }

  /* ---------- layout ---------- */
  #app { height: calc(100vh - var(--header-h)); position: relative; }
  .tab { display: none; height: 100%; }
  .tab.active { display: block; }
  .dot {
    width: 9px; height: 9px; border-radius: 99px; flex: 0 0 auto;
    border: 1px solid rgba(255,255,255,0.35);
  }

  /* ---------- chips ---------- */
  .chip {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 0.7rem;
    padding: 3px 9px;
    border-radius: 999px;
    border: 1px solid var(--line);
    background: rgba(255,255,255,0.03);
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    white-space: nowrap;
  }
  .chip.cat { color: var(--c, var(--muted)); border-color: color-mix(in srgb, var(--c, #888) 45%, transparent); background: color-mix(in srgb, var(--c, #888) 10%, transparent); }
  .chip.status { text-transform: capitalize; }
  .chip.theme { cursor: pointer; text-transform: none; letter-spacing: 0; font-size: 0.74rem; }
  .chip.theme:hover { border-color: rgba(143,169,255,0.55); color: var(--ink); }

  /* ---------- graph tab ---------- */
  #tab-graph { display: none; grid-template-columns: 252px 1fr; }
  #tab-graph.active { display: grid; }
  .rail {
    border-right: 1px solid var(--line-soft);
    background: rgba(13, 14, 20, 0.65);
    padding: 14px;
    overflow: auto;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .rail h3 {
    margin: 0;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--faint);
    font-weight: 600;
  }
  .rail-group { display: flex; flex-direction: column; gap: 8px; }
  .cat-row {
    display: flex; align-items: center; gap: 8px;
    font-size: 0.82rem;
    color: var(--muted);
    cursor: pointer;
    user-select: none;
    padding: 3px 6px;
    border-radius: 7px;
  }
  .cat-row:hover { background: rgba(255,255,255,0.04); color: var(--ink); }
  .cat-row input { accent-color: var(--accent); margin: 0; }
  .cat-row .count { margin-left: auto; color: var(--faint); font-size: 0.72rem; }
  .rail label.slider { display: grid; gap: 4px; font-size: 0.78rem; color: var(--muted); }
  .rail input[type="range"] { width: 100%; accent-color: var(--accent); }
  .rail .btn-row { display: flex; gap: 8px; flex-wrap: wrap; }
  .ghost-btn {
    border: 1px solid var(--line);
    background: var(--panel);
    color: var(--muted);
    border-radius: 9px;
    padding: 6px 11px;
    font-size: 0.76rem;
    cursor: pointer;
  }
  .ghost-btn:hover { color: var(--ink); border-color: rgba(143,169,255,0.45); }
  .toggle-row { display: flex; align-items: center; gap: 8px; font-size: 0.8rem; color: var(--muted); cursor: pointer; user-select: none; }
  .toggle-row input { accent-color: var(--accent); margin: 0; }
  #graph-wrap { position: relative; overflow: hidden; }
  #graph { width: 100%; height: 100%; display: block; cursor: default; }
  #graph.panning { cursor: grabbing; }
  #graph-hud {
    position: absolute; left: 12px; bottom: 10px;
    font-size: 0.72rem; color: var(--faint);
    background: rgba(10,11,16,0.7);
    border: 1px solid var(--line-soft);
    padding: 5px 10px;
    border-radius: 8px;
    pointer-events: none;
  }
  #graph-hint {
    position: absolute; right: 12px; bottom: 10px;
    font-size: 0.7rem; color: var(--faint);
    pointer-events: none;
  }
  .gnode { stroke: rgba(8, 10, 20, 0.9); stroke-width: 1.2; cursor: pointer; transition: opacity .15s; }
  .gnode.dim { opacity: 0.07; }
  .gnode.sel { stroke: #fff; stroke-width: 2.4; }
  .gedge { stroke: #38415f; stroke-opacity: 0.5; stroke-width: 1; transition: opacity .15s; }
  .gedge.dim { opacity: 0.04; }
  .gedge.hot { stroke: var(--accent); stroke-opacity: 0.95; stroke-width: 1.6; }
  .glabel {
    font-size: 10px; fill: #d7ddf0;
    paint-order: stroke; stroke: rgba(5,6,10,0.85); stroke-width: 2.5px;
    pointer-events: none;
    transition: opacity .15s;
  }
  .glabel.dim { opacity: 0.05; }
  #tooltip {
    position: fixed;
    z-index: 60;
    pointer-events: none;
    background: rgba(14, 16, 24, 0.95);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 8px 11px;
    font-size: 0.78rem;
    display: none;
    max-width: 280px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  }
  #tooltip .t-name { font-weight: 600; margin-bottom: 2px; }
  #tooltip .t-sub { color: var(--muted); font-size: 0.72rem; }

  /* ---------- scrollable tab shells ---------- */
  .scroll-tab { overflow: auto; padding: 18px 20px 40px; height: 100%; }
  .toolbar {
    display: flex; flex-wrap: wrap; gap: 10px; align-items: center;
    margin-bottom: 16px;
    position: sticky; top: -18px;
    background: linear-gradient(rgba(7,7,11,0.96), rgba(7,7,11,0.88));
    padding: 12px 0 10px;
    z-index: 5;
  }
  .toolbar input[type="text"], .toolbar select {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 9px;
    color: var(--ink);
    padding: 7px 11px;
    font-size: 0.82rem;
    outline: none;
  }
  .toolbar input[type="text"]:focus { border-color: rgba(143,169,255,0.5); }
  .pill {
    border: 1px solid var(--line);
    background: rgba(255,255,255,0.03);
    color: var(--muted);
    border-radius: 999px;
    font-size: 0.76rem;
    padding: 5px 12px;
    cursor: pointer;
    display: inline-flex; align-items: center; gap: 6px;
  }
  .pill.on { border-color: color-mix(in srgb, var(--c, var(--accent)) 60%, transparent); color: var(--ink); background: color-mix(in srgb, var(--c, var(--accent)) 13%, transparent); }
  .result-count { color: var(--faint); font-size: 0.76rem; margin-left: auto; }

  /* ---------- explorer cards ---------- */
  .card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(285px, 1fr));
    gap: 12px;
  }
  .card {
    background: var(--panel);
    border: 1px solid var(--line-soft);
    border-radius: var(--radius);
    padding: 13px 14px 11px;
    cursor: pointer;
    display: flex; flex-direction: column; gap: 8px;
    transition: transform .12s, border-color .12s, background .12s;
    border-top: 2px solid var(--c, var(--line));
    min-height: 130px;
  }
  .card:hover { transform: translateY(-2px); border-color: color-mix(in srgb, var(--c, #888) 50%, var(--line)); background: var(--panel-2); }
  .card .chips { display: flex; gap: 6px; flex-wrap: wrap; }
  .card h4 { margin: 0; font-size: 0.95rem; font-weight: 600; }
  .card p { margin: 0; font-size: 0.78rem; color: var(--muted); line-height: 1.45; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
  .card .foot { margin-top: auto; display: flex; gap: 12px; color: var(--faint); font-size: 0.7rem; padding-top: 4px; }

  /* ---------- gallery ---------- */
  .gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
    gap: 12px;
  }
  .gal-item {
    background: var(--panel);
    border: 1px solid var(--line-soft);
    border-radius: var(--radius);
    overflow: hidden;
    cursor: pointer;
    transition: transform .12s, border-color .12s;
  }
  .gal-item:hover { transform: translateY(-2px); border-color: rgba(143,169,255,0.45); }
  .gal-item img { width: 100%; aspect-ratio: 1 / 1; object-fit: cover; display: block; background: #0a0b10; }
  .gal-cap { padding: 9px 11px; }
  .gal-cap b { display: block; font-size: 0.82rem; font-weight: 600; }
  .gal-cap span { display: block; color: var(--faint); font-size: 0.7rem; margin-top: 2px; }

  /* ---------- themes ---------- */
  #tab-themes.active { display: grid; grid-template-columns: 300px 1fr; height: 100%; }
  #theme-list-col {
    border-right: 1px solid var(--line-soft);
    overflow: auto;
    padding: 14px;
    display: flex; flex-direction: column; gap: 4px;
    background: rgba(13,14,20,0.6);
  }
  #theme-list-col input {
    background: var(--panel); border: 1px solid var(--line); border-radius: 9px;
    color: var(--ink); padding: 7px 11px; font-size: 0.82rem; outline: none; margin-bottom: 8px;
  }
  .theme-row {
    display: flex; align-items: center; gap: 8px;
    padding: 6px 10px;
    border-radius: 8px;
    font-size: 0.82rem;
    color: var(--muted);
    cursor: pointer;
  }
  .theme-row:hover { background: rgba(255,255,255,0.05); color: var(--ink); }
  .theme-row.sel { background: rgba(143,169,255,0.14); color: var(--ink); outline: 1px solid rgba(143,169,255,0.4); }
  .theme-row .count { margin-left: auto; color: var(--faint); font-size: 0.72rem; }
  #theme-entries { overflow: auto; padding: 18px 20px 40px; }
  #theme-entries h2 { margin: 0 0 4px; font-size: 1.1rem; }
  #theme-entries .sub { color: var(--faint); font-size: 0.8rem; margin-bottom: 16px; }

  /* ---------- hierarchy ---------- */
  #tab-hierarchy .scroll-inner { max-width: 860px; }
  .hier-root, .hier-children { list-style: none; margin: 0; padding: 0; }
  .hier-children { padding-left: 20px; border-left: 1px dashed rgba(120, 138, 198, 0.25); margin-left: 9px; }
  .hier-row {
    display: flex; align-items: center; gap: 8px;
    padding: 4px 8px;
    border-radius: 8px;
    cursor: pointer;
    user-select: none;
    color: #d6dbee;
    font-size: 0.88rem;
  }
  .hier-row:hover { background: rgba(143,169,255,0.10); }
  .hier-toggle {
    width: 18px; height: 18px;
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 5px;
    background: rgba(255,255,255,0.05);
    color: #cdd5f5;
    font-size: 11px; line-height: 15px; text-align: center;
    padding: 0; cursor: pointer; flex: 0 0 auto;
  }
  .hier-toggle.spacer { border-color: transparent; background: transparent; cursor: default; }
  .hier-meta { margin-left: auto; font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--faint); }

  /* ---------- insights ---------- */
  .insight-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 14px;
    align-items: start;
  }
  .stat-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-bottom: 16px; }
  .stat-card {
    background: var(--panel);
    border: 1px solid var(--line-soft);
    border-radius: var(--radius);
    padding: 13px 15px;
  }
  .stat-card b { display: block; font-size: 1.45rem; font-weight: 700; }
  .stat-card span { color: var(--faint); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; }
  .panel {
    background: var(--panel);
    border: 1px solid var(--line-soft);
    border-radius: var(--radius);
    padding: 15px 16px;
  }
  .panel h3 { margin: 0 0 12px; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.12em; color: var(--faint); font-weight: 600; }
  .bar-row { display: grid; grid-template-columns: 130px 1fr 36px; align-items: center; gap: 10px; margin-bottom: 7px; font-size: 0.78rem; }
  .bar-row .name { color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; cursor: pointer; }
  .bar-row .name:hover { color: var(--ink); }
  .bar-row .track { height: 8px; border-radius: 99px; background: rgba(255,255,255,0.05); overflow: hidden; }
  .bar-row .fill { display: block; height: 100%; border-radius: 99px; }
  .bar-row .num { color: var(--faint); text-align: right; font-size: 0.72rem; }
  .rank-item {
    display: flex; align-items: center; gap: 9px;
    padding: 6px 8px; border-radius: 8px; cursor: pointer;
    font-size: 0.83rem; color: var(--muted);
  }
  .rank-item:hover { background: rgba(255,255,255,0.05); color: var(--ink); }
  .rank-item .num { margin-left: auto; color: var(--faint); font-size: 0.74rem; }
  .issue-item { padding: 7px 9px; border-radius: 8px; font-size: 0.8rem; margin-bottom: 6px; background: rgba(242, 184, 107, 0.06); border: 1px solid rgba(242, 184, 107, 0.18); }
  .issue-item b { cursor: pointer; color: var(--ink); font-weight: 600; }
  .issue-item b:hover { text-decoration: underline; }
  .issue-item span { color: var(--muted); }
  .empty-note { color: var(--faint); font-size: 0.8rem; }

  /* ---------- drawer ---------- */
  #drawer {
    position: fixed;
    top: var(--header-h);
    right: 0;
    bottom: 0;
    width: min(460px, 92vw);
    background: rgba(15, 17, 25, 0.97);
    border-left: 1px solid var(--line);
    transform: translateX(105%);
    transition: transform 0.22s ease;
    z-index: 40;
    display: flex;
    flex-direction: column;
    box-shadow: -24px 0 60px rgba(0,0,0,0.5);
  }
  #drawer.open { transform: translateX(0); }
  #drawer-scroll { overflow: auto; flex: 1; }
  #drawer-close {
    position: absolute; top: 10px; right: 12px;
    z-index: 3;
    width: 30px; height: 30px;
    border-radius: 99px;
    border: 1px solid var(--line);
    background: rgba(10,11,16,0.8);
    color: var(--ink);
    font-size: 15px;
    cursor: pointer;
  }
  .drawer-hero { position: relative; background: #0a0b10; }
  .drawer-hero img { width: 100%; max-height: 290px; object-fit: contain; display: block; cursor: zoom-in; }
  .drawer-body { padding: 16px 18px 30px; }
  .drawer-body h2 { margin: 8px 0 6px; font-size: 1.3rem; line-height: 1.25; }
  .drawer-summary { color: var(--muted); font-size: 0.85rem; line-height: 1.5; margin: 0 0 12px; }
  .meta-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px 14px;
    margin: 12px 0;
    padding: 12px;
    background: rgba(255,255,255,0.025);
    border: 1px solid var(--line-soft);
    border-radius: 12px;
  }
  .meta-item .mk { display: block; color: var(--faint); font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.08em; }
  .meta-item .mv { display: block; font-size: 0.82rem; margin-top: 2px; }
  .meta-item .mv.link { color: var(--accent); cursor: pointer; }
  .meta-item .mv.link:hover { text-decoration: underline; }
  .drawer-stats { display: flex; gap: 16px; color: var(--faint); font-size: 0.74rem; margin: 10px 0 4px; }
  .drawer-stats b { color: var(--muted); }
  .drawer-section-title {
    margin: 18px 0 8px;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--faint);
    font-weight: 600;
    border-bottom: 1px solid var(--line-soft);
    padding-bottom: 5px;
  }
  .conn-group { margin-bottom: 10px; }
  .conn-group .cg-head { font-size: 0.72rem; color: var(--faint); margin: 8px 0 4px; }
  .conn-item {
    display: flex; align-items: center; gap: 8px;
    padding: 5px 8px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.83rem;
  }
  .conn-item:hover { background: rgba(143,169,255,0.10); }
  .conn-item .kind { margin-left: auto; color: var(--faint); font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.04em; white-space: nowrap; }
  .doc-section h3 { font-size: 0.92rem; margin: 16px 0 6px; color: #dfe4f5; }
  .doc-section p { font-size: 0.83rem; line-height: 1.6; color: var(--muted); margin: 0 0 10px; }
  .doc-section ul { margin: 0 0 10px; padding-left: 20px; }
  .doc-section li { font-size: 0.83rem; line-height: 1.55; color: var(--muted); margin-bottom: 3px; }
  .doc-section code { background: rgba(255,255,255,0.07); border-radius: 5px; padding: 1px 5px; font-size: 0.78rem; }
  .doc-section strong { color: #e6e9f5; }
  .path-line { margin-top: 16px; color: var(--faint); font-size: 0.72rem; word-break: break-all; }
  .drawer-actions { display: flex; gap: 8px; margin: 12px 0 2px; flex-wrap: wrap; }
  .unresolved-box { margin-top: 8px; }
  .unresolved-box .u-item { font-size: 0.78rem; color: #f2b86b; padding: 2px 0; }
  .asset-strip { display: flex; gap: 6px; margin-top: 8px; flex-wrap: wrap; }
  .asset-strip img { width: 56px; height: 56px; object-fit: cover; border-radius: 8px; border: 1px solid var(--line); cursor: pointer; }

  /* ---------- lightbox ---------- */
  #lightbox {
    position: fixed; inset: 0;
    background: rgba(4,5,8,0.92);
    display: none;
    align-items: center; justify-content: center;
    z-index: 80;
    cursor: zoom-out;
  }
  #lightbox.open { display: flex; }
  #lightbox img { max-width: 92vw; max-height: 90vh; border-radius: 10px; }

  /* ---------- map tab ---------- */
  #tab-map { display: none; grid-template-columns: 260px 1fr; height: 100%; }
  #tab-map.active { display: grid; }
  #map-rail {
    border-right: 1px solid var(--line-soft);
    background: var(--bg-soft);
    overflow: auto;
    padding: 14px 14px 24px;
  }
  #map-rail h3 {
    margin: 0 0 8px;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--faint);
  }
  #map-rail .rail-group { margin-bottom: 18px; }
  #map-freq {
    width: 100%;
    background: var(--panel);
    border: 1px solid var(--line);
    color: var(--ink);
    border-radius: 10px;
    padding: 8px 10px;
    font-size: 0.88rem;
  }
  #map-note {
    margin-top: 8px;
    font-size: 0.78rem;
    color: var(--muted);
    line-height: 1.45;
  }
  #map-stats {
    font-size: 0.75rem;
    color: var(--faint);
    margin-top: 6px;
  }
  #map-wrap {
    position: relative;
    min-height: 0;
    background: #06080e;
    overflow: hidden;
  }
  #world-map {
    width: 100%;
    height: 100%;
    display: block;
    cursor: crosshair;
    image-rendering: pixelated;
  }
  #map-hover {
    position: absolute;
    pointer-events: none;
    z-index: 5;
    min-width: 160px;
    max-width: 280px;
    background: rgba(12, 14, 22, 0.94);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 10px 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    display: none;
  }
  #map-hover.open { display: block; }
  #map-hover .mh-kind {
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 4px;
  }
  #map-hover .mh-title { font-size: 0.95rem; font-weight: 600; margin-bottom: 4px; }
  #map-hover .mh-sum { font-size: 0.76rem; color: var(--muted); line-height: 1.4; }
  #map-hover .mh-miss { font-size: 0.72rem; color: #d08888; }
  #map-hint {
    position: absolute;
    left: 12px;
    bottom: 10px;
    font-size: 0.7rem;
    color: var(--faint);
    pointer-events: none;
  }
  .map-legend-row {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.8rem;
    color: var(--muted);
    margin: 5px 0;
  }
  .map-swatch {
    width: 12px;
    height: 12px;
    border-radius: 3px;
    image-rendering: pixelated;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.15);
  }
</style>
</head>
<body>
<header>
  <div class="brand"><b>__BRAND__</b><span>__SUBTITLE__</span></div>
  <nav id="tabs-nav">
    <button data-tab="graph" class="active">Graph</button>
    <button data-tab="map">Map</button>
    <button data-tab="explorer">Explorer</button>
    <button data-tab="gallery">Gallery</button>
    <button data-tab="themes">Themes</button>
    <button data-tab="hierarchy">Hierarchy</button>
    <button data-tab="insights">Insights</button>
  </nav>
  <div class="header-search">
    <input id="global-search" placeholder="Search the atlas..." autocomplete="off" />
    <div id="search-results"></div>
  </div>
  <div class="header-stats" id="header-stats"></div>
</header>

<div id="app">
  <section id="tab-graph" class="tab active">
    <div class="rail">
      <div class="rail-group">
        <h3>Categories</h3>
        <div id="cat-filters"></div>
        <div class="btn-row">
          <button class="ghost-btn" id="cats-all">All</button>
          <button class="ghost-btn" id="cats-none">None</button>
        </div>
      </div>
      <div class="rail-group">
        <h3>Layout</h3>
        <label class="slider">Node spacing
          <input id="spacing" type="range" min="60" max="300" step="1" value="150" />
        </label>
        <label class="toggle-row"><input type="checkbox" id="focus-toggle" /> Focus on selection</label>
        <label class="toggle-row"><input type="checkbox" id="labels-toggle" checked /> Show labels</label>
        <div class="btn-row">
          <button class="ghost-btn" id="reset-layout">Reshuffle</button>
          <button class="ghost-btn" id="reset-view">Reset view</button>
        </div>
      </div>
    </div>
    <div id="graph-wrap">
      <svg id="graph" viewBox="0 0 2400 1700" preserveAspectRatio="xMidYMid meet"></svg>
      <div id="graph-hud"></div>
      <div id="graph-hint">drag background to pan &middot; scroll to zoom &middot; drag nodes to arrange</div>
    </div>
  </section>

  <section id="tab-map" class="tab">
    <div id="map-rail">
      <div class="rail-group">
        <h3>Frequency</h3>
        <select id="map-freq"></select>
        <div id="map-note"></div>
        <div id="map-stats"></div>
      </div>
      <div class="rail-group">
        <h3>Layers</h3>
        <label class="toggle-row"><input type="checkbox" id="map-layer-regions" checked /> Region fills</label>
        <label class="toggle-row"><input type="checkbox" id="map-layer-places" checked /> Places</label>
        <label class="toggle-row"><input type="checkbox" id="map-layer-landmarks" checked /> Landmarks</label>
        <label class="toggle-row"><input type="checkbox" id="map-layer-inhabitants" checked /> Inhabitants</label>
        <label class="toggle-row"><input type="checkbox" id="map-layer-stories" checked /> Stories</label>
        <label class="toggle-row"><input type="checkbox" id="map-layer-myths" checked /> Myths</label>
        <label class="toggle-row"><input type="checkbox" id="map-layer-artifacts" checked /> Artifacts</label>
        <label class="toggle-row"><input type="checkbox" id="map-layer-artworks" checked /> Artworks</label>
        <label class="toggle-row"><input type="checkbox" id="map-layer-cultures" checked /> Cultures</label>
        <label class="toggle-row"><input type="checkbox" id="map-layer-phenomena" checked /> Phenomena</label>
        <label class="toggle-row"><input type="checkbox" id="map-layer-symbols" checked /> Symbols</label>
        <label class="toggle-row"><input type="checkbox" id="map-layer-rules" checked /> Rules</label>
        <label class="toggle-row"><input type="checkbox" id="map-layer-world" checked /> World</label>
      </div>
      <div class="rail-group">
        <h3>Legend</h3>
        <div class="map-legend-row"><span class="map-swatch" style="background:#8fa9ff"></span> Place</div>
        <div class="map-legend-row"><span class="map-swatch" style="background:#e2c36b"></span> Landmark</div>
        <div class="map-legend-row"><span class="map-swatch" style="background:#d48cff"></span> Inhabitant</div>
        <div class="map-legend-row"><span class="map-swatch" style="background:#7dcea0"></span> Story</div>
        <div class="map-legend-row"><span class="map-swatch" style="background:#f0a060"></span> Myth</div>
        <div class="map-legend-row"><span class="map-swatch" style="background:#6ec6d4"></span> Artifact</div>
        <div class="map-legend-row"><span class="map-swatch" style="background:#f278a8"></span> Artwork</div>
        <div class="map-legend-row"><span class="map-swatch" style="background:#a8d46e"></span> Culture</div>
        <div class="map-legend-row"><span class="map-swatch" style="background:#c090ff"></span> Phenomenon</div>
        <div class="map-legend-row"><span class="map-swatch" style="background:#ffd27a"></span> Symbol</div>
        <div class="map-legend-row"><span class="map-swatch" style="background:#9aa7c2"></span> Rule</div>
        <div class="map-legend-row"><span class="map-swatch" style="background:#ffffff"></span> World</div>
      </div>
      <div class="rail-group">
        <h3>Registry</h3>
        <div class="empty-note" style="font-size:0.72rem;line-height:1.45">
          Positions live in <code style="background:rgba(255,255,255,0.07);border-radius:5px;padding:1px 5px">dashboard/map-registry.yaml</code>.
          Rebuild after edits.
        </div>
      </div>
    </div>
    <div id="map-wrap">
      <canvas id="world-map" width="1200" height="900"></canvas>
      <div id="map-hover"></div>
      <div id="map-hint">scroll to zoom &middot; drag to pan &middot; hover for lore &middot; click to open</div>
    </div>
  </section>

  <section id="tab-explorer" class="tab">
    <div class="scroll-tab">
      <div class="toolbar">
        <input type="text" id="exp-search" placeholder="Filter entries..." />
        <span id="exp-cat-pills"></span>
        <select id="exp-sort">
          <option value="name">Sort: Name</option>
          <option value="connections">Sort: Most connected</option>
          <option value="words">Sort: Longest</option>
          <option value="category">Sort: Category</option>
        </select>
        <span class="result-count" id="exp-count"></span>
      </div>
      <div class="card-grid" id="exp-grid"></div>
    </div>
  </section>

  <section id="tab-gallery" class="tab">
    <div class="scroll-tab">
      <div class="toolbar">
        <input type="text" id="gal-search" placeholder="Filter artworks..." />
        <span class="result-count" id="gal-count"></span>
      </div>
      <div class="gallery-grid" id="gal-grid"></div>
    </div>
  </section>

  <section id="tab-themes" class="tab">
    <div id="theme-list-col">
      <input type="text" id="theme-search" placeholder="Filter themes..." />
      <div id="theme-list"></div>
    </div>
    <div id="theme-entries">
      <h2 id="theme-title">Themes</h2>
      <div class="sub" id="theme-sub">Select a theme to see every entry that carries it.</div>
      <div class="card-grid" id="theme-grid"></div>
    </div>
  </section>

  <section id="tab-hierarchy" class="tab">
    <div class="scroll-tab">
      <div class="toolbar">
        <button class="ghost-btn" id="hier-expand">Expand all</button>
        <button class="ghost-btn" id="hier-collapse">Collapse all</button>
        <span class="result-count">Containment tree built from region / parent region fields</span>
      </div>
      <div class="scroll-inner"><ul class="hier-root" id="hier-root"></ul></div>
    </div>
  </section>

  <section id="tab-insights" class="tab">
    <div class="scroll-tab">
      <div class="stat-cards" id="stat-cards"></div>
      <div class="insight-grid" id="insight-grid"></div>
    </div>
  </section>
</div>

<aside id="drawer">
  <button id="drawer-close" aria-label="Close">&times;</button>
  <div id="drawer-scroll"></div>
</aside>

<div id="tooltip"></div>
<div id="lightbox"><img id="lightbox-img" alt="" /></div>

<script>
const DATA = __DATA__;

/* ============ shared data prep ============ */
const nodes = DATA.nodes;
const edges = DATA.edges;
const nodesById = new Map(nodes.map(n => [n.id, n]));

const CAT_COLORS = {
  world: '#7aa2ff', region: '#f48fb1', rule: '#8dd3c7', culture: '#4dd0e1',
  inhabitant: '#ffd180', artifact: '#ce93d8', symbol: '#ffcc80', myth: '#b0bec5',
  story: '#90caf9', artwork: '#ff8a65', phenomenon: '#a5d6a7', unknown: '#90a4ae',
};
const STATUS_COLORS = {
  canonical: '#5dd39e', myth: '#c792ea', rumor: '#f2b86b', unknown: '#8a93a6', unspecified: '#6b7186',
};
function catColor(c) {
  if (CAT_COLORS[c]) return CAT_COLORS[c];
  let hash = 0;
  for (let i = 0; i < c.length; i++) hash = (hash * 31 + c.charCodeAt(i)) | 0;
  return `hsl(${Math.abs(hash) % 360} 65% 70%)`;
}
function statusColor(s) { return STATUS_COLORS[s] || '#8a93a6'; }

const categories = [...new Set(nodes.map(n => n.category))].sort();
const statuses = [...new Set(nodes.map(n => n.status))].sort();
const catCounts = new Map();
for (const n of nodes) catCounts.set(n.category, (catCounts.get(n.category) || 0) + 1);

// adjacency with direction + kinds
const adj = new Map();
function addAdj(a, b, kinds, dir) {
  if (!adj.has(a)) adj.set(a, []);
  adj.get(a).push({ id: b, kinds, dir });
}
for (const e of edges) {
  addAdj(e.source, e.target, e.kinds, 'out');
  addAdj(e.target, e.source, e.kinds, 'in');
}
for (const n of nodes) n.degree = (adj.get(n.id) || []).length;

// label / slug lookups for hierarchy refs
const idByLabel = new Map();
const idBySlug = new Map();
function slugifyJs(t) {
  return (t || '').toLowerCase().trim().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}
for (const n of nodes) {
  idByLabel.set(n.label.toLowerCase().trim(), n.id);
  if (n.slug) idBySlug.set(n.slug, n.id);
}
function resolveRef(ref) {
  const raw = (ref || '').trim();
  if (!raw) return null;
  return idByLabel.get(raw.toLowerCase()) || idBySlug.get(slugifyJs(raw)) || null;
}

// themes
const themeMap = new Map();
for (const n of nodes) {
  for (const t of n.themes) {
    if (!themeMap.has(t)) themeMap.set(t, []);
    themeMap.get(t).push(n.id);
  }
}

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
function assetUrl(p) { return '../' + p; }
function fmtKey(k) { return k.replace(/_/g, ' '); }

/* ============ tiny markdown renderer ============ */
function inlineMd(s) {
  let out = esc(s);
  out = out.replace(/`([^`]+)`/g, '<code>$1</code>');
  out = out.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  out = out.replace(/(^|[^*])\*([^*\n]+)\*(?!\*)/g, '$1<em>$2</em>');
  return out;
}
function mdToHtml(text) {
  const lines = (text || '').split('\n');
  let html = '';
  let para = [];
  let list = null;
  const flushPara = () => {
    if (para.length) { html += '<p>' + inlineMd(para.join(' ')) + '</p>'; para = []; }
  };
  const flushList = () => {
    if (list) { html += '<ul>' + list.map(li => '<li>' + inlineMd(li) + '</li>').join('') + '</ul>'; list = null; }
  };
  for (const raw of lines) {
    const line = raw.trim();
    if (!line) { flushPara(); flushList(); continue; }
    if (/^[-*]\s+/.test(line)) {
      flushPara();
      if (!list) list = [];
      list.push(line.replace(/^[-*]\s+/, ''));
      continue;
    }
    if (/^#{3,6}\s+/.test(line)) {
      flushPara(); flushList();
      html += '<p><strong>' + inlineMd(line.replace(/^#+\s+/, '')) + '</strong></p>';
      continue;
    }
    flushList();
    para.push(line);
  }
  flushPara(); flushList();
  return html;
}

/* ============ tabs ============ */
const tabsNav = document.getElementById('tabs-nav');
let activeTab = 'graph';
function switchTab(name) {
  activeTab = name;
  for (const btn of tabsNav.querySelectorAll('button')) {
    btn.classList.toggle('active', btn.dataset.tab === name);
  }
  for (const sec of document.querySelectorAll('.tab')) {
    sec.classList.toggle('active', sec.id === 'tab-' + name);
  }
  if (name === 'map' && window.DiasMap) window.DiasMap.resize();
}
tabsNav.addEventListener('click', (e) => {
  const btn = e.target.closest('button[data-tab]');
  if (btn) switchTab(btn.dataset.tab);
});

/* ============ header stats ============ */
document.getElementById('header-stats').innerHTML =
  `<span><b>${nodes.length}</b> entries</span>` +
  `<span><b>${edges.length}</b> links</span>` +
  `<span><b>${themeMap.size}</b> themes</span>`;

/* ============ drawer ============ */
const drawer = document.getElementById('drawer');
const drawerScroll = document.getElementById('drawer-scroll');
const lightbox = document.getElementById('lightbox');
const lightboxImg = document.getElementById('lightbox-img');
let currentEntryId = null;

function metaItemHtml(key, value) {
  const refId = resolveRef(value);
  const cls = refId ? 'mv link' : 'mv';
  const attr = refId ? ` data-open="${esc(refId)}"` : '';
  return `<div class="meta-item"><span class="mk">${esc(fmtKey(key))}</span><span class="${cls}"${attr}>${esc(value)}</span></div>`;
}

function connectionsHtml(id) {
  const links = adj.get(id) || [];
  if (!links.length) return '<div class="empty-note">No links to other entries.</div>';
  const out = links.filter(l => l.dir === 'out');
  const inc = links.filter(l => l.dir === 'in');
  const renderGroup = (items, label) => {
    if (!items.length) return '';
    const byCat = new Map();
    for (const l of items) {
      const n = nodesById.get(l.id);
      if (!n) continue;
      if (!byCat.has(n.category)) byCat.set(n.category, []);
      byCat.get(n.category).push(l);
    }
    let html = `<div class="conn-group"><div class="cg-head">${label} (${items.length})</div>`;
    for (const cat of [...byCat.keys()].sort()) {
      for (const l of byCat.get(cat).sort((a, b) => nodesById.get(a.id).label.localeCompare(nodesById.get(b.id).label))) {
        const n = nodesById.get(l.id);
        html += `<div class="conn-item" data-open="${esc(n.id)}">` +
          `<span class="dot" style="background:${catColor(n.category)}"></span>` +
          `<span>${esc(n.label)}</span>` +
          `<span class="kind">${esc(n.category)} &middot; ${esc(l.kinds.join(', '))}</span></div>`;
      }
    }
    return html + '</div>';
  };
  return renderGroup(out, 'Links out') + renderGroup(inc, 'Referenced by');
}

function openEntry(id, opts = {}) {
  const n = nodesById.get(id);
  if (!n) return;
  currentEntryId = id;
  let html = '';

  if (n.assets.length) {
    html += `<div class="drawer-hero"><img src="${esc(assetUrl(n.assets[0]))}" alt="${esc(n.label)}" data-lightbox="${esc(assetUrl(n.assets[0]))}" loading="lazy" /></div>`;
  }
  html += '<div class="drawer-body">';
  html += `<div class="chips" style="display:flex;gap:6px;flex-wrap:wrap;">` +
    `<span class="chip cat" style="--c:${catColor(n.category)}">${esc(n.category)}</span>` +
    `<span class="chip status" style="color:${statusColor(n.status)};border-color:color-mix(in srgb,${statusColor(n.status)} 40%,transparent)">${esc(n.status)}</span>` +
    `</div>`;
  html += `<h2>${esc(n.label)}</h2>`;
  if (n.summary) html += `<p class="drawer-summary">${esc(n.summary)}</p>`;

  html += `<div class="drawer-stats">` +
    `<span><b>${n.degree}</b> links</span>` +
    `<span><b>${n.words}</b> words</span>` +
    `<span><b>${n.sections.length}</b> sections</span>` +
    `</div>`;

  html += `<div class="drawer-actions">` +
    `<button class="ghost-btn" data-locate="${esc(n.id)}">Locate in graph</button>` +
    `</div>`;

  const metaKeys = Object.keys(n.meta);
  if (metaKeys.length) {
    html += '<div class="meta-grid">';
    for (const k of metaKeys) html += metaItemHtml(k, n.meta[k]);
    html += '</div>';
  }

  if (n.themes.length) {
    html += '<div class="drawer-section-title">Themes</div>';
    html += '<div style="display:flex;gap:6px;flex-wrap:wrap;">';
    for (const t of n.themes) html += `<span class="chip theme" data-theme="${esc(t)}">${esc(t)}</span>`;
    html += '</div>';
  }

  if (n.assets.length > 1) {
    html += '<div class="drawer-section-title">Assets</div><div class="asset-strip">';
    for (const a of n.assets) html += `<img src="${esc(assetUrl(a))}" data-lightbox="${esc(assetUrl(a))}" loading="lazy" alt="" />`;
    html += '</div>';
  }

  html += '<div class="drawer-section-title">Connections</div>';
  html += connectionsHtml(n.id);

  if (n.unresolved.length) {
    html += '<div class="drawer-section-title">Unresolved references</div><div class="unresolved-box">';
    for (const u of n.unresolved) html += `<div class="u-item">${esc(u)}</div>`;
    html += '</div>';
  }

  if (n.sections.length) {
    html += '<div class="drawer-section-title">Document</div><div class="doc-section">';
    for (const sec of n.sections) {
      if (sec.h) html += `<h3>${esc(sec.h)}</h3>`;
      html += mdToHtml(sec.t);
    }
    html += '</div>';
  }

  html += `<div class="path-line">${esc(n.path)}</div>`;
  html += '</div>';

  drawerScroll.innerHTML = html;
  drawerScroll.scrollTop = 0;
  drawer.classList.add('open');

  if (!opts.skipGraphSelect) graphSelect(id, { center: false });
}

function closeDrawer() {
  drawer.classList.remove('open');
  currentEntryId = null;
  graphSelect(null);
}

document.getElementById('drawer-close').addEventListener('click', closeDrawer);
drawerScroll.addEventListener('click', (e) => {
  const openEl = e.target.closest('[data-open]');
  if (openEl) { openEntry(openEl.dataset.open); return; }
  const themeEl = e.target.closest('[data-theme]');
  if (themeEl) { selectTheme(themeEl.dataset.theme); return; }
  const locateEl = e.target.closest('[data-locate]');
  if (locateEl) { locateInGraph(locateEl.dataset.locate); return; }
  const lb = e.target.closest('[data-lightbox]');
  if (lb) { lightboxImg.src = lb.dataset.lightbox; lightbox.classList.add('open'); }
});
lightbox.addEventListener('click', () => lightbox.classList.remove('open'));
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    if (lightbox.classList.contains('open')) lightbox.classList.remove('open');
    else closeDrawer();
  }
});

/* ============ global search ============ */
const searchInput = document.getElementById('global-search');
const searchResults = document.getElementById('search-results');
function runSearch(q) {
  const query = q.trim().toLowerCase();
  if (!query) { searchResults.classList.remove('open'); return; }
  const scored = [];
  for (const n of nodes) {
    const name = n.label.toLowerCase();
    let score = -1;
    if (name === query) score = 0;
    else if (name.startsWith(query)) score = 1;
    else if (name.includes(query)) score = 2;
    else if (n.themes.some(t => t.toLowerCase().includes(query))) score = 3;
    else if (n.category.includes(query) || n.status.includes(query)) score = 4;
    else if (n.summary.toLowerCase().includes(query)) score = 5;
    if (score >= 0) scored.push([score, n]);
  }
  scored.sort((a, b) => a[0] - b[0] || a[1].label.localeCompare(b[1].label));
  const top = scored.slice(0, 14);
  if (!top.length) { searchResults.classList.remove('open'); return; }
  searchResults.innerHTML = top.map(([, n]) =>
    `<div class="search-item" data-open="${esc(n.id)}">` +
    `<span class="dot" style="background:${catColor(n.category)}"></span>` +
    `<span>${esc(n.label)}</span><span class="cat-mini">${esc(n.category)}</span></div>`
  ).join('');
  searchResults.classList.add('open');
}
searchInput.addEventListener('input', () => runSearch(searchInput.value));
searchInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    const first = searchResults.querySelector('[data-open]');
    if (first) { openEntry(first.dataset.open); searchResults.classList.remove('open'); searchInput.blur(); }
  }
  if (e.key === 'Escape') searchResults.classList.remove('open');
});
searchResults.addEventListener('click', (e) => {
  const item = e.target.closest('[data-open]');
  if (item) { openEntry(item.dataset.open); searchResults.classList.remove('open'); searchInput.value = ''; }
});
document.addEventListener('click', (e) => {
  if (!e.target.closest('.header-search')) searchResults.classList.remove('open');
});

/* ============ graph tab ============ */
const svg = document.getElementById('graph');
const GW = 2400, GH = 1700;
const graphRoot = document.createElementNS('http://www.w3.org/2000/svg', 'g');
const edgeGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
const nodeGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
const labelGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
graphRoot.append(edgeGroup, nodeGroup, labelGroup);
svg.appendChild(graphRoot);

const tooltip = document.getElementById('tooltip');
const hud = document.getElementById('graph-hud');
const selectedCats = new Set(categories);
let focusMode = false;
let showLabels = true;
let spacing = 150;
let selectedId = null;
let view = { scale: 1, x: 0, y: 0 };
let energy = 1.0;
const MIN_ENERGY = 0.012;
let settled = 0;

function seedPositions() {
  const catIdx = new Map(categories.map((c, i) => [c, i]));
  for (const n of nodes) {
    const baseAngle = (catIdx.get(n.category) / categories.length) * Math.PI * 2;
    const r = 540 + Math.random() * 260;
    const jitter = (Math.random() - 0.5) * 0.9;
    n.x = GW / 2 + Math.cos(baseAngle + jitter) * r;
    n.y = GH / 2 + Math.sin(baseAngle + jitter) * r;
    n.vx = 0; n.vy = 0;
  }
}
for (const n of nodes) {
  n.r = (n.category === 'world' ? 11 : 4.5) + Math.min(7, Math.sqrt(n.degree) * 1.25);
  n.color = catColor(n.category);
}
seedPositions();

const edgeEls = edges.map((e) => {
  const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
  line.setAttribute('class', 'gedge');
  edgeGroup.appendChild(line);
  return [e, line];
});
const nodeEls = nodes.map((n) => {
  const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
  c.setAttribute('class', 'gnode');
  c.setAttribute('r', n.r);
  c.setAttribute('fill', n.color);
  c.dataset.id = n.id;
  nodeGroup.appendChild(c);
  return [n, c];
});
const labelEls = nodes.map((n) => {
  const t = document.createElementNS('http://www.w3.org/2000/svg', 'text');
  t.setAttribute('class', 'glabel');
  t.textContent = n.label;
  labelGroup.appendChild(t);
  return [n, t];
});

function graphVisibleSet() {
  let vis = new Set(nodes.filter(n => selectedCats.has(n.category)).map(n => n.id));
  if (focusMode && selectedId) {
    const hood = new Set([selectedId]);
    for (const l of adj.get(selectedId) || []) hood.add(l.id);
    vis = new Set([...vis].filter(id => hood.has(id)));
    if (nodesById.has(selectedId)) vis.add(selectedId);
  }
  return vis;
}

function applyGraphFilters() {
  const vis = graphVisibleSet();
  const hood = selectedId ? new Set([selectedId, ...(adj.get(selectedId) || []).map(l => l.id)]) : null;
  for (const [n, el] of nodeEls) {
    const v = vis.has(n.id);
    el.style.display = v ? '' : 'none';
    el.classList.toggle('dim', v && hood ? !hood.has(n.id) : false);
    el.classList.toggle('sel', n.id === selectedId);
  }
  for (const [n, el] of labelEls) {
    const v = vis.has(n.id) && showLabels;
    el.style.display = v ? '' : 'none';
    el.classList.toggle('dim', v && hood ? !hood.has(n.id) : false);
  }
  let visEdges = 0;
  for (const [e, el] of edgeEls) {
    const v = vis.has(e.source) && vis.has(e.target);
    if (v) visEdges++;
    el.style.display = v ? '' : 'none';
    const hot = !!(selectedId && v && (e.source === selectedId || e.target === selectedId));
    el.classList.toggle('hot', hot);
    el.classList.toggle('dim', v && selectedId ? !hot : false);
  }
  hud.textContent = `${vis.size} nodes \u00b7 ${visEdges} links`;
}

function graphSelect(id, opts = {}) {
  selectedId = id;
  applyGraphFilters();
  if (id && opts.center) centerOn(id);
}

function centerOn(id) {
  const n = nodesById.get(id);
  if (!n) return;
  view.scale = Math.max(view.scale, 1.35);
  view.x = GW / 2 - n.x * view.scale;
  view.y = GH / 2 - n.y * view.scale;
  applyView();
}

function locateInGraph(id) {
  switchTab('graph');
  graphSelect(id, { center: true });
}

function applyView() {
  graphRoot.setAttribute('transform', `translate(${view.x} ${view.y}) scale(${view.scale})`);
}
function fitView() {
  const vis = graphVisibleSet();
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  for (const n of nodes) {
    if (!vis.has(n.id)) continue;
    if (n.x < minX) minX = n.x;
    if (n.x > maxX) maxX = n.x;
    if (n.y < minY) minY = n.y;
    if (n.y > maxY) maxY = n.y;
  }
  if (!isFinite(minX)) { view.scale = 1; view.x = 0; view.y = 0; applyView(); return; }
  const pad = 130;
  const bw = Math.max(240, maxX - minX + pad * 2);
  const bh = Math.max(240, maxY - minY + pad * 2);
  view.scale = Math.min(3.0, Math.max(0.3, Math.min(GW / bw, GH / bh)));
  view.x = GW / 2 - ((minX + maxX) / 2) * view.scale;
  view.y = GH / 2 - ((minY + maxY) / 2) * view.scale;
  applyView();
}
let userInteracted = false;
let fitStamp = 0;
function scheduleFit(delay = 1700) {
  fitView();
  const stamp = ++fitStamp;
  setTimeout(() => { if (!userInteracted && stamp === fitStamp) fitView(); }, delay);
}

function tick() {
  if (energy <= MIN_ENERGY) return;
  for (const e of edges) {
    const a = nodesById.get(e.source), b = nodesById.get(e.target);
    const dx = b.x - a.x, dy = b.y - a.y;
    const dist = Math.max(1, Math.hypot(dx, dy));
    const force = (dist - spacing) * 0.0028 * energy;
    const fx = (dx / dist) * force, fy = (dy / dist) * force;
    a.vx += fx; a.vy += fy; b.vx -= fx; b.vy -= fy;
  }
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const a = nodes[i], b = nodes[j];
      const dx = b.x - a.x, dy = b.y - a.y;
      const dist = Math.max(1, Math.hypot(dx, dy));
      const minDist = a.r + b.r + spacing * 0.5;
      if (dist < minDist) {
        const push = (minDist - dist) * 0.06 * energy;
        const px = (dx / dist) * push, py = (dy / dist) * push;
        a.vx -= px; a.vy -= py; b.vx += px; b.vy += py;
      }
    }
  }
  let motion = 0;
  for (const n of nodes) {
    n.vx += (GW / 2 - n.x) * 0.00012 * energy;
    n.vy += (GH / 2 - n.y) * 0.00012 * energy;
    n.vx *= 0.82; n.vy *= 0.82;
    n.x = Math.min(GW - 20, Math.max(20, n.x + n.vx));
    n.y = Math.min(GH - 20, Math.max(20, n.y + n.vy));
    motion += Math.abs(n.vx) + Math.abs(n.vy);
  }
  energy *= 0.992;
  if (motion < nodes.length * 0.01) settled++; else settled = 0;
  if (settled > 24) { energy = MIN_ENERGY; for (const n of nodes) { n.vx = 0; n.vy = 0; } }
  if (energy < MIN_ENERGY) energy = MIN_ENERGY;
}
function render() {
  for (const [e, line] of edgeEls) {
    const a = nodesById.get(e.source), b = nodesById.get(e.target);
    line.setAttribute('x1', a.x); line.setAttribute('y1', a.y);
    line.setAttribute('x2', b.x); line.setAttribute('y2', b.y);
  }
  for (const [n, c] of nodeEls) { c.setAttribute('cx', n.x); c.setAttribute('cy', n.y); }
  for (const [n, t] of labelEls) { t.setAttribute('x', n.x + n.r + 3); t.setAttribute('y', n.y + 3); }
}
(function frame() { tick(); render(); requestAnimationFrame(frame); })();

// pointer interactions
let pan = null;
let dragNode = null;
let downPos = null;
let downId = null;
let moved = false;

function svgPoint(evt) {
  const rect = svg.getBoundingClientRect();
  const sx = GW / rect.width, sy = GH / rect.height;
  const px = (evt.clientX - rect.left) * sx;
  const py = (evt.clientY - rect.top) * sy;
  return { x: (px - view.x) / view.scale, y: (py - view.y) / view.scale, rawX: px, rawY: py };
}

svg.addEventListener('pointerdown', (evt) => {
  if (evt.button !== 0 && evt.button !== 1) return;
  userInteracted = true;
  downPos = { x: evt.clientX, y: evt.clientY };
  moved = false;
  downId = (evt.target.dataset && evt.target.dataset.id) || null;
  if (downId) {
    dragNode = nodesById.get(downId);
  } else {
    pan = { x: evt.clientX, y: evt.clientY };
    svg.classList.add('panning');
  }
  svg.setPointerCapture(evt.pointerId);
});
svg.addEventListener('pointermove', (evt) => {
  if (downPos && Math.hypot(evt.clientX - downPos.x, evt.clientY - downPos.y) > 4) moved = true;
  if (dragNode && moved) {
    const p = svgPoint(evt);
    dragNode.x = p.x; dragNode.y = p.y;
    dragNode.vx = 0; dragNode.vy = 0;
    energy = Math.max(energy, 0.28);
    settled = 0;
  } else if (pan) {
    const rect = svg.getBoundingClientRect();
    view.x += (evt.clientX - pan.x) * (GW / rect.width);
    view.y += (evt.clientY - pan.y) * (GH / rect.height);
    pan = { x: evt.clientX, y: evt.clientY };
    applyView();
  }
  // hover tooltip
  const id = evt.target.dataset && evt.target.dataset.id;
  if (id && !pan && !(dragNode && moved)) {
    const n = nodesById.get(id);
    tooltip.innerHTML = `<div class="t-name">${esc(n.label)}</div>` +
      `<div class="t-sub">${esc(n.category)} \u00b7 ${esc(n.status)} \u00b7 ${n.degree} links</div>` +
      (n.summary ? `<div class="t-sub" style="margin-top:4px">${esc(n.summary.slice(0, 110))}${n.summary.length > 110 ? '...' : ''}</div>` : '');
    tooltip.style.display = 'block';
    tooltip.style.left = Math.min(window.innerWidth - 300, evt.clientX + 14) + 'px';
    tooltip.style.top = (evt.clientY + 14) + 'px';
  } else {
    tooltip.style.display = 'none';
  }
});
svg.addEventListener('pointerup', (evt) => {
  if (!moved) {
    if (downId) openEntry(downId);
    else closeDrawer();
  }
  dragNode = null; pan = null; downPos = null; downId = null;
  svg.classList.remove('panning');
  try { svg.releasePointerCapture(evt.pointerId); } catch (_e) {}
});
svg.addEventListener('pointerleave', () => { tooltip.style.display = 'none'; });
svg.addEventListener('wheel', (evt) => {
  evt.preventDefault();
  userInteracted = true;
  const rect = svg.getBoundingClientRect();
  const sx = GW / rect.width, sy = GH / rect.height;
  const cx = (evt.clientX - rect.left) * sx, cy = (evt.clientY - rect.top) * sy;
  const factor = evt.deltaY < 0 ? 1.12 : 0.89;
  const next = Math.min(3.4, Math.max(0.3, view.scale * factor));
  if (next === view.scale) return;
  const wx = (cx - view.x) / view.scale, wy = (cy - view.y) / view.scale;
  view.scale = next;
  view.x = cx - wx * next;
  view.y = cy - wy * next;
  applyView();
}, { passive: false });

// rail controls
const catFiltersEl = document.getElementById('cat-filters');
for (const c of categories) {
  const row = document.createElement('label');
  row.className = 'cat-row';
  row.innerHTML = `<input type="checkbox" checked value="${esc(c)}" />` +
    `<span class="dot" style="background:${catColor(c)}"></span>` +
    `<span>${esc(c)}</span><span class="count">${catCounts.get(c)}</span>`;
  row.querySelector('input').addEventListener('change', (e) => {
    if (e.target.checked) selectedCats.add(c); else selectedCats.delete(c);
    applyGraphFilters();
  });
  catFiltersEl.appendChild(row);
}
document.getElementById('cats-all').addEventListener('click', () => {
  selectedCats.clear(); categories.forEach(c => selectedCats.add(c));
  catFiltersEl.querySelectorAll('input').forEach(i => { i.checked = true; });
  applyGraphFilters();
});
document.getElementById('cats-none').addEventListener('click', () => {
  selectedCats.clear();
  catFiltersEl.querySelectorAll('input').forEach(i => { i.checked = false; });
  applyGraphFilters();
});
document.getElementById('spacing').addEventListener('input', (e) => {
  spacing = Number(e.target.value);
  energy = 1.0; settled = 0;
});
document.getElementById('focus-toggle').addEventListener('change', (e) => {
  focusMode = e.target.checked;
  applyGraphFilters();
});
document.getElementById('labels-toggle').addEventListener('change', (e) => {
  showLabels = e.target.checked;
  applyGraphFilters();
});
document.getElementById('reset-layout').addEventListener('click', () => {
  seedPositions(); energy = 1.0; settled = 0;
  userInteracted = false;
  scheduleFit();
});
document.getElementById('reset-view').addEventListener('click', () => {
  userInteracted = false;
  fitView();
});

/* ============ explorer tab ============ */
const expSearch = document.getElementById('exp-search');
const expSort = document.getElementById('exp-sort');
const expGrid = document.getElementById('exp-grid');
const expCount = document.getElementById('exp-count');
const expCatPills = document.getElementById('exp-cat-pills');
const expCats = new Set(categories);

for (const c of categories) {
  const b = document.createElement('button');
  b.className = 'pill on';
  b.style.setProperty('--c', catColor(c));
  b.innerHTML = `<span class="dot" style="background:${catColor(c)};width:7px;height:7px"></span>${esc(c)}`;
  b.addEventListener('click', () => {
    if (expCats.has(c)) { expCats.delete(c); b.classList.remove('on'); }
    else { expCats.add(c); b.classList.add('on'); }
    renderExplorer();
  });
  expCatPills.appendChild(b);
}

function cardHtml(n) {
  const themes = n.themes.slice(0, 3).map(t => `<span class="chip theme" data-theme="${esc(t)}">${esc(t)}</span>`).join('');
  return `<div class="card" data-open="${esc(n.id)}" style="--c:${catColor(n.category)}">` +
    `<div class="chips"><span class="chip cat" style="--c:${catColor(n.category)}">${esc(n.category)}</span>` +
    `<span class="chip status" style="color:${statusColor(n.status)}">${esc(n.status)}</span></div>` +
    `<h4>${esc(n.label)}</h4>` +
    (n.summary ? `<p>${esc(n.summary)}</p>` : '') +
    (themes ? `<div class="chips">${themes}</div>` : '') +
    `<div class="foot"><span>${n.degree} links</span><span>${n.words} words</span>` +
    (n.assets.length ? `<span>${n.assets.length} image${n.assets.length > 1 ? 's' : ''}</span>` : '') +
    `</div></div>`;
}

function renderExplorer() {
  const q = expSearch.value.trim().toLowerCase();
  let list = nodes.filter(n => expCats.has(n.category));
  if (q) {
    list = list.filter(n =>
      n.label.toLowerCase().includes(q) ||
      n.summary.toLowerCase().includes(q) ||
      n.themes.some(t => t.toLowerCase().includes(q)) ||
      (n.meta.region || '').toLowerCase().includes(q)
    );
  }
  const sort = expSort.value;
  if (sort === 'name') list.sort((a, b) => a.label.localeCompare(b.label));
  else if (sort === 'connections') list.sort((a, b) => b.degree - a.degree);
  else if (sort === 'words') list.sort((a, b) => b.words - a.words);
  else if (sort === 'category') list.sort((a, b) => a.category.localeCompare(b.category) || a.label.localeCompare(b.label));
  expCount.textContent = `${list.length} of ${nodes.length} entries`;
  expGrid.innerHTML = list.map(cardHtml).join('');
}
expSearch.addEventListener('input', renderExplorer);
expSort.addEventListener('change', renderExplorer);
expGrid.addEventListener('click', (e) => {
  const themeEl = e.target.closest('[data-theme]');
  if (themeEl) { e.stopPropagation(); selectTheme(themeEl.dataset.theme); return; }
  const card = e.target.closest('[data-open]');
  if (card) openEntry(card.dataset.open);
});
renderExplorer();

/* ============ gallery tab ============ */
const galGrid = document.getElementById('gal-grid');
const galSearch = document.getElementById('gal-search');
const galCount = document.getElementById('gal-count');
const galleryNodes = nodes.filter(n => n.assets.length > 0);

function renderGallery() {
  const q = galSearch.value.trim().toLowerCase();
  let list = galleryNodes;
  if (q) {
    list = list.filter(n =>
      n.label.toLowerCase().includes(q) ||
      (n.meta.region || '').toLowerCase().includes(q) ||
      n.themes.some(t => t.toLowerCase().includes(q))
    );
  }
  galCount.textContent = `${list.length} pieces`;
  galGrid.innerHTML = list.map(n =>
    `<div class="gal-item" data-open="${esc(n.id)}">` +
    `<img src="${esc(assetUrl(n.assets[0]))}" loading="lazy" alt="${esc(n.label)}" />` +
    `<div class="gal-cap"><b>${esc(n.label)}</b>` +
    `<span>${esc(n.category)}${n.meta.region ? ' \u00b7 ' + esc(n.meta.region) : ''}</span></div></div>`
  ).join('');
}
galSearch.addEventListener('input', renderGallery);
galGrid.addEventListener('click', (e) => {
  const item = e.target.closest('[data-open]');
  if (item) openEntry(item.dataset.open);
});
renderGallery();

/* ============ themes tab ============ */
const themeListEl = document.getElementById('theme-list');
const themeSearchEl = document.getElementById('theme-search');
const themeTitleEl = document.getElementById('theme-title');
const themeSubEl = document.getElementById('theme-sub');
const themeGridEl = document.getElementById('theme-grid');
let activeTheme = null;
const sortedThemes = [...themeMap.entries()].sort((a, b) => b[1].length - a[1].length || a[0].localeCompare(b[0]));

function renderThemeList() {
  const q = themeSearchEl.value.trim().toLowerCase();
  themeListEl.innerHTML = sortedThemes
    .filter(([t]) => !q || t.toLowerCase().includes(q))
    .map(([t, ids]) =>
      `<div class="theme-row${t === activeTheme ? ' sel' : ''}" data-t="${esc(t)}">` +
      `<span>${esc(t)}</span><span class="count">${ids.length}</span></div>`
    ).join('');
}
function selectTheme(t) {
  activeTheme = t;
  switchTab('themes');
  renderThemeList();
  const ids = themeMap.get(t) || [];
  themeTitleEl.textContent = t;
  themeSubEl.textContent = `${ids.length} entr${ids.length === 1 ? 'y' : 'ies'} carry this theme`;
  themeGridEl.innerHTML = ids.map(id => cardHtml(nodesById.get(id))).join('');
  const row = themeListEl.querySelector('.theme-row.sel');
  if (row) row.scrollIntoView({ block: 'nearest' });
}
themeSearchEl.addEventListener('input', renderThemeList);
themeListEl.addEventListener('click', (e) => {
  const row = e.target.closest('[data-t]');
  if (row) selectTheme(row.dataset.t);
});
themeGridEl.addEventListener('click', (e) => {
  const themeEl = e.target.closest('[data-theme]');
  if (themeEl) { selectTheme(themeEl.dataset.theme); return; }
  const card = e.target.closest('[data-open]');
  if (card) openEntry(card.dataset.open);
});
renderThemeList();

/* ============ hierarchy tab ============ */
const hierRootEl = document.getElementById('hier-root');
const ROOT_ID = '__root__';
const childrenOf = new Map();
const parentOf = new Map();
const collapsed = new Set();

(function buildHierarchy() {
  const worldIds = nodes.filter(n => n.category === 'world').map(n => n.id);
  for (const n of nodes) {
    let parent = null;
    if (n.category === 'world') parent = ROOT_ID;
    else {
      const pr = resolveRef(n.parent_region);
      const r = resolveRef(n.region);
      if (pr && pr !== n.id) parent = pr;
      else if (r && r !== n.id) parent = r;
      else if (worldIds.length) parent = worldIds[0];
      else parent = ROOT_ID;
    }
    parentOf.set(n.id, parent);
    if (!childrenOf.has(parent)) childrenOf.set(parent, []);
    childrenOf.get(parent).push(n.id);
  }
  for (const kids of childrenOf.values()) {
    kids.sort((a, b) => {
      const na = nodesById.get(a), nb = nodesById.get(b);
      return na.category.localeCompare(nb.category) || na.label.localeCompare(nb.label);
    });
  }
  for (const [pid, kids] of childrenOf.entries()) {
    if (pid !== ROOT_ID && kids.length) collapsed.add(pid);
  }
  for (const w of worldIds) collapsed.delete(w);
})();

function renderHierarchy() {
  hierRootEl.innerHTML = '';
  function renderNode(id, ul) {
    const n = nodesById.get(id);
    const kids = childrenOf.get(id) || [];
    const li = document.createElement('li');
    ul.appendChild(li);
    const row = document.createElement('div');
    row.className = 'hier-row';
    li.appendChild(row);

    const toggle = document.createElement('button');
    if (kids.length) {
      toggle.className = 'hier-toggle';
      toggle.textContent = collapsed.has(id) ? '+' : '\u2212';
      toggle.addEventListener('click', (e) => {
        e.stopPropagation();
        if (collapsed.has(id)) collapsed.delete(id); else collapsed.add(id);
        renderHierarchy();
      });
    } else {
      toggle.className = 'hier-toggle spacer';
      toggle.disabled = true;
    }
    row.appendChild(toggle);

    const dot = document.createElement('span');
    dot.className = 'dot';
    dot.style.background = catColor(n.category);
    row.appendChild(dot);
    const label = document.createElement('span');
    label.textContent = n.label;
    row.appendChild(label);
    const meta = document.createElement('span');
    meta.className = 'hier-meta';
    meta.textContent = n.category + (kids.length ? ` \u00b7 ${kids.length}` : '');
    row.appendChild(meta);
    row.addEventListener('click', () => openEntry(id));

    if (kids.length && !collapsed.has(id)) {
      const nested = document.createElement('ul');
      nested.className = 'hier-children';
      li.appendChild(nested);
      for (const kid of kids) renderNode(kid, nested);
    }
  }
  for (const id of childrenOf.get(ROOT_ID) || []) renderNode(id, hierRootEl);
}
document.getElementById('hier-expand').addEventListener('click', () => { collapsed.clear(); renderHierarchy(); });
document.getElementById('hier-collapse').addEventListener('click', () => {
  for (const [pid, kids] of childrenOf.entries()) if (pid !== ROOT_ID && kids.length) collapsed.add(pid);
  renderHierarchy();
});
renderHierarchy();

/* ============ insights tab ============ */
(function renderInsights() {
  const statCards = document.getElementById('stat-cards');
  const grid = document.getElementById('insight-grid');
  const totalWords = nodes.reduce((a, n) => a + n.words, 0);
  const withImages = nodes.filter(n => n.assets.length).length;
  const orphans = nodes.filter(n => n.degree === 0);
  const unresolvedNodes = nodes.filter(n => n.unresolved.length);
  const unresolvedTotal = unresolvedNodes.reduce((a, n) => a + n.unresolved.length, 0);

  statCards.innerHTML = [
    [nodes.length, 'entries'],
    [edges.length, 'links'],
    [categories.length, 'categories'],
    [themeMap.size, 'themes'],
    [totalWords.toLocaleString(), 'words of lore'],
    [withImages, 'illustrated'],
  ].map(([v, l]) => `<div class="stat-card"><b>${v}</b><span>${l}</span></div>`).join('');

  function barsPanel(title, rows, colorFn, clickAttr) {
    const max = Math.max(1, ...rows.map(r => r[1]));
    let html = `<div class="panel"><h3>${esc(title)}</h3>`;
    for (const [name, count, extra] of rows) {
      html += `<div class="bar-row">` +
        `<span class="name" ${clickAttr ? `${clickAttr}="${esc(extra != null ? extra : name)}"` : ''}>${esc(name)}</span>` +
        `<span class="track"><span class="fill" style="width:${(count / max) * 100}%;background:${colorFn(name)}"></span></span>` +
        `<span class="num">${count}</span></div>`;
    }
    return html + '</div>';
  }

  const catRows = categories.map(c => [c, catCounts.get(c)]).sort((a, b) => b[1] - a[1]);
  const statusCounts = new Map();
  for (const n of nodes) statusCounts.set(n.status, (statusCounts.get(n.status) || 0) + 1);
  const statusRows = [...statusCounts.entries()].sort((a, b) => b[1] - a[1]);
  const themeRows = sortedThemes.slice(0, 18).map(([t, ids]) => [t, ids.length]);
  const topConnected = [...nodes].sort((a, b) => b.degree - a.degree).slice(0, 12);

  let html = '';
  html += barsPanel('Entries by category', catRows, catColor);
  html += barsPanel('Canon status', statusRows, statusColor);
  html += barsPanel('Top themes', themeRows, () => 'rgba(143,169,255,0.8)', 'data-theme');

  html += `<div class="panel"><h3>Most connected</h3>` + topConnected.map(n =>
    `<div class="rank-item" data-open="${esc(n.id)}">` +
    `<span class="dot" style="background:${catColor(n.category)}"></span>` +
    `<span>${esc(n.label)}</span><span class="num">${n.degree} links</span></div>`
  ).join('') + '</div>';

  html += `<div class="panel"><h3>Orphan entries (${orphans.length})</h3>` +
    (orphans.length
      ? orphans.map(n =>
          `<div class="rank-item" data-open="${esc(n.id)}">` +
          `<span class="dot" style="background:${catColor(n.category)}"></span>` +
          `<span>${esc(n.label)}</span><span class="num">${esc(n.category)}</span></div>`).join('')
      : '<div class="empty-note">Every entry is linked into the world. Nice.</div>') +
    '</div>';

  html += `<div class="panel"><h3>Unresolved references (${unresolvedTotal})</h3>` +
    (unresolvedNodes.length
      ? unresolvedNodes.map(n =>
          `<div class="issue-item"><b data-open="${esc(n.id)}">${esc(n.label)}</b> ` +
          `<span>\u2192 ${n.unresolved.map(esc).join(', ')}</span></div>`).join('')
      : '<div class="empty-note">All related references resolve to existing entries.</div>') +
    '</div>';

  html += `<div class="panel"><h3>About</h3>` +
    `<div class="empty-note">Generated ${esc(DATA.generated)} from lore markdown frontmatter and bodies.<br>` +
    `Map positions come from <code style="background:rgba(255,255,255,0.07);border-radius:5px;padding:1px 5px">dashboard/map-registry.yaml</code>.<br>` +
    `Regenerate with <code style="background:rgba(255,255,255,0.07);border-radius:5px;padding:1px 5px">python3 scripts/build_story_dashboard.py</code></div></div>`;

  grid.innerHTML = html;
  grid.addEventListener('click', (e) => {
    const themeEl = e.target.closest('[data-theme]');
    if (themeEl) { selectTheme(themeEl.dataset.theme); return; }
    const openEl = e.target.closest('[data-open]');
    if (openEl) openEntry(openEl.dataset.open);
  });
})();

/* ============ world map (canvas) ============ */
window.DiasMap = (function initWorldMap() {
  const mapData = DATA.map || { frequencies: {}, default_frequency: null };
  const freqs = mapData.frequencies || {};
  const freqSelect = document.getElementById('map-freq');
  const noteEl = document.getElementById('map-note');
  const statsEl = document.getElementById('map-stats');
  const canvas = document.getElementById('world-map');
  const wrap = document.getElementById('map-wrap');
  const hoverEl = document.getElementById('map-hover');
  if (!canvas || !freqSelect) return { resize() {} };

  const ctx = canvas.getContext('2d');
  const KIND_COLOR = {
    place: '#8fa9ff',
    landmark: '#e2c36b',
    inhabitant: '#d48cff',
    story: '#7dcea0',
    myth: '#f0a060',
    artifact: '#6ec6d4',
    artwork: '#f278a8',
    culture: '#a8d46e',
    phenomenon: '#c090ff',
    symbol: '#ffd27a',
    rule: '#9aa7c2',
    world: '#ffffff'
  };
  const layers = {
    regions: document.getElementById('map-layer-regions'),
    places: document.getElementById('map-layer-places'),
    landmarks: document.getElementById('map-layer-landmarks'),
    inhabitants: document.getElementById('map-layer-inhabitants'),
    stories: document.getElementById('map-layer-stories'),
    myths: document.getElementById('map-layer-myths'),
    artifacts: document.getElementById('map-layer-artifacts'),
    artworks: document.getElementById('map-layer-artworks'),
    cultures: document.getElementById('map-layer-cultures'),
    phenomena: document.getElementById('map-layer-phenomena'),
    symbols: document.getElementById('map-layer-symbols'),
    rules: document.getElementById('map-layer-rules'),
    world: document.getElementById('map-layer-world')
  };

  let freqId = mapData.default_frequency || Object.keys(freqs)[0] || null;
  let view = { scale: 1, ox: 0, oy: 0 };
  let hoverHit = null;
  let dragging = false;
  let lastX = 0, lastY = 0;
  let hitList = [];

  for (const id of Object.keys(freqs)) {
    const opt = document.createElement('option');
    opt.value = id;
    opt.textContent = freqs[id].label || id;
    if (id === freqId) opt.selected = true;
    freqSelect.appendChild(opt);
  }

  function currentFreq() {
    return freqs[freqId] || null;
  }

  function layerOn(kind) {
    const map = {
      place: layers.places,
      landmark: layers.landmarks,
      inhabitant: layers.inhabitants,
      story: layers.stories,
      myth: layers.myths,
      artifact: layers.artifacts,
      artwork: layers.artworks,
      culture: layers.cultures,
      phenomenon: layers.phenomena,
      symbol: layers.symbols,
      rule: layers.rules,
      world: layers.world
    };
    const el = map[kind];
    return el ? el.checked : true;
  }

  function worldToScreen(x, y, w, h) {
    return {
      x: view.ox + (x / 100) * w * view.scale,
      y: view.oy + (y / 100) * h * view.scale
    };
  }

  function screenToWorld(sx, sy, w, h) {
    return {
      x: ((sx - view.ox) / (w * view.scale)) * 100,
      y: ((sy - view.oy) / (h * view.scale)) * 100
    };
  }

  function drawPoly(poly, w, h, fill, stroke) {
    if (!poly || poly.length < 3) return;
    ctx.beginPath();
    poly.forEach((pt, i) => {
      const p = worldToScreen(pt[0], pt[1], w, h);
      if (i === 0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y);
    });
    ctx.closePath();
    if (fill) { ctx.fillStyle = fill; ctx.fill(); }
    if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = 1; ctx.stroke(); }
  }

  function drawPixelMarker(sx, sy, kind, size) {
    const color = KIND_COLOR[kind] || '#fff';
    const s = Math.max(2, size);
    const x = Math.round(sx);
    const y = Math.round(sy);
    ctx.fillStyle = color;
    ctx.strokeStyle = 'rgba(0,0,0,0.45)';
    ctx.lineWidth = 1;

    if (kind === 'inhabitant') {
      // person: head + body
      ctx.fillRect(x - 1, y - s, 2, 2);
      ctx.fillRect(x - s + 1, y - s + 3, s * 2 - 2, s);
    } else if (kind === 'landmark') {
      // triangle peak
      ctx.beginPath();
      ctx.moveTo(x, y - s);
      ctx.lineTo(x + s, y + s);
      ctx.lineTo(x - s, y + s);
      ctx.closePath();
      ctx.fill();
    } else if (kind === 'story') {
      // open book
      ctx.fillRect(x - s, y - s + 1, s * 2, s * 2 - 2);
      ctx.fillStyle = 'rgba(0,0,0,0.35)';
      ctx.fillRect(x - 1, y - s + 1, 2, s * 2 - 2);
    } else if (kind === 'myth') {
      // diamond
      ctx.beginPath();
      ctx.moveTo(x, y - s);
      ctx.lineTo(x + s, y);
      ctx.lineTo(x, y + s);
      ctx.lineTo(x - s, y);
      ctx.closePath();
      ctx.fill();
    } else if (kind === 'artifact') {
      // hex-ish square with notch
      ctx.fillRect(x - s, y - s, s * 2, s * 2);
      ctx.fillStyle = 'rgba(0,0,0,0.35)';
      ctx.fillRect(x - 1, y - 1, 2, 2);
    } else if (kind === 'artwork') {
      // frame
      ctx.fillRect(x - s, y - s, s * 2, s * 2);
      ctx.fillStyle = 'rgba(0,0,0,0.4)';
      ctx.fillRect(x - s + 2, y - s + 2, s * 2 - 4, s * 2 - 4);
    } else if (kind === 'culture') {
      // ring
      ctx.beginPath();
      ctx.arc(x, y, s - 0.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = 'rgba(10,12,18,0.85)';
      ctx.beginPath();
      ctx.arc(x, y, Math.max(1, s - 2.5), 0, Math.PI * 2);
      ctx.fill();
    } else if (kind === 'phenomenon') {
      // spark / plus
      ctx.fillRect(x - 1, y - s, 2, s * 2);
      ctx.fillRect(x - s, y - 1, s * 2, 2);
    } else if (kind === 'symbol') {
      // star-ish X
      ctx.fillRect(x - 1, y - s, 2, s * 2);
      ctx.fillRect(x - s, y - 1, s * 2, 2);
      ctx.fillRect(x - s + 1, y - s + 1, 2, 2);
      ctx.fillRect(x + s - 3, y - s + 1, 2, 2);
      ctx.fillRect(x - s + 1, y + s - 3, 2, 2);
      ctx.fillRect(x + s - 3, y + s - 3, 2, 2);
    } else if (kind === 'rule') {
      // tablet
      ctx.fillRect(x - s + 1, y - s, s * 2 - 2, s * 2);
      ctx.fillStyle = 'rgba(0,0,0,0.35)';
      ctx.fillRect(x - s + 3, y - 2, s * 2 - 6, 1);
      ctx.fillRect(x - s + 3, y + 1, s * 2 - 6, 1);
    } else if (kind === 'world') {
      // globe square
      ctx.beginPath();
      ctx.arc(x, y, s - 0.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = 'rgba(0,0,0,0.5)';
      ctx.beginPath();
      ctx.arc(x, y, s - 0.5, 0, Math.PI * 2);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(x - s + 1, y);
      ctx.lineTo(x + s - 1, y);
      ctx.stroke();
    } else {
      // place: solid block
      ctx.fillRect(x - s, y - s, s * 2, s * 2);
    }
    // shadow lip for click readability
    ctx.fillStyle = 'rgba(0,0,0,0.25)';
    ctx.fillRect(x - s, y + s - 1, s * 2, 1);
  }

  function draw() {
    const freq = currentFreq();
    const rect = wrap.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    const cssW = Math.max(320, rect.width);
    const cssH = Math.max(280, rect.height);
    canvas.width = Math.floor(cssW * dpr);
    canvas.height = Math.floor(cssH * dpr);
    canvas.style.width = cssW + 'px';
    canvas.style.height = cssH + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.imageSmoothingEnabled = false;

    const w = cssW;
    const h = cssH;
    hitList = [];

    ctx.fillStyle = (freq && freq.water) || '#0c2438';
    ctx.fillRect(0, 0, w, h);

    if (!freq) {
      noteEl.textContent = 'No map registry loaded.';
      statsEl.textContent = '';
      return;
    }

    noteEl.textContent = freq.note || '';
    const resolvedMarkers = (freq.markers || []).filter(m => m.entry_id).length;
    statsEl.textContent =
      `${(freq.regions || []).length} regions · ${(freq.markers || []).length} pins · ${resolvedMarkers} linked`;

    for (const lm of freq.landmasses || []) {
      drawPoly(lm.polygon, w, h, lm.fill || freq.land, 'rgba(255,255,255,0.22)');
    }

    if (layers.regions.checked) {
      for (const reg of freq.regions || []) {
        drawPoly(reg.polygon, w, h, reg.fill || 'rgba(255,255,255,0.12)', 'rgba(255,255,255,0.18)');
        // centroid label
        let cx = 0, cy = 0;
        for (const pt of reg.polygon) { cx += pt[0]; cy += pt[1]; }
        cx /= reg.polygon.length; cy /= reg.polygon.length;
        const p = worldToScreen(cx, cy, w, h);
        ctx.fillStyle = 'rgba(233,235,242,0.75)';
        ctx.font = '600 11px Inter, system-ui, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(reg.entry || reg.id, p.x, p.y);
        hitList.push({
          kind: 'region',
          entry_id: reg.entry_id,
          label: reg.entry || reg.id,
          x: cx, y: cy, r: 4
        });
      }
    }

    const markerSize = Math.max(3, Math.min(7, 4 * view.scale));
    for (const m of freq.markers || []) {
      if (!layerOn(m.kind)) continue;
      const p = worldToScreen(m.x, m.y, w, h);
      drawPixelMarker(p.x, p.y, m.kind, markerSize);
      hitList.push({
        kind: m.kind,
        entry_id: m.entry_id,
        label: m.label || m.entry,
        x: m.x, y: m.y, r: markerSize + 2
      });
    }

    if (hoverHit) {
      const p = worldToScreen(hoverHit.x, hoverHit.y, w, h);
      ctx.strokeStyle = 'rgba(255,255,255,0.85)';
      ctx.lineWidth = 1;
      ctx.strokeRect(Math.round(p.x - markerSize - 2), Math.round(p.y - markerSize - 2), (markerSize + 2) * 2, (markerSize + 2) * 2);
    }
  }

  function pick(sx, sy) {
    const rect = wrap.getBoundingClientRect();
    const w = rect.width, h = rect.height;
    let best = null, bestD = 1e9;
    // Prefer markers over region labels when both are near the cursor.
    const ordered = hitList.slice().sort((a, b) => {
      const ar = a.kind === 'region' ? 1 : 0;
      const br = b.kind === 'region' ? 1 : 0;
      return ar - br;
    });
    for (const hit of ordered) {
      const p = worldToScreen(hit.x, hit.y, w, h);
      const dx = p.x - sx, dy = p.y - sy;
      const d = Math.sqrt(dx * dx + dy * dy);
      const maxR = hit.kind === 'region' ? 22 : Math.max(10, (hit.r || 8) + 6);
      if (d <= maxR && d < bestD) { best = hit; bestD = d; }
    }
    return best;
  }

  function showHover(hit, clientX, clientY) {
    if (!hit) { hoverEl.classList.remove('open'); return; }
    const node = hit.entry_id ? nodesById.get(hit.entry_id) : null;
    const wrapRect = wrap.getBoundingClientRect();
    let html = `<div class="mh-kind">${esc(hit.kind)}</div><div class="mh-title">${esc(hit.label)}</div>`;
    if (node && node.summary) html += `<div class="mh-sum">${esc(node.summary)}</div>`;
    else if (!node) html += `<div class="mh-miss">Not linked to a lore entry yet.</div>`;
    hoverEl.innerHTML = html;
    hoverEl.classList.add('open');
    const left = Math.min(wrapRect.width - 200, Math.max(8, clientX - wrapRect.left + 14));
    const top = Math.min(wrapRect.height - 80, Math.max(8, clientY - wrapRect.top + 14));
    hoverEl.style.left = left + 'px';
    hoverEl.style.top = top + 'px';
  }

  function resetView() {
    view = { scale: 1, ox: 0, oy: 0 };
    draw();
  }

  freqSelect.addEventListener('change', () => {
    freqId = freqSelect.value;
    resetView();
  });
  for (const el of Object.values(layers)) {
    el.addEventListener('change', draw);
  }

  canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    const sx = e.clientX - rect.left;
    const sy = e.clientY - rect.top;
    if (dragging) {
      view.ox += sx - lastX;
      view.oy += sy - lastY;
      lastX = sx; lastY = sy;
      hoverHit = null;
      hoverEl.classList.remove('open');
      draw();
      return;
    }
    hoverHit = pick(sx, sy);
    canvas.style.cursor = hoverHit ? 'pointer' : (dragging ? 'grabbing' : 'crosshair');
    draw();
    showHover(hoverHit, e.clientX, e.clientY);
  });
  canvas.addEventListener('mouseleave', () => {
    hoverHit = null;
    hoverEl.classList.remove('open');
    dragging = false;
    draw();
  });
  canvas.addEventListener('mousedown', (e) => {
    const rect = canvas.getBoundingClientRect();
    lastX = e.clientX - rect.left;
    lastY = e.clientY - rect.top;
    dragging = true;
  });
  window.addEventListener('mouseup', () => { dragging = false; });
  canvas.addEventListener('click', (e) => {
    if (Math.abs(e.movementX) + Math.abs(e.movementY) > 4) return;
    const rect = canvas.getBoundingClientRect();
    const hit = pick(e.clientX - rect.left, e.clientY - rect.top);
    if (hit && hit.entry_id) openEntry(hit.entry_id);
  });
  canvas.addEventListener('wheel', (e) => {
    e.preventDefault();
    const rect = canvas.getBoundingClientRect();
    const sx = e.clientX - rect.left;
    const sy = e.clientY - rect.top;
    const before = screenToWorld(sx, sy, rect.width, rect.height);
    const factor = e.deltaY < 0 ? 1.1 : 0.9;
    view.scale = Math.max(0.6, Math.min(4.5, view.scale * factor));
    const after = worldToScreen(before.x, before.y, rect.width, rect.height);
    view.ox += sx - after.x;
    view.oy += sy - after.y;
    draw();
  }, { passive: false });

  window.addEventListener('resize', () => {
    if (activeTab === 'map') draw();
  });

  draw();
  return {
    resize() { draw(); },
    redraw: draw,
    warnings: mapData.warnings || []
  };
})();

/* ============ boot ============ */
scheduleFit();
applyGraphFilters();
const TAB_NAMES = ['graph', 'map', 'explorer', 'gallery', 'themes', 'hierarchy', 'insights'];
function applyHash() {
  const h = decodeURIComponent((location.hash || '').replace('#', ''));
  if (TAB_NAMES.includes(h)) { switchTab(h); return; }
  if (h.startsWith('entry=')) {
    const id = h.slice(6);
    if (nodesById.has(id)) openEntry(id);
  }
}
window.addEventListener('hashchange', applyHash);
applyHash();
</script>
</body>
</html>
"""


def main() -> None:
    entries = discover_entries()
    payload = build_payload(entries)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render_html(payload, world_title(entries)), encoding="utf-8")
    nodes = payload["nodes"]
    edges = payload["edges"]
    unresolved = sum(len(n["unresolved"]) for n in nodes)  # type: ignore[index]
    print(f"Generated {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Entries: {len(nodes)} | Links: {len(edges)} | Unresolved refs: {unresolved}")  # type: ignore[arg-type]

    world_map = payload.get("map") or {}
    stats = world_map.get("stats") or {}
    print(
        "Map: "
        f"{stats.get('frequencies', 0)} frequencies | "
        f"{stats.get('regions', 0)} region polys | "
        f"{stats.get('markers', 0)} markers "
        f"(manual {stats.get('manual_markers', 0)} / auto {stats.get('auto_markers', 0)}) | "
        f"{stats.get('unresolved', 0)} unresolved map refs"
    )
    for warning in world_map.get("warnings") or []:
        print(f"  map warning: {warning}")


if __name__ == "__main__":
    main()
