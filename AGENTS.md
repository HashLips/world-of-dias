# Agent Guidance — World of Dias

Thin root entry for agents and authoring tools.

**Human orientation** stays at the repo root (`START-HERE.md`, `GUIDED-PATH.md`, `CORE-PILLARS.md`, `SAGAS.md`, and related paths).  
**Agent-only ops** live under [`agent/`](agent/).  
**Always-on Cursor rules** live under [`.cursor/rules/`](.cursor/rules/).

Lore stays in category folders. Do not invent a second lore store.

## Human docs agents should also read

| File | Role |
| --- | --- |
| [`START-HERE.md`](START-HERE.md) | Fast entry |
| [`README.md`](README.md) | Repo purpose and sharing notice |
| [`CORE-PILLARS.md`](CORE-PILLARS.md) | World identity pillars and exemplars |
| [`GUIDED-PATH.md`](GUIDED-PATH.md) | Stable reading path through canon |
| [`SAGAS.md`](SAGAS.md) | Saga index |
| [`HARMONIC-SAGA-PATH.md`](HARMONIC-SAGA-PATH.md) | Main narrative journey |

## Agent-only materials

| File | Role |
| --- | --- |
| [`agent/DIAS-REFERENCE-MAP.md`](agent/DIAS-REFERENCE-MAP.md) | External GUID bridge (IRL / Arweave / social / physical) |
| [`agent/dias-map.yaml`](agent/dias-map.yaml) | Permanent `DIAS-{UUID}` → Markdown index |
| [`.cursor/rules/dias-reference-map.mdc`](.cursor/rules/dias-reference-map.mdc) | Always-on permanence rule |

## Lore folders

Canon entries live in: `world/`, `regions/`, `rules/`, `cultures/`, `inhabitants/`, `artifacts/`, `phenomena/`, `myths/`, `stories/`, `symbols/`, `artworks/`, `assets/`.

Note: `rules/` is **world lore** (laws, protocols). Agent instructions are **not** stored there.

## External references

When capturing something outside this repo (artwork, letter, Arweave, social post, NFC, Easter egg, and so on):

1. Read [`agent/DIAS-REFERENCE-MAP.md`](agent/DIAS-REFERENCE-MAP.md).
2. Add or update an entry in [`agent/dias-map.yaml`](agent/dias-map.yaml).
3. Point `file` at an existing canonical Markdown entry when possible (paths are relative to the **repo root**).
4. Treat mapped Markdown files as protected during moves, renames, and cleanup.

Core rule: **DIAS GUID → Markdown file**. The map is a bridge, not a lore database.

## How to grow the world

1. Prefer extending and categorizing existing entries over rewriting them.
2. Use [`CORE-PILLARS.md`](CORE-PILLARS.md) when deciding what new lore should serve.
3. Keep [`GUIDED-PATH.md`](GUIDED-PATH.md) steps 1–5 stable; add saga journeys via [`SAGAS.md`](SAGAS.md).
4. Create a Dias ID only when something must be independently referenceable outside normal Markdown lore.
