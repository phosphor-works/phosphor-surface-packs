# SPDX-FileCopyrightText: 2026 fuddlesworth
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
