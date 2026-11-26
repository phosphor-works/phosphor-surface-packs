<!-- SPDX-FileCopyrightText: 2026 Phosphor Works Team -->
<!-- SPDX-License-Identifier: CC0-1.0 -->

# Changelog

This file records each release of phosphor-surface-packs, the surface shader packs.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html), as the phosphor-works conventions say.

## [Unreleased]

### Added

- A `PhosphorSurfacePacks` CMake package, installed with the packs. An application that uses the packaged packs
  finds it with `find_package(PhosphorSurfacePacks)`, which sets `PHOSPHOR_SURFACE_PACKS_DIR` to the installed packs.

## [0.1.0] - 2026-11-26

The first release. It holds the surface shader packs that the suite ships, in `packs/`. The tag `v0.1.0` is commit `572e2240`, which PlasmaZones and Lambent pin.

[Unreleased]: https://github.com/phosphor-works/phosphor-surface-packs/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/phosphor-works/phosphor-surface-packs/releases/tag/v0.1.0
