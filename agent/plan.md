# Dias Book-Series Canon Plan

Agent-only plan to prepare World of Dias lore so **six companion volumes** can be written from canon without inventing missing world rules mid-book.

**Prior plan:** Stage-building Sections **1–35** are complete. This file replaces that expansion track as the active work plan.

**Location:** `agent/plan.md` — not a human reading path. Lore stays in category folders only.

---

## North star

Fill and deepen canon until each volume’s **definition of done** and **completion test** can pass. Phases ready ≠ first edition ready: after all volumes, the **Universal publication checklist** must still pass.

| Volume | Title | Done when |
| --- | --- | --- |
| I | The Laws of Dias | A reader understands how the universe operates and its fundamental limitations |
| II | The Atlas of Dias | A reader knows where important places exist and how they relate geographically |
| III | The Living World | A reader understands living systems and can identify representative species |
| IV | Peoples and Civilizations | A reader understands who inhabits Dias, how they live, and how societies function |
| V | Artifacts and Inventions | A reader understands the material world: tools, travel, trade, tech |
| VI | Echoes and Mysteries | A reader understands historical framework, remembered belief, and what remains unknown |

Tone to protect (from pillars and prior stage work): surface life, wonder, unease, conflict, and sparingly used unimaginable scale. **Core principle:** Everything resonates. Everything leaves an echo. See [`../CORE-PILLARS.md`](../CORE-PILLARS.md).

---

## How agents must run this plan

### Story Architect (required for every entry)

**Whenever you create or edit lore for any phase, use the Cursor Story Architect skill.** This is not optional and not “remembered from earlier.”

Before writing files in a phase:

1. Read Story Architect `SKILL.md`.
2. Read its `references/` as needed for the work: at minimum `schema.md`, `file-templates.md`, `categories.md`, `naming-conventions.md`, `canon-rules.md`, and `hierarchy.md`.
3. Classify each concept with the skill’s category guide.
4. Generate or enrich each file with the skill’s **full category template** (frontmatter + body sections)—never a parallel stub format.
5. Run the skill’s canon-check / progressive-enrichment behavior; frame conflicts (`rumor` / `myth` / `unknown` / `contradicted`), do not silently overwrite.

If Story Architect is unavailable in the session: **stop** and tell the human. Do not improvise lore files without it.

Also read Dias companions every phase: [`contributor-start.md`](contributor-start.md), [`canon-safety.md`](canon-safety.md), [`stage-readiness.md`](stage-readiness.md).

### One phase at a time

1. Read **this volume’s intro** and the **single phase** you are running.
2. **Load Story Architect** (`SKILL.md` + needed `references/`) plus the Dias companion docs above.
3. Canon-check existing hubs and related entries **before** creating files.
4. Answer the phase question with due diligence (see below). **Take your time.**
5. Mark the phase checkbox only when the question is **fully** answered and its **exit criteria** pass.
6. Stop. Summarize what was added/enriched. Do **not** silently start the next phase.

### Pace: leave no stone unturned (every phase)

We have all the time in the world. Speed is not a goal. Completeness is.

- **Fully answer the phase question** before stopping. Partial coverage is failure.
- **Leave no stone unturned** — inventory gaps, chase cross-links, cover ordinary life and edge cases the book will need, not only the obvious hub entry.
- **Volume of entries is fine** — if a phase needs **100, 500, or more** new or deeply enriched files to answer honestly, do that. Prefer many rich entries over one thin overview.
- **Every entry stays richly descriptive** — full Story Architect templates; no stubs, no two-liners, no three-sentence skim entries, no checklist prose pretending to be lore. If you enrich a file, add real texture (sensory detail, place, practice, consequence)—not a thin bolt-on paragraph.
- **Do not stop early** because the session is long, the count is high, or “enough examples” feel convenient. Stop only when a book chapter could be written from canon without inventing rules.
- Soft limits still apply: openness and mystery are not excuses to skip required texture elsewhere.

### Due diligence (required every phase)

Before declaring a phase done, the agent must:

1. **Inventory** — Search existing lore for the question’s domain. Listed folders are **starting points only**—follow links, indexes, saga paths, and further search across any category until the gap map is honest. List what already answers it and what gaps remain.
2. **Judge sufficiency** — Ask: could a full book chapter on this topic be written from current entries alone without inventing rules? If no, keep going. If yes only by hand-waving, keep going.
3. **Enrich first** — Prefer deepening existing entries over parallel stubs—then create whatever else is still missing.
4. **Create as many entries as needed** — Per phase, **100–500+ descriptive entries is acceptable** when the question demands it. Hundreds or thousands across the full plan is expected. Do not stop at one thin file, a short list of examples, or a hub page alone if the question still fails.
5. **Story Architect on every file** — Re-apply the skill’s schema, template, naming, and category rules for each create/enrich. Do not mass-generate lore that skips the template sections. **Hand-author each file** (see “Hand-authored lore only” below)—never Python/shell bulk-write of category Markdown.
6. **Quality bar** — No two-liner or three-sentence skim entries. Every new or substantially touched entry must use the full Story Architect template for its category and be **rich enough to illustrate or narrate from**: lived sensory detail, how it sits in place, who uses or fears it, and how it connects to resonance / frequency logic where relevant. Enrichment means deepening the entry, not tacking on three short lines. **Definition first:** a book author must be able to state the rule in plain words without guessing—see “Definitional clarity” below.
7. **Classify correctly** — Put each concept in the right folder per Story Architect (`world/`, `regions/`, `rules/`, `cultures/`, `inhabitants/`, `flora/`, `artifacts/`, `phenomena/`, `myths/`, `stories/`, `symbols/`, `artworks/`).
8. **Lore voice (not book editorial)** — Category lore is the world source. Do **not** write Notes/Overview that address “Volume I,” “for the book,” “Phase I.x,” “publication checklist,” or other agent/plan scaffolding. Keep volume/phase language in `agent/plan.md` only. Prefer explaining relationships **inside the real entry** via `related:` / `parent_region` and body prose—not parallel meta files (e.g. do not create “Nest Path: …” twins for every place).
9. **Link cleanly** — Exact `name:` matching in `related:`; rebuild dashboard when links/map pins change; aim for unresolved refs 0.
10. **Protect soft limits** — Do not solve Frequency Zero, invent band ferries, promote Distant Companies / Horizon-Nulls / Unraveled to confirmed taxonomy, or rewrite `GUIDED-PATH.md` steps 1–5. Frame unknowns as `unknown` / `rumor` / `myth` when appropriate.
11. **Volume completion test** — After the last phase in a volume, run that volume’s completion test in the summary.

### Hand-authored lore only (non-negotiable)

**Do not use Python, shell loops, templates-as-code, or any script to create or bulk-write lore Markdown entries.**

- The agent must **author each entry itself** (Write / edit tools), with Story Architect judgment on classification, canon check, naming, `related:` exactness, and lived texture.
- Scripts are allowed only for **non-authoring** ops: search/inventory (`rg`, `find`), dashboard rebuild (`scripts/build_story_dashboard.py`), git, and similar read/verify tooling.
- Mass-generating dozens of near-identical files from a Python string template produces thin, low-attention lore. That is a phase failure even if the count looks high.
- If a phase needs many files, write them **one by one** (or in small careful batches), each with its own sensory detail, place, and consequence—not a shared skeleton with swapped band names.

### Definitional clarity (non-negotiable)

Canon is the source a book will be written from. **Definitions must be plain and usable—not poetry standing in for physics.**

- Every major term (frequency, resonance, echo, realm, region, local phenomenon, matter/life/memory/perception/environment effects, claim grades, soft limits, etc.) needs a **clear operational meaning**: what it is, what it does, what it is not, and what happens when someone treats it wrong.
- Lived texture and Softfruit voice are welcome **after** the definition is locked. Atmosphere must not replace the definition.
- A book author must not have to guess whether a phrase is metaphor, law, observation, or taboo. Use claim grades and “plain job” wording so sorting is obvious.
- Soft limits and genuine unknowns stay open **on purpose**—but they must be labeled as unknown/taboo/soft-limit, not wrapped in beautiful ambiguity that looks like a hidden answer.
- When enriching older entries that lean poetic, add or tighten a plain definition first; keep wonder in examples, not in the meaning of the word.

### Entry quality bar (non-negotiable)

Reject / rewrite work that is:

- written without Story Architect schema/template
- a title plus one sentence, or a thin three-sentence skim
- enrichment that only adds a short bolt-on note instead of real body depth
- a bullet list with no lived texture
- Earth-tech pasted in (phones, apps, generic AI) without Dias framing
- a duplicate of an existing entry under a new name
- a parallel meta twin of an existing concept (relationship belongs in `related:` / body of the real entry)
- **script-/template-bulk-generated** lore (Python/shell loops filling Markdown from string templates)
- **poetry-as-definition** — evocative prose with no clear “what it is / does / isn’t,” leaving a book author to guess

Accept work that:

- follows Story Architect classification, naming, frontmatter, and full template sections
- was **hand-authored** with attention to that concept’s particular place and manners
- leads with a **plain, book-usable definition**, then adds lived texture
- reads as a **decent, rich** lore record—enough prose that a stranger could picture and use it
- a reader can **picture**, **place**, and **connect** to at least one other domain
- leaves mystery where canon soft-limits require it, without fake final answers or undefined fog

### Folder starting points (not limits)

Each phase lists **starting points**—places to open first. They are **not** a closed allow-list.

- Search further wherever the question leads (`related:` webs, hubs, indexes, map registry, artworks, myths, etc.).
- Create or enrich entries in **any** correct category if that is where the answer belongs.
- Classify by Story Architect rules; do not force a concept into a starting folder just because it was listed.

| Domain | Start here |
| --- | --- |
| Cosmology, time, history indexes, mysteries | `world/`, `rules/` |
| Realms, regions, settlements, landforms, routes | `regions/` (+ `world/` indexes, `dashboard/map-registry.yaml`) |
| Climate, weather-as-phenomena | `phenomena/`, `regions/` |
| Plants & growth | `flora/` (index: `world/flora-of-dias.md`) |
| Animals, creatures, peoples, named persons | `inhabitants/` |
| Cultures, language, religion, daily life, orgs, economy | `cultures/` |
| Laws, protocols, absolute vs theory framing | `rules/` |
| Objects, tech, vehicles, relics, records | `artifacts/` |
| Folklore, entertainment stories | `myths/`, `stories/` |
| Emblems, signs, belief marks | `symbols/` |
| Visual plates / field-guide art | `artworks/` + `assets/` |

### Status tracking

- Phase checkbox `- [ ]` → `- [x]` only when exit criteria pass.
- Volume status: **pending** → **in progress** → **ready for book draft**.
- Do not mark a volume ready until its **completion test** can be answered honestly.

---

## Phase map (high level)

| Volume | Phases | Goal |
| --- | --- | --- |
| **I — Laws** | I.1–I.11 | Cosmology, resonance, frequencies, limits, unknowns |
| **II — Atlas** | II.1–II.10 | Hierarchy, F432 geography, climates, routes, maps |
| **III — Living World** | III.1–III.10 | Ecosystems, flora, fauna, frequency-biology |
| **IV — Peoples** | IV.1–IV.10 | Peoples, cultures, daily life, governance, belief |
| **V — Artifacts** | V.1–V.10 | Materials, tech, transport, trade, relics |
| **VI — Echoes** | VI.1–VI.10 | Eras, Fracture consequences, figures, mysteries, timeline |

**Total:** 61 phases. Run in order within a volume; volumes may be scheduled by human priority, but do not skip soft-limit phases casually.

---

# Volume I: The Laws of Dias

**Theme:** Foundations, cosmology, frequencies, and the nature of reality.

**Definition of done:** A reader understands how the universe operates and what its fundamental limitations are.

**Completion test:** Give the finished material to someone unfamiliar with Dias. Can they explain its fundamental laws and identify why an event would or would not be possible?

**Volume status:** ready for book draft

---

### Phase I.1 — What Dias is; how realms, regions, and local phenomena fit

- [x] Can we explain exactly what Dias is and how frequency realms, regions, and local phenomena fit together?

**Starting points** (search further as needed): `world/`, `rules/`, `regions/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Inventory cosmology hubs and realm primers. Ensure a clear hierarchy (Dias → frequency realm → region → local phenomenon) exists in linked entries, not only in root docs. Enrich or create orientation entries until the stack is teachable without saga spoilers.

**Exit criteria:** A new reader can state what Dias is and correctly nest realm / region / local phenomenon with examples.

---

### Phase I.2 — Resonance and echo

- [x] Can we explain what resonance is and why everything leaves an echo?

**Starting points** (search further as needed): `rules/`, `world/`, `phenomena/`, `symbols/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Make resonance and echo concrete (effects, metaphors inhabitants use, observable traces). Avoid turning “echo” into unlimited magic.

**Exit criteria:** Plain-speech explanation of resonance + echo exists in canon entries, with at least two lived examples.

---

### Phase I.3 — Absolute laws vs theories vs observations

- [x] Do we know which principles are absolute laws versus theories or observations?

**Starting points** (search further as needed): `rules/`, `world/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Tag or structure entries so law / theory / observation / taboo-guess are distinguishable. Do not collapse scholarly dispute into false certainty.

**Exit criteria:** A reader can sort major principles into law vs theory vs observation using canon wording.

---

### Phase I.4 — Established frequency realms

- [x] Can we describe every established frequency realm and what makes it fundamentally different?

**Starting points** (search further as needed): `regions/` (realm entries), `world/`, `artworks/` (map plates if needed)

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Cover each established band (including F432 home and established neighbors). Difference must be fundamental (matter, mood, physics-of-meaning), not only aesthetic.

**Exit criteria:** Each established realm has a descriptive entry (or enriched hub) stating what makes it unlike the others.

---

### Phase I.5 — Frequency effects on matter, life, memory, perception, environments

- [x] Do we understand how frequencies affect matter, life, memory, perception, and environments?

**Starting points** (search further as needed): `rules/`, `phenomena/`, `world/`, `inhabitants/`, `flora/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** For each affected domain, ensure concrete examples across more than one band where established. Prefer enrichment of existing phenomena over generic “magic differs.”

**Exit criteria:** Canon supports explaining frequency influence on all five domains with examples.

---

### Phase I.6 — What resonance can and cannot do

- [x] Do we know what resonance can and cannot do, including its consequences and limitations?

**Starting points** (search further as needed): `rules/`, `artifacts/`, `phenomena/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Document capabilities, costs, failures, and social consequences. Soft-limit: no casual Zero solve; no band-ferry tickets.

**Exit criteria:** A reader can say why a proposed resonant feat would succeed, fail, or be forbidden/taboo.

---

### Phase I.7 — Inter-frequency interaction and exceptional travel

- [x] Do we understand inter-frequency interaction, communication, and why travel between realms is exceptional?

**Starting points** (search further as needed): `rules/`, `world/`, `phenomena/`, `cultures/`, `artifacts/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Cover bleed, residual measurement, communication limits, No-Ferry ethics, and exceptional crossings as rare/dangerous—not infrastructure.

**Exit criteria:** Canon explains interaction + communication + why ordinary travel between realms is exceptional.

---

### Phase I.8 — Prime Realm, Prime Age, Fracture (without inventing missing answers)

- [x] Can we explain what is known about the Prime Realm, Prime Age, and Fracture without inventing missing answers?

**Starting points** (search further as needed): `world/`, `rules/`, `myths/`, `artifacts/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Separate documented, disputed, and unknown. Enrich evidence and remembered accounts; do not fabricate a complete Prime atlas.

**Exit criteria:** A reader can summarize what is known vs unknown about Prime / Prime Age / Fracture without false closure.

---

### Phase I.9 — Time, causality, and change

- [x] Do we understand how time, causality, and change work wherever these are established?

**Starting points** (search further as needed): `rules/`, `world/`, `phenomena/`, `regions/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Document only where established (including band-specific weirdness). Mark gaps explicitly rather than globalizing F432 assumptions.

**Exit criteria:** Established time/causality rules are stated; unknowns are labeled as such.

---

### Phase I.10 — Unknowns, especially Frequency Zero

- [x] Have we clearly identified what remains unknown, particularly around Frequency Zero?

**Starting points** (search further as needed): `world/`, `rules/`, `myths/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Create or enrich “known unknowns” orientation. Clues and pressure only—**do not solve Zero**.

**Exit criteria:** A clear canon list of major unknowns exists; Zero remains open.

---

### Phase I.11 — Diagrams, timelines, frequency comparisons

- [x] Can we represent the universe's structure with diagrams, timelines, and frequency comparisons?

**Starting points** (search further as needed): `world/`, `artworks/`, `assets/`, `symbols/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Add comparison plates, structural diagrams, or timeline anchors as lore/art entries as needed. Keep them consistent with realm primers and soft limits.

**Exit criteria:** At least one teachable structural comparison and one timeline/frequency comparison artifact exist in-repo for book use.

---

# Volume II: The Atlas of Dias

**Theme:** Realms, regions, cities, geography, climates, and landmarks.

**Definition of done:** A reader knows where important places exist and how they relate geographically.

**Completion test:** Can someone plan a believable journey across F432, locate major destinations, and understand the environments they would encounter?

**Volume status:** pending

---

### Phase II.1 — Geographical hierarchy

- [ ] Do we have a clear geographical hierarchy of realms, regions, settlements, and landmarks?

**Starting points** (search further as needed): `world/`, `regions/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Ensure parent/child relationships and place_type usage are consistent and readable as a hierarchy.

**Exit criteria:** Hierarchy can be explained with examples from F432 and at least one other established realm where applicable.

---

### Phase II.2 — F432 regions: Nauw, Wabet, Sorel

- [ ] Can we accurately locate and distinguish the established regions of F432, including Nauw, Wabet, and Sorel?

**Starting points** (search further as needed): `regions/`, `dashboard/map-registry.yaml`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Deepen regional distinctiveness (terrain, culture touch, travel feel). Align map pins/polygons with established map art where relevant.

**Exit criteria:** Nauw, Wabet, and Sorel are clearly distinguishable in prose and map placement.

---

### Phase II.3 — Major cities (e.g. Veloria)

- [ ] Are major cities such as Veloria sufficiently described, including their layout and surroundings?

**Starting points** (search further as needed): `regions/`, `cultures/`, `inhabitants/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Layout, districts/quarters, approaches, surroundings—not a single skyline sentence. Add subordinate place entries as needed.

**Exit criteria:** Veloria (and other major named cities in scope) support a walkable mental map.

---

### Phase II.4 — Landforms

- [ ] Have we established important mountains, rivers, seas, islands, forests, deserts, and other landforms?

**Starting points** (search further as needed): `regions/`, `phenomena/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Seed or deepen named landforms across Wabet / Nauw / Sorel and other established geographies. Quantity is fine if each entry is descriptive.

**Exit criteria:** Each major F432 region has multiple concrete landforms a journey can route through.

---

### Phase II.5 — Climate, seasons, environmental phenomena

- [ ] Do we understand the climate, seasons, and characteristic environmental phenomena in each major region?

**Starting points** (search further as needed): `phenomena/`, `regions/`, `world/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Climate must feel regional and frequency-aware where relevant (e.g. F380 weather-as-mood is not F432 weather).

**Exit criteria:** Major regions have characteristic climate/season/phenomena coverage sufficient for travel writing.

---

### Phase II.6 — Roads, bridges, ferries, trade routes, travel constraints

- [ ] Are important roads, bridges, ferries, trade routes, and physical travel constraints documented?

**Starting points** (search further as needed): `regions/`, `artifacts/`, `cultures/`, `rules/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Document mundane travel richly. Keep **band ferry** soft limits: local ferries ≠ inter-frequency tickets.

**Exit criteria:** A journey planner can name routes and constraints between major F432 destinations.

---

### Phase II.7 — Safe, dangerous, sacred, restricted, unexplored

- [ ] Do we know which places are safe, dangerous, sacred, restricted, or unexplored?

**Starting points** (search further as needed): `regions/`, `cultures/`, `rules/`, `myths/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Status should be inhabitant-facing where possible (who says it’s sacred?). Avoid turning the atlas into a combat zone list.

**Exit criteria:** Representative places exist in each safety/sacred/restricted/unexplored class with reasons.

---

### Phase II.8 — Objective geography vs unreliable maps

- [ ] Can we distinguish objective geography from incomplete or unreliable maps created by inhabitants?

**Starting points** (search further as needed): `artifacts/`, `artworks/`, `world/`, `cultures/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Map lineage, survey error, political maps, sailor charts—canonize the difference without erasing wonder.

**Exit criteria:** Canon explicitly teaches that some maps are wrong, partial, or motivated—and why.

---

### Phase II.9 — Locations linked to people, civilizations, artifacts, history

- [ ] Have we linked important locations to their inhabitants, civilizations, artifacts, and historical significance?

**Starting points** (search further as needed): `regions/` + cross-links to `inhabitants/`, `cultures/`, `artifacts/`, `world/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Enrich `related:` webs; add missing bridge entries where a famous place lacks people/history hooks.

**Exit criteria:** Major locations point to people, culture, at least one artifact or historical beat where appropriate.

---

### Phase II.10 — Consistent maps (realm, regional, settlement)

- [ ] Can we produce consistent maps at realm, regional, and settlement levels?

**Starting points** (search further as needed): `artworks/`, `assets/`, `dashboard/map-registry.yaml`, `regions/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Align dashboard shapes/pins with V2 map art and prose. Add settlement-level sketch plates or registry detail as needed for book atlas work.

**Exit criteria:** Realm + regional consistency verified; at least one settlement-level map depth exists for a major city (e.g. Veloria).

---

# Volume III: The Living World

**Theme:** Flora, fauna, creatures, biology, habitats, and ecology.

**Definition of done:** A reader understands the living systems of Dias and can identify its representative species.

**Completion test:** Can a reader open the book, recognize a creature or plant, understand where it lives, and learn what makes it special?

**Volume status:** pending

---

### Phase III.1 — Ordinary animals, extraordinary creatures, peoples, ambiguous life

- [ ] Have we distinguished ordinary animals, extraordinary creatures, peoples, and ambiguous forms of life?

**Starting points** (search further as needed): `inhabitants/`, `world/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Clear classification language in entries (`nature` / status / framing). Do not blur peoples into monsters casually.

**Exit criteria:** Taxonomy of life-kinds is teachable from canon examples.

---

### Phase III.2 — Major ecosystems and habitats

- [ ] Have we established the major ecosystems and habitats across known regions and frequencies?

**Starting points** (search further as needed): `regions/`, `flora/`, `inhabitants/`, `phenomena/`, `world/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Habitats should be placeable on the atlas and frequency-aware where established.

**Exit criteria:** Multiple ecosystems per major F432 region (and key other-band habitats where known) exist as descriptive entries or deeply enriched region sections plus linked species.

---

### Phase III.3 — Plants, trees, flowers, fungi, growth

- [ ] Can we describe the major plants, trees, flowers, fungi, and other forms of growth in the world?

**Starting points** (search further as needed): `flora/`, `world/flora-of-dias.md`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Expand flora with full descriptive entries (appearance, place, growth habit). Indexes alone are not enough.

**Exit criteria:** Field-guide-ready plant entries cover major biomes in scope.

---

### Phase III.4 — Edible, medicinal, dangerous, commercial, cultural plants

- [ ] Do we understand which plants are edible, medicinal, dangerous, commercially important, or culturally significant?

**Starting points** (search further as needed): `flora/`, `cultures/`, `artifacts/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Tag uses in body prose and links to foodways / trade / ritual. Include warnings and taboos.

**Exit criteria:** Examples exist in each use-class; readers can cook, heal, trade, or avoid with canon support.

---

### Phase III.5 — Wildlife, domesticates, working animals, dangerous species

- [ ] Have we identified common wildlife, domesticated animals, working animals, and dangerous species?

**Starting points** (search further as needed): `inhabitants/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Balance wonder-creatures with ordinary animals that make settlements feel alive.

**Exit criteria:** Each class has multiple descriptive species entries tied to places.

---

### Phase III.6 — Feeding, reproduction, migration, ecological interaction

- [ ] Do we understand how major species feed, reproduce, migrate, and interact within their environments where known?

**Starting points** (search further as needed): `inhabitants/`, `flora/`, `regions/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Add life-cycle and ecology detail where known; label unknowns. No Earth-wiki dumps that ignore frequency.

**Exit criteria:** Major representative species have ecology sections sufficient for natural-history prose.

---

### Phase III.7 — Frequency influence on biology

- [ ] Have we established how different frequencies influence biology and lifeforms?

**Starting points** (search further as needed): `rules/`, `inhabitants/`, `flora/`, `phenomena/`, `world/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Cross-band examples where established; do not invent full biospheres for bands that should stay thin.

**Exit criteria:** Canon explains biological difference by frequency with concrete species/habitat examples.

---

### Phase III.8 — Appearance, size, behavior, identifying traits

- [ ] Do important creatures have recognizable appearances, sizes, behaviors, and identifying characteristics?

**Starting points** (search further as needed): `inhabitants/`, `artworks/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Descriptive morphology and behavior in prose; commission/add artwork plates where helpful.

**Exit criteria:** Important creatures are identifiable from text alone; key ones have or link visual plates.

---

### Phase III.9 — Confirmed species vs rumor/legend creatures

- [ ] Have we distinguished confirmed species from creatures existing only in rumor or legend?

**Starting points** (search further as needed): `inhabitants/`, `myths/`, `stories/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Use canon status framing (`canon` / `rumor` / `myth` / `unknown`). Keep legendary beings useful without fake zoology.

**Exit criteria:** Readers can tell field-guide fact from campfire creature.

---

### Phase III.10 — Illustrated field-guide capability

- [ ] Can we create illustrated field-guide entries showing anatomy, habitat, scale, and distinguishing features?

**Starting points** (search further as needed): `artworks/`, `assets/`, `flora/`, `inhabitants/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Ensure a repeatable entry+plate pattern exists for book production (even if not every species is illustrated yet).

**Exit criteria:** A field-guide pattern is demonstrated on multiple plants and creatures (text + art or clear art brief in artwork entries).

---

# Volume IV: Peoples and Civilizations

**Theme:** Inhabitants, characters, cultures, governments, and everyday life.

**Definition of done:** A reader understands who inhabits Dias, how they live, and how their societies function.

**Completion test:** Can a reader imagine what it would be like to live in Veloria, or another established settlement, and describe a normal day there?

**Volume status:** pending

---

### Phase IV.1 — Major intelligent peoples

- [ ] Have we identified the major intelligent peoples and established their physical characteristics and abilities?

**Starting points** (search further as needed): `inhabitants/`, `world/`, `cultures/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Physical description + abilities with limits. Keep race/people framing canon-safe (no Earth race-tag shortcuts).

**Exit criteria:** Major peoples are descriptively distinct and placeable.

---

### Phase IV.2 — Where peoples live and how they interact

- [ ] Do we know where these peoples predominantly live and how they interact?

**Starting points** (search further as needed): `inhabitants/`, `regions/`, `cultures/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Homelands, diasporas, contact zones, manners of meeting—not only “also found in.”

**Exit criteria:** Interaction patterns between major peoples are documented with place anchors.

---

### Phase IV.3 — Cultures, customs, celebrations, traditions, expectations

- [ ] Have we established major cultures, customs, celebrations, traditions, and social expectations?

**Starting points** (search further as needed): `cultures/`, `myths/`, `symbols/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Full cultural entries; festivals and etiquette should be enactable in a scene.

**Exit criteria:** Multiple cultures have customs/celebrations/expectations rich enough for daily-life chapters.

---

### Phase IV.4 — Languages, naming, etiquette

- [ ] Do we understand how people communicate, including languages, naming conventions, and etiquette?

**Starting points** (search further as needed): `cultures/`, `symbols/`, `artifacts/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Naming patterns, greetings, insults, register—resonance-aware where relevant.

**Exit criteria:** A writer can name a character correctly and stage a polite vs rude exchange from canon.

---

### Phase IV.5 — Ordinary life (family, education, professions, food, entertainment)

- [ ] Can we explain how ordinary life works, including family, education, professions, food, and entertainment?

**Starting points** (search further as needed): `cultures/`, `flora/`, `artifacts/`, `stories/`, `myths/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** This phase may require many entries. Prioritize Veloria / major F432 settlements first, then widen.

**Exit criteria:** A “normal day” in at least one major settlement can be narrated hour-by-hour from canon.

---

### Phase IV.6 — Governments, authorities, organizations, factions

- [ ] Have we described the governments, authorities, organizations, and factions that influence societies?

**Starting points** (search further as needed): `cultures/`, `regions/`, `rules/`, `inhabitants/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Power should have offices, habits, and limits—not only villain labels. Prefer civic texture over wardefault.

**Exit criteria:** Major settlements/regions have identifiable authorities and competing influences.

---

### Phase IV.7 — Laws, trade, economies, political relationships

- [ ] Do we understand how laws, trade, economies, and political relationships differ between regions?

**Starting points** (search further as needed): `rules/`, `cultures/`, `artifacts/`, `regions/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Regional difference must be concrete (tolls, currencies, banned goods, obligations).

**Exit criteria:** A reader can contrast at least two regions’ law/trade/politics with examples.

---

### Phase IV.8 — Religions, beliefs, rituals, cultural readings of resonance

- [ ] Have we identified the major religions, beliefs, rituals, and cultural interpretations of resonance?

**Starting points** (search further as needed): `cultures/`, `symbols/`, `myths/`, `rules/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Multiple interpretations encouraged; do not collapse into one church of Zero.

**Exit criteria:** Belief systems and rituals are enactable; resonance interpretations differ by culture.

---

### Phase IV.9 — Named inhabitant reference profiles

- [ ] Do important named inhabitants have consistent reference profiles covering identity, origin, role, and relationships?

**Starting points** (search further as needed): `inhabitants/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Audit saga-facing and civic figures; enrich identity/origin/role/relationships; fix contradictions via canon-safe framing.

**Exit criteria:** Important named figures have consistent profiles usable as encyclopedia entries.

---

### Phase IV.10 — Visual culture (peoples, clothing, symbols, architecture, relationships)

- [ ] Can we illustrate recognizable peoples, clothing, cultural symbols, architecture, and relationship diagrams?

**Starting points** (search further as needed): `artworks/`, `assets/`, `cultures/`, `symbols/`, `world/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Ensure architecture/clothing/symbol entries + plates support illustration briefs.

**Exit criteria:** Book illustrators could brief peoples, dress, symbols, and architecture from canon without guessing.

---

# Volume V: Artifacts and Inventions

**Theme:** Objects, technologies, vehicles, materials, transport, and trade.

**Definition of done:** A reader understands how the material world functions and what inhabitants use to live, build, communicate, and travel.

**Completion test:** Can a reader equip an adventurer, choose a believable way to travel, and understand what everyday technologies are available without inventing new rules?

**Volume status:** pending

---

### Phase V.1 — Classification of objects and artifacts

- [ ] Have we classified common objects, tools, technologies, resonant devices, and rare artifacts?

**Starting points** (search further as needed): `artifacts/`, `world/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Clear artifact_type / rarity / role language across entries. Separate kitchen tool from relic.

**Exit criteria:** Classification is usable as a book taxonomy with examples in each class.

---

### Phase V.2 — Materials, energy, manufacturing

- [ ] Do we know what materials, energy sources, and manufacturing methods are used?

**Starting points** (search further as needed): `artifacts/`, `cultures/`, `regions/`, `flora/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Workshops, mills, resonant craft, mundane industry—descriptive and place-linked.

**Exit criteria:** A maker’s chapter can be written for at least two regional craft traditions.

---

### Phase V.3 — Resonant technology: capabilities, limits, failures

- [ ] Are the capabilities, limitations, and possible failures of resonant technology established?

**Starting points** (search further as needed): `artifacts/`, `rules/`, `phenomena/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Failure modes and social consequences matter as much as powers. Soft limits apply.

**Exit criteria:** Readers know what resonant devices can/can’t do and how they break or mislead.

---

### Phase V.4 — Domestic objects, tools, agriculture, clothing, instruments

- [ ] Have we described common domestic objects, tools, agricultural equipment, clothing, and instruments?

**Starting points** (search further as needed): `artifacts/`, `cultures/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** High volume expected. Each entry still fully descriptive—no stub catalogs.

**Exit criteria:** Household / farm / clothing / instrument coverage supports everyday scenes without invention.

---

### Phase V.5 — Vehicles and transportation systems

- [ ] Do we know which vehicles and transportation systems exist and how they operate?

**Starting points** (search further as needed): `artifacts/`, `regions/`, `cultures/`, `rules/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Carts, boats, bridges, local ferries, mounts, schedule culture—plus constraints. No inter-band subway.

**Exit criteria:** Multiple transport modes documented with operation and limits.

---

### Phase V.6 — Recording, delivering, preserving, communicating information

- [ ] Can we explain how information is recorded, delivered, preserved, and communicated?

**Starting points** (search further as needed): `artifacts/`, `cultures/`, `symbols/`, `rules/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Ledgers, songs, seals, runners, resonant records—echo-aware, not Earth internet.

**Exit criteria:** Message and archive methods are clear enough for plot logistics.

---

### Phase V.7 — Trade, currency, markets, manufacturing, distribution

- [ ] Have we established how trade, currency, markets, manufacturing, and the distribution of goods work?

**Starting points** (search further as needed): `cultures/`, `artifacts/`, `regions/`, `rules/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Markets should smell and sound like places; currency and credit must be regional where established.

**Exit criteria:** A merchant plot can price, move, and sell goods using canon systems.

---

### Phase V.8 — Major relics and artifacts

- [ ] Have we documented the major relics and artifacts, including their known origins and capabilities?

**Starting points** (search further as needed): `artifacts/`, `myths/`, `world/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Origins may be disputed—say so. Capabilities must not break Volume I limits.

**Exit criteria:** Major relics have descriptive dossier-quality entries (known / disputed / unknown sorted).

---

### Phase V.9 — Dangerous, restricted, rare, expensive, taboo inventions

- [ ] Do we understand which inventions are dangerous, restricted, rare, expensive, or socially taboo?

**Starting points** (search further as needed): `artifacts/`, `rules/`, `cultures/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Social enforcement matters (who bans, who sells anyway).

**Exit criteria:** Examples exist in each risk/rarity/taboo class with in-world reasons.

---

### Phase V.10 — Consistent illustration of artifacts and machines

- [ ] Can we illustrate important artifacts and machines with sufficiently consistent shapes, materials, dimensions, and details?

**Starting points** (search further as needed): `artworks/`, `assets/`, `artifacts/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Prose must specify shape/material/scale; add plates for flagship objects.

**Exit criteria:** Important artifacts can be drawn consistently from canon text + existing art.

---

# Volume VI: Echoes and Mysteries

**Theme:** Recorded history, important events, beliefs, symbols, and unresolved mysteries.

**Definition of done:** A reader understands the historical framework of Dias, what different societies remember, and what remains unknown.

**Completion test:** Can a reader explain the broad history of Dias, recognize its most important events, and distinguish what is known from what is believed?

**Volume status:** pending

---

### Phase VI.1 — Major historical eras and chronology

- [ ] Have we established the major historical eras and their chronological relationships?

**Starting points** (search further as needed): `world/`, `rules/`, `cultures/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Era names and order must be stable and cross-linked. Avoid fake precise calendars where canon is soft.

**Exit criteria:** A broad era sequence is teachable from canon hubs.

---

### Phase VI.2 — Documented vs disputed vs myth vs unknown

- [ ] Can we distinguish documented historical events from disputed accounts, myths, and unknown events?

**Starting points** (search further as needed): `world/`, `myths/`, `stories/`, `artifacts/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Status discipline across history-facing entries.

**Exit criteria:** Readers can classify event claims by evidence grade using canon labels.

---

### Phase VI.3 — Fracture and foundational event consequences

- [ ] Have we described the established consequences of the Fracture and other foundational events?

**Starting points** (search further as needed): `world/`, `rules/`, `regions/`, `cultures/`, `phenomena/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Consequences in lived world (institutions, geography, fear, craft)—not a solved cosmology dump.

**Exit criteria:** Fracture consequences are multiple, concrete, and still leave Zero open.

---

### Phase VI.4 — Migrations, conflicts, discoveries, disasters

- [ ] Do we know which migrations, conflicts, discoveries, and disasters shaped the current world?

**Starting points** (search further as needed): `world/`, `regions/`, `cultures/`, `inhabitants/`, `myths/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Prefer regional shaping events with aftermath still visible. Conflict ≠ endless war setting.

**Exit criteria:** Each event class has multiple grounded examples tied to present geography/culture.

---

### Phase VI.5 — Important historical figures and legacies

- [ ] Have we identified important historical figures and their verified contributions or legacies?

**Starting points** (search further as needed): `inhabitants/`, `world/`, `artifacts/`, `myths/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Separate verified legacy from legend inflation.

**Exit criteria:** Key figures have profiles stating what is verified vs attributed.

---

### Phase VI.6 — How history is preserved

- [ ] Do we understand how history is preserved through monuments, artifacts, songs, documents, and traditions?

**Starting points** (search further as needed): `artifacts/`, `cultures/`, `symbols/`, `regions/`, `myths/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Preservation methods should differ by culture/region.

**Exit criteria:** Multiple preservation channels are documented with examples.

---

### Phase VI.7 — Symbols, meanings, legends, beliefs tied to history

- [ ] Have we documented the major symbols, meanings, legends, and beliefs associated with the world's history?

**Starting points** (search further as needed): `symbols/`, `myths/`, `cultures/`, `artworks/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Symbols need meaning + usage + lore connection (full template).

**Exit criteria:** Major historical symbols/legends are encyclopedia-ready and cross-linked.

---

### Phase VI.8 — Observed phenomena vs speculative causes

- [ ] Are significant observed phenomena separated from speculation about their causes?

**Starting points** (search further as needed): `phenomena/`, `rules/`, `myths/`, `world/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Observation sections vs interpretation sections; keep scholarly disagreement.

**Exit criteria:** Flagship phenomena entries cleanly separate what is seen from what is guessed.

---

### Phase VI.9 — Boundaries of unresolved mysteries (no forced solves)

- [ ] Have we defined the known boundaries of each major unresolved mystery without unnecessarily revealing its solution?

**Starting points** (search further as needed): `world/`, `rules/`, [`secrets-pointer.md`](secrets-pointer.md) (author pressure only)

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Public lore gets edges and clues; do not dump spoiler bible. Frequency Zero stays open.

**Exit criteria:** Each major mystery has a bounded “what is known / not known” entry surface.

---

### Phase VI.10 — Annotated timeline for non-saga readers

- [ ] Can we construct an annotated timeline that makes history understandable without requiring readers to follow the sagas?

**Starting points** (search further as needed): `world/`, `artworks/`, `assets/`

**Pace:** Take as long as needed. Leave no stone unturned. Fully answer this question—**100–500+** fully descriptive entries in this phase is fine if required. Do not stop early.

**Diligence:** Timeline must work as a Volume VI spine: eras, foundational events, regional beats—saga-optional.

**Exit criteria:** An annotated timeline artifact/entry exists that a non-saga reader can follow.

---

## After each phase (agent close-out)

1. Confirm Story Architect was used for every new/edited lore file (schema + category template).
2. List new files and enriched files (counts are welcome; high counts are not a problem).
3. State how the phase question is now **fully** answerable (quote entry names / examples). If any sub-angle is still thin, say so and do not mark done.
4. Note remaining soft-limit gaps intentionally left open (mystery ≠ unfinished homework).
5. Rebuild dashboard if links/pins changed: `python3 scripts/build_story_dashboard.py`
6. Mark the phase `- [x]` only if exit criteria truly pass **and** a book chapter could be drafted without inventing rules.
7. Stop for human review unless the human asked to continue to the next phase.

## After each volume

Run the volume **completion test** in prose. If it fails, reopen the weakest phases—do not mark the volume ready.

---

## Final definition of done — every first edition

Even if all world-building phase questions have answers, a book is **not** ready to publish until these conditions pass.

Applies to **each** first edition (Volumes I–VI individually, and to any combined release that claims first-edition status).

### Universal publication checklist

**Publication gates:** 0 of 8 completed

- [ ] Every important claim traces to an approved canonical source.
- [ ] No significant contradictions remain across the six volumes.
- [ ] Unknowns and mysteries are explicitly classified rather than invented.
- [ ] Referenced published facts have approved canon protection.
- [ ] Maps and illustrations accurately reflect the canon.
- [ ] Writing, captions, diagrams, and glossary are understandable independently of the sagas.
- [ ] The edition records its repository commit and approved publication scope.
- [ ] A reader test, editorial review, and publishing proof have been completed.

### How to use this checklist

1. Finish all **61 phases** (or the volumes in scope for that edition) with exit criteria honestly marked.
2. Run each in-scope volume **completion test** again against the drafted book text.
3. Walk the **8 publication gates** above. Do not ship on partial gates.
4. Record: edition name, volumes included, git commit SHA, date, who approved scope, and gate outcomes (agent summary + human sign-off).
5. Only then treat the first edition as **publication-ready**.

**Agent note:** Lore phases prepare the repository. Publication gates cover tracing, cross-volume consistency, art accuracy, saga-independence, commit pinning, and human editorial/proof passes. Agents may help inventory and draft evidence for gates 1–7; gate 8 requires explicit human reader test, editorial review, and publishing proof.
