"use client";

import dynamic from "next/dynamic";
import { useEffect, useState } from "react";
import {
  Archive,
  ChevronRight,
  Compass,
  Map,
  Radio,
  SlidersHorizontal,
  Sparkles,
  X,
} from "lucide-react";
import {
  discoveries,
  frequencies,
  frequencyLocations,
  regions,
  veloriaJourney,
} from "@/data/world";
import { useWorldStore } from "@/store/world-store";

const WorldCanvas = dynamic(
  () => import("./world-canvas").then((module) => module.WorldCanvas),
  {
    ssr: false,
    loading: () => (
      <div className="scene-loading">
        <span />
        <p>Tuning local resonance</p>
      </div>
    ),
  },
);

export function WorldExperience() {
  const hasEntered = useWorldStore((state) => state.hasEntered);
  const activePanel = useWorldStore((state) => state.activePanel);

  return (
    <main className="experience-shell">
      <div className="world-canvas">
        <WorldCanvas />
      </div>
      <div className="grain" aria-hidden="true" />
      {hasEntered ? <WorldHud /> : <EntryScreen />}
      {activePanel === "map" ? <MapPanel /> : null}
      {activePanel === "codex" ? <CodexPanel /> : null}
      {activePanel === "settings" ? <SettingsPanel /> : null}
      <DiscoveryPanel />
    </main>
  );
}

function EntryScreen() {
  const enterWorld = useWorldStore((state) => state.enterWorld);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const timer = window.setTimeout(() => setReady(true), 900);
    return () => window.clearTimeout(timer);
  }, []);

  return (
    <section className={`entry-screen ${ready ? "is-ready" : ""}`}>
      <div className="entry-orbit orbit-one" />
      <div className="entry-orbit orbit-two" />
      <div className="entry-copy">
        <div className="eyebrow"><span /> Dias // F432</div>
        <h1>
          Enter a world
          <em>between frequencies.</em>
        </h1>
        <p>
          Reality fractured, but did not end. Walk the resonant paths, listen to
          what survived, and recover the shape of the Prime Realm.
        </p>
        <button className="enter-button" onClick={enterWorld}>
          <span>Begin resonance</span>
          <ChevronRight size={18} />
        </button>
        <small>WASD to move · Hold Shift to run · Drag to look</small>
      </div>
      <div className="entry-index">
        <span>Known bands</span>
        <strong>08</strong>
        <i />
        <span>Present age</span>
      </div>
    </section>
  );
}

function WorldHud() {
  const activeFrequency = useWorldStore((state) => state.activeFrequency);
  const setFrequency = useWorldStore((state) => state.setFrequency);
  const setPanel = useWorldStore((state) => state.setPanel);
  const activePanel = useWorldStore((state) => state.activePanel);
  const discoveredCount = useWorldStore((state) => state.discoveredIds.length);
  const journeyStep = useWorldStore((state) => state.journeyStep);
  const currentRegionId = useWorldStore((state) => state.currentRegionId);
  const currentFrequencyLocationId = useWorldStore(
    (state) => state.currentFrequencyLocationId,
  );
  const visitedRegionIds = useWorldStore((state) => state.visitedRegionIds);
  const frequency = frequencies.find((item) => item.id === activeFrequency)!;
  const currentRegion = regions.find((region) => region.id === currentRegionId) ?? regions[0];
  const currentFrequencyLocation = frequencyLocations.find(
    (location) => location.id === currentFrequencyLocationId,
  );
  const journey = veloriaJourney[journeyStep];

  return (
    <div className="hud">
      <header className="topbar">
        <button className="dias-mark" onClick={() => setPanel(null)} aria-label="Close panels">
          <span className="mark-symbol">D</span>
          <span><b>DIAS</b><small>Resonance atlas</small></span>
        </button>
        <nav className="hud-nav">
          <button
            className={activePanel === "map" ? "active" : ""}
            onClick={() => setPanel("map")}
          >
            <Map size={16} /> World map
          </button>
          <button
            className={activePanel === "codex" ? "active" : ""}
            onClick={() => setPanel("codex")}
          >
            <Archive size={16} /> Codex <i>{discoveredCount}</i>
          </button>
          <button
            className={activePanel === "settings" ? "active" : ""}
            onClick={() => setPanel("settings")}
          >
            <SlidersHorizontal size={16} /> Settings
          </button>
        </nav>
      </header>

      <aside className="frequency-rail">
        <div className="rail-heading"><Radio size={14} /><span>Frequency</span></div>
        {frequencies.map((item) => (
          <button
            key={item.id}
            aria-label={`${item.id} ${item.name}`}
            className={item.id === activeFrequency ? "active" : ""}
            style={{ "--frequency-color": item.color } as React.CSSProperties}
            onClick={() => setFrequency(item.id)}
          >
            <i />
            <span>{item.id}</span>
            <small>{item.name}</small>
          </button>
        ))}
      </aside>

      {activeFrequency === "F432" ? (
        <aside className="journey-card">
          <div className="journey-heading">
            <span>First day in Veloria</span>
            <b>{String(journeyStep + 1).padStart(2, "0")} / 05</b>
          </div>
          <div className="journey-progress">
            {veloriaJourney.map((_, index) => (
              <i key={index} className={index <= journeyStep ? "reached" : ""} />
            ))}
          </div>
          <h3>{journey.title}</h3>
          <p>{journey.instruction}</p>
          <small>“{journey.reflection}”</small>
        </aside>
      ) : (
        <aside className="journey-card frequency-brief">
          <div className="journey-heading">
            <span>Frequency layer</span>
            <b>{frequency.id}</b>
          </div>
          <div className="journey-progress">
            {frequencies.map((item) => (
              <i key={item.id} className={item.id === activeFrequency ? "reached" : ""} />
            ))}
          </div>
          <h3>{currentFrequencyLocation?.name ?? frequency.epithet}</h3>
          <p>{frequency.description}</p>
          <small>Cross-frequency records remain partial until witnessed.</small>
        </aside>
      )}

      <div className="location-card">
        <span className="eyebrow">
          <Compass size={12} /> {frequency.id} {"//"}{" "}
          {currentFrequencyLocation
            ? `${currentFrequencyLocation.access} frequency route`
            : `${visitedRegionIds.length} of ${regions.length} regions`}
        </span>
        <h2>{currentFrequencyLocation?.name ?? currentRegion.name}</h2>
        <p>{currentFrequencyLocation?.description ?? currentRegion.summary}</p>
        <div className="signal">
          {Array.from({ length: 12 }, (_, index) => (
            <i key={index} style={{ height: `${7 + ((index * 7) % 18)}px` }} />
          ))}
          <span>{frequency.id}</span>
        </div>
      </div>

      <div className="controls-hint">
        <span><kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd> Move</span>
        <span><i className="mouse-icon" /> Drag to look</span>
        <span><Sparkles size={13} /> Select resonant lights</span>
      </div>
    </div>
  );
}

function MapPanel() {
  const setPanel = useWorldStore((state) => state.setPanel);
  const setFrequency = useWorldStore((state) => state.setFrequency);
  const activeFrequency = useWorldStore((state) => state.activeFrequency);
  const visitedRegionIds = useWorldStore((state) => state.visitedRegionIds);
  const requestTravel = useWorldStore((state) => state.requestTravel);
  const requestFrequencyTravel = useWorldStore(
    (state) => state.requestFrequencyTravel,
  );
  const selectedFrequency =
    frequencies.find((frequency) => frequency.id === activeFrequency) ?? frequencies[0];
  const selectedLocations = frequencyLocations.filter(
    (location) => location.frequency === activeFrequency,
  );

  return (
    <section className="overlay-panel map-panel">
      <PanelHeader
        eyebrow="Cartographic layer 01"
        title="The known shape of Dias"
        onClose={() => setPanel("map")}
      />
      <div className="map-content">
        <div className="map-visual">
          <div className="map-rings">
            {frequencies.map((frequency, index) => (
              <button
                key={frequency.id}
                className={frequency.id === activeFrequency ? "active" : ""}
                style={{
                  "--ring-color": frequency.color,
                  "--ring-size": `${24 + index * 8}%`,
                } as React.CSSProperties}
                onClick={() => setFrequency(frequency.id)}
                aria-label={`Tune to ${frequency.id}`}
              >
                <span>{frequency.id}</span>
              </button>
            ))}
            <div
              className="map-core"
              style={{ "--core-color": selectedFrequency.color } as React.CSSProperties}
            >
              <b>{selectedFrequency.id}</b>
              <small>{selectedFrequency.name}</small>
            </div>
          </div>
          <div className="map-current">
            <span>Selected layer</span>
            <strong>{selectedFrequency.epithet}</strong>
            <p>{selectedFrequency.description}</p>
          </div>
        </div>
        <div className="map-regions">
          <span className="section-label">Destinations // {activeFrequency}</span>
          {activeFrequency === "F432"
            ? regions.map((region, index) => (
                <article
                  key={region.id}
                  className={visitedRegionIds.includes(region.id) ? "visited" : ""}
                >
                  <i>{String(index + 1).padStart(2, "0")}</i>
                  <div>
                    <h3>{region.name}</h3>
                    <p>
                      {visitedRegionIds.includes(region.id)
                        ? region.summary
                        : "Uncharted. Follow its illuminated route to restore this region."}
                    </p>
                  </div>
                  <button
                    disabled={!visitedRegionIds.includes(region.id)}
                    onClick={() =>
                      requestTravel([
                        region.position[0],
                        0.35,
                        region.position[2] + (region.id === "velorian-basin" ? 5 : 3.5),
                      ])
                    }
                  >
                    {visitedRegionIds.includes(region.id) ? "Travel" : "Uncharted"}
                    <ChevronRight size={13} />
                  </button>
                </article>
              ))
            : selectedLocations.map((location, index) => (
                <article
                  key={location.id}
                  className={location.access === "unsafe" ? "unsafe" : "visited"}
                >
                  <i>{String(index + 1).padStart(2, "0")}</i>
                  <div>
                    <h3>
                      {location.name}
                      <span className={`access-badge ${location.access}`}>{location.access}</span>
                    </h3>
                    <p>{location.description}</p>
                  </div>
                  <button
                    disabled={location.access === "unsafe"}
                    onClick={() =>
                      requestFrequencyTravel(
                        location.frequency,
                        location.id,
                        location.arrival,
                      )
                    }
                  >
                    {location.access === "unsafe" ? "Sealed" : "Traverse"}
                    <ChevronRight size={13} />
                  </button>
                </article>
              ))}
        </div>
      </div>
    </section>
  );
}

function CodexPanel() {
  const setPanel = useWorldStore((state) => state.setPanel);
  const discoveredIds = useWorldStore((state) => state.discoveredIds);
  const selectDiscovery = useWorldStore((state) => state.selectDiscovery);

  return (
    <section className="overlay-panel codex-panel">
      <PanelHeader
        eyebrow="Personal archive"
        title="Recovered knowledge"
        onClose={() => setPanel("codex")}
      />
      <div className="codex-stats">
        <strong>{discoveredIds.length}</strong>
        <span>of {discoveries.length} nearby echoes recovered</span>
        <i><b style={{ width: `${(discoveredIds.length / discoveries.length) * 100}%` }} /></i>
      </div>
      <div className="codex-grid">
        {discoveries.map((discovery) => {
          const unlocked = discoveredIds.includes(discovery.id);
          return (
            <button
              key={discovery.id}
              className={unlocked ? "unlocked" : "locked"}
              onClick={() => unlocked && selectDiscovery(discovery)}
            >
              <span>{discovery.type}</span>
              <h3>{unlocked ? discovery.name : "Unresolved echo"}</h3>
              <p>{unlocked ? discovery.excerpt : "Find its light in the world to restore this entry."}</p>
              <i style={{ background: unlocked ? discovery.color : undefined }} />
            </button>
          );
        })}
      </div>
    </section>
  );
}

function SettingsPanel() {
  const setPanel = useWorldStore((state) => state.setPanel);
  const graphicsQuality = useWorldStore((state) => state.graphicsQuality);
  const setGraphicsQuality = useWorldStore((state) => state.setGraphicsQuality);

  return (
    <section className="overlay-panel settings-panel">
      <PanelHeader
        eyebrow="Experience controls"
        title="Tune your passage"
        onClose={() => setPanel("settings")}
      />
      <div className="settings-content">
        <section>
          <span className="section-label">Rendering profile</span>
          <h3>Visual fidelity</h3>
          <p>
            Automatic mode reduces post-processing and pixel density on smaller
            devices or when reduced motion is requested.
          </p>
          <div className="segmented-control">
            {(["auto", "high", "low"] as const).map((quality) => (
              <button
                key={quality}
                className={graphicsQuality === quality ? "active" : ""}
                onClick={() => setGraphicsQuality(quality)}
              >
                {quality}
              </button>
            ))}
          </div>
        </section>
        <section>
          <span className="section-label">Controls</span>
          <h3>World navigation</h3>
          <div className="controls-reference">
            <span><kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd><i>Move through Dias</i></span>
            <span><kbd>Shift</kbd><i>Run</i></span>
            <span><i className="mouse-icon" /><i>Rotate the follow camera</i></span>
            <span><kbd>Esc</kbd><i>Release focus</i></span>
          </div>
        </section>
      </div>
    </section>
  );
}

function PanelHeader({
  eyebrow,
  title,
  onClose,
}: {
  eyebrow: string;
  title: string;
  onClose: () => void;
}) {
  return (
    <header className="panel-header">
      <div><span>{eyebrow}</span><h2>{title}</h2></div>
      <button onClick={onClose} aria-label="Close panel"><X size={19} /></button>
    </header>
  );
}

function DiscoveryPanel() {
  const discovery = useWorldStore((state) => state.selectedDiscovery);
  const selectDiscovery = useWorldStore((state) => state.selectDiscovery);
  if (!discovery) return null;

  return (
    <aside className="discovery-panel">
      <button onClick={() => selectDiscovery(null)} aria-label="Close discovery"><X size={18} /></button>
      <span className="eyebrow">
        <i style={{ background: discovery.color }} />
        {discovery.type} {"//"} {discovery.frequency}
      </span>
      <p className="discovery-kicker">New archive entry</p>
      <h2>{discovery.name}</h2>
      <h3>{discovery.excerpt}</h3>
      <p>{discovery.lore}</p>
      <footer><Compass size={14} /> {discovery.region}</footer>
    </aside>
  );
}
