# SPDX-FileCopyrightText: 2026 Phosphor Works Team
# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Installs the packs on their own, for a distribution that packages this
# repository once for every application that draws them:
#
#   cmake -B build && cmake --install build --prefix /usr
#
# Applications don't add this directory. They include
# cmake/PhosphorSurfacePacks.cmake instead (see there).

cmake_minimum_required(VERSION 3.20)
project(phosphor-surface-packs VERSION 0.1.0 LANGUAGES NONE)

include(GNUInstallDirs)
include(cmake/PhosphorSurfacePacks.cmake)
phosphor_install_surface_packs()

# The PhosphorSurfacePacks package, for an application that uses the
# installed packs (cmake/PhosphorSurfacePacksConfig.cmake.in). The packs hold
# no binaries, so the package is architecture-independent and lives under the
# data directory.
include(CMakePackageConfigHelpers)
set(PHOSPHOR_SURFACE_PACKS_INSTALL_DIR "${CMAKE_INSTALL_DATADIR}/${PHOSPHOR_SURFACE_PACKS_DATA_SUBDIR}")
set(_package_dir "${CMAKE_INSTALL_DATADIR}/cmake/PhosphorSurfacePacks")
configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/PhosphorSurfacePacksConfig.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/PhosphorSurfacePacksConfig.cmake"
    INSTALL_DESTINATION "${_package_dir}"
    PATH_VARS PHOSPHOR_SURFACE_PACKS_INSTALL_DIR
)
write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/PhosphorSurfacePacksConfigVersion.cmake"
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMinorVersion
    ARCH_INDEPENDENT
)
install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/PhosphorSurfacePacksConfig.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/PhosphorSurfacePacksConfigVersion.cmake"
    DESTINATION "${_package_dir}"
)
