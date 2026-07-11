"use client";

import { useEffect, useMemo, useRef } from "react";
import { useFrame, useThree } from "@react-three/fiber";
import * as THREE from "three";
import { regions } from "@/data/world";
import { useWorldStore } from "@/store/world-store";

const PLAYER_HEIGHT = 0.35;
const WALK_SPEED = 3.9;
const RUN_SPEED = 6.4;
const ACCELERATION = 13;
const DECELERATION = 17;
const PLAYER_RADIUS = 0.24;
const WORLD_UP = new THREE.Vector3(0, 1, 0);

const pressedKeys = new Set<string>();

interface Route {
  startX: number;
  startZ: number;
  deltaX: number;
  deltaZ: number;
  lengthSquared: number;
}

interface CameraObstacle {
  center: THREE.Vector3;
  radius: number;
  height: number;
}

const routes: Route[] = regions.slice(1).map((region) => {
  const destination = new THREE.Vector3(...region.position);
  const direction = destination.clone().setY(0).normalize();
  const start = direction.clone().multiplyScalar(4.35);
  const end = destination.clone().sub(direction.clone().multiplyScalar(4.2));
  const deltaX = end.x - start.x;
  const deltaZ = end.z - start.z;
  return {
    startX: start.x,
    startZ: start.z,
    deltaX,
    deltaZ,
    lengthSquared: deltaX * deltaX + deltaZ * deltaZ,
  };
});

const collisionRegions = regions.map((region) => ({
  x: region.position[0],
  z: region.position[2],
  radiusSquared: (4.12 * region.scale - PLAYER_RADIUS) ** 2,
}));

const cameraObstacles: CameraObstacle[] = [
  { center: new THREE.Vector3(0, 1.4, 0), radius: 1.05, height: 3.4 },
  { center: new THREE.Vector3(0, 1.1, 4.05), radius: 1.45, height: 2.8 },
  { center: new THREE.Vector3(-2.15, 1.25, 0), radius: 1.2, height: 2.7 },
];

function distanceSquaredToRoute(x: number, z: number, route: Route) {
  if (route.lengthSquared === 0) {
    return (x - route.startX) ** 2 + (z - route.startZ) ** 2;
  }
  const progress = THREE.MathUtils.clamp(
    ((x - route.startX) * route.deltaX + (z - route.startZ) * route.deltaZ) /
      route.lengthSquared,
    0,
    1,
  );
  const closestX = route.startX + route.deltaX * progress;
  const closestZ = route.startZ + route.deltaZ * progress;
  return (x - closestX) ** 2 + (z - closestZ) ** 2;
}

export function isWalkablePosition(x: number, z: number) {
  // The DEB Gate approach extends slightly beyond the circular city collider.
  // Without this apron, the canonical spawn point sits millimetres outside the
  // conservative player-radius boundary and every attempted step is rejected.
  const onVeloriaGateApproach = Math.abs(x) <= 0.72 && z >= 3.65 && z <= 5.35;
  if (onVeloriaGateApproach) return true;

  const onRegion = collisionRegions.some(
    (region) => (x - region.x) ** 2 + (z - region.z) ** 2 <= region.radiusSquared,
  );
  if (onRegion) return true;
  return routes.some((route) => distanceSquaredToRoute(x, z, route) <= 0.34 ** 2);
}

function resolveWalkablePosition(
  current: THREE.Vector3,
  desired: THREE.Vector3,
  output: THREE.Vector3,
) {
  if (isWalkablePosition(desired.x, desired.z)) return output.copy(desired);
  if (isWalkablePosition(desired.x, current.z)) {
    return output.set(desired.x, current.y, current.z);
  }
  if (isWalkablePosition(current.x, desired.z)) {
    return output.set(current.x, current.y, desired.z);
  }
  return output.copy(current);
}

function damp(current: number, target: number, smoothing: number, delta: number) {
  return THREE.MathUtils.lerp(current, target, 1 - Math.exp(-smoothing * delta));
}

function dampAngle(current: number, target: number, smoothing: number, delta: number) {
  const difference = Math.atan2(Math.sin(target - current), Math.cos(target - current));
  return current + difference * (1 - Math.exp(-smoothing * delta));
}

function clippedCameraDistance(
  target: THREE.Vector3,
  desired: THREE.Vector3,
  requestedDistance: number,
) {
  const ray = cameraScratch.ray.copy(desired).sub(target);
  const rayLength = ray.length();
  if (rayLength === 0) return requestedDistance;
  ray.divideScalar(rayLength);

  let safeDistance = requestedDistance;
  for (const obstacle of cameraObstacles) {
    if (target.y > obstacle.height) continue;
    const toCenter = cameraScratch.toCenter.copy(obstacle.center).sub(target);
    const projected = THREE.MathUtils.clamp(toCenter.dot(ray), 0, rayLength);
    const closest = cameraScratch.closest.copy(target).addScaledVector(ray, projected);
    const horizontalDistance = Math.hypot(
      closest.x - obstacle.center.x,
      closest.z - obstacle.center.z,
    );
    if (
      horizontalDistance < obstacle.radius &&
      closest.y < obstacle.height &&
      target.distanceTo(obstacle.center) > obstacle.radius
    ) {
      safeDistance = Math.min(safeDistance, Math.max(1.5, projected - obstacle.radius - 0.2));
    }
  }
  return safeDistance;
}

const cameraScratch = {
  ray: new THREE.Vector3(),
  toCenter: new THREE.Vector3(),
  closest: new THREE.Vector3(),
};

function useControllerInput() {
  const yaw = useRef(0);
  const pitch = useRef(0.48);
  const distance = useRef(6.4);
  const dragging = useRef(false);

  useEffect(() => {
    const keyDown = (event: KeyboardEvent) => {
      if (["KeyW", "KeyA", "KeyS", "KeyD", "ShiftLeft", "ShiftRight"].includes(event.code)) {
        pressedKeys.add(event.code);
      }
    };
    const keyUp = (event: KeyboardEvent) => pressedKeys.delete(event.code);
    const pointerDown = (event: PointerEvent) => {
      if (event.target instanceof HTMLCanvasElement && event.button === 0) {
        dragging.current = true;
      }
    };
    const pointerUp = () => {
      dragging.current = false;
    };
    const pointerMove = (event: PointerEvent) => {
      if (!dragging.current) return;
      yaw.current -= event.movementX * 0.004;
      pitch.current = THREE.MathUtils.clamp(
        pitch.current + event.movementY * 0.003,
        -0.65,
        1.15,
      );
    };
    const wheel = (event: WheelEvent) => {
      if (!(event.target instanceof HTMLCanvasElement)) return;
      distance.current = THREE.MathUtils.clamp(distance.current + event.deltaY * 0.006, 3.3, 8.5);
    };
    const blur = () => {
      pressedKeys.clear();
      dragging.current = false;
    };

    window.addEventListener("keydown", keyDown);
    window.addEventListener("keyup", keyUp);
    window.addEventListener("pointerdown", pointerDown);
    window.addEventListener("pointerup", pointerUp);
    window.addEventListener("pointermove", pointerMove);
    window.addEventListener("wheel", wheel, { passive: true });
    window.addEventListener("blur", blur);
    return () => {
      pressedKeys.clear();
      window.removeEventListener("keydown", keyDown);
      window.removeEventListener("keyup", keyUp);
      window.removeEventListener("pointerdown", pointerDown);
      window.removeEventListener("pointerup", pointerUp);
      window.removeEventListener("pointermove", pointerMove);
      window.removeEventListener("wheel", wheel);
      window.removeEventListener("blur", blur);
    };
  }, []);

  return { yaw, pitch, distance };
}

function updateWorldProgress(position: THREE.Vector3) {
  const distanceFromCore = Math.hypot(position.x, position.z);
  const distanceFromGate = Math.hypot(position.x, position.z - 4.05);
  const { journeyStep, setJourneyStep, currentRegionId, visitRegion } = useWorldStore.getState();
  let reachedStep = journeyStep;
  if (distanceFromGate < 0.68) reachedStep = Math.max(reachedStep, 1);
  if (position.z < 3.65 && distanceFromCore < 4.15) reachedStep = Math.max(reachedStep, 2);
  if (distanceFromCore < 2.9) reachedStep = Math.max(reachedStep, 3);
  if (distanceFromCore < 1.4) reachedStep = Math.max(reachedStep, 4);
  if (reachedStep !== journeyStep) setJourneyStep(reachedStep);

  let nearestRegion = regions[0];
  let nearestDistance = Number.POSITIVE_INFINITY;
  for (const region of regions) {
    const distance = Math.hypot(position.x - region.position[0], position.z - region.position[2]);
    if (distance < nearestDistance) {
      nearestDistance = distance;
      nearestRegion = region;
    }
  }
  if (nearestDistance < 5.3 && nearestRegion.id !== currentRegionId) {
    visitRegion(nearestRegion.id);
  }
}

export function ThirdPersonController() {
  const root = useRef<THREE.Group>(null);
  const visual = useRef<THREE.Group>(null);
  const leftArm = useRef<THREE.Mesh>(null);
  const rightArm = useRef<THREE.Mesh>(null);
  const leftLeg = useRef<THREE.Mesh>(null);
  const rightLeg = useRef<THREE.Mesh>(null);
  const velocity = useRef(new THREE.Vector3());
  const cameraVelocityTarget = useRef(new THREE.Vector3());
  const animationTime = useRef(0);
  const progressAccumulator = useRef(0);
  const { camera } = useThree();
  const input = useControllerInput();

  const movementVectors = useMemo(
    () => ({
      forward: new THREE.Vector3(),
      right: new THREE.Vector3(),
      desired: new THREE.Vector3(),
      target: new THREE.Vector3(),
      lookTarget: new THREE.Vector3(),
      cameraOffset: new THREE.Vector3(),
      nextPosition: new THREE.Vector3(),
      resolvedPosition: new THREE.Vector3(),
      requestedCamera: new THREE.Vector3(),
    }),
    [],
  );

  useEffect(() => {
    camera.position.set(5.2, 4.2, 10.5);
  }, [camera]);

  useFrame((_, rawDelta) => {
    if (!root.current || !visual.current) return;
    const delta = Math.min(rawDelta, 1 / 20);
    const pendingTravel = useWorldStore.getState().travelTarget;
    if (pendingTravel) {
      root.current.position.set(pendingTravel[0], PLAYER_HEIGHT, pendingTravel[2]);
      velocity.current.set(0, 0, 0);
      cameraVelocityTarget.current.copy(root.current.position);
      useWorldStore.getState().clearTravelTarget();
    }

    const horizontalInput =
      Number(pressedKeys.has("KeyD")) - Number(pressedKeys.has("KeyA"));
    const verticalInput =
      Number(pressedKeys.has("KeyW")) - Number(pressedKeys.has("KeyS"));
    const hasInput = horizontalInput !== 0 || verticalInput !== 0;
    const running = pressedKeys.has("ShiftLeft") || pressedKeys.has("ShiftRight");
    const speed = running ? RUN_SPEED : WALK_SPEED;

    movementVectors.forward.set(-Math.sin(input.yaw.current), 0, -Math.cos(input.yaw.current));
    movementVectors.right.set(Math.cos(input.yaw.current), 0, -Math.sin(input.yaw.current));
    movementVectors.desired
      .copy(movementVectors.forward)
      .multiplyScalar(verticalInput)
      .addScaledVector(movementVectors.right, horizontalInput);
    if (movementVectors.desired.lengthSq() > 1) movementVectors.desired.normalize();
    movementVectors.desired.multiplyScalar(speed);

    const smoothing = hasInput ? ACCELERATION : DECELERATION;
    velocity.current.x = damp(velocity.current.x, movementVectors.desired.x, smoothing, delta);
    velocity.current.z = damp(velocity.current.z, movementVectors.desired.z, smoothing, delta);
    if (!hasInput && velocity.current.lengthSq() < 0.002) velocity.current.set(0, 0, 0);

    movementVectors.nextPosition
      .copy(root.current.position)
      .addScaledVector(velocity.current, delta);
    root.current.position.copy(
      resolveWalkablePosition(
        root.current.position,
        movementVectors.nextPosition,
        movementVectors.resolvedPosition,
      ),
    );
    root.current.position.y = PLAYER_HEIGHT;

    const movementSpeed = Math.hypot(velocity.current.x, velocity.current.z);
    if (movementSpeed > 0.08) {
      const targetRotation = Math.atan2(velocity.current.x, velocity.current.z);
      visual.current.rotation.y = dampAngle(
        visual.current.rotation.y,
        targetRotation,
        14,
        delta,
      );
      animationTime.current += delta * movementSpeed * 2.1;
    }
    const stride = Math.sin(animationTime.current) * Math.min(0.75, movementSpeed * 0.13);
    const bob = Math.abs(Math.sin(animationTime.current * 2)) * Math.min(0.07, movementSpeed * 0.012);
    visual.current.position.y = damp(visual.current.position.y, bob, 14, delta);
    if (leftArm.current) leftArm.current.rotation.x = stride;
    if (rightArm.current) rightArm.current.rotation.x = -stride;
    if (leftLeg.current) leftLeg.current.rotation.x = -stride;
    if (rightLeg.current) rightLeg.current.rotation.x = stride;

    progressAccumulator.current += delta;
    if (progressAccumulator.current >= 0.2) {
      updateWorldProgress(root.current.position);
      progressAccumulator.current = 0;
    }

    movementVectors.target.copy(root.current.position).addScaledVector(WORLD_UP, 1.05);
    const horizontalDistance = Math.cos(input.pitch.current) * input.distance.current;
    movementVectors.cameraOffset.set(
      Math.sin(input.yaw.current) * horizontalDistance,
      Math.sin(input.pitch.current) * input.distance.current + 0.8,
      Math.cos(input.yaw.current) * horizontalDistance,
    );
    movementVectors.requestedCamera
      .copy(movementVectors.target)
      .add(movementVectors.cameraOffset);
    movementVectors.requestedCamera.y = Math.max(0.72, movementVectors.requestedCamera.y);
    const requestedDistance = movementVectors.requestedCamera.distanceTo(movementVectors.target);
    const safeDistance = clippedCameraDistance(
      movementVectors.target,
      movementVectors.requestedCamera,
      requestedDistance,
    );
    movementVectors.cameraOffset
      .copy(movementVectors.requestedCamera)
      .sub(movementVectors.target)
      .setLength(safeDistance);
    cameraVelocityTarget.current.copy(movementVectors.target).add(movementVectors.cameraOffset);
    camera.position.lerp(cameraVelocityTarget.current, 1 - Math.exp(-10 * delta));
    movementVectors.lookTarget
      .copy(movementVectors.target)
      .addScaledVector(WORLD_UP, Math.max(0, -input.pitch.current) * 7.5);
    camera.lookAt(movementVectors.lookTarget);
  });

  return (
    <group ref={root} position={[0, PLAYER_HEIGHT, 5]}>
      <group ref={visual}>
        <mesh castShadow position={[0, 0.7, 0]}>
          <capsuleGeometry args={[0.23, 0.62, 5, 10]} />
          <meshStandardMaterial color="#dbe9e2" roughness={0.58} metalness={0.12} />
        </mesh>
        <mesh castShadow position={[0, 1.25, 0]}>
          <sphereGeometry args={[0.2, 12, 10]} />
          <meshStandardMaterial color="#eef5f1" roughness={0.5} />
        </mesh>
        <mesh ref={leftArm} castShadow position={[-0.29, 0.75, 0]}>
          <capsuleGeometry args={[0.065, 0.48, 4, 8]} />
          <meshStandardMaterial color="#9fb5aa" roughness={0.64} />
        </mesh>
        <mesh ref={rightArm} castShadow position={[0.29, 0.75, 0]}>
          <capsuleGeometry args={[0.065, 0.48, 4, 8]} />
          <meshStandardMaterial color="#9fb5aa" roughness={0.64} />
        </mesh>
        <mesh ref={leftLeg} castShadow position={[-0.12, 0.2, 0]}>
          <capsuleGeometry args={[0.075, 0.42, 4, 8]} />
          <meshStandardMaterial color="#61756b" roughness={0.7} />
        </mesh>
        <mesh ref={rightLeg} castShadow position={[0.12, 0.2, 0]}>
          <capsuleGeometry args={[0.075, 0.42, 4, 8]} />
          <meshStandardMaterial color="#61756b" roughness={0.7} />
        </mesh>
      </group>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.03, 0]}>
        <ringGeometry args={[0.34, 0.39, 24]} />
        <meshBasicMaterial color="#c7f2df" transparent opacity={0.58} />
      </mesh>
    </group>
  );
}
