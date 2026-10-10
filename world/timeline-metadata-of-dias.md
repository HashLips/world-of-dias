---
category: world
name: Timeline Metadata of Dias
related:
  - Historical Eras and Chronology of Dias
  - Known Eras and Markers
  - Annotated Timeline of Dias
  - F432 Civic Time
  - Time Causality and Change of Dias
  - History of Dias
  - Soft Limits of Dias
themes:
  - timeline
  - metadata
  - chronology
  - dashboard
status: canonical
time_era: present
time_span: ongoing
---

# Timeline Metadata of Dias

## Overview

**Timeline Metadata of Dias** defines the minimal frontmatter every lore entry uses so concepts can sit on a soft Dias timeline (readers + dashboard Timeline tab)—without Earth centuries or a pinned Fracture year.

## Core Premise

### Plain rule

Two fields only: **`time_era`** (where on the spine) and **`time_span`** (how it sits in time). Nuance lives in the body, not more metadata.

Do not invent numbered Fracture years. Soft chronology stays law ([Historical Eras and Chronology of Dias](historical-eras-and-chronology-of-dias.md)).

---

## `time_era` — spine order

Dashboard sort order (oldest → newest):

| Value | Name | Meaning |
| --- | --- | --- |
| `prime` | Prime Age | Unified reality before the Fracture |
| `fracture` | The Fracture | The break itself / immediate hinge |
| `settling` | Settling Present | Early Present Age: frequencies settle, bands take shape—after Fracture, before thick civic memory |
| `formative` | Formative Present | Institutions and roads crystallize: civic thickening, Long Gate era, ring expansion, Compacts/Keeps becoming “old” |
| `present` | Present (lived) | Current ordinary world—default for living places, peoples, flora, cultures, everyday tech |
| `near` | Near-present | Recent observational seasons (echo-rise, ledger-wave talk)—still Present Age, closer to “now” |
| `unknown` | Unknown | Cannot place honestly; prefer a soft lean to `present` or `settling` when possible |

### Why intermediates exist

Prime → Present alone hides everything that happened **after** the Fracture but **before** today’s Softfruit queue. `settling` and `formative` hold that middle without fake dates. `near` holds “just lately” without promoting saga clocks to law.

---

## `time_span` — shape

| Value | Meaning |
| --- | --- |
| `point` | One-shot event or founding moment |
| `ongoing` | Still true, living, practiced, or extant |
| `recurring` | Seasonal / cyclic (Flagweek, First Fruit, Bleed-Sky nights) |

---

## Placement rule (primary focus)

Pick the era that matches **what the entry is mainly about**, not every moment it ever touched.

| Entry focus | Typical pair |
| --- | --- |
| Living moss, market, culture pack, settlement | `present` + `ongoing` |
| Festival / Flagweek custom | `present` + `recurring` |
| Long Gate founding memory / early Compact | `formative` + `point` or `ongoing` |
| Band-settling after Fracture | `settling` + `point` / `ongoing` |
| The Fracture as event | `fracture` + `point` |
| Prime relic origin / Prime myth | `prime` + `point` (or `ongoing` if still circulating as practice) |
| Echo-rise season talk | `near` + `recurring` or `ongoing` |
| Mystery still open in life | `present` or `near` + `ongoing` |

Something that **began** in `formative` and **still runs** today: if the entry is the living practice → `present` + `ongoing`; if the entry is the founding → `formative` + `point`. Body prose may mention both.

---

## Required on every lore entry

```yaml
time_era: present
time_span: ongoing
```

Allowed values only from the tables above. No extra timeline keys in frontmatter unless schema is deliberately extended later.

## Global Lore

Agent ops: [`agent/timeline-metadata.md`](../agent/timeline-metadata.md). Story Architect: schema `time_era` / `time_span`. Annotated spine for readers: [Annotated Timeline of Dias](annotated-timeline-of-dias.md).

## Notes

The dashboard Timeline tab sorts by `time_era` order, then filters by `time_span` and category. Soft limits unchanged—no Fracture year stamp.
