# SPDX-FileCopyrightText: 2026 fuddlesworth
# SPDX-License-Identifier: LGPL-2.1-or-later

# Included by an application that draws the Phosphor surface decoration packs,
# after it has fetched this repository (at a pinned commit, with CPM):
#
#   include(${phosphor-surface-packs_SOURCE_DIR}/cmake/PhosphorSurfacePacks.cmake)
#
# It sets:
#
#   PHOSPHOR_SURFACE_PACKS_DIR          the packs in this tree, for tests and
#                                       validators that read them unbuilt
#   PHOSPHOR_SURFACE_PACKS_DATA_SUBDIR  where the packs install, relative to an
#                                       XDG data directory: phosphor-works/surface.
#                                       An application looks for packs there
#                                       under every XDG data directory, the
#                                       user's own included, and passes the
#                                       directories it finds to the libraries.
#
# and provides:
#
#   phosphor_install_surface_packs()
#
# which installs the packs to ${KDE_INSTALL_DATADIR}, else
# ${CMAKE_INSTALL_DATADIR}, else share, under the data subdir. A distribution
# that packages this repository on its own skips the call.

set(PHOSPHOR_SURFACE_PACKS_DIR "${CMAKE_CURRENT_LIST_DIR}/../packs")
cmake_path(NORMAL_PATH PHOSPHOR_SURFACE_PACKS_DIR)
set(PHOSPHOR_SURFACE_PACKS_DATA_SUBDIR "phosphor-works/surface")

function(phosphor_install_surface_packs)
    if(DEFINED KDE_INSTALL_DATADIR)
        set(dataDir "${KDE_INSTALL_DATADIR}")
    elseif(DEFINED CMAKE_INSTALL_DATADIR)
        set(dataDir "${CMAKE_INSTALL_DATADIR}")
    else()
        set(dataDir "share")
    endif()
    install(DIRECTORY "${PHOSPHOR_SURFACE_PACKS_DIR}/"
            DESTINATION "${dataDir}/${PHOSPHOR_SURFACE_PACKS_DATA_SUBDIR}")
endfunction()
