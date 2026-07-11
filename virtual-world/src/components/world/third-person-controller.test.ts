import { describe, expect, it } from "vitest";
import { regions } from "@/data/world";
import { isWalkablePosition } from "./third-person-controller";

describe("third-person controller navigation", () => {
  it("allows immediate movement from the Veloria spawn point", () => {
    expect(isWalkablePosition(0, 5)).toBe(true);
    expect(isWalkablePosition(0, 4.95)).toBe(true);
  });

  it("allows movement across every region surface", () => {
    regions.forEach((region) => {
      expect(isWalkablePosition(region.position[0], region.position[2])).toBe(true);
    });
  });

  it("allows movement along generated connecting roads", () => {
    regions.slice(1).forEach((region) => {
      expect(isWalkablePosition(region.position[0] * 0.5, region.position[2] * 0.5)).toBe(true);
    });
  });

  it("rejects movement into the surrounding void", () => {
    expect(isWalkablePosition(24, 24)).toBe(false);
    expect(isWalkablePosition(-24, -24)).toBe(false);
  });
});
