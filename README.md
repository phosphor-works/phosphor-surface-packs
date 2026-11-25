<!-- SPDX-FileCopyrightText: 2026 Phosphor Works Team -->
<!-- SPDX-License-Identifier: CC0-1.0 -->

# Phosphor surface packs

This repository holds the surface decoration packs that Phosphor apps draw around windows, panels and popups. The
packs give borders, glows, shadows, blur and glass materials, and animated backdrops.
[PlasmaZones](https://github.com/phosphor-works/PlasmaZones) draws them on KDE Plasma windows.
[Lambent](https://github.com/phosphor-works/Lambent) draws them on its bar and popouts.

## Contents

| Path | Contents |
| --- | --- |
| `packs/<id>/` | One pack: a `metadata.json` (its id, name, parameters and the shaders it runs) and its GLSL |
| `packs/shared/` | The uniform contract and the helpers that each pack includes, and the blur passes that packs name as `builtin:` |
| `cmake/PhosphorSurfacePacks.cmake` | The CMake helper for an app |
| `scripts/check.py` | The pack check |

The metadata schema and the renderer are in [phosphor-libs](https://github.com/phosphor-works/phosphor-libs)
(`data/schemas/surface-metadata.schema.json`, `libs/phosphor-surface`).

## Use

An app pins a commit of this repository and gets it with CPM, as it does with its other pinned sources. Then the app
includes the helper:

```cmake
include(${phosphor-surface-packs_SOURCE_DIR}/cmake/PhosphorSurfacePacks.cmake)
phosphor_install_surface_packs()  # skipped where the distribution packages this repo on its own
target_compile_definitions(myapp PRIVATE
    SURFACE_PACKS_DATA_SUBDIR="${PHOSPHOR_SURFACE_PACKS_DATA_SUBDIR}")
```

`PHOSPHOR_SURFACE_PACKS_DIR` is the folder of the packs in the source tree, for tests and validators.

A distribution can also package this repository one time and make each app depend on that package:

```sh
cmake -B build && cmake --install build --prefix /usr
```

## Install location

The packs install to `share/phosphor-works/shaders/surface`. An app looks for packs there under each XDG data
directory. Thus a pack that a user puts into `~/.local/share/phosphor-works/shaders/surface/<id>/` shows in each app
that draws the packs.

## Checks

`python3 scripts/check.py` checks the metadata, the shader files, the includes and the license headers of each pack.
CI also runs `reuse lint`. The apps check the output of the GLSL compiler. PlasmaZones runs
`plasmazones-shader-validate --surface` over the commit that it pins.

## License

The shared contract and most packs are licensed under LGPL-2.1-or-later, so other tools and packs can use them. Seven
`.frag` files are licensed under GPL-3.0-or-later. Two files credit an upstream project:

- `glass` ports kwin-effects-glass.
- `shared/surface_color.glsl` has a vibrancy block that is a BSD-3-Clause port from Hyprland.

The header of each shader gives its license, and `REUSE.toml` gives the license of the metadata. The license texts
are in `LICENSES/`.
