import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { Discovery, FrequencyId } from "@/data/world";

type Panel = "map" | "codex" | "settings" | null;
export type GraphicsQuality = "auto" | "high" | "low";

interface WorldState {
  activeFrequency: FrequencyId;
  activePanel: Panel;
  selectedDiscovery: Discovery | null;
  discoveredIds: string[];
  currentRegionId: string;
  currentFrequencyLocationId: string | null;
  visitedRegionIds: string[];
  travelTarget: [number, number, number] | null;
  journeyStep: number;
  hasEntered: boolean;
  graphicsQuality: GraphicsQuality;
  setFrequency: (frequency: FrequencyId) => void;
  setPanel: (panel: Panel) => void;
  selectDiscovery: (discovery: Discovery | null) => void;
  visitRegion: (regionId: string) => void;
  requestTravel: (position: [number, number, number]) => void;
  requestFrequencyTravel: (
    frequency: FrequencyId,
    locationId: string,
    position: [number, number, number],
  ) => void;
  clearTravelTarget: () => void;
  setJourneyStep: (step: number) => void;
  enterWorld: () => void;
  setGraphicsQuality: (quality: GraphicsQuality) => void;
}

export const useWorldStore = create<WorldState>()(
  persist(
    (set) => ({
      activeFrequency: "F432",
      activePanel: null,
      selectedDiscovery: null,
      discoveredIds: [],
      currentRegionId: "velorian-basin",
      currentFrequencyLocationId: null,
      visitedRegionIds: ["velorian-basin"],
      travelTarget: null,
      journeyStep: 0,
      hasEntered: false,
      graphicsQuality: "auto",
      setFrequency: (activeFrequency) =>
        set({ activeFrequency, currentFrequencyLocationId: null }),
      setPanel: (panel) =>
        set((state) => ({ activePanel: state.activePanel === panel ? null : panel })),
      selectDiscovery: (selectedDiscovery) =>
        set((state) => ({
          selectedDiscovery,
          discoveredIds:
            selectedDiscovery && !state.discoveredIds.includes(selectedDiscovery.id)
              ? [...state.discoveredIds, selectedDiscovery.id]
              : state.discoveredIds,
        })),
      visitRegion: (currentRegionId) =>
        set((state) => ({
          currentRegionId,
          visitedRegionIds: state.visitedRegionIds.includes(currentRegionId)
            ? state.visitedRegionIds
            : [...state.visitedRegionIds, currentRegionId],
        })),
      requestTravel: (travelTarget) =>
        set({ travelTarget, activePanel: null, currentFrequencyLocationId: null }),
      requestFrequencyTravel: (activeFrequency, currentFrequencyLocationId, travelTarget) =>
        set({
          activeFrequency,
          currentFrequencyLocationId,
          travelTarget,
          activePanel: null,
        }),
      clearTravelTarget: () => set({ travelTarget: null }),
      setJourneyStep: (journeyStep) =>
        set((state) => ({ journeyStep: Math.max(state.journeyStep, journeyStep) })),
      enterWorld: () => set({ hasEntered: true }),
      setGraphicsQuality: (graphicsQuality) => set({ graphicsQuality }),
    }),
    {
      name: "dias-explorer-v1",
      version: 1,
      partialize: (state) => ({
        discoveredIds: state.discoveredIds,
        visitedRegionIds: state.visitedRegionIds,
        journeyStep: state.journeyStep,
        graphicsQuality: state.graphicsQuality,
      }),
    },
  ),
);
