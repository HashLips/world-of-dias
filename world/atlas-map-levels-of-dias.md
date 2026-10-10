---
category: world
name: Atlas Map Levels of Dias
related:
  - Geographical Hierarchy of Dias
  - Objective and Unreliable Maps of Dias
  - F432 Map V2
  - Map of Nauw
  - Map of Wabet
  - Map of Sorel
  - Veloria Ring Walk Sketch
  - Hollowmere Cove Walk Sketch
  - Tubehold Dam Walk Sketch
  - Secondfire Kiln Walk Sketch
  - Poster of Veloria City
  - Rings of Veloria Primer
  - Veloria Walkable Atlas of Dias
  - F432 Settlement Walks of Dias
  - F432 Major Regions of Dias
  - Landforms of F432
themes:
  - maps
  - atlas
  - consistency
  - levels
status: canonical
time_era: present
time_span: ongoing
---

# Atlas Map Levels of Dias

## Overview

**Atlas Map Levels of Dias** defines three consistent map levels—realm, regional, settlement—and how prose, artworks, and the dashboard atlas must agree.

## Core Premise

### Plain levels

| Level | Shows | Canon anchors |
| --- | --- | --- |
| **Realm** | One frequency layer’s major bodies (for F432: Wabet west, Nauw north-east, Sorel south) | F432 Map V2; other band Map V2 family |
| **Regional** | One major region’s basins, marches, coasts, named landforms | Map of Nauw; Map of Wabet; Map of Sorel |
| **Settlement** | Walkable corners, gates, halls, approaches | Veloria Ring Walk Sketch; Hollowmere Cove Walk Sketch; Tubehold Dam Walk Sketch; Secondfire Kiln Walk Sketch; Poster of Veloria City |

### Consistency rules (plain)

1. **Same nesting as Geographical Hierarchy** — Veloria sits in Basin in Nauw in F432; never as a floating capital on F500.  
2. **Pins match prose** — Long Gate is southern Nauw → Hearthvale; fruit roads run Wabet → Nauw.  
3. **Settlement ink cannot contradict regional coastlines** — rings may be sketchy; Outer Rim still sits north of Nauw as established.  
4. **Dashboard atlas** (`map-registry.yaml`) is a reading aid; V2 artworks and region files of record win conflicts after deliberate revision.  
5. **Wrong maps** (mercy / motivated) are labeled as such—they are not a fourth “true” level.

### Consistency check (F432 deepen pass)

| Claim in prose | Map / registry check |
| --- | --- |
| Wabet west, Nauw north-east, Sorel south | F432 Map V2 + registry region polygons |
| Veloria in Velorian Basin (NW Nauw) | Pin ~58,24 inside Nauw polygon |
| Hollowmere on Outer Rim | Under Nauw Outer Rim Seas; north rim pins |
| Tubehold in Glasswater | Glasswater Fields east Nauw |
| Hearthvale / Secondfire south of Long Gate | Hearthvale ~50,54; Sorel polygon |
| Driftfall / Claimscar SE coastal | Driftfall ~72,70; salvage shore nearby |
| Lumira south Wabet; Quiet Well there | Lumira ~24,72; Quiet Well ~22,68 |
| Fruit road Wabet → Nauw | Eastbound Fruit Road ~42,38 between west and basin |

Unresolved map refs after dashboard build must stay at **0** when closing Volume II.

### Book-atlas use

- Chapter openers: realm glance  
- Travel chapters: regional landforms + journey routes + seasons  
- City / town chapters: settlement walk sketches (not only Veloria)  

## Global Lore

Objective vs unreliable maps: Objective and Unreliable Maps of Dias. Mercy cartography index: Maps and Wrong Maps of Dias. Settlement walks index: F432 Settlement Walks of Dias.

## Notes

Exit criterion for Volume II.10: realm + regional consistency verified; settlement-level depth for Veloria **and** representative other towns (Hollowmere, Tubehold, Secondfire).
