import { describe, expect, it } from "vitest";
import {
  discoveries,
  frequencies,
  frequencyById,
  frequencyLocations,
  regions,
  veloriaJourney,
} from "./world";

function expectUnique(values: string[]) {
  expect(new Set(values).size).toBe(values.length);
}

function expectFinitePosition(position: [number, number, number]) {
  expect(position).toHaveLength(3);
  position.forEach((coordinate) => expect(Number.isFinite(coordinate)).toBe(true));
}

describe("Dias world data", () => {
  it("uses unique stable identifiers", () => {
    expectUnique(frequencies.map((frequency) => frequency.id));
    expectUnique(regions.map((region) => region.id));
    expectUnique(discoveries.map((discovery) => discovery.id));
  });

  it("indexes every frequency exactly once", () => {
    expect(frequencyById.size).toBe(frequencies.length);
    frequencies.forEach((frequency) => {
      expect(frequencyById.get(frequency.id)).toBe(frequency);
    });
  });

  it("keeps region records connected to known frequencies", () => {
    regions.forEach((region) => {
      expect(frequencyById.has(region.frequency)).toBe(true);
      expect(region.name.trim()).not.toBe("");
      expect(region.summary.trim().length).toBeGreaterThan(20);
      expect(region.scale).toBeGreaterThan(0);
      expectFinitePosition(region.position);
    });
  });

  it("keeps discoveries complete and placeable", () => {
    discoveries.forEach((discovery) => {
      expect(frequencyById.has(discovery.frequency)).toBe(true);
      expect(discovery.name.trim()).not.toBe("");
      expect(discovery.region.trim()).not.toBe("");
      expect(discovery.excerpt.trim().length).toBeGreaterThan(10);
      expect(discovery.lore.trim().length).toBeGreaterThan(40);
      expect(discovery.color).toMatch(/^#[0-9a-f]{6}$/i);
      expectFinitePosition(discovery.position);
    });
  });

  it("defines valid visual tokens for every frequency", () => {
    frequencies.forEach((frequency) => {
      expect(frequency.color).toMatch(/^#[0-9a-f]{6}$/i);
      expect(frequency.fog).toMatch(/^#[0-9a-f]{6}$/i);
      expect(frequency.sky).toMatch(/^#[0-9a-f]{6}$/i);
      expect(frequency.accent).toMatch(/^#[0-9a-f]{6}$/i);
      expect(frequency.intensity).toBeGreaterThanOrEqual(0);
      expect(frequency.intensity).toBeLessThanOrEqual(1);
    });
  });

  it("maps every non-material frequency to a destination", () => {
    const nonMaterialFrequencies = frequencies.filter((frequency) => frequency.id !== "F432");
    nonMaterialFrequencies.forEach((frequency) => {
      const locations = frequencyLocations.filter(
        (location) => location.frequency === frequency.id,
      );
      expect(locations.length).toBeGreaterThan(0);
      locations.forEach((location) => {
        expect(location.name.trim()).not.toBe("");
        expect(location.description.trim().length).toBeGreaterThan(20);
        expectFinitePosition(location.arrival);
      });
    });
    expectUnique(frequencyLocations.map((location) => location.id));
  });

  it("keeps the guided journey ordered and complete", () => {
    expect(veloriaJourney).toHaveLength(5);
    veloriaJourney.forEach((step) => {
      expect(step.title.trim()).not.toBe("");
      expect(step.instruction.trim()).not.toBe("");
      expect(step.reflection.trim()).not.toBe("");
    });
  });
});
