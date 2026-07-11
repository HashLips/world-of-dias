# Dias Virtual World

An immersive, data-driven exploration of Dias built with Next.js, TypeScript,
Three.js, and React Three Fiber.

## Features

- Third-person movement with orbiting camera controls
- Connected F432 regions with unlockable map travel
- Eight frequency states with distinct light, fog, geometry, and atmosphere
- Guided *First Day in Veloria* onboarding journey
- Interactive inhabitants, artifacts, artworks, landmarks, and phenomena
- Persistent codex, journey progress, visited regions, and preferences
- Adaptive rendering for mobile and reduced-motion environments

## Run Locally

Requirements:

- Node.js 20.19 or newer
- npm 9 or newer

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

Production verification:

```bash
npm run lint
npm test
npm run build
npm start
```

## Controls

- **Move** — `W`, `A`, `S`, `D`
- **Look** — drag with a mouse or pointer
- **Zoom** — mouse wheel or trackpad
- **Inspect** — select resonant lights, inhabitants, or artworks
- **Travel** — unlock a region by visiting it, then use the world map

## Architecture

- `src/app/` — application shell, metadata, and global visual system
- `src/components/world/world-experience.tsx` — HUD, panels, onboarding, map, and codex
- `src/components/world/world-canvas.tsx` — R3F scene, movement, biomes, inhabitants, and phenomena
- `src/components/world/third-person-controller.tsx` — movement, collision, camera, and animation
- `src/data/world.ts` — typed frequencies, regions, discoveries, and journey content
- `src/store/world-store.ts` — Zustand interaction state and persisted progress

The Canvas is loaded dynamically without server rendering. World content is
kept in typed data records so additions do not require routing or component
restructuring.

## Add World Content

### Add a frequency

1. Add its identifier to `FrequencyId` in `src/data/world.ts`.
2. Add a `Frequency` record with atmosphere colors and intensity.
3. Add an optional physical effect in `FrequencyPhenomena`.

### Add a region

1. Add a `Region` record in `src/data/world.ts`.
2. Assign a world position, scale, landmark, and canonical summary.
3. Add specialized landmark geometry only when the region needs it.

Roads, proximity detection, map progress, and fast travel consume the region
record automatically.

### Add a discovery

Add a `Discovery` record in `src/data/world.ts` with:

- Stable kebab-case `id`
- Name and discovery type
- Frequency and region
- Short excerpt and canon-safe lore
- World position and identifying color

Discovery markers and codex entries are generated from this collection.

## Canon Rules

Source lore remains in the parent repository. Interactive interpretations must
preserve these constraints:

- The Fracture happened, but its cause remains unknown.
- Cross-frequency claims from F432 use partial knowledge, rumor, or witness framing.
- Lineborn and Palewind Swarms are persons, not effects or anonymous scenery.
- F500 is erasure and unmoored absence, not ordinary darkness.
- F960 represents intentional incompletion, not ruin.
- Gilding hour is meteorological and culturally meaningful, not established magic.
- Myths and institutional records must not be presented as equally certain.

## Performance

The default `Auto` profile:

- Caps device pixel ratio
- Reduces effects on compact viewports
- Honors `prefers-reduced-motion`
- Removes post-processing in low-power mode
- Uses instancing for particle-based inhabitants

Users can override the profile in the in-world settings panel.

## Persistence

The browser stores:

- Codex discoveries
- Visited regions
- Guided journey progress
- Graphics preference

Storage is versioned under `dias-explorer-v1`. No account or network request is
required.
