#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: MPL-2.0
#

include(FetchContent)


#################################################
# pybind11

set(PYBIND11_PATCH git apply ${CMAKE_CURRENT_SOURCE_DIR}/cmake/patches/pybind11.patch)

FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG "a2e59f0e7065404b44dfe92a28aca47ba1378dc4"    # aka v2.13.6
    PATCH_COMMAND ${PYBIND11_PATCH}
    UPDATE_DISCONNECTED 1
)
FetchContent_MakeAvailable(pybind11)


#################################################
# gafro

set(GAFRO_PATCH git apply ${CMAKE_CURRENT_SOURCE_DIR}/cmake/patches/gafro.patch)

FetchContent_Declare(
    gafro
    GIT_REPOSITORY https://github.com/idiap/gafro.git
    GIT_TAG "f6a64023b3cc10437f16aa4da48cd410befa46b3"
    PATCH_COMMAND ${GAFRO_PATCH}
    UPDATE_DISCONNECTED 1
)
FetchContent_MakeAvailable(gafro)


#################################################
# gafro_robot_descriptions

set(GAFRO_ROBOT_DESCRIPTION_PATCH git apply ${CMAKE_CURRENT_SOURCE_DIR}/cmake/patches/gafro_robot_descriptions.patch)

FetchContent_Declare(
    gafro_robot_descriptions
    GIT_REPOSITORY https://github.com/idiap/gafro_robot_descriptions.git
    GIT_TAG "1444fca9fc8a04103b52e26ca8f4a2512d0d2299"
    PATCH_COMMAND ${GAFRO_ROBOT_DESCRIPTION_PATCH}
    UPDATE_DISCONNECTED 1
)
FetchContent_MakeAvailable(gafro_robot_descriptions)

configure_file(
    "${FETCHCONTENT_BASE_DIR}/gafro_robot_descriptions-src/src/gafro_robot_descriptions/gafro_robot_descriptions_package_config.h.in"
    "${CMAKE_CURRENT_BINARY_DIR}/generated/gafro_robot_descriptions/gafro_robot_descriptions_package_config.hpp"
)


#################################################
# yaml-cpp

option(YAML_BUILD_SHARED_LIBS "Enable yaml-cpp contrib in library" OFF)
option(YAML_CPP_BUILD_TOOLS "Enable parse tools" OFF)

set(YAML_PATCH git apply ${CMAKE_CURRENT_SOURCE_DIR}/cmake/patches/yaml-cpp.patch)

FetchContent_Declare(
    yaml-cpp
    GIT_REPOSITORY https://github.com/jbeder/yaml-cpp.git
    GIT_TAG "0.8.0"
    PATCH_COMMAND ${YAML_PATCH}
    UPDATE_DISCONNECTED 1
)
FetchContent_MakeAvailable(yaml-cpp)


#################################################
# Eigen3

set(EIGEN3_PATCH git apply ${CMAKE_CURRENT_SOURCE_DIR}/cmake/patches/eigen3.patch)

FetchContent_Declare(
    eigen3
    GIT_REPOSITORY https://gitlab.com/libeigen/eigen.git
    GIT_TAG "3147391d946bb4b6c68edd901f2add6ac1f31f8c" # aka "3.4.0"
    PATCH_COMMAND ${EIGEN3_PATCH}
    UPDATE_DISCONNECTED 1
)
FetchContent_MakeAvailable(eigen3)
