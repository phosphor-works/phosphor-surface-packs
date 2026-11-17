# Phosphor surface packs

The surface decoration packs that Phosphor apps draw around windows, panels and popups: borders, glows, shadows, blur and glass materials, and animated backdrops. [PlasmaZones](https://github.com/phosphor-works/PlasmaZones) draws them on KDE Plasma windows. [Lambent](https://github.com/phosphor-works/Lambent) draws them on its bar and popouts.

A pack is a directory under `packs/` with a `metadata.json` (its id, name, parameters and the shaders it runs) and its GLSL. `packs/shared/` holds the uniform contract and the helpers every pack includes, and the blur passes packs name as `builtin:`. The metadata schema and the renderer are in [phosphor-libs](https://github.com/phosphor-works/phosphor-libs) (`data/schemas/shader-metadata.schema.json`, `libs/phosphor-surface`).

## Install location

The packs install to `share/phosphor-works/surface`. An app looks for packs there under every XDG data directory, so a pack a user drops into `~/.local/share/phosphor-works/surface/<id>/` shows up in every app that draws them.

## Using them from an app

An app pins a commit of this repository, fetches it with CPM like its other pinned sources, and includes the helper:

```cmake
include(${phosphor-surface-packs_SOURCE_DIR}/cmake/PhosphorSurfacePacks.cmake)
phosphor_install_surface_packs()  # skipped where the distribution packages this repo on its own
target_compile_definitions(myapp PRIVATE
    SURFACE_PACKS_DATA_SUBDIR="${PHOSPHOR_SURFACE_PACKS_DATA_SUBDIR}")
```

`PHOSPHOR_SURFACE_PACKS_DIR` is the packs in the source tree, for tests and validators. A distribution can also package this repository once and have every app depend on it: `cmake -B build && cmake --install build --prefix /usr`.

## Checks

`python3 scripts/check.py` checks every pack's metadata, shader files, includes and licence headers, and CI also runs `reuse lint`. The apps check what the GLSL compiles to: PlasmaZones runs `plasmazones-shader-validate --surface` over the commit it pins.

## Licence

The shared contract and most packs are LGPL-2.1-or-later, so other tools and packs can build on them. A few `.frag` files are GPL-3.0-or-later, and two credit an upstream: `glass` (kwin-effects-glass), and `shared/surface_color.glsl`, whose vibrancy block is a BSD-3-Clause port from Hyprland. Every shader says which in its header, and `REUSE.toml` covers the metadata. The licence texts are in `LICENSES/`.
