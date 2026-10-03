# Agent Guidance — World of Dias

Thin root entry for agents and authoring tools.

**Human orientation** stays at the repo root (`START-HERE.md`, `GUIDED-PATH.md`, `CORE-PILLARS.md`, `SAGAS.md`, and related paths).  
**Agent-only ops** live under [`agent/`](agent/).  
**Always-on Cursor rules** live under [`.cursor/rules/`](.cursor/rules/).

Lore stays in category folders. Do not invent a second lore store.

## Before you contribute (required)

Any agent that creates or edits lore must:

1. Read [`agent/contributor-start.md`](agent/contributor-start.md).
2. **Always use the Story Architect skill** — read its `SKILL.md` and `references/` (schema, templates, naming, categories, canon rules) before writing files. Do not invent a parallel format or stub schema.
3. Follow [`agent/canon-safety.md`](agent/canon-safety.md) (soft limits, conflict framing, GUID protection).
4. Orient with [`agent/world-orientation.md`](agent/world-orientation.md), then check [`agent/stage-readiness.md`](agent/stage-readiness.md) for what is safe to write next.

Always-on reminder: [`.cursor/rules/dias-contributor.mdc`](.cursor/rules/dias-contributor.mdc).

## Human docs agents should also read

| File | Role |
| --- | --- |
| [`START-HERE.md`](START-HERE.md) | Fast entry |
| [`README.md`](README.md) | Repo purpose and sharing notice |
| [`CORE-PILLARS.md`](CORE-PILLARS.md) | World identity pillars and exemplars |
| [`GUIDED-PATH.md`](GUIDED-PATH.md) | Stable reading path through canon |
| [`SAGAS.md`](SAGAS.md) | Saga index |
| [`HARMONIC-SAGA-PATH.md`](HARMONIC-SAGA-PATH.md) | Main narrative journey |
| [`LUMEN-SAGA-PATH.md`](LUMEN-SAGA-PATH.md) | Second narrative journey |
| [`CALIBRATION-SAGA-PATH.md`](CALIBRATION-SAGA-PATH.md) | Third narrative journey (spectrum / Caliburn) |

## Agent-only materials

| File | Role |
| --- | --- |
| [`agent/contributor-start.md`](agent/contributor-start.md) | **First stop** for contributing agents; Story Architect gate + checklist |
| [`agent/canon-safety.md`](agent/canon-safety.md) | Soft limits, canon-safe enrichment, GUID protection |
| [`agent/world-orientation.md`](agent/world-orientation.md) | Hubs, primers, navigation starting points |
| [`agent/stage-readiness.md`](agent/stage-readiness.md) | What sagas/arcs may touch next; forbidden solves |
| [`agent/DIAS-REFERENCE-MAP.md`](agent/DIAS-REFERENCE-MAP.md) | External GUID bridge (IRL / Arweave / social / physical) |
| [`agent/dias-map.yaml`](agent/dias-map.yaml) | Permanent `DIAS-{UUID}` → Markdown index |
| [`agent/plan.md`](agent/plan.md) | World expansion plan (stage-building; section-by-section; complete) |
| [`agent/secrets-pointer.md`](agent/secrets-pointer.md) | Author secret staging (saga-key vs texture; not a spoiler bible) |
| [`.cursor/rules/dias-contributor.mdc`](.cursor/rules/dias-contributor.mdc) | Always-on: Story Architect + contributor docs |
| [`.cursor/rules/dias-reference-map.mdc`](.cursor/rules/dias-reference-map.mdc) | Always-on permanence rule for Dias GUIDs |
| [`dashboard/map-registry.yaml`](dashboard/map-registry.yaml) | 2D atlas pin/land positions for the Map tab |

## Lore folders

Canon entries live in: `world/`, `regions/`, `rules/`, `cultures/`, `inhabitants/`, `flora/`, `artifacts/`, `phenomena/`, `myths/`, `stories/`, `symbols/`, `artworks/`, `assets/`.

Note: `rules/` is **world lore** (laws, protocols). Agent instructions are **not** stored there. `flora/` holds plant species and growth entries; [`world/flora-of-dias.md`](world/flora-of-dias.md) is the index.

## External references

When capturing something outside this repo (artwork, letter, Arweave, social post, NFC, Easter egg, and so on):

1. Read [`agent/DIAS-REFERENCE-MAP.md`](agent/DIAS-REFERENCE-MAP.md).
2. Add or update an entry in [`agent/dias-map.yaml`](agent/dias-map.yaml).
3. Point `file` at an existing canonical Markdown entry when possible (paths are relative to the **repo root**).
4. Treat mapped Markdown files as protected during moves, renames, and cleanup.

Core rule: **DIAS GUID → Markdown file**. The map is a bridge, not a lore database.

## How to grow the world

Follow [`agent/contributor-start.md`](agent/contributor-start.md) and Story Architect first. Then:

1. Prefer extending and categorizing existing entries over rewriting them.
2. Use [`CORE-PILLARS.md`](CORE-PILLARS.md) when deciding what new lore should serve.
3. Keep [`GUIDED-PATH.md`](GUIDED-PATH.md) steps 1–5 stable; add saga journeys via [`SAGAS.md`](SAGAS.md).
4. Create a Dias ID only when something must be independently referenceable outside normal Markdown lore.
5. When adding a place or inhabitant that should appear on the atlas Map tab, add an `x`/`y` pin (0–100) in [`dashboard/map-registry.yaml`](dashboard/map-registry.yaml) and regenerate with `python3 scripts/build_story_dashboard.py`. The build prints unresolved map refs so pixels can be double-checked.
