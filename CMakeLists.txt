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


set(Python_FIND_STRATEGY "LOCATION")
set(PYTHON_VERSION 3 CACHE STRING "Python version")
set(PYBIND11_PYTHON_VERSION ${PYTHON_VERSION} CACHE STRING "Python version used by PyBind11")

find_package(Python REQUIRED COMPONENTS Interpreter Development ${_pybind11_quiet})

set(PACKAGE_NAME "pygafro")
set(LIBRARY_NAME "_${PACKAGE_NAME}")
SET(PYTHON_MODULE_EXTENSION ".so")


set(PYTHON_SITE_PACKAGES_REL_INSTALL_DIR "lib/python${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}/dist-packages")
set(PYTHON_SITE_PACKAGES_INSTALL_DIR "${CMAKE_INSTALL_PREFIX}/${PYTHON_SITE_PACKAGES_REL_INSTALL_DIR}")

if(DEFINED ENV{VIRTUAL_ENV})
    message(STATUS "VIRTUAL ENV INSTALLATION DETECTED")
    set(PYTHON_SITE_PACKAGES_INSTALL_DIR "$ENV{VIRTUAL_ENV}/lib/python${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}/site-packages")

elseif(DEFINED ENV{CONDA_PREFIX})
  message(STATUS "CONDA INSTALLATION DETECTED")
  set(PYTHON_SITE_PACKAGES_INSTALL_DIR "$ENV{CONDA_PREFIX}/lib/python${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}/site-packages")

elseif(DEFINED ENV{USE_COLCON})
  message(STATUS "ROS2 INSTALLATION DETECTED")
  find_package(ament_cmake REQUIRED)
  find_package(ament_cmake_python REQUIRED)
  ament_python_install_package(src)

  # https://answers.ros.org/question/394564/colcon-not-adding-python-module-built-with-cmake-to-pythonpath/
  file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/share/ament_index/resource_index/packages/${PROJECT_NAME} "")
  install(FILES ${CMAKE_CURRENT_BINARY_DIR}/share/ament_index/resource_index/packages/${PROJECT_NAME} DESTINATION share/ament_index/resource_index/packages)
  file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/share/${PROJECT_NAME}/hook/ament_prefix_path.dsv "prepend-non-duplicate;AMENT_PREFIX_PATH;")
  install(FILES ${CMAKE_CURRENT_BINARY_DIR}/share/${PROJECT_NAME}/hook/ament_prefix_path.dsv DESTINATION share/${PROJECT_NAME}/hook)
  file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/share/${PROJECT_NAME}/hook/python_path.dsv "prepend-non-duplicate;PYTHONPATH;${PYTHON_SITE_PACKAGES_REL_INSTALL_DIR}")
  install(FILES ${CMAKE_CURRENT_BINARY_DIR}/share/${PROJECT_NAME}/hook/python_path.dsv DESTINATION share/${PROJECT_NAME}/hook)
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
