#!/usr/bin/env python3
"""Load, validate, and auto-complete dashboard/map-registry.yaml for the Map tab."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "PyYAML is required for the map registry. Install with: pip install pyyaml"
    ) from exc

ROOT = Path(__file__).resolve().parents[1]
MAP_REGISTRY_PATH = ROOT / "dashboard" / "map-registry.yaml"

# Lore categories that receive map pins.
MAPPABLE_CATEGORIES = {
    "region",
    "inhabitant",
    "story",
    "myth",
    "artifact",
    "artwork",
    "culture",
    "phenomenon",
    "symbol",
    "rule",
    "world",
}

VALID_KINDS = set(MAPPABLE_CATEGORIES) | {"place", "landmark", "land"}

FREQ_NAME_TO_ID = {
    "f120 (frequency realm)": "f120",
    "f200 (frequency realm)": "f200",
    "f380 (frequency realm)": "f380",
    "f432 (frequency realm)": "f432",
    "f500 (frequency realm)": "f500",
    "f610 (frequency realm)": "f610",
    "f840 (frequency realm)": "f840",
    "f960 (frequency realm)": "f960",
}

MIN_SEP = 1.35  # minimum map-units between markers


def load_map_registry(path: Path = MAP_REGISTRY_PATH) -> Dict[str, object]:
    if not path.exists():
        return {
            "version": 1,
            "default_frequency": None,
            "frequencies": {},
            "warnings": [f"Missing map registry: {path.relative_to(ROOT)}"],
            "stats": {"frequencies": 0, "markers": 0, "regions": 0, "unresolved": 0},
        }
    with path.open(encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    if not isinstance(raw, dict):
        raise ValueError("map-registry.yaml must be a mapping at the top level")
    return raw


def _resolve(
    ref: str,
    title_index: Dict[str, str],
    slug_index: Dict[str, str],
    slugify,
) -> Optional[str]:
    key = ref.lower().strip()
    return title_index.get(key) or slug_index.get(slugify(ref))


def _centroid(poly: Sequence[Sequence[float]]) -> Tuple[float, float]:
    xs = [float(p[0]) for p in poly]
    ys = [float(p[1]) for p in poly]
    return sum(xs) / len(xs), sum(ys) / len(ys)


def _kind_for_entry(category: str, place_type: str = "") -> str:
    cat = (category or "").strip().lower()
    pt = (place_type or "").strip().lower()
    if cat == "region":
        if pt in {"landmark", "gallery", "pub", "shop", "building"}:
            return "landmark"
        if pt in {"town", "city", "district", "island", "territory"}:
            return "place"
        return "place"
    if cat in MAPPABLE_CATEGORIES:
        return cat
    return "place"


def _freq_id_from_name(name: str) -> Optional[str]:
    return FREQ_NAME_TO_ID.get(name.lower().strip())


def _walk_freq(
    entry_id: str,
    by_id: Dict[str, dict],
    cache: Dict[str, Optional[str]],
) -> Optional[str]:
    if entry_id in cache:
        return cache[entry_id]
    node = by_id.get(entry_id)
    if not node:
        cache[entry_id] = None
        return None
    label = node["label"]
    direct = _freq_id_from_name(label)
    if direct:
        cache[entry_id] = direct
        return direct
    for key in ("region", "parent_region"):
        ref = (node.get(key) or "").strip()
        if not ref:
            continue
        # Prefer exact title match in by_id via label lookup later
        for other in by_id.values():
            if other["label"].lower() == ref.lower():
                found = _walk_freq(other["id"], by_id, cache)
                if found:
                    cache[entry_id] = found
                    return found
        # Also accept raw frequency realm names
        found = _freq_id_from_name(ref)
        if found:
            cache[entry_id] = found
            return found
    # Dias-scoped content defaults to f432 lived theater unless it's clearly other
    region = (node.get("region") or "").lower()
    if region == "dias" or not region:
        cache[entry_id] = "f432"
        return "f432"
    cache[entry_id] = "f432"
    return "f432"


def _find_slot(
    x: float,
    y: float,
    occupied: List[Tuple[float, float]],
    min_sep: float = MIN_SEP,
) -> Tuple[float, float]:
    def free(px: float, py: float) -> bool:
        if not (1.5 <= px <= 98.5 and 1.5 <= py <= 98.5):
            return False
        for ox, oy in occupied:
            if (px - ox) ** 2 + (py - oy) ** 2 < min_sep * min_sep:
                return False
        return True

    if free(x, y):
        return x, y
    # Spiral search
    for ring in range(1, 80):
        radius = ring * (min_sep * 0.7)
        steps = max(8, ring * 6)
        for i in range(steps):
            ang = (2 * math.pi * i) / steps
            px = x + math.cos(ang) * radius
            py = y + math.sin(ang) * radius
            if free(px, py):
                return px, py
    # Last resort: nudge randomly along ring
    return max(2.0, min(98.0, x)), max(2.0, min(98.0, y))


def compile_map_payload(
    registry: Dict[str, object],
    title_index: Dict[str, str],
    slug_index: Dict[str, str],
    slugify,
    entries: Optional[Sequence[object]] = None,
) -> Tuple[Dict[str, object], List[str]]:
    """Resolve lore entries, auto-place missing pins, return (payload, warnings)."""
    warnings: List[str] = []
    frequencies_out: Dict[str, object] = {}
    region_total = 0
    unresolved = 0
    manual_markers = 0
    auto_markers = 0

    freqs = registry.get("frequencies") or {}
    if not isinstance(freqs, dict):
        warnings.append("frequencies must be a mapping")
        freqs = {}

    # Normalize entry list into plain dicts
    entry_nodes: List[dict] = []
    by_id: Dict[str, dict] = {}
    if entries:
        for e in entries:
            node = {
                "id": e.id,
                "label": e.title,
                "category": e.category,
                "region": e.meta.get("region", ""),
                "parent_region": e.meta.get("parent_region", ""),
                "place_type": e.meta.get("place_type", ""),
                "summary": e.summary,
            }
            entry_nodes.append(node)
            by_id[e.id] = node

    freq_cache: Dict[str, Optional[str]] = {}

    # First pass: compile authored geography
    authored: Dict[str, dict] = {}
    for freq_id, freq in freqs.items():
        if not isinstance(freq, dict):
            warnings.append(f"{freq_id}: frequency block must be a mapping")
            continue

        entry_name = str(freq.get("entry") or "").strip()
        entry_id = _resolve(entry_name, title_index, slug_index, slugify) if entry_name else None
        if entry_name and not entry_id:
            unresolved += 1
            warnings.append(f"{freq_id}: unresolved frequency entry '{entry_name}'")

        grid = freq.get("grid") or [100, 100]
        if not (isinstance(grid, list) and len(grid) == 2):
            grid = [100, 100]
            warnings.append(f"{freq_id}: invalid grid; using [100, 100]")

        landmasses = []
        for lm in freq.get("landmasses") or []:
            if not isinstance(lm, dict):
                continue
            poly = lm.get("polygon") or []
            if len(poly) < 3:
                warnings.append(f"{freq_id}/{lm.get('id', '?')}: landmass needs ≥3 points")
                continue
            landmasses.append(
                {
                    "id": str(lm.get("id") or ""),
                    "label": str(lm.get("label") or lm.get("id") or ""),
                    "fill": lm.get("fill"),
                    "polygon": poly,
                }
            )

        regions = []
        anchors: Dict[str, Tuple[float, float]] = {}
        for reg in freq.get("regions") or []:
            if not isinstance(reg, dict):
                continue
            region_total += 1
            r_entry = str(reg.get("entry") or "").strip()
            r_id = _resolve(r_entry, title_index, slug_index, slugify) if r_entry else None
            if r_entry and not r_id:
                unresolved += 1
                warnings.append(f"{freq_id}: unresolved region entry '{r_entry}'")
            poly = reg.get("polygon") or []
            if len(poly) < 3:
                warnings.append(f"{freq_id}/{reg.get('id', r_entry)}: region needs ≥3 points")
                continue
            regions.append(
                {
                    "id": str(reg.get("id") or ""),
                    "entry": r_entry,
                    "entry_id": r_id,
                    "fill": reg.get("fill"),
                    "polygon": poly,
                }
            )
            cx, cy = _centroid(poly)
            if r_id:
                anchors[r_id] = (cx, cy)
            if r_entry:
                anchors[r_entry.lower()] = (cx, cy)

        for lm in landmasses:
            cx, cy = _centroid(lm["polygon"])
            anchors[f"land:{lm['id']}"] = (cx, cy)

        # Hand markers (preferred positions)
        hand: List[dict] = []
        for mark in freq.get("markers") or []:
            if not isinstance(mark, dict):
                continue
            manual_markers += 1
            m_entry = str(mark.get("entry") or "").strip()
            m_id = _resolve(m_entry, title_index, slug_index, slugify) if m_entry else None
            if m_entry and not m_id:
                unresolved += 1
                warnings.append(f"{freq_id}: unresolved marker '{m_entry}'")
            kind = str(mark.get("kind") or "place").strip().lower()
            if kind == "land":
                kind = "place"
            if kind not in VALID_KINDS:
                # allow legacy kinds
                if kind not in {"place", "landmark"}:
                    warnings.append(f"{freq_id}/{m_entry}: unknown kind '{kind}' (using place)")
                    kind = "place"
            try:
                x = float(mark["x"])
                y = float(mark["y"])
            except (KeyError, TypeError, ValueError):
                warnings.append(f"{freq_id}/{m_entry}: marker needs numeric x,y")
                continue
            if m_id and m_id in by_id:
                kind = _kind_for_entry(by_id[m_id]["category"], by_id[m_id].get("place_type", ""))
                # keep landmark override if author set landmark for a region landmark
                if str(mark.get("kind") or "").lower() == "landmark":
                    kind = "landmark"
            hand.append(
                {
                    "entry": m_entry,
                    "entry_id": m_id,
                    "x": x,
                    "y": y,
                    "kind": kind,
                    "label": str(mark.get("label") or m_entry),
                    "source": "registry",
                }
            )
            if m_id:
                anchors[m_id] = (x, y)
            anchors[m_entry.lower()] = (x, y)

        authored[str(freq_id)] = {
            "id": str(freq_id),
            "label": str(freq.get("label") or freq_id),
            "entry": entry_name,
            "entry_id": entry_id,
            "note": str(freq.get("note") or ""),
            "water": str(freq.get("water") or "#0c2438"),
            "land": str(freq.get("land") or "#2f4a32"),
            "grid": [int(grid[0]), int(grid[1])],
            "landmasses": landmasses,
            "regions": regions,
            "hand": hand,
            "anchors": anchors,
        }

    # Auto-place every mappable entry onto a frequency layer
    placed_ids: Dict[str, str] = {}  # entry_id -> freq
    occupied: Dict[str, List[Tuple[float, float]]] = {fid: [] for fid in authored}

    # Seed occupied with hand markers
    for fid, block in authored.items():
        for m in block["hand"]:
            occupied[fid].append((m["x"], m["y"]))
            if m.get("entry_id"):
                placed_ids[m["entry_id"]] = fid

    def anchor_for(node: dict, freq_id: str) -> Tuple[float, float]:
        block = authored[freq_id]
        anchors = block["anchors"]
        # Prefer parent / region anchors
        for key in (node.get("parent_region"), node.get("region"), node["label"]):
            if not key:
                continue
            if key.lower() in anchors:
                return anchors[key.lower()]
            # match by resolved id label
            rid = _resolve(key, title_index, slug_index, slugify)
            if rid and rid in anchors:
                return anchors[rid]
        # Prefer any hand/region centroid
        if anchors:
            # average of all anchors
            xs = [p[0] for p in anchors.values()]
            ys = [p[1] for p in anchors.values()]
            return sum(xs) / len(xs), sum(ys) / len(ys)
        return 50.0, 50.0

    auto_by_freq: Dict[str, List[dict]] = {fid: [] for fid in authored}

    for node in entry_nodes:
        if node["category"] not in MAPPABLE_CATEGORIES:
            continue
        # Frequency realm root entries: skip as pins (they are the layer)
        if _freq_id_from_name(node["label"]):
            continue
        if node["id"] in placed_ids:
            continue
        freq_id = _walk_freq(node["id"], by_id, freq_cache) or "f432"
        if freq_id not in authored:
            # create stub layer on the fly
            authored[freq_id] = {
                "id": freq_id,
                "label": freq_id.upper(),
                "entry": "",
                "entry_id": None,
                "note": "Auto-created stub layer",
                "water": "#102030",
                "land": "#304050",
                "grid": [100, 100],
                "landmasses": [],
                "regions": [],
                "hand": [],
                "anchors": {},
            }
            occupied[freq_id] = []
            auto_by_freq[freq_id] = []

        ax, ay = anchor_for(node, freq_id)
        x, y = _find_slot(ax, ay, occupied[freq_id])
        occupied[freq_id].append((x, y))
        kind = _kind_for_entry(node["category"], node.get("place_type", ""))
        auto_by_freq[freq_id].append(
            {
                "entry": node["label"],
                "entry_id": node["id"],
                "x": round(x, 2),
                "y": round(y, 2),
                "kind": kind,
                "label": node["label"],
                "source": "auto",
            }
        )
        placed_ids[node["id"]] = freq_id
        auto_markers += 1
        # Update anchors so children can cluster nearby
        authored[freq_id]["anchors"][node["id"]] = (x, y)
        authored[freq_id]["anchors"][node["label"].lower()] = (x, y)

    # Merge hand + auto (hand first; skip auto duplicates)
    for freq_id, block in authored.items():
        markers = list(block["hand"])
        seen = {m["entry_id"] for m in markers if m.get("entry_id")}
        for m in auto_by_freq.get(freq_id, []):
            if m["entry_id"] in seen:
                continue
            markers.append(m)
            seen.add(m["entry_id"])
        frequencies_out[freq_id] = {
            "id": block["id"],
            "label": block["label"],
            "entry": block["entry"],
            "entry_id": block["entry_id"],
            "note": block["note"],
            "water": block["water"],
            "land": block["land"],
            "grid": block["grid"],
            "landmasses": block["landmasses"],
            "regions": block["regions"],
            "markers": markers,
        }

    default_frequency = registry.get("default_frequency") or (
        "f432" if "f432" in frequencies_out else next(iter(frequencies_out.keys()), None)
    )
    if default_frequency and default_frequency not in frequencies_out:
        warnings.append(f"default_frequency '{default_frequency}' not found in frequencies")
        default_frequency = next(iter(frequencies_out.keys()), None)

    unmapped = [
        n["label"]
        for n in entry_nodes
        if n["category"] in MAPPABLE_CATEGORIES
        and not _freq_id_from_name(n["label"])
        and n["id"] not in placed_ids
    ]
    if unmapped:
        warnings.append(f"{len(unmapped)} mappable entries still unplaced")

    marker_total = sum(len(f["markers"]) for f in frequencies_out.values())
    payload = {
        "version": registry.get("version", 1),
        "default_frequency": default_frequency,
        "frequencies": frequencies_out,
        "registry_path": MAP_REGISTRY_PATH.relative_to(ROOT).as_posix(),
        "stats": {
            "frequencies": len(frequencies_out),
            "markers": marker_total,
            "regions": region_total,
            "unresolved": unresolved,
            "warnings": len(warnings),
            "manual_markers": manual_markers,
            "auto_markers": auto_markers,
            "placed_entries": len(placed_ids),
        },
        "warnings": warnings,
    }
    return payload, warnings
