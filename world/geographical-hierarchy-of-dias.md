---
category: world
name: Geographical Hierarchy of Dias
related:
  - Nesting and Scale of Dias
  - Place-Type Vocabulary of Dias
  - Dias nesting hierarchy
  - Structure of Dias
  - Settlements of Dias
  - Landmarks of Dias
  - Atlas Hierarchy Teaching
  - Atlas Hierarchy Ladder Card
  - Nesting Structure Comparison Plate
  - F432 (frequency realm)
  - F200 (frequency realm)
  - Nauw
  - Wabet
  - Sorel
  - Velorian Basin
  - Veloria City
  - Long Gate
  - Quiet Well
  - Driftfall
  - Claimscar Yard
  - Eastbound Fruit Road
  - The Returning Span
  - Aurel Meridian
  - Frequency realm is not a country
  - Local phenomenon scope rule
  - F432 Major Regions of Dias
  - Landforms of F432
  - Atlas Map Levels of Dias
  - Veloria Walkable Atlas of Dias
  - F432 Journey Routes of Dias
themes:
  - geography
  - hierarchy
  - atlas
  - place_type
  - orientation
status: canonical
time_era: present
time_span: ongoing
---

# Geographical Hierarchy of Dias

## Overview

**Geographical Hierarchy of Dias** is the atlas primer for how places nest: frequency realm → region (or territory) → settlement → landmark / route / room. It is the map-facing sibling of Nesting and Scale of Dias (which also covers local phenomena). Use this when planning journeys and filing `parent_region` / `place_type`.

## Core Premise

### Plain definitions

| Rung | Definition | Typical `place_type` |
| --- | --- | --- |
| **Frequency realm** | Vibrational layer of Dias; not a country | `realm` |
| **Major region / territory** | Broad land or sea body inside a realm | `region`, `territory` |
| **Settlement** | Place people live with civic or yard habits | `city`, `town`, and settlement-tier places |
| **Landmark / route / crossing** | Named geography feet can aim at; may not be a government | `landmark`, `crossing`, `island` |
| **Room-scale place** | Building, shop, hall, pub, gallery | `building`, `shop`, `pub`, `gallery`, `district` |

**Local phenomena** are not a geography rung. They visit places (Local phenomenon scope rule).

### Immediate parent rule

`parent_region` is always the **immediate** container—not Dias, not a skip-level shortcut.

Wrong: Veloria City → F432  
Right: Veloria City → Velorian Basin → Nauw → F432 → Dias

### Worked hierarchy (F432 home band)

```
Dias
 └── F432 (frequency realm)          [realm]
      ├── Nauw                       [region]
      │    ├── Velorian Basin        [region]
      │    │    └── Veloria City     [city]
      │    │         └── Softfruit Table Hall  [building / hall]
      │    └── Long Gate             [landmark]
      ├── Wabet                      [region]
      │    ├── Lumira Sands          [region / territory as filed]
      │    │    └── Quiet Well       [landmark]
      │    └── Eastbound Fruit Road  [landmark — route]
      └── Sorel                      [region]
           ├── Driftfall             [territory]
           │    └── Claimscar Yard   [town / frontier yard as filed]
           └── Hearthvale            [region / approach as filed]
```

### Worked hierarchy (other established realm)

```
Dias
 └── F200 (frequency realm)          [realm]
      └── Aurel Meridian             [region]
           └── Soft-Ray halls / Lumen Stair approaches  [landmark / building scale]
```

```
Dias
 └── F120 (frequency realm)          [realm]
      └── The Returning Span         [region]
           └── lanes / difference marks / waysides  [landmark scale]
```

F500 rarely offers friendly settlement rungs; null margins are events and warnings more than districts (Frequency realm is not a country).

### How to read Settlements vs Landmarks indexes

- **Settlements of Dias** — lived places with jobs, safety tiers, and stay-length  
- **Landmarks of Dias** — traveler bones: direction, ceremony, fear, argument  
- Both sit under this hierarchy; neither replaces region files of record

## Global Lore

Archive honesty depends on matching `name:` in `parent_region` and choosing a `place_type` from Place-Type Vocabulary of Dias. Stack Teaching and Atlas Hierarchy Teaching drill the ladder with bowls and cards. Nesting Structure Comparison Plate shows the same stack as a diagram.

## Notes

Volume II atlas work deepens each rung’s content; this entry locks how rungs relate. Do not draw frequency realms as neighboring provinces on an F432 road map.
