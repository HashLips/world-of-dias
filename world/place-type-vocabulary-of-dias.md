---
category: world
name: Place-Type Vocabulary of Dias
related:
  - Nesting and Scale of Dias
  - Geographical Hierarchy of Dias
  - Dias nesting hierarchy
  - Settlements of Dias
  - Landmarks of Dias
  - Structure of Dias
  - Stack Teaching Customs
  - Atlas Hierarchy Teaching
  - F432 (frequency realm)
themes:
  - vocabulary
  - geography
  - orientation
  - hierarchy
status: canonical
---

# Place-Type Vocabulary of Dias

## Overview

**Place-Type Vocabulary of Dias** names the ordinary scale words inhabitants and clerks use for places, and how those words map to archive `place_type` fields under the geographical hierarchy.

## Core Premise

### Plain definition

A **place-type** answers: what kind of geography is this *inside* its frequency layer? It does not answer which frequency you are in (that is the realm rung).

### Vocabulary table

| Word | Typical use | Archive `place_type` | Nest note |
| --- | --- | --- | --- |
| **realm** | Frequency layer (F432…) | `realm` | Parent is Dias |
| **region** | Broad land or sea body | `region` | Inside a realm |
| **territory** | Broad body with looser civic edges | `territory` | Inside a realm (e.g. Driftfall under Sorel) |
| **city** | Major settlement with layered civic life | `city` | Inside a region/basin |
| **town** | Smaller settlement | `town` | Inside a region/territory |
| **district** | Part of a city | `district` | Still a place rung |
| **landmark** | Named geography; may not govern | `landmark` | Place rung (wells, gates, roads-as-bones) |
| **crossing** | Threshold / span approach | `crossing` | Place rung |
| **island** | Isle geography | `island` | Place rung |
| **building / shop / pub / gallery** | Rooms and thresholds | matching type | Finest common place rungs |
| *(not a place-type)* **phenomenon** | Recurring event | *(phenomena folder)* | Hosted by places |

### Filing rules (plain)

1. Choose the type that matches lived use, not poetry (“a city is a whole world” is speech, not a ledger).  
2. `parent_region` = immediate container only.  
3. Routes travelers treat as bones (fruit roads, gates) often file as `landmark` even when long.  
4. Never file a frequency realm as a district of F432.

### Worked type choices

| Place | `place_type` | Why |
| --- | --- | --- |
| Nauw | `region` | Major F432 land body |
| Veloria City | `city` | Capital settlement |
| Long Gate | `landmark` | Named threshold geography |
| Eastbound Fruit Road | `landmark` | Route bone, not a government |
| Driftfall | `territory` | Broad coastal body under Sorel |
| Aurel Meridian | `region` | Major body inside F200 |

## Global Lore

Archive files use these words in frontmatter so the dashboard Map and graph stay honest. Softfruit rarely says “place_type,” but Atlas Hierarchy Teaching and Stack Teaching Customs teach the same distinctions with cards and bowls. Houses prefer Scale Ladder Glyphs and primer cards.

## Notes

Worked chains live in place entries via `parent_region` and Nesting notes. Binding rules: Dias nesting hierarchy; Geographical Hierarchy of Dias; Local phenomenon scope rule; Frequency realm is not a country.
