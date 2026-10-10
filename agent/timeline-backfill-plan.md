# Timeline Backfill Plan

Agent-only plan to place **every** lore entry on the soft Dias timeline via `time_era` + `time_span`.

**Vocabulary / rules:** [`timeline-metadata.md`](timeline-metadata.md) · canon hub [`../world/timeline-metadata-of-dias.md`](../world/timeline-metadata-of-dias.md)  
**Schema:** Story Architect `references/schema.md`  
**Prior track:** Book-series phases in [`plan.md`](plan.md) are complete (Volumes I–VI ready for book draft). This file is the **active execution plan** for timeline coverage.

---

## North star

After this plan, a reader or dashboard Timeline tab can ask “where does this sit?” for **any** lore file—without Earth years or a pinned Fracture date.

| Done when | Test |
| --- | --- |
| Coverage | Every lore Markdown under category folders has both fields |
| Honesty | Values match primary focus; `unknown` only when placement would be a lie |
| Soft limits | No invented century numbers; mysteries stay open |
| Navigable | Era distribution is inspectable; dashboard meta shows the fields |

---

## Universal rule: no skips

**Every entry gets `time_era` and `time_span`.** Including:

- world hubs and primers  
- regions, rules, cultures  
- inhabitants (peoples **and** animals)  
- flora, artifacts, phenomena  
- myths, stories, symbols, artworks  

Stories, rumors, teaching myths, and plates all have an origin or currency on the spine. If you truly cannot place it, use `unknown`—that is still a placement, not a skip.

There is **no** “timeless / N/A” opt-out.

---

## Fields (reminder)

```yaml
time_era: present     # prime | fracture | settling | formative | present | near | unknown
time_span: ongoing    # point | ongoing | recurring
```

**Primary focus:** tag what the entry is *about*, not every era it brushes.  
**Body prose** may still narrate older origins; metadata stays minimal.

---

## How agents must run this plan

### Story Architect + timeline docs

Before each phase: Story Architect schema (timeline fields), [`contributor-start.md`](contributor-start.md), [`timeline-metadata.md`](timeline-metadata.md), [`canon-safety.md`](canon-safety.md).

### One phase at a time

1. Inventory the phase folder: count files; count missing `time_era`.  
2. Judge each entry (or small batch) from title, overview, and known related hubs—do not blind-default everything to `present`/`ongoing`.  
3. Add or correct the two fields in frontmatter only (unless a body note is truly needed).  
4. Spot-check: sample prime/fracture/formative/near candidates were not flattened to `present`.  
5. Mark the phase `- [x]` only when **every** file in scope has both fields with allowed values.  
6. Stop for human review unless asked to continue.

### Judgment, not mass sameness

- Defaults in [`timeline-metadata.md`](timeline-metadata.md) are **starting guesses**, not automatic answers.  
- Prefer `present`/`ongoing` for living ordinary world when honest.  
- Prefer `formative`/`point` for founding events and early institutions.  
- Prefer `prime` for Prime Age cosmology / Prime-origin relics.  
- Prefer `fracture` only for the hinge itself (and immediate Fracture-as-event entries).  
- Prefer `settling` for early band-settling texture.  
- Prefer `near` for echo-rise / ledger-wave / clearly recent observational pressure.  
- Use `recurring` for festivals, seasons, cyclic phenomena.  
- Use `unknown` sparingly when competing frames make any shelf a lie.

### Understand-then-tag (non-negotiable)

Wrong time is worse than slow tagging. **You must understand the entry** (and enough related canon) before setting `time_era` / `time_span`.

- **Read** the file (at least Overview / core sections) before tagging. Glance at `related:` and linked hubs when placement is unclear.  
- **Do not** use Python, shell loops, regex dumps, or any script to *choose* or *write* timeline values. Lore judgment is not automatable here.  
- Scripts **are** allowed only for **non-authoring** ops: count missing fields, list invalid enums, coverage reports, dashboard rebuild, git.  
- After you understand an entry, add the two fields with normal edit tools (one file or a small hand-judged batch—never a content-blind stamp).  
- If you do not understand the entry, **stop and read more** (or use `unknown` only when honest uncertainty remains after reading)—do not guess `present`/`ongoing` to clear a checklist.

### Soft limits

Do not invent Fracture years. Do not use timeline tags to close Frequency Zero or promote rumor taxonomies.

---

## Inventory snapshot (start of plan)

Approximate lore Markdown counts (category folders only):

| Folder | ~Files | Phase |
| --- | --- | --- |
| `world/` | 171 | T.1 |
| `regions/` | 142 | T.2 |
| `rules/` | 124 | T.3 |
| `cultures/` | 166 | T.4 |
| `inhabitants/` | 386 | T.5–T.6 |
| `flora/` | 182 | T.7 |
| `artifacts/` | 371 | T.8–T.9 |
| `phenomena/` | 207 | T.10 |
| `myths/` | 117 | T.11 |
| `stories/` | 167 | T.12 |
| `symbols/` | 136 | T.13 |
| `artworks/` | 720 | T.14–T.16 |
| **Total** | **~2889** | — |

At plan start, almost none have `time_era` yet (hub exceptions only). Re-count each phase open.

---

## Phase map

| Phase | Scope | Goal |
| --- | --- | --- |
| **T.0** | Vocabulary lock | Confirm enum + no-skip rule (docs already seeded) |
| **T.1** | `world/` | All world hubs tagged |
| **T.2** | `regions/` | All places tagged |
| **T.3** | `rules/` | All rules tagged |
| **T.4** | `cultures/` | All cultures tagged |
| **T.5** | `inhabitants/` (peoples / named / anomalous persons) | Intelligent peoples & named figures |
| **T.6** | `inhabitants/` (animals / creatures / working beasts) | Non-person fauna & related |
| **T.7** | `flora/` | All flora tagged |
| **T.8** | `artifacts/` (A–M by filename) | First half of artifacts |
| **T.9** | `artifacts/` (N–Z by filename) | Second half of artifacts |
| **T.10** | `phenomena/` | All phenomena tagged |
| **T.11** | `myths/` | All myths tagged |
| **T.12** | `stories/` | All stories tagged |
| **T.13** | `symbols/` | All symbols tagged |
| **T.14** | `artworks/` (first third) | Plates / artworks batch 1 |
| **T.15** | `artworks/` (second third) | Batch 2 |
| **T.16** | `artworks/` (final third) | Batch 3 |
| **T.17** | Audit + dashboard | Coverage 100%; rebuild; report distribution |

**Total:** 18 phases (T.0–T.17).

---

### Phase T.0 — Vocabulary lock

- [x] Have we locked `time_era` / `time_span` enums, no-skip rule, and agent docs?

**Exit criteria:** [`timeline-metadata.md`](timeline-metadata.md) + [`../world/timeline-metadata-of-dias.md`](../world/timeline-metadata-of-dias.md) + Story Architect schema agree; this plan is the active track in [`stage-readiness.md`](stage-readiness.md).

**Closed:** Vocabulary + agent/schema docs in place; this plan linked from stage-readiness / AGENTS / contributor-start.

---

## Plan status

**Status:** **complete** — T.0–T.17 closed. Coverage **2889 / 2889** (0 missing, 0 invalid enums). Dashboard rebuilt.

---

### Phase T.1 — `world/`

- [x] Does every `world/*.md` have `time_era` + `time_span`?

**Pace:** Judge hubs carefully—many are `present`/`ongoing`; cosmology/Fracture/Prime hubs lean `prime` / `fracture` / `settling`; near-present mystery pressure may be `near`.

**Exit criteria:** 0 missing fields in `world/`.

**Closed:** All 171 `world/*.md` tagged (161 newly placed this phase). Coverage: present 167, prime 2, settling 1, fracture 1; spans ongoing 168, recurring 2, point 1.

---

### Phase T.2 — `regions/`

- [x] Does every `regions/*.md` have both fields?

**Diligence:** Living settlements → usually `present`/`ongoing`. Frequency-realm primers may still be `present`/`ongoing` (lived band) unless the entry is about settling after Fracture.

**Exit criteria:** 0 missing fields in `regions/`.

---

### Phase T.3 — `rules/`

- [x] Does every `rules/*.md` have both fields?

**Diligence:** Soft-limit / Fracture-adjacent rules: do not force `fracture` unless the rule *is* the hinge. Most civic rules → `present`/`ongoing`.

**Exit criteria:** 0 missing fields in `rules/`.

**Done:** 124/124 tagged. Era: present 123, near 1. Span: ongoing 110, recurring 14. No fracture/formative/prime in this folder (none were hinge- or Compact-founding sheets).

---

### Phase T.4 — `cultures/`

- [x] Does every `cultures/*.md` have both fields?

**Diligence:** Living practice → `present`/`ongoing`. Festival customs → often `present`/`recurring`. Founding/Compact origin sheets → often `formative`.

**Exit criteria:** 0 missing fields in `cultures/`.

---

### Phase T.5 — `inhabitants/` (peoples & named)

- [x] Are all people-kind, named persons, and anomalous-person entries tagged?

**Scope:** Major races, named civic/saga figures, person-class entries (`nature: person` / peoples). Exclude pure fauna when split is clear; if unsure, include here and skip in T.6.

**Exit criteria:** Every in-scope inhabitant file tagged; list any deferred to T.6.

**Closed:** Tagged with T.6 in one pass (all 386 `inhabitants/*.md`). Peoples/named: mostly `present`/`ongoing`; 11 legendary founding figures `formative`/`point`; Census Tally Vaun `prime`/`point`; Jorin Fell `present`/`point`.

---

### Phase T.6 — `inhabitants/` (animals & creatures)

- [x] Are all remaining inhabitant fauna/creature entries tagged?

**Diligence:** Living species → usually `present`/`ongoing`. Legendary-only beasts may be `formative`/`point` or `unknown` if myth-only.

**Exit criteria:** 0 missing fields across all `inhabitants/`.

**Closed:** 0 missing across `inhabitants/`. Fauna mostly `present`/`ongoing`; 23 cyclic/festival/window species `present`/`recurring`; 13 abyss/mystery placements `unknown`/`ongoing`.

---

### Phase T.7 — `flora/`

- [x] Does every `flora/*.md` have both fields?

**Diligence:** Extant plants → `present`/`ongoing`. Omen/seasonal flora may be `recurring` if the entry is about a cycle.

**Exit criteria:** 0 missing fields in `flora/`.

**Closed:** 0 missing across `flora/` (182). Living species mostly `present`/`ongoing` (167); 15 cycle/festival/omen blooms `present`/`recurring`; Echo-Rise Thistle `near`/`recurring`.

---

### Phase T.8 — `artifacts/` (filenames A–M)

- [x] Are artifacts with slug starting A–M tagged?

**Diligence:** Everyday tools → `present`/`ongoing`. Prime relics / Fracture-hinge objects → `prime` or `fracture` as primary focus. Documents about recent events → may be `near`.

**Exit criteria:** All A–M artifact files tagged.

**Closed:** 0 missing across A–M artifacts (181, incl. digit prefixes). 173 `present`/`ongoing`; 4 festival/weekly `present`/`recurring`; 2 singular-deed objects `present`/`point`; Exile Mask `formative`/`point`; Early F432 Survey Map `formative`/`ongoing`. No `prime`/`fracture`/`near` in this half (`prime-relics` is P → T.9).

---

### Phase T.9 — `artifacts/` (filenames N–Z)

- [x] Are remaining artifacts tagged?

**Exit criteria:** 0 missing fields in `artifacts/` N–Z (190/190). Full `artifacts/` folder **371/371**.

---

### Phase T.10 — `phenomena/`

- [x] Does every `phenomena/*.md` have both fields?

**Diligence:** Ongoing weather/conditions → `present`/`ongoing` or `recurring`. Fracture-linked phenomena: place by primary focus, not automatic `fracture`.

**Exit criteria:** 0 missing fields in `phenomena/`.

**Closed:** 0 missing across `phenomena/` (207). Left Bleed-Sky Weather `present`/`recurring` and Harmonic Echo-Rise `near`/`recurring`. Lived conditions mostly `present`/`ongoing` (153); cyclic weather/windows/omens `present`/`recurring` (54 total incl. prior); 5 `near` (Echo-Rise + Caliburn-aftermath quartet).

---

### Phase T.11 — `myths/`

- [x] Does every `myths/*.md` have both fields?

**Diligence:** Myth *about* Prime/Fracture → often `prime` / `fracture` / `formative` + `point`. Living teaching tale still told → may be `present`/`ongoing` if the entry is the practice of telling. Prefer the story’s setting age when the myth encodes a past event.

**Exit criteria:** 0 missing fields in `myths/`.

**Closed:** 117/117 tagged. Era: present 72, formative 35, fracture 5, settling 2, near 2, prime 1. Span: ongoing 65, point 44, recurring 8. Left The Long Gate Argument `formative`/`point`. Fracture quartet + Split Tide → `fracture`/`point`; Census Echoes → `prime`/`point`.

---

### Phase T.12 — `stories/`

- [x] Does every `stories/*.md` have both fields?

**Diligence:** Saga chapters and daily-life vignettes usually sit in `present` or `near` + `point` (or `ongoing` only if the entry is a standing practice, not a narrative beat). Origin rumors still have a shelf—often `present`/`point` or `formative`/`point`.

**Exit criteria:** 0 missing fields in `stories/`.

**Closed:** 167/167 tagged. Era: present 121, near 42, formative 4. Span: point 145, ongoing 19, recurring 3. Echo-rise / Caliburn / ledger-wave chapters → `near`; Softfruit teaching practices → `present`/`ongoing`.

---

### Phase T.13 — `symbols/`

- [x] Does every `symbols/*.md` have both fields?

**Diligence:** Living marks → `present`/`ongoing`. Founding of a mark → `formative`/`point` if that is the entry’s focus.

**Exit criteria:** 0 missing fields in `symbols/`.

**Closed:** 136/136 tagged. Era: present 134, formative 2. Span: ongoing 130, recurring 6 (Flagweek/festival + dawn thrum + market-wing weather). Compact seals still used (Second-Beginning Right Mark, Exile-Mutual Table Mark) → `formative`/`ongoing`. Carrow’s Mask / Red-Sail Crown / Caliburn Slit kept `present`/`ongoing` (living use primary).

---

### Phase T.14 — `artworks/` batch 1

- [x] First ~1/3 of `artworks/*.md` tagged (alphabetical)?

**Range:** `1-vel-mark.md` → `fruit-display.md` (240 files). Tagged 240; 0 remaining in this third.

**Diligence:** Tag by **depicted subject’s** primary era when clear; else `present`/`point` for a contemporary plate. Portrait of a living figure → usually `present`. Prime-Age depiction → `prime`.

**Exit criteria:** Batch 1 complete; record count.

---

### Phase T.15 — `artworks/` batch 2

- [x] Second ~1/3 tagged?

**Range:** `fruit-road-draft-ponies.md` → `pole-and-banana-pad.md` (indexes 240–479). Tagged 240.

**Exit criteria:** Batch 2 complete.

---

### Phase T.16 — `artworks/` batch 3

- [x] Remaining artworks tagged?

**Range:** `pole-and-banana-pad.md` → `yes-no-yes.md` (241 files, index 480–end). Tagged 241; 0 remaining in this third.

**Diligence:** Tag by depicted subject time. Living world default `present`/`ongoing`; Flagweek/seasonal/reveal-window/`recurring`; echo-rise subjects `near`/`recurring`. F120 near-return geometry stays `present` (band nature ≠ near shelf).

**Exit criteria:** Batch 3 complete; full `artworks/` at 720/720.

---

### Phase T.17 — Audit, dashboard, close-out

- [x] Is coverage 100% with only allowed enum values?

**Closed (2026-10-10):**

1. Missing `time_era` / `time_span`: **0**  
2. Invalid enum values: **0**  
3. Distribution — eras: present **2743**, near **57**, formative **56**, unknown **15**, prime **7**, fracture **6**, settling **5**; spans: ongoing **2473**, point **214**, recurring **202** (two Compact seals later corrected to formative/ongoing)  
4. Dashboard rebuilt: `python3 scripts/build_story_dashboard.py` (Timeline tab reads all tags)  
5. Spot-audit: random sample + full `prime`/`fracture`/`unknown` list reviewed for honesty (living-world bulk as `present` is expected)  
6. [`stage-readiness.md`](stage-readiness.md) updated — timeline backfill plan complete  

**Exit criteria:** Full coverage; dashboard rebuilt; short distribution summary for the human.

---

## After each phase

1. Count tagged vs remaining in scope.  
2. Note hard judgment calls (especially `unknown`, `fracture`, `prime`).  
3. Do not start the next phase unless the human asked to continue.  
4. Optional: commit only when the human asks (prefer non-spoilery messages).

---

**Note:** The dashboard Timeline tab now exists and grows as this backfill fills `time_era` / `time_span`. This plan still only assigns metadata—do not use scripts to guess times.
