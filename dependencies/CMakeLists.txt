#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

add_subdirectory(gafro)
add_subdirectory(pybind11)

configure_file(
    "${CMAKE_CURRENT_LIST_DIR}/gafro_robot_descriptions/src/gafro_robot_descriptions/gafro_robot_descriptions_package_config.h.in"
    "${CMAKE_CURRENT_BINARY_DIR}/gafro_robot_descriptions/src/gafro_robot_descriptions/gafro_robot_descriptions_package_config.hpp"
)
