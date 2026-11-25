<!-- SPDX-FileCopyrightText: 2026 Phosphor Works Team -->
<!-- SPDX-License-Identifier: CC0-1.0 -->

<!-- BEGIN shared: tools/sync writes this block from workspace/sync/claude-header.md. Change it there. -->
# phosphor-surface-packs

This file has two parts. The rules that every phosphor-works repository follows come first, from the conventions of
the workspace repository, imported below. The sections after them belong to this repository only: what it is, its
layout, how to build and test it, and its own rules, code, skills and agents, and links to the other repositories.
A section here does not repeat a convention. When a section and the conventions disagree, change one of them so
that they agree.

The Claude Code tooling comes from the plugins that `.claude/settings.json` enables and `workspace/tools/setup`
installs. The `phosphor-works` plugin has the command guard, the shared skills (`phosphor-works:build`, `debug`,
`code-audit`, `record-lesson`, `new-repo`), the shared reviewers, and the lesson index, which adds the lessons that
fit each prompt.

@../workspace/claude/conventions.md
<!-- END shared -->

## Overview

The surface decoration shader packs (borders, glows, shadows, blur, glass and animated backdrops) that the
phosphor-works apps draw around windows, panels and popups. The repository is data only: GLSL, pack metadata and a
CMake helper that installs them to `share/phosphor-works/shaders/surface`.

## Layout

- `packs/<id>/` is one pack: `metadata.json` and its GLSL (most packs have one `effect.frag`).
- `packs/shared/` is the surface family's contract: `surface_uniforms.glsl`, `surface.vert`, the helpers every pack
  includes (`surface_lib.glsl`, `surface_color.glsl`, `surface_blur.glsl` and others) and the Kawase and Gaussian
  blur passes a pack names as `builtin:` in `bufferShaders`.
- `cmake/PhosphorSurfacePacks.cmake` sets `PHOSPHOR_SURFACE_PACKS_DIR` and `PHOSPHOR_SURFACE_PACKS_DATA_SUBDIR` and
  defines `phosphor_install_surface_packs()`. The root `CMakeLists.txt` only installs the packs, for a distribution.

## Build and test

There is nothing to compile here. CI (`.github/workflows/ci.yml`) runs three steps on every push to `main` and every
pull request:

- `python3 scripts/check.py` (standard library only, read-only): the metadata parses, ids and shader files match,
  includes resolve, and every shader has an SPDX copyright and a license of `LGPL-2.1-or-later` or
  `GPL-3.0-or-later`, optionally joined with `AND` to `BSD-3-Clause` or `MIT`.
- `reuse lint`.
- A standalone `cmake --install` into a staging prefix.

check.py does not compile GLSL or compare parameters with the shader. PlasmaZones does that, against the commit it
pins: `plasmazones-shader-validate --surface` and its JSON schema gate (`scripts/validate-json-schemas.py`).
Before a pull request that changes GLSL or metadata, run `plasmazones-shader-validate --surface <pack dirs>` from a
PlasmaZones build over this checkout's packs, and the schema gate with `PHOSPHOR_SURFACE_PACKS_DIR=<checkout>/packs`.

## Rules

### The pack format

- The metadata `id` must equal the directory name. `fragmentShader`, `vertexShader` and every non-`builtin:` entry
  of `bufferShaders` must name a file in the pack. An `#include` resolves beside the shader or in `packs/shared/`.
- The schema is `data/schemas/surface-metadata.schema.json` in phosphor-libs, and the renderer is
  `libs/phosphor-surface` there. The uniform block in `surface_uniforms.glsl` is mirrored by `SurfaceUniforms` in
  phosphor-surface's `SurfaceShaderUniforms.h` (672 bytes, pinned by `static_assert`), so a contract change is a
  change set with phosphor-libs.
- Metadata `name`, `description` and parameter descriptions are user-facing text.

### Licensing

REUSE governs the repository. Each shader states its own license in its header. The shared contract and most packs
are `LGPL-2.1-or-later`. Seven `.frag` files are `GPL-3.0-or-later` (`blur`, `duotone`, `frosted-glass`, `glass`,
`mosaic`, `rain-glass`, `rippled-glass`). `glass` ports kwin-effects-glass and carries a second
`SPDX-FileCopyrightText` for it. The vibrancy block in `shared/surface_color.glsl` ports Hyprland and is
`LGPL-2.1-or-later AND BSD-3-Clause`. A new pack is LGPL unless it incorporates copyleft upstream code. Metadata
JSON, `.gitignore`, `README.md` and `.claude/settings.json` are licensed in `REUSE.toml`. The license texts are in
`LICENSES/`.

## Other repositories

### How a change reaches the apps

PlasmaZones and Lambent pin a commit of this repository by archive URL and SHA-256, and fetch it with CPM. A pack
change is a pull request here, then a pin bump in each app: `cmake/PlasmaZonesDependencies.cmake` and the
PlasmaZones packaging (`packaging/nix/package.nix`, `arch/PKGBUILD`, `rpm/plasmazones.spec`), and
`cmake/LambentDependencies.cmake` with Lambent's `packaging/nix/package.nix`. A pin that moves past a breaking
commit (`refactor!:`) needs the app-side change in the same bump.
