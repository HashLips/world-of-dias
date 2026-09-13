# Dias Reference Map

## Purpose

The World of Dias uses a simple permanent reference system to connect things outside the repository back into the canonical Dias world.

These external things may include:

- artworks
- sculptures
- letters
- Arweave records
- blockchain transactions
- websites
- social posts
- audio
- video
- images
- NFC tags
- physical objects
- hidden Easter eggs
- archived material
- any other external reference

Every referenceable external element receives a globally unique Dias ID.

The format is:

`DIAS-{UUIDv4}`

Example:

`DIAS-3f7c8e18-1f22-4c37-bb61-4b640b918274`

The purpose of the Dias ID is simple:

**A Dias ID points back to one canonical Markdown file in the World of Dias repository.**

The Markdown file is the source of truth.

The reference map is only the bridge between the outside world and Dias.

---

## Core Rule

The system should remain deliberately simple:

**DIAS GUID -> Markdown file**

Each reference may optionally contain:

- a note
- an external link

That is all that is required.

Do not turn the reference map into a second lore database.

---

## Mapping File

Maintain one YAML mapping file in the repository.

Filename:

[`dias-map.yaml`](dias-map.yaml)

(`file` values inside the map are relative to the **repository root**, not this folder.)

Each entry uses this format:

```yaml
DIAS-3f7c8e18-1f22-4c37-bb61-4b640b918274:
  file: regions/wabet.md
  note: Artwork connected to Wabet and the forest.
  link: https://example.com
```

Only `file` is required.

`note` is optional.

`link` is optional.

---

## Field Definitions

### `file`

Required.

This must point to a canonical Markdown file in the World of Dias repository.

Example:

```yaml
file: regions/wabet.md
```

The linked Markdown file contains the actual lore, character, place, object, event, door, artwork context, or other canonical information.

The mapping file should not duplicate that information.

---

### `note`

Optional.

A note may contain any useful authoring context about why the Dias ID exists.

Examples:

```yaml
note: Artwork associated with Wabet.
```

```yaml
note: Secret Easter egg hidden somewhere inside a tree.
```

```yaml
note: Letter discovered in connection with this inhabitant.
```

```yaml
note: Physical sculpture containing an engraved Dias ID.
```

The note is primarily for the author and Dias agent.

It does not automatically need to be exposed publicly.

---

### `link`

Optional.

Use this field whenever there is an external location that should not be forgotten.

Examples include:

- Arweave
- blockchain explorers
- websites
- Reddit posts
- social posts
- audio
- video
- IPFS
- Git commits
- archives
- external documents

Example:

```yaml
link: https://arweave.net/...
```

The purpose of this field is archival.

If Dias places something somewhere outside the repository, the map should remember where it exists.

Omit `link` when the external thing should stay hard to discover. The ID still proves it exists.

---

## Example Entries

### Artwork

```yaml
DIAS-3f7c8e18-1f22-4c37-bb61-4b640b918274:
  file: regions/wabet.md
  note: Artwork connected to Wabet. Something unusual appears within a tree.
```

### Arweave Letter

```yaml
DIAS-d92bd5e1-57a8-4583-a8fd-8665fa43af70:
  file: inhabitants/oriven-tal.md
  note: Letter associated with Oriven Tal and stored permanently on Arweave.
  link: https://arweave.net/TRANSACTION_ID
```

### Audio

```yaml
DIAS-b3159d75-6304-47f2-a084-09d26cd68420:
  file: rules/everything-resonates-echo-principle.md
  note: Audio recording containing an unidentified resonance.
  link: https://example.com/audio
```

---

## What Can Receive a Dias ID?

Anything that needs to connect the external world back into Dias may receive a Dias ID.

Examples:

- physical artwork
- digital artwork
- sculpture
- hidden symbol
- letter
- document
- Arweave record
- blockchain transaction
- social-media message
- Reddit post
- website
- photograph
- image
- audio recording
- video
- NFC payload
- QR-linked artifact
- physical collectible
- book
- printed material
- exhibition item
- Easter egg
- puzzle element

Not every detail inside Dias needs a GUID.

Create a Dias ID only when the thing needs to be independently referenceable outside the normal Markdown lore structure.

---

## Agent Instructions

When the user asks to capture a new Dias reference, follow this process.

### 1. Check the ID

If the user provides a Dias ID, preserve it exactly.

Expected format:

`DIAS-{UUIDv4}`

If the user asks the agent to create one, generate a UUID v4 and prefix it with:

`DIAS-`

Never reuse an existing ID.

Never replace an existing ID.

---

### 2. Find the Canonical Markdown File

Determine which existing Markdown file in the Dias repository best represents the reference.

Examples:

- an artwork involving Wabet may point to the canonical Wabet Markdown file
- an object from a specific region may point to that region's Markdown file
- a letter written by an inhabitant may point to that inhabitant's Markdown file
- an audio artifact about resonance may point to the relevant resonance lore file

Do not create a new Markdown file merely because a new GUID has been added.

Create a new Markdown file only when the underlying Dias concept itself genuinely requires one.

---

### 3. Add the Mapping

Add the GUID to the YAML map.

Minimum entry:

```yaml
DIAS-{UUID}:
  file: path/to/file.md
```

Add a note when useful:

```yaml
DIAS-{UUID}:
  file: path/to/file.md
  note: Short authoring context.
```

Add a link when an external reference exists:

```yaml
DIAS-{UUID}:
  file: path/to/file.md
  note: Short authoring context.
  link: https://...
```

---

### 4. Keep Notes Simple

The note should explain why the reference exists or anything important that should not be forgotten.

Do not duplicate the full contents of the Markdown file.

The map is an index, not a lore database.

---

## Permanent Reference Rules

Once a Dias GUID appears in the reference map, treat it as permanent history.

The GUID may already exist:

- engraved into an artwork
- printed on an object
- stored on Arweave
- embedded into a blockchain transaction
- hidden inside an image
- included in an internet post
- attached to a physical collectible
- stored somewhere that cannot be edited later

Therefore:

### Never

- delete an existing Dias GUID
- reuse a Dias GUID
- change the meaning of a Dias GUID
- silently point a GUID at an unrelated piece of canon
- remove its canonical Markdown destination without handling the reference

External references may be impossible to update.

The repository must respect them.

---

## Protected Markdown Files

Any Markdown file referenced by at least one Dias GUID becomes a **protected file**.

Before deleting, moving, renaming, merging, or replacing a Markdown file, the agent must check the Dias mapping file.

If the file appears in the map, the agent must treat it as externally referenced.

The agent must not accidentally remove it.

---

## Moving or Renaming Protected Files

A protected Markdown file may still be reorganized.

Repository paths do not need to remain permanent.

The mapping only needs to continue resolving correctly.

For example:

Before:

```yaml
DIAS-3f7c8e18-1f22-4c37-bb61-4b640b918274:
  file: regions/wabet.md
```

If the file moves to:

`regions/wabet/index.md`

then update the map in the same change:

```yaml
DIAS-3f7c8e18-1f22-4c37-bb61-4b640b918274:
  file: regions/wabet/index.md
```

The Dias GUID does not change.

The internal file path may change.

The reference must continue to resolve.

---

## Deleting Canon

If a protected Markdown file becomes outdated, disputed, superseded, or no longer represents current understanding, prefer preserving it rather than deleting it.

Its Markdown content may explain that it is:

- historical
- disputed
- superseded
- reinterpreted
- incomplete
- no longer the current understanding

Dias should preserve its own history where possible.

Do not erase externally referenced canon casually.

---

## Repository Safety Check

Before repository cleanup or restructuring, the Dias agent must:

1. Read [`dias-map.yaml`](dias-map.yaml).
2. Collect every Markdown file referenced by the map.
3. Treat those files as protected.
4. Check proposed deletes, moves, and renames against those protected files.
5. Prevent dangling references.
6. Update the map whenever a referenced Markdown file moves.
7. Never modify the external Dias GUID itself.

---

## Recommended Validation

A small validation script should eventually verify the Dias map automatically.

It should check:

1. Every key matches the expected `DIAS-{UUID}` format.
2. Every Dias GUID is unique.
3. Every entry contains a `file`.
4. Every `file` points to a `.md` file.
5. Every referenced Markdown file exists.
6. No YAML keys are duplicated.

If a referenced Markdown file disappears, validation should fail.

Example error:

```text
Broken Dias reference:

DIAS-3f7c8e18-1f22-4c37-bb61-4b640b918274
-> regions/wabet.md

Referenced Markdown file does not exist.
```

---

## Example Agent Interaction

The user says:

> I added a new artwork.
> Its ID is:
> DIAS-3f7c8e18-1f22-4c37-bb61-4b640b918274
>
> It is connected to Wabet, somewhere in the forest.
> There is something inside a tree.

The agent should:

1. Search the existing Dias repository for the canonical Wabet or relevant forest Markdown file.
2. Avoid creating duplicate lore.
3. Add the GUID to [`dias-map.yaml`](dias-map.yaml).
4. Add a concise note.

Example:

```yaml
DIAS-3f7c8e18-1f22-4c37-bb61-4b640b918274:
  file: regions/wabet.md
  note: Artwork connected to Wabet and the forest. Something significant appears inside a tree.
```

If the user later supplies an external location, add it:

```yaml
DIAS-3f7c8e18-1f22-4c37-bb61-4b640b918274:
  file: regions/wabet.md
  note: Artwork connected to Wabet and the forest. Something significant appears inside a tree.
  link: https://arweave.net/...
```

---

## Guiding Principle

The external world may remember Dias longer than the current repository structure does.

An artwork may survive for generations.

An Arweave record may be permanent.

A blockchain transaction cannot simply be rewritten.

A photograph or old internet post may surface years later.

For that reason:

**The Dias GUID is permanent.**

**The map remembers where it belongs.**

**The Markdown file contains the world.**

**Referenced Markdown files must never accidentally disappear.**

And the entire system remains:

**DIAS GUID -> Markdown file**
