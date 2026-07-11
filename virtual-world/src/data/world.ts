export type FrequencyId =
  | "F120"
  | "F200"
  | "F380"
  | "F432"
  | "F500"
  | "F610"
  | "F840"
  | "F960";

export type DiscoveryType =
  | "place"
  | "inhabitant"
  | "artifact"
  | "artwork"
  | "phenomenon"
  | "story";

export interface Frequency {
  id: FrequencyId;
  name: string;
  epithet: string;
  description: string;
  color: string;
  fog: string;
  sky: string;
  accent: string;
  intensity: number;
}

export interface Region {
  id: string;
  name: string;
  frequency: FrequencyId;
  summary: string;
  position: [number, number, number];
  color: string;
  scale: number;
  landmark: string;
}

export interface Discovery {
  id: string;
  name: string;
  type: DiscoveryType;
  frequency: FrequencyId;
  region: string;
  excerpt: string;
  lore: string;
  position: [number, number, number];
  color: string;
}

export interface JourneyStep {
  title: string;
  instruction: string;
  reflection: string;
}

export interface FrequencyLocation {
  id: string;
  name: string;
  frequency: FrequencyId;
  description: string;
  access: "charted" | "partial" | "unsafe";
  arrival: [number, number, number];
}

export const frequencies: Frequency[] = [
  {
    id: "F120",
    name: "Echo",
    epithet: "The Near-Return",
    description: "Events recur in familiar patterns, altered in timing and outcome.",
    color: "#a8c7ff",
    fog: "#10182f",
    sky: "#060a18",
    accent: "#d4e1ff",
    intensity: 0.55,
  },
  {
    id: "F200",
    name: "Luminosity",
    epithet: "The Aurel Meridian",
    description: "Matter becomes held radiance in a serene field of harmonic light.",
    color: "#ffd875",
    fog: "#3b2914",
    sky: "#120d08",
    accent: "#fff0b5",
    intensity: 1,
  },
  {
    id: "F380",
    name: "Hearttide",
    epithet: "The Bloomline",
    description: "Collective feeling moves through the landscape like weather.",
    color: "#ff7fa6",
    fog: "#2c1225",
    sky: "#100812",
    accent: "#ffc2d8",
    intensity: 0.78,
  },
  {
    id: "F432",
    name: "Material",
    epithet: "The Stable Realm",
    description: "The most charted band: roads, cities, trade, and living frontiers.",
    color: "#83c9a8",
    fog: "#0b1b21",
    sky: "#040b10",
    accent: "#c7f2df",
    intensity: 0.66,
  },
  {
    id: "F500",
    name: "Null",
    epithet: "The Abyss Frequency",
    description: "An anti-landscape where distance unmoors and contrast is stolen.",
    color: "#8d80bd",
    fog: "#030306",
    sky: "#000000",
    accent: "#bcb0e8",
    intensity: 0.2,
  },
  {
    id: "F610",
    name: "Reveal",
    epithet: "The Glassfold",
    description: "Brief intervals expose the hidden structure beneath ordinary form.",
    color: "#7de3ef",
    fog: "#092028",
    sky: "#031014",
    accent: "#c7fbff",
    intensity: 0.8,
  },
  {
    id: "F840",
    name: "Ember",
    epithet: "The Hearthline",
    description: "A quiet frequency of aftermath, trace warmth, and patient recovery.",
    color: "#e57b4d",
    fog: "#24110e",
    sky: "#0d0706",
    accent: "#ffc09d",
    intensity: 0.58,
  },
  {
    id: "F960",
    name: "Becoming",
    epithet: "The Unfinished",
    description: "Forms arrive in drafts—outlined, revised, and never finally still.",
    color: "#d7d1c5",
    fog: "#222225",
    sky: "#0d0d10",
    accent: "#ff9f55",
    intensity: 0.5,
  },
];

export const regions: Region[] = [
  {
    id: "velorian-basin",
    name: "Velorian Basin",
    frequency: "F432",
    summary: "A ring-city basin of open ledgers, lantern routes, and resonant trade.",
    position: [0, 0, 0],
    color: "#7ba992",
    scale: 1.25,
    landmark: "The Resonant Spire",
  },
  {
    id: "aelwyn-canopy",
    name: "Aelwyn Canopy",
    frequency: "F432",
    summary: "Seven living paths braid through a forest that remembers every truce.",
    position: [-13, 0, -12],
    color: "#4b8d69",
    scale: 1,
    landmark: "The Sevenfold Tree",
  },
  {
    id: "glasswater-fields",
    name: "Glasswater Fields",
    frequency: "F432",
    summary: "Shallow mirrored plains preserve fragments of an old sky-raid.",
    position: [14, 0, -13],
    color: "#64a9bb",
    scale: 1.05,
    landmark: "The Witness Pools",
  },
  {
    id: "lumira-sands",
    name: "Lumira Sands",
    frequency: "F432",
    summary: "Copper dunes, drifting faces, and moon markets beneath a violet horizon.",
    position: [15, 0, 13],
    color: "#b88a59",
    scale: 1.1,
    landmark: "The Long Gate",
  },
  {
    id: "driftfall",
    name: "Driftfall",
    frequency: "F432",
    summary: "A fractured coast where waterfalls climb and sky-drifters make port.",
    position: [-14, 0, 14],
    color: "#7187a8",
    scale: 0.95,
    landmark: "The Inverted Falls",
  },
];

export const discoveries: Discovery[] = [
  {
    id: "vailor-quentin",
    name: "Vailor Quentin",
    type: "inhabitant",
    frequency: "F432",
    region: "Velorian Basin",
    excerpt: "High Resonant of F432",
    lore: "Vailor listens for instability beneath civic harmony. His authority rests less on command than on his ability to hear when a city is falling out of tune.",
    position: [2.8, 1.3, -1.5],
    color: "#f3d58d",
  },
  {
    id: "prime-bridge",
    name: "The Prime Bridge",
    type: "artifact",
    frequency: "F432",
    region: "Velorian Basin",
    excerpt: "A remnant seen across several realities",
    lore: "Its broken spans recur in multiple Frequencies, each fragment insisting it once connected a world that had not yet learned to separate.",
    position: [-5, 1.2, -5],
    color: "#d8e7df",
  },
  {
    id: "choirglass",
    name: "Choirglass Envoy",
    type: "inhabitant",
    frequency: "F432",
    region: "Glasswater Fields",
    excerpt: "A faceted person speaking in sound-light",
    lore: "Choirglass exchange meaning through harmonized refraction. This envoy has been watching the Witness Pools for a note no one else can hear.",
    position: [14, 1.4, -12],
    color: "#8ff3ff",
  },
  {
    id: "lineborn-citizen",
    name: "Lineborn Citizen",
    type: "inhabitant",
    frequency: "F432",
    region: "Velorian Basin",
    excerpt: "A living person drawn in calligraphic edges",
    lore: "Lineborn are fully embodied people whose near-planar forms can disappear at a side angle, then return as richly textured ink, chalk, and crosshatch.",
    position: [1.7, 1.1, 2.7],
    color: "#f0e8d5",
  },
  {
    id: "palewind-traveler",
    name: "Palewind Traveler",
    type: "inhabitant",
    frequency: "F432",
    region: "Velorian Basin",
    excerpt: "One coherent person carried by many motes",
    lore: "A Palewind identity is distributed across a coordinated veil of micro-bodies. The swarm may branch for a task and gather again without losing continuity of self.",
    position: [-3.1, 1.4, 2.4],
    color: "#d7f3e8",
  },
  {
    id: "kharad-waykeeper",
    name: "Kharad Waykeeper",
    type: "inhabitant",
    frequency: "F432",
    region: "Driftfall",
    excerpt: "A dense-bodied keeper of structural memory",
    lore: "Kharad traditions treat infrastructure as a long promise. This waykeeper reads stress in the road by touch, recording what pressure has asked the stone to remember.",
    position: [-13.5, 1.2, 12.2],
    color: "#c77c5a",
  },
  {
    id: "unfinished-edge",
    name: "Unfinished Edge Drift",
    type: "phenomenon",
    frequency: "F960",
    region: "Driftfall",
    excerpt: "A soft incursion of revisable form",
    lore: "Guide marks gather where the coast loses confidence in its outline. Objects near the drift may return with an earlier version of themselves still visible.",
    position: [-12.5, 1.1, 13],
    color: "#ff9f55",
  },
  {
    id: "blue-rose-vow",
    name: "The Blue Rose Vow",
    type: "story",
    frequency: "F380",
    region: "Aelwyn Canopy",
    excerpt: "A promise that changes the weather",
    lore: "When spoken without witnesses, the vow is said to tint nearby rain blue. The Canopy records no proof, only seasons of impossible flowers.",
    position: [-12, 1, -10],
    color: "#709bff",
  },
  {
    id: "long-gate",
    name: "The Long Gate",
    type: "place",
    frequency: "F432",
    region: "Lumira Sands",
    excerpt: "A threshold argued into existence",
    lore: "No account agrees whether the gate was built before the road or whether generations of travelers made it real by expecting an entrance.",
    position: [15, 1.6, 12],
    color: "#e5a36e",
  },
  {
    id: "emergence-artwork",
    name: "Emergence",
    type: "artwork",
    frequency: "F432",
    region: "The Sketchy Gallery",
    excerpt: "Acrylic silhouettes suspended in open darkness",
    lore: "The painting is Veloria's primary visual language for the Sky Drifters: separate figures moving through a shared field, endlessly grouping and parting without ground.",
    position: [-1.85, 1.25, -1.3],
    color: "#d8eee9",
  },
  {
    id: "green-garden-artwork",
    name: "Green Garden",
    type: "artwork",
    frequency: "F432",
    region: "The Sketchy Gallery",
    excerpt: "A bloomscape ordered by shifting light",
    lore: "Rows of individually potted green blooms gather into the scale of a field. The work preserves the therapeutic pause of the Green Garden Border Lanes.",
    position: [-2.2, 1.25, -0.1],
    color: "#70bc75",
  },
  {
    id: "bronze-umbrella",
    name: "Bronze Umbrella Seated Figure",
    type: "artifact",
    frequency: "F432",
    region: "The Sketchy Gallery",
    excerpt: "The contemplative midpoint of the gallery",
    lore: "A seated bronze figure holds an umbrella beneath a circular skylight. Visitors pause here before continuing toward the unexplained blue door.",
    position: [-1.8, 1.05, 1.1],
    color: "#b27c4b",
  },
];

export const frequencyById = new Map(frequencies.map((frequency) => [frequency.id, frequency]));

export const frequencyLocations: FrequencyLocation[] = [
  {
    id: "returning-span",
    name: "The Returning Span",
    frequency: "F120",
    description: "Three navigable drift lanes where near-return patterns become legible.",
    access: "partial",
    arrival: [0, 0.35, 5],
  },
  {
    id: "aurel-meridian",
    name: "Aurel Meridian",
    frequency: "F200",
    description: "The bright spine of stable standing waves and energy-native life.",
    access: "partial",
    arrival: [0, 0.35, 5],
  },
  {
    id: "bloomline-estuary",
    name: "The Bloomline Estuary",
    frequency: "F380",
    description: "A branching confluence where emotional weather can be charted.",
    access: "partial",
    arrival: [0, 0.35, 5],
  },
  {
    id: "null-warning-boundary",
    name: "Null Warning Boundary",
    frequency: "F500",
    description: "The last mapped interval before distance, memory, and contrast become unreliable.",
    access: "unsafe",
    arrival: [0, 0.35, 5],
  },
  {
    id: "glassfold-ledge",
    name: "The Glassfold Ledge",
    frequency: "F610",
    description: "Mirrored shelves where hidden structure appears in brief reveal windows.",
    access: "partial",
    arrival: [0, 0.35, 5],
  },
  {
    id: "ashen-hearthline",
    name: "The Ashen Hearthline",
    frequency: "F840",
    description: "A stable warmth corridor built around shelter, relay, and quiet recovery.",
    access: "partial",
    arrival: [0, 0.35, 5],
  },
  {
    id: "the-unfinished",
    name: "The Unfinished",
    frequency: "F960",
    description: "A revisable district of scaffold arcs, ghost quarters, and living drafts.",
    access: "partial",
    arrival: [0, 0.35, 5],
  },
];

export const veloriaJourney: JourneyStep[] = [
  {
    title: "The road to Veloria",
    instruction: "Walk toward the gold-lit gate.",
    reflection: "The road leaves enough lane for every stranger to pass.",
  },
  {
    title: "Look up before you look in",
    instruction: "Pass beneath the DEB Gate.",
    reflection: "Pale figures drift above the city. No one runs.",
  },
  {
    title: "The first ring",
    instruction: "Cross the old stone outer ring.",
    reflection: "Market bells and hand-work endure beside a changing city.",
  },
  {
    title: "Same city, different layer",
    instruction: "Travel inward through the modern rings.",
    reflection: "Glass, machines, and old songs share one civic rhythm.",
  },
  {
    title: "The radiant core",
    instruction: "Reach the innermost power district.",
    reflection: "Dias is one world. That is not the same as one place.",
  },
];
