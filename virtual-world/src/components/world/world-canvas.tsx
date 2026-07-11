"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { Canvas, useFrame, useThree, type ThreeEvent } from "@react-three/fiber";
import {
  Float,
  Html,
  PerformanceMonitor,
  Sparkles,
  Stars,
} from "@react-three/drei";
import { Bloom, EffectComposer, Noise, Vignette } from "@react-three/postprocessing";
import * as THREE from "three";
import { discoveries, frequencyById, regions, type Region } from "@/data/world";
import { useWorldStore } from "@/store/world-store";
import { ThirdPersonController } from "./third-person-controller";

function RegionIsland({ region, index }: { region: Region; index: number }) {
  const activeFrequency = useWorldStore((state) => state.activeFrequency);
  const frequency = frequencyById.get(activeFrequency)!;
  const [hovered, setHovered] = useState(false);
  const rotation = useMemo(() => (index * 1.71) % Math.PI, [index]);

  return (
    <group position={region.position}>
      <mesh
        receiveShadow
        castShadow
        scale={[region.scale, 0.65, region.scale]}
        rotation={[0, rotation, 0]}
        onPointerEnter={() => setHovered(true)}
        onPointerLeave={() => setHovered(false)}
      >
        <cylinderGeometry args={[4.6, 3.5, 1.4, 9, 3]} />
        <meshStandardMaterial
          color={hovered ? frequency.accent : region.color}
          roughness={0.76}
          metalness={activeFrequency === "F610" ? 0.72 : 0.12}
          emissive={frequency.color}
          emissiveIntensity={frequency.intensity * 0.13}
          wireframe={activeFrequency === "F960"}
        />
      </mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.48, 0]} receiveShadow>
        <circleGeometry args={[4.15 * region.scale, 48]} />
        <meshStandardMaterial
          color={region.color}
          roughness={0.88}
          transparent
          opacity={activeFrequency === "F500" ? 0.3 : 0.98}
        />
      </mesh>
      <Landmark region={region} frequencyColor={frequency.color} />
      <Html position={[0, 3.2, 0]} center distanceFactor={15}>
        <div className={`world-label ${hovered ? "is-hovered" : ""}`}>
          <span>{region.name}</span>
          <small>{region.landmark}</small>
        </div>
      </Html>
    </group>
  );
}

function Landmark({ region, frequencyColor }: { region: Region; frequencyColor: string }) {
  if (region.id === "velorian-basin") {
    return <VeloriaCity frequencyColor={frequencyColor} />;
  }

  if (region.id === "aelwyn-canopy") {
    return (
      <group position={[0, 0.5, 0]}>
        {Array.from({ length: 7 }, (_, index) => (
          <mesh
            key={index}
            castShadow
            position={[
              Math.cos((index / 7) * Math.PI * 2) * 1.7,
              0.7 + (index % 3) * 0.18,
              Math.sin((index / 7) * Math.PI * 2) * 1.7,
            ]}
          >
            <coneGeometry args={[0.65, 2.2, 7]} />
            <meshStandardMaterial color="#3d7254" emissive={frequencyColor} emissiveIntensity={0.08} />
          </mesh>
        ))}
      </group>
    );
  }

  if (region.id === "glasswater-fields") {
    return (
      <group position={[0, 0.55, 0]}>
        {[-1.8, -0.6, 0.8, 2].map((x, index) => (
          <mesh key={x} position={[x, 0.1 + index * 0.08, (index % 2) * 1.2 - 0.5]}>
            <cylinderGeometry args={[0.65, 0.85, 0.12, 32]} />
            <meshPhysicalMaterial color="#79b9c8" transmission={0.5} roughness={0.12} />
          </mesh>
        ))}
      </group>
    );
  }

  if (region.id === "lumira-sands") {
    return <LumiraSands frequencyColor={frequencyColor} />;
  }

  if (region.id === "driftfall") {
    return <DriftfallCoast frequencyColor={frequencyColor} />;
  }

  return (
    <Float speed={1.1} rotationIntensity={0.14} floatIntensity={0.28}>
      <mesh castShadow position={[0, 1.45, 0]}>
        <octahedronGeometry args={[1.05, 0]} />
        <meshStandardMaterial
          color={region.color}
          emissive={frequencyColor}
          emissiveIntensity={0.4}
          roughness={0.35}
          metalness={0.45}
        />
      </mesh>
    </Float>
  );
}

function LumiraSands({ frequencyColor }: { frequencyColor: string }) {
  return (
    <group position={[0, 0.5, 0]}>
      {[
        [-1.8, 0, -0.8, 1.2],
        [0.7, 0.05, -1.5, 1.5],
        [1.8, 0.02, 1.1, 1.05],
        [-0.9, 0.03, 1.5, 1.35],
      ].map(([x, y, z, scale], index) => (
        <mesh
          key={index}
          position={[x, y, z]}
          scale={[scale, 0.32, scale * 0.72]}
          rotation={[0, index * 0.55, 0]}
        >
          <sphereGeometry args={[1, 18, 8, 0, Math.PI * 2, 0, Math.PI / 2]} />
          <meshStandardMaterial
            color={index % 2 === 0 ? "#b98655" : "#c99b65"}
            emissive={frequencyColor}
            emissiveIntensity={0.04}
            roughness={0.95}
          />
        </mesh>
      ))}
      <group position={[0, 0.85, 0.2]}>
        <mesh position={[-0.72, 0.45, 0]}>
          <boxGeometry args={[0.28, 1.8, 0.34]} />
          <meshStandardMaterial color="#76523d" roughness={0.8} />
        </mesh>
        <mesh position={[0.72, 0.45, 0]}>
          <boxGeometry args={[0.28, 1.8, 0.34]} />
          <meshStandardMaterial color="#76523d" roughness={0.8} />
        </mesh>
        <mesh position={[0, 1.28, 0]}>
          <boxGeometry args={[1.7, 0.24, 0.36]} />
          <meshStandardMaterial color="#8b6348" roughness={0.76} />
        </mesh>
        <pointLight position={[0, 0.8, 0.4]} color="#e8a772" intensity={0.9} distance={3} />
      </group>
    </group>
  );
}

function DriftfallCoast({ frequencyColor }: { frequencyColor: string }) {
  const falls = useRef<THREE.Group>(null);

  useFrame(({ clock }) => {
    if (!falls.current) return;
    falls.current.children.forEach((child, index) => {
      child.scale.y = 0.84 + Math.sin(clock.elapsedTime * 0.7 + index) * 0.12;
      child.position.y = 1.7 + Math.sin(clock.elapsedTime * 0.45 + index * 0.8) * 0.2;
    });
  });

  return (
    <group position={[0, 0.5, 0]}>
      <group ref={falls}>
        {[-1.5, -0.45, 0.65, 1.55].map((x, index) => (
          <mesh key={x} position={[x, 1.7, -0.4 + (index % 2) * 0.8]}>
            <cylinderGeometry args={[0.06, 0.28, 3.2 + index * 0.3, 12, 1, true]} />
            <meshBasicMaterial
              color={index % 2 === 0 ? "#8dc7db" : "#b5ddea"}
              transparent
              opacity={0.28}
              side={THREE.DoubleSide}
            />
          </mesh>
        ))}
      </group>
      {[-1.8, -0.6, 0.8, 1.9].map((x, index) => (
        <mesh
          key={x}
          castShadow
          position={[x, 0.2, -1 + (index % 3)]}
          rotation={[index * 0.25, index * 0.6, index * 0.12]}
        >
          <tetrahedronGeometry args={[0.72 + (index % 2) * 0.25, 0]} />
          <meshStandardMaterial
            color="#56677a"
            emissive={frequencyColor}
            emissiveIntensity={0.07}
            roughness={0.82}
          />
        </mesh>
      ))}
      <pointLight position={[0, 2.8, 0]} color="#8dc7db" intensity={1.1} distance={5} />
    </group>
  );
}

function VeloriaCity({ frequencyColor }: { frequencyColor: string }) {
  const buildings = useMemo(
    () =>
      [
        { radius: 3.45, count: 18, height: 0.55, color: "#88755f" },
        { radius: 2.65, count: 15, height: 0.82, color: "#8b9894" },
        { radius: 1.82, count: 12, height: 1.15, color: "#617981" },
      ].flatMap((ring, ringIndex) =>
        Array.from({ length: ring.count }, (_, index) => {
          const angle = (index / ring.count) * Math.PI * 2 + ringIndex * 0.19;
          return {
            key: `${ringIndex}-${index}`,
            position: [
              Math.cos(angle) * ring.radius,
              ring.height / 2 + 0.52,
              Math.sin(angle) * ring.radius,
            ] as [number, number, number],
            rotation: [0, -angle, 0] as [number, number, number],
            height: ring.height + ((index * 7) % 4) * 0.09,
            color: ring.color,
            width: ringIndex === 0 ? 0.36 : 0.28,
          };
        }),
      ),
    [],
  );

  return (
    <group position={[0, 0.5, 0]}>
      {[3.8, 3.02, 2.23, 1.38].map((radius, index) => (
        <mesh key={radius} rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.05 + index * 0.02, 0]}>
          <ringGeometry args={[radius - 0.045, radius, 96]} />
          <meshBasicMaterial
            color={index === 3 ? frequencyColor : "#b49769"}
            transparent
            opacity={0.36 + index * 0.08}
          />
        </mesh>
      ))}

      {buildings.map((building) => (
        <mesh
          key={building.key}
          castShadow
          position={building.position}
          rotation={building.rotation}
        >
          <boxGeometry args={[building.width, building.height, building.width * 1.35]} />
          <meshStandardMaterial
            color={building.color}
            emissive={frequencyColor}
            emissiveIntensity={0.05}
            roughness={0.65}
            metalness={building.height > 1 ? 0.5 : 0.12}
          />
        </mesh>
      ))}

      <group position={[0, 1.15, 0]}>
        <mesh castShadow>
          <cylinderGeometry args={[0.72, 1.05, 2.3, 8]} />
          <meshStandardMaterial
            color="#273e42"
            emissive={frequencyColor}
            emissiveIntensity={0.8}
            metalness={0.86}
            roughness={0.2}
          />
        </mesh>
        <mesh position={[0, 1.28, 0]}>
          <octahedronGeometry args={[0.42, 0]} />
          <meshStandardMaterial color="#d7fff0" emissive={frequencyColor} emissiveIntensity={2.4} />
        </mesh>
        <pointLight color={frequencyColor} intensity={2.6} distance={7} />
      </group>

      <DebGate />
    </group>
  );
}

function DebGate() {
  return (
    <group position={[0, 0.72, 4.05]}>
      <mesh castShadow position={[-0.92, 0.2, 0]}>
        <boxGeometry args={[0.72, 1.85, 0.42]} />
        <meshStandardMaterial color="#b49a70" roughness={0.72} />
      </mesh>
      <mesh castShadow position={[0.92, 0.2, 0]}>
        <boxGeometry args={[0.72, 1.85, 0.42]} />
        <meshStandardMaterial color="#b49a70" roughness={0.72} />
      </mesh>
      <mesh castShadow position={[0, 1.12, 0]}>
        <boxGeometry args={[2.56, 0.34, 0.52]} />
        <meshStandardMaterial color="#c2a87a" roughness={0.66} />
      </mesh>
      {[-0.38, 0.38].map((x) => (
        <mesh key={x} castShadow position={[x, 0.12, 0.03]}>
          <boxGeometry args={[0.68, 1.55, 0.19]} />
          <meshStandardMaterial
            color="#443427"
            emissive="#c99e58"
            emissiveIntensity={0.16}
            metalness={0.28}
            roughness={0.58}
          />
        </mesh>
      ))}
      <mesh position={[0, 1.34, 0.08]}>
        <torusGeometry args={[0.34, 0.035, 8, 28, Math.PI]} />
        <meshBasicMaterial color="#e3c479" />
      </mesh>
      <pointLight position={[0, 0.35, 0.6]} color="#ffd789" intensity={1.5} distance={3} />
      <Html position={[0, 1.75, 0]} center distanceFactor={12}>
        <div className="gate-plaque">DEB GATE <small>Look up before you look in</small></div>
      </Html>
    </group>
  );
}

function SkyDrifters() {
  const group = useRef<THREE.Group>(null);
  const drifters = useMemo(
    () =>
      Array.from({ length: 11 }, (_, index) => ({
        position: [
          Math.cos(index * 2.17) * (5 + (index % 4) * 2.2),
          9 + (index % 5) * 1.1,
          Math.sin(index * 1.63) * (6 + (index % 3) * 2.5),
        ] as [number, number, number],
        scale: 0.7 + (index % 3) * 0.18,
        phase: index * 0.72,
      })),
    [],
  );

  useFrame(({ clock }) => {
    if (!group.current) return;
    group.current.rotation.y = clock.elapsedTime * 0.008;
    group.current.children.forEach((child, index) => {
      child.position.y =
        drifters[index].position[1] + Math.sin(clock.elapsedTime * 0.22 + drifters[index].phase) * 0.45;
    });
  });

  return (
    <group ref={group}>
      {drifters.map((drifter, index) => (
        <group key={index} position={drifter.position} scale={drifter.scale}>
          <mesh>
            <capsuleGeometry args={[0.16, 0.7, 4, 8]} />
            <meshBasicMaterial color="#d9eee8" transparent opacity={0.36} depthWrite={false} />
          </mesh>
          <mesh position={[0, 0.62, 0]}>
            <sphereGeometry args={[0.22, 10, 10]} />
            <meshBasicMaterial color="#edf9f5" transparent opacity={0.3} depthWrite={false} />
          </mesh>
        </group>
      ))}
    </group>
  );
}

function LivingInhabitants() {
  const lineborn = useRef<THREE.Group>(null);
  const choirglass = useRef<THREE.Group>(null);
  const selectDiscovery = useWorldStore((state) => state.selectDiscovery);
  const byId = useMemo(
    () => new Map(discoveries.map((discovery) => [discovery.id, discovery])),
    [],
  );

  useFrame(({ clock }) => {
    if (lineborn.current) {
      lineborn.current.rotation.y = Math.sin(clock.elapsedTime * 0.32) * 1.18;
    }
    if (choirglass.current) {
      choirglass.current.rotation.y = clock.elapsedTime * 0.16;
      const pulse = 1 + Math.sin(clock.elapsedTime * 1.4) * 0.035;
      choirglass.current.scale.setScalar(pulse);
    }
  });

  return (
    <group>
      <group
        ref={lineborn}
        position={[1.35, 1.08, 2.55]}
        onClick={(event) => {
          event.stopPropagation();
          selectDiscovery(byId.get("lineborn-citizen") ?? null);
        }}
      >
        <mesh>
          <planeGeometry args={[0.48, 1.28]} />
          <meshBasicMaterial color="#ede4d1" side={THREE.DoubleSide} />
        </mesh>
        <mesh position={[0, 0.12, 0.006]}>
          <planeGeometry args={[0.33, 0.72]} />
          <meshBasicMaterial color="#222a27" side={THREE.DoubleSide} />
        </mesh>
        <mesh position={[0, 0.78, 0]}>
          <circleGeometry args={[0.2, 16]} />
          <meshBasicMaterial color="#ede4d1" side={THREE.DoubleSide} />
        </mesh>
      </group>

      <group
        ref={choirglass}
        position={[13.6, 1.24, -11.7]}
        onClick={(event) => {
          event.stopPropagation();
          selectDiscovery(byId.get("choirglass") ?? null);
        }}
      >
        <mesh>
          <octahedronGeometry args={[0.48, 1]} />
          <meshPhysicalMaterial
            color="#9eeaf1"
            emissive="#58cbd8"
            emissiveIntensity={0.5}
            transmission={0.48}
            roughness={0.08}
            metalness={0.12}
          />
        </mesh>
        <mesh position={[0, 0.72, 0]}>
          <icosahedronGeometry args={[0.28, 0]} />
          <meshPhysicalMaterial color="#d6fbff" transmission={0.6} roughness={0.06} />
        </mesh>
        <pointLight color="#75e8f3" intensity={1.4} distance={3} />
      </group>

      <group
        position={[-13.3, 1.08, 12.3]}
        onClick={(event) => {
          event.stopPropagation();
          selectDiscovery(byId.get("kharad-waykeeper") ?? null);
        }}
      >
        <mesh castShadow>
          <dodecahedronGeometry args={[0.56, 0]} />
          <meshStandardMaterial color="#6e5043" roughness={0.88} metalness={0.18} />
        </mesh>
        <mesh castShadow position={[0, 0.73, 0]}>
          <dodecahedronGeometry args={[0.3, 0]} />
          <meshStandardMaterial color="#8a6653" roughness={0.8} metalness={0.22} />
        </mesh>
      </group>

      <PalewindPerson
        position={[-3.1, 1.35, 2.4]}
        onSelect={() => selectDiscovery(byId.get("palewind-traveler") ?? null)}
      />
    </group>
  );
}

function PalewindPerson({
  position,
  onSelect,
}: {
  position: [number, number, number];
  onSelect: () => void;
}) {
  const mesh = useRef<THREE.InstancedMesh>(null);
  const dummy = useMemo(() => new THREE.Object3D(), []);
  const motes = useMemo(
    () =>
      Array.from({ length: 42 }, (_, index) => ({
        radius: 0.12 + ((index * 17) % 100) / 150,
        height: ((index * 29) % 100) / 65 - 0.55,
        speed: 0.22 + (index % 7) * 0.028,
        phase: index * 1.71,
      })),
    [],
  );

  useFrame(({ clock }) => {
    if (!mesh.current) return;
    motes.forEach((mote, index) => {
      const angle = mote.phase + clock.elapsedTime * mote.speed;
      const taper = 1 - Math.abs(mote.height) * 0.3;
      dummy.position.set(
        Math.cos(angle) * mote.radius * taper,
        mote.height + Math.sin(angle * 1.7) * 0.07,
        Math.sin(angle) * mote.radius * taper,
      );
      const scale = 0.025 + (index % 4) * 0.007;
      dummy.scale.setScalar(scale);
      dummy.updateMatrix();
      mesh.current!.setMatrixAt(index, dummy.matrix);
    });
    mesh.current.instanceMatrix.needsUpdate = true;
  });

  return (
    <group position={position}>
      <instancedMesh ref={mesh} args={[undefined, undefined, motes.length]} onClick={onSelect}>
        <sphereGeometry args={[1, 6, 6]} />
        <meshBasicMaterial color="#d8f1e7" transparent opacity={0.68} />
      </instancedMesh>
      <pointLight color="#d8f1e7" intensity={0.65} distance={2.4} />
    </group>
  );
}

function SketchyGalleryInstallation() {
  const panels = useRef<THREE.Group>(null);
  const selectDiscovery = useWorldStore((state) => state.selectDiscovery);
  const byId = useMemo(
    () => new Map(discoveries.map((discovery) => [discovery.id, discovery])),
    [],
  );

  useFrame(({ clock }) => {
    if (!panels.current) return;
    panels.current.children.forEach((panel, index) => {
      panel.position.y = 1.2 + Math.sin(clock.elapsedTime * 0.55 + index * 1.8) * 0.16;
      panel.position.z = -1.25 + index * 1.25 + Math.sin(clock.elapsedTime * 0.28 + index) * 0.14;
    });
  });

  const openEntry = (id: string) => (event: ThreeEvent<MouseEvent>) => {
    event.stopPropagation();
    selectDiscovery(byId.get(id) ?? null);
  };

  return (
    <group position={[-2.15, 0.45, 0]}>
      <group ref={panels}>
        <group position={[0, 1.2, -1.25]} onClick={openEntry("emergence-artwork")}>
          <mesh rotation={[0, Math.PI / 2, 0]}>
            <boxGeometry args={[1.15, 0.78, 0.06]} />
            <meshStandardMaterial color="#090d13" emissive="#172735" emissiveIntensity={0.5} />
          </mesh>
          {[-0.26, 0, 0.28].map((y, index) => (
            <mesh
              key={y}
              position={[-0.035, y, -0.22 + index * 0.22]}
              rotation={[0, Math.PI / 2, 0]}
            >
              <capsuleGeometry args={[0.035, 0.16, 3, 6]} />
              <meshBasicMaterial color="#dfebe8" />
            </mesh>
          ))}
        </group>

        <group position={[0, 1.2, 0]} onClick={openEntry("green-garden-artwork")}>
          <mesh rotation={[0, Math.PI / 2, 0]}>
            <boxGeometry args={[1.15, 0.78, 0.06]} />
            <meshStandardMaterial color="#173b28" emissive="#2d7a47" emissiveIntensity={0.4} />
          </mesh>
          {Array.from({ length: 12 }, (_, index) => (
            <mesh
              key={index}
              position={[
                -0.04,
                -0.25 + Math.floor(index / 4) * 0.24,
                -0.36 + (index % 4) * 0.24,
              ]}
              rotation={[0, Math.PI / 2, 0]}
            >
              <circleGeometry args={[0.06, 7]} />
              <meshBasicMaterial color={index % 3 === 0 ? "#a2cf72" : "#5aa865"} />
            </mesh>
          ))}
        </group>

        <group position={[0, 1.2, 1.25]} onClick={openEntry("bronze-umbrella")}>
          <mesh rotation={[0, Math.PI / 2, 0]}>
            <boxGeometry args={[1.15, 0.78, 0.06]} />
            <meshStandardMaterial color="#39261c" emissive="#785032" emissiveIntensity={0.35} />
          </mesh>
          <mesh position={[-0.05, -0.08, 0]} rotation={[0, 0, Math.PI / 2]}>
            <coneGeometry args={[0.3, 0.12, 18, 1, true]} />
            <meshBasicMaterial color="#b47a47" side={THREE.DoubleSide} />
          </mesh>
          <mesh position={[-0.04, -0.24, 0]}>
            <sphereGeometry args={[0.11, 10, 10]} />
            <meshBasicMaterial color="#9a673e" />
          </mesh>
        </group>
      </group>

      <mesh position={[-0.25, 0.74, 2.1]} rotation={[0, Math.PI / 2, 0]}>
        <boxGeometry args={[0.72, 1.35, 0.12]} />
        <meshStandardMaterial color="#1557a3" emissive="#0c3b74" emissiveIntensity={0.4} />
      </mesh>
      <Html position={[-0.35, 2.25, 0]} center distanceFactor={11}>
        <div className="gate-plaque">
          THE SKETCHY GALLERY <small>Moving exhibition // third ring</small>
        </div>
      </Html>
    </group>
  );
}

function DiscoveryMarkers() {
  const selectDiscovery = useWorldStore((state) => state.selectDiscovery);
  const markerGroup = useRef<THREE.Group>(null);

  useFrame(({ clock }) => {
    if (!markerGroup.current) return;
    markerGroup.current.children.forEach((marker, index) => {
      marker.position.y =
        discoveries[index].position[1] + Math.sin(clock.elapsedTime * 1.5 + index * 0.72) * 0.12;
      marker.rotation.y = clock.elapsedTime * 0.32 + index;
    });
  });

  return (
    <group ref={markerGroup}>
      {discoveries.map((discovery) => (
        <group key={discovery.id} position={discovery.position}>
          <mesh
            onClick={(event) => {
              event.stopPropagation();
              selectDiscovery(discovery);
            }}
            onPointerEnter={() => {
              document.body.style.cursor = "pointer";
            }}
            onPointerLeave={() => {
              document.body.style.cursor = "default";
            }}
          >
            <icosahedronGeometry args={[0.28, 1]} />
            <meshStandardMaterial
              color={discovery.color}
              emissive={discovery.color}
              emissiveIntensity={1.8}
            />
          </mesh>
          <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.32, 0]}>
            <ringGeometry args={[0.42, 0.48, 24]} />
            <meshBasicMaterial color={discovery.color} transparent opacity={0.6} />
          </mesh>
        </group>
      ))}
    </group>
  );
}

function ResonanceRings() {
  const activeFrequency = useWorldStore((state) => state.activeFrequency);
  const color = frequencyById.get(activeFrequency)!.color;
  return (
    <group>
      {[9, 17, 25].map((radius, index) => (
        <mesh key={radius} rotation={[-Math.PI / 2, 0, index * 0.2]} position={[0, -0.1, 0]}>
          <ringGeometry args={[radius, radius + 0.035, 128]} />
          <meshBasicMaterial color={color} transparent opacity={0.18 - index * 0.035} />
        </mesh>
      ))}
    </group>
  );
}

function RoadNetwork() {
  const activeFrequency = useWorldStore((state) => state.activeFrequency);
  const frequencyColor = frequencyById.get(activeFrequency)!.color;
  const routes = useMemo(
    () =>
      regions.slice(1).map((region) => {
        const destination = new THREE.Vector3(...region.position);
        const direction = destination.clone().setY(0).normalize();
        const start = direction.clone().multiplyScalar(4.35);
        const end = destination.clone().sub(direction.clone().multiplyScalar(4.2));
        const midpoint = start.clone().add(end).multiplyScalar(0.5);
        const length = start.distanceTo(end);
        return {
          region,
          start,
          end,
          midpoint,
          length,
          angle: Math.atan2(end.x - start.x, end.z - start.z),
        };
      }),
    [],
  );

  return (
    <group>
      {routes.map((route) => (
        <group key={route.region.id}>
          <mesh
            receiveShadow
            position={[route.midpoint.x, 0.34, route.midpoint.z]}
            rotation={[0, route.angle, 0]}
          >
            <boxGeometry args={[0.82, 0.11, route.length]} />
            <meshStandardMaterial
              color="#5f6159"
              emissive={frequencyColor}
              emissiveIntensity={0.04}
              roughness={0.92}
            />
          </mesh>
          {[-0.47, 0.47].map((side) => (
            <mesh
              key={side}
              position={[
                route.midpoint.x + Math.cos(route.angle) * side,
                0.46,
                route.midpoint.z - Math.sin(route.angle) * side,
              ]}
              rotation={[0, route.angle, 0]}
            >
              <boxGeometry args={[0.035, 0.18, route.length]} />
              <meshBasicMaterial color={route.region.color} transparent opacity={0.42} />
            </mesh>
          ))}
          {Array.from({ length: 7 }, (_, index) => {
            const progress = (index + 1) / 8;
            const point = route.start.clone().lerp(route.end, progress);
            return (
              <group key={index} position={[point.x, 0.62, point.z]}>
                <mesh>
                  <sphereGeometry args={[0.055, 8, 8]} />
                  <meshBasicMaterial color={route.region.color} />
                </mesh>
              </group>
            );
          })}
        </group>
      ))}
    </group>
  );
}

function FrequencyPhenomena() {
  const activeFrequency = useWorldStore((state) => state.activeFrequency);
  const group = useRef<THREE.Group>(null);

  useFrame(({ clock }, delta) => {
    if (!group.current) return;
    group.current.rotation.y += delta * (activeFrequency === "F120" ? 0.1 : 0.025);
    const pulse = 1 + Math.sin(clock.elapsedTime * 0.8) * 0.045;
    group.current.scale.setScalar(activeFrequency === "F380" ? pulse : 1);
  });

  if (activeFrequency === "F432") return null;

  if (activeFrequency === "F120") {
    return (
      <group ref={group} position={[0, 1.1, 0]}>
        {[5.2, 7.4, 10.1].map((radius, index) => (
          <mesh
            key={radius}
            rotation={[Math.PI / 2, index * 0.23, index * 0.16]}
            position={[index * 0.28, index * 0.12, -index * 0.2]}
          >
            <torusGeometry args={[radius, 0.035, 8, 96, Math.PI * 1.72]} />
            <meshBasicMaterial color="#a8c7ff" transparent opacity={0.24 - index * 0.045} />
          </mesh>
        ))}
      </group>
    );
  }

  if (activeFrequency === "F200") {
    return (
      <group ref={group}>
        {Array.from({ length: 14 }, (_, index) => {
          const angle = (index / 14) * Math.PI * 2;
          const radius = 7 + (index % 3) * 3.2;
          return (
            <mesh
              key={index}
              position={[Math.cos(angle) * radius, 4.5 + (index % 4), Math.sin(angle) * radius]}
            >
              <cylinderGeometry args={[0.018, 0.055, 9 + (index % 4) * 2, 6]} />
              <meshBasicMaterial color="#ffe29a" transparent opacity={0.34} />
            </mesh>
          );
        })}
      </group>
    );
  }

  if (activeFrequency === "F380") {
    return (
      <group ref={group} position={[0, 0.22, 0]}>
        {["#ff7fa6", "#8f7cff", "#ffc36f", "#72d7c2"].map((color, index) => (
          <mesh key={color} rotation={[-Math.PI / 2, 0, index * 0.4]}>
            <ringGeometry args={[5 + index * 3.7, 5.08 + index * 3.7, 96]} />
            <meshBasicMaterial color={color} transparent opacity={0.24} />
          </mesh>
        ))}
      </group>
    );
  }

  if (activeFrequency === "F500") {
    return (
      <group ref={group}>
        <mesh position={[8, 3.4, -8]}>
          <sphereGeometry args={[3.2, 32, 32]} />
          <meshBasicMaterial color="#000000" />
        </mesh>
        {[3.5, 4.2, 5.1].map((radius, index) => (
          <mesh key={radius} position={[8, 3.4, -8]} rotation={[index * 0.6, 0.2, 0]}>
            <torusGeometry args={[radius, 0.025, 6, 72]} />
            <meshBasicMaterial color="#574a7e" transparent opacity={0.2 - index * 0.04} />
          </mesh>
        ))}
      </group>
    );
  }

  if (activeFrequency === "F610") {
    return (
      <group ref={group}>
        {Array.from({ length: 8 }, (_, index) => {
          const angle = (index / 8) * Math.PI * 2;
          return (
            <mesh
              key={index}
              position={[Math.cos(angle) * 8.5, 2.3 + (index % 3), Math.sin(angle) * 8.5]}
              rotation={[0, -angle, (index % 2) * 0.18]}
            >
              <planeGeometry args={[2.8, 4.8, 5, 8]} />
              <meshBasicMaterial
                color="#8cecf4"
                wireframe
                transparent
                opacity={0.18}
                side={THREE.DoubleSide}
              />
            </mesh>
          );
        })}
      </group>
    );
  }

  if (activeFrequency === "F840") {
    return (
      <group ref={group} position={[0, 1, 0]}>
        <Sparkles count={120} scale={[30, 8, 30]} size={2.2} speed={0.12} color="#e57b4d" />
        {[6, 12, 18].map((radius) => (
          <mesh key={radius} rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.58, 0]}>
            <ringGeometry args={[radius, radius + 0.025, 96]} />
            <meshBasicMaterial color="#b74f32" transparent opacity={0.26} />
          </mesh>
        ))}
      </group>
    );
  }

  return (
    <group ref={group}>
      {Array.from({ length: 12 }, (_, index) => {
        const angle = (index / 12) * Math.PI * 2;
        const radius = 6 + (index % 4) * 3.4;
        return (
          <mesh
            key={index}
            position={[Math.cos(angle) * radius, 1.8 + (index % 3), Math.sin(angle) * radius]}
            rotation={[0.1 * index, -angle, 0.07 * index]}
          >
            <boxGeometry args={[1.2 + (index % 3), 2.4 + (index % 4), 1]} />
            <meshBasicMaterial color="#d7d1c5" wireframe transparent opacity={0.2} />
          </mesh>
        );
      })}
    </group>
  );
}

function Atmosphere({ reducedEffects }: { reducedEffects: boolean }) {
  const activeFrequency = useWorldStore((state) => state.activeFrequency);
  const frequency = frequencyById.get(activeFrequency)!;
  const { scene } = useThree();

  useEffect(() => {
    scene.background = new THREE.Color(frequency.sky);
    scene.fog = new THREE.FogExp2(frequency.fog, activeFrequency === "F500" ? 0.065 : 0.025);
  }, [activeFrequency, frequency, scene]);

  return (
    <>
      <ambientLight intensity={0.25 + frequency.intensity * 0.35} color={frequency.accent} />
      <GildingSun color={frequency.color} intensity={0.8 + frequency.intensity} />
      <hemisphereLight args={[frequency.accent, frequency.fog, 0.45]} />
      <Stars radius={80} depth={45} count={activeFrequency === "F500" ? 600 : 1800} factor={3} fade />
      <Sparkles
        count={reducedEffects ? 35 : activeFrequency === "F200" ? 230 : 90}
        scale={45}
        size={1.7}
        speed={activeFrequency === "F120" ? 0.8 : 0.25}
        color={frequency.color}
        opacity={activeFrequency === "F500" ? 0.2 : 0.65}
      />
    </>
  );
}

function GildingSun({ color, intensity }: { color: string; intensity: number }) {
  const light = useRef<THREE.DirectionalLight>(null);

  useFrame(({ clock }) => {
    if (!light.current) return;
    const cycle = (Math.sin(clock.elapsedTime * 0.035) + 1) / 2;
    light.current.position.x = 5 + cycle * 7;
    light.current.position.y = 8 + cycle * 5;
    light.current.intensity = intensity + cycle * 0.55;
    light.current.color.lerpColors(
      new THREE.Color(color),
      new THREE.Color("#ffd28a"),
      cycle * 0.58,
    );
  });

  return (
    <directionalLight
        ref={light}
        castShadow
        position={[8, 13, 7]}
        intensity={intensity}
        color={color}
        shadow-mapSize={[1024, 1024]}
      />
  );
}

function WorldScene({ reducedEffects }: { reducedEffects: boolean }) {
  const activeFrequency = useWorldStore((state) => state.activeFrequency);
  const frequency = frequencyById.get(activeFrequency)!;

  return (
    <>
      <Atmosphere reducedEffects={reducedEffects} />
      <FrequencyPhenomena />
      <ResonanceRings />
      <RoadNetwork />
      {regions.map((region, index) => (
        <RegionIsland key={region.id} region={region} index={index} />
      ))}
      <SkyDrifters />
      <LivingInhabitants />
      <SketchyGalleryInstallation />
      <DiscoveryMarkers />
      <ThirdPersonController />
      {reducedEffects ? null : (
        <EffectComposer multisampling={0}>
          <Bloom luminanceThreshold={0.55} intensity={0.8 + frequency.intensity * 0.65} mipmapBlur />
          <Noise opacity={activeFrequency === "F960" ? 0.08 : 0.025} />
          <Vignette eskil={false} offset={0.16} darkness={0.72} />
        </EffectComposer>
      )}
    </>
  );
}

export function WorldCanvas() {
  const graphicsQuality = useWorldStore((state) => state.graphicsQuality);
  const [compactViewport, setCompactViewport] = useState(false);
  const [performanceDegraded, setPerformanceDegraded] = useState(false);

  useEffect(() => {
    const media = window.matchMedia("(max-width: 800px), (prefers-reduced-motion: reduce)");
    const update = () => setCompactViewport(media.matches);
    update();
    media.addEventListener("change", update);
    return () => media.removeEventListener("change", update);
  }, []);

  const reducedEffects =
    graphicsQuality === "low" ||
    (graphicsQuality === "auto" && (compactViewport || performanceDegraded));

  return (
    <Canvas
      shadows={!reducedEffects}
      dpr={reducedEffects ? 1 : [1, 1.6]}
      camera={{ position: [7, 6, 12], fov: 48, near: 0.1, far: 150 }}
      gl={{
        antialias: false,
        powerPreference: reducedEffects ? "low-power" : "high-performance",
      }}
    >
      <PerformanceMonitor
        onDecline={() => {
          if (graphicsQuality === "auto") setPerformanceDegraded(true);
        }}
      />
      <WorldScene reducedEffects={reducedEffects} />
    </Canvas>
  );
}
