# Contributor start — agents

**Read this before creating or editing lore in World of Dias.**

Human onboarding stays at repo-root [`START-HERE.md`](../START-HERE.md). This file is the agent entry for contribution.

## Non-negotiable: Story Architect

Before any lore create, classify, enrich, rename, or restructure:

1. **Read and follow** the Cursor skill **story-architect** (`SKILL.md` and its `references/`).
2. Use its schema, templates, naming (kebab-case), category guide, hierarchy, and canon rules.
3. Do **not** invent a parallel schema, folder layout, or “quick stub” format outside that skill.

If the skill is unavailable in the session, stop and tell the human—do not improvise lore files.

Companion Dias rules (this repo):

| File | Role |
| --- | --- |
| [`canon-safety.md`](canon-safety.md) | Soft limits, conflict framing, what not to solve |
| [`world-orientation.md`](world-orientation.md) | Hubs, primers, where to start reading before writing |
| [`stage-readiness.md`](stage-readiness.md) | What is safe to write next on stage |
| [`plan.md`](plan.md) | Active book-series canon plan (Volumes I–VI phases) |
| [`timeline-metadata.md`](timeline-metadata.md) | Required `time_era` / `time_span` for every lore entry (dashboard Timeline) |
| [`timeline-backfill-plan.md`](timeline-backfill-plan.md) | Active backfill of timeline fields across all existing entries |
| [`../AGENTS.md`](../AGENTS.md) | Thin root index for all agent materials |

## First-session reading order (short)

1. This file + [`canon-safety.md`](canon-safety.md)
2. Story Architect skill + `references/canon-rules.md` and `references/categories.md`
3. [`../CORE-PILLARS.md`](../CORE-PILLARS.md) — what new lore should serve
4. [`../GUIDED-PATH.md`](../GUIDED-PATH.md) steps 1–5 — **do not rewrite**
5. [`stage-readiness.md`](stage-readiness.md) — safe next / forbidden without a plan
6. [`world-orientation.md`](world-orientation.md) — pick the hub you will touch

Then open the specific entries you will relate to, and run a Story Architect canon check.

## Where lore lives

One concept → one Markdown file in the matching category folder:

`world/` · `regions/` · `rules/` · `cultures/` · `inhabitants/` · `flora/` · `artifacts/` · `phenomena/` · `myths/` · `stories/` · `symbols/` · `artworks/` · `assets/`

- `rules/` is **world lore** (laws, protocols)—not agent instructions.
- Do not invent a second lore store under `agent/` or elsewhere.
- Prefer extending and categorizing existing entries over rewriting them.

## Hand-authored lore only

**Do not use Python, shell loops, or code templates to create lore Markdown.** Author each entry with Write/edit tools under Story Architect judgment. Scripts are fine for search, inventory, git, and dashboard rebuild—not for bulk-writing `world/`, `rules/`, `phenomena/`, or other category lore. See [`plan.md`](plan.md) “Hand-authored lore only.”

## Definitional clarity

Canon must support book writing without guessing. Lead with **plain operational definitions** (what it is / does / isn’t). Lived Softfruit texture comes after. Do not use poetry as a substitute for physics. Soft limits and unknowns stay open only when labeled as such—not as beautiful fog. See [`plan.md`](plan.md) “Definitional clarity.”

## Contribution checklist

- [ ] Story Architect skill read and applied
- [ ] Category/classification decided from the skill’s guide
- [ ] Canon check against related entries; conflicts framed (`rumor` / `myth` / etc.), not silently overwritten
- [ ] Frontmatter + body match the category template
- [ ] Entry hand-authored (no Python/shell bulk generation of lore files)
- [ ] Plain definition present (not poetry-as-physics); claim grade clear where relevant
- [ ] `time_era` + `time_span` set ([`timeline-metadata.md`](timeline-metadata.md); canon: [`../world/timeline-metadata-of-dias.md`](../world/timeline-metadata-of-dias.md))
- [ ] `related:` names match other entries’ `name:` fields exactly (dashboard links by exact name)
- [ ] Soft limits respected ([`canon-safety.md`](canon-safety.md))
- [ ] If a place/inhabitant should appear on the Map tab: pin in [`../dashboard/map-registry.yaml`](../dashboard/map-registry.yaml), then `python3 scripts/build_story_dashboard.py`
- [ ] External / IRL references: [`DIAS-REFERENCE-MAP.md`](DIAS-REFERENCE-MAP.md) + [`dias-map.yaml`](dias-map.yaml)

## After substantive lore edits

Rebuild the story dashboard when you changed links, new entries, or map pins:

```bash
python3 scripts/build_story_dashboard.py
```

Aim for **unresolved refs: 0** unless the human accepts a listed gap.
