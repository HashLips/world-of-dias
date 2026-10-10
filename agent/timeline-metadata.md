# Timeline metadata — agents

Companion to canon hub [`../world/timeline-metadata-of-dias.md`](../world/timeline-metadata-of-dias.md). Story Architect schema: `time_era`, `time_span`.

**Backfill execution plan (every existing entry):** [`timeline-backfill-plan.md`](timeline-backfill-plan.md).

## Always set on create (and when enriching)

Every lore Markdown entry in category folders must include:

```yaml
time_era: <value>
time_span: <value>
```

No exceptions for “timeless” concepts—use `present` + `ongoing` or `unknown` honestly. Detail stays in the body; do not add `time_start` / `time_end` / notes as frontmatter unless schema is extended on purpose.

## Allowed values

### `time_era` (spine, oldest → newest)

| Value | Use when the entry is mainly about… |
| --- | --- |
| `prime` | Prime Age (before Fracture) |
| `fracture` | The Fracture hinge itself |
| `settling` | Early Present: bands/frequencies settling after Fracture, before thick civic memory |
| `formative` | Formative Present: Long Gate era, civic thickening, ring expansion, Compacts/Keeps crystallizing |
| `present` | Lived Present Age (default for living world) |
| `near` | Near-present seasons (echo-rise / ledger-wave style “lately”) |
| `unknown` | Cannot place; prefer a soft lean when possible |

### `time_span`

| Value | Use when… |
| --- | --- |
| `point` | One event / founding / singular deed |
| `ongoing` | Still exists, practiced, or true |
| `recurring` | Cyclic / seasonal |

## Defaults (speed)

| Category feel | Default |
| --- | --- |
| Flora, animals, peoples, cultures, settlements, ordinary tech | `present` + `ongoing` |
| Festivals, Flagweeks, civic seasons | `present` + `recurring` |
| Founding myths / early institutions | `formative` + `point` (or `ongoing` if still the practice) |
| Fracture event entries | `fracture` + `point` |
| Prime Age cosmology / Prime origin relics | `prime` + `point` |
| Recent observational pressure | `near` + `ongoing` or `recurring` |

**Primary focus rule:** place by what the entry is *about*, not every era it brushes. Living fruit reverence → `present`/`ongoing` even if fruit roads are older; a Long Gate founding story → `formative`/`point`.

## Soft limits

- Do not invent numbered Fracture years or Earth-style centuries.
- Do not use timeline fields to “solve” Frequency Zero or close mysteries.
- Cross-band entries default to F432 civic spine unless the entry is explicitly another band’s age-feel (still use the same enum; explain band time-feel in body).

## Understand before you tag

Timeline values require **canon comprehension**. Read the entry (and related hubs when needed) before choosing `time_era` / `time_span`. Do **not** use Python or scripts to assign times—only to report coverage/gaps. Guessing `present`/`ongoing` without understanding is a failure.

## Dashboard

The story dashboard **Timeline** tab reads `time_era` / `time_span` and lays entries on a horizontal era spine (click → detail drawer). Keep `related:` name-exact. Rebuild after timeline tags or bulk backfills: `python3 scripts/build_story_dashboard.py`.

## Checklist add-on

When creating or substantially editing lore:

- [ ] `time_era` set to an allowed value  
- [ ] `time_span` set to an allowed value  
- [ ] Placement matches primary focus of the entry  
