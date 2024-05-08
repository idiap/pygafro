#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

cmake_minimum_required(VERSION 3.11)

project(pygafro)


set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    message(WARNING "We recommend the usage of clang instead of gcc, which requires significantly more memory resources to compile pygafro")
endif()


set(PYTHON_VERSION 3 CACHE STRING "Python version")
set(PYBIND11_PYTHON_VERSION ${PYTHON_VERSION} CACHE STRING "Python version used by PyBind11")

cmake_policy(SET CMP0148 OLD)

find_package(PythonInterp ${PYTHON_VERSION} REQUIRED)
find_package(PythonLibs ${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR} REQUIRED)


set(PACKAGE_NAME "pygafro")
set(LIBRARY_NAME "_${PACKAGE_NAME}")
SET(PYTHON_MODULE_EXTENSION ".so")

set(PYTHON_SITE_PACKAGES_INSTALL_DIR "${CMAKE_INSTALL_PREFIX}/lib/python${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}/dist-packages")

if(DEFINED ENV{VIRTUAL_ENV})
    message(STATUS "VIRTUAL ENV INSTALLATION DETECTED")
    set(PYTHON_SITE_PACKAGES_INSTALL_DIR "$ENV{VIRTUAL_ENV}/lib/python${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}/site-packages")

elseif(DEFINED ENV{CONDA_PREFIX})
  message(STATUS "CONDA INSTALLATION DETECTED")
  set(PYTHON_SITE_PACKAGES_INSTALL_DIR "$ENV{CONDA_PREFIX}/lib/python${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}/site-packages")
endif()

message(STATUS "Python package will be installed in: ${PYTHON_SITE_PACKAGES_INSTALL_DIR}")


# Fetch yaml-cpp
include(FetchContent)

option(YAML_BUILD_SHARED_LIBS "Enable yaml-cpp contrib in library" OFF)
option(YAML_CPP_BUILD_TOOLS "Enable parse tools" OFF)

FetchContent_Declare(
  yaml-cpp
  GIT_REPOSITORY https://github.com/jbeder/yaml-cpp.git
  GIT_TAG "0.8.0"
)
FetchContent_MakeAvailable(yaml-cpp)


add_subdirectory(dependencies)
add_subdirectory(scripts)
add_subdirectory(src)
add_subdirectory(tests)
