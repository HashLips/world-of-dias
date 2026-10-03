# Canon safety — World of Dias

Dias-specific guardrails for agents. Use with Story Architect’s `references/canon-rules.md` (status values, progressive enrichment, conflict framing).

## Protect existing canon

- Read before you write. Prefer **new files** or **additive enrichment** over rewriting established prose.
- Only fill empty / `unknown` / placeholder metadata unless the human explicitly asks to revise.
- Prefer additive updates to `related` and `themes`.
- On conflict: report it; keep the old record; frame the new idea as `rumor`, `myth`, `unknown`, or `contradicted`—do not silently overwrite.

## Soft limits (do not “solve” casually)

These stay open or constrained unless the human gives a deliberate plan:

| Topic | Rule of thumb |
| --- | --- |
| **Frequency Zero** | Clues and pressure only—do not close or explain it away |
| **Band ferries / subways** | Understanding a band ≠ a ticket there. Keep No-Ferry ethics; no safe ferry between bands |
| **Frederick Lumens–class crossings** | Do not invent easy passage solutions |
| **Distant Companies / Horizon-Nulls / Unraveled** | Do not promote to confirmed taxonomy without a plan |
| **Caliburn haunt signs** | Do not spam new slit variants; thicken carefully |
| **War as default weather** | Prefer wonder, manners, craft, mystery over turning Dias into a war setting |

See also [`stage-readiness.md`](stage-readiness.md) “Do not do next without deliberate plan.”

## Stable human paths

- Do **not** rewrite [`../GUIDED-PATH.md`](../GUIDED-PATH.md) steps 1–5.
- Keep [`../START-HERE.md`](../START-HERE.md) onboarding flow stable; grow lore in category folders.
- New saga journeys: add a reading path, then list in [`../SAGAS.md`](../SAGAS.md)—not the reverse.

## Quality over bulk

Stage leveling (categories ≥100) is **done**. Do not chase counts with stubs.

- Full template sections for the category (e.g. phenomena: Conditions + Cultural Interpretations; rules: who follows / breaks / what happens; symbols: Meaning / Usage / Lore Connection).
- Echo-aware / resonant tech framing—not Earth phones, app stores, or generic AI assistants as lore.
- Exact `name:` matching in `related:` lists so the dashboard graph stays clean.

## Protected external IDs

Files listed in [`dias-map.yaml`](dias-map.yaml) are externally referenced (`DIAS-{UUID}`).

- Never delete or reuse a Dias GUID.
- Never change a GUID’s meaning.
- Update the map in the same change if a mapped path moves.
- Prefer marking superseded canon over deleting mapped Markdown.

Spec: [`DIAS-REFERENCE-MAP.md`](DIAS-REFERENCE-MAP.md). Always-on rule: [`.cursor/rules/dias-reference-map.mdc`](../.cursor/rules/dias-reference-map.mdc).

## Secrets

Author-only staging: [`secrets-pointer.md`](secrets-pointer.md). Use for secret *pressure*, not spoiler bible dumps into public lore.

## When unsure

Ask one minimal, targeted question—or leave status as `unknown` / `rumor` and link existing hubs—rather than inventing a Forced-Final answer.
