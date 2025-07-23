#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: MPL-2.0
#

cmake_minimum_required(VERSION 3.15)

project(pygafro)


set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    message(WARNING "We recommend the usage of clang instead of gcc, which requires significantly more memory resources to compile pygafro")
endif()


set(Python3_FIND_STRATEGY "LOCATION")
find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module ${_pybind11_quiet})


set(PACKAGE_NAME "pygafro")
set(LIBRARY_NAME "_${PACKAGE_NAME}")
set(PYTHON_MODULE_EXTENSION ".so")

if (DEFINED COMPILING_FROM_PIP)
  set(PYTHON_SITE_PACKAGES_INSTALL_DIR "")
else()
  set(PYTHON_SITE_PACKAGES_INSTALL_DIR "${Python3_SITEARCH}/")
endif()


if(DEFINED ENV{USE_COLCON})

  set(PYTHON_SITE_PACKAGES_REL_INSTALL_DIR "lib/python${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}/dist-packages")
  set(PYTHON_SITE_PACKAGES_INSTALL_DIR "${CMAKE_INSTALL_PREFIX}/${PYTHON_SITE_PACKAGES_REL_INSTALL_DIR}")

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
else()
  if (PYTHON_SITE_PACKAGES_INSTALL_DIR STREQUAL "")
    message(STATUS "Python package will be installed in: ${PYTHON_SITE_PACKAGES_INSTALL_DIR}")
  endif()
endif()


include(cmake/dependencies.cmake)

add_subdirectory(scripts)
add_subdirectory(src)
add_subdirectory(tests)
