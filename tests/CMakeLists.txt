#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

# Run the unit tests
add_custom_target(run-unittests ALL
                  PYTHONPATH=${CMAKE_BINARY_DIR}/src python3 main.py
                  DEPENDS ${LIBRARY_NAME}
                  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                  COMMENT "Unit testing..." VERBATIM
)
