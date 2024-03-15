#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

set(DEST_DIR "${CMAKE_CURRENT_BINARY_DIR}/pygafro")
set(GENERATED_DIR ${CMAKE_BINARY_DIR}/generated)

file(COPY "${PROJECT_SOURCE_DIR}/dependencies/gafro_robot_descriptions/assets/" DESTINATION "${DEST_DIR}/assets/")


set(PYTHON_SRCS
    __init__.py
    manipulator.py
    multivector.py
    singlemanipulatortarget.py
    singlemanipulatordualtarget.py
    singlemanipulatormotorcost.py
    utils.py
    ${CMAKE_BINARY_DIR}/generated/mv_combinations.py
    ${CMAKE_BINARY_DIR}/generated/geometricproductcayleytable.py
    ${CMAKE_BINARY_DIR}/generated/innerproductcayleytable.py
    ${CMAKE_BINARY_DIR}/generated/outerproductcayleytable.py
)


# Build the module
pybind11_add_module(${LIBRARY_NAME}
    cpp/algebra.cpp
    cpp/algebra/motor.cpp
    cpp/algebra/motor_utils.hpp
    cpp/algebra/multivector_utils.hpp
    cpp/algebra/products_utils.hpp
    cpp/algebra/rotor.cpp
    cpp/algebra/rotor_utils.hpp
    cpp/algebra/types.h

    cpp/bindings.cpp
    cpp/physics.cpp
    cpp/physics_types.h

    cpp/robots.cpp
    cpp/robots/types.h
    cpp/robots/FixedJoint.hpp
    cpp/robots/FrankaEmikaRobot.hpp
    cpp/robots/Joint.hpp
    cpp/robots/KinematicChain.hpp
    cpp/robots/Link.hpp
    cpp/robots/Manipulator.hpp
    cpp/robots/PrismaticJoint.hpp
    cpp/robots/RevoluteJoint.hpp
    cpp/robots/System.hpp
    cpp/robots/UR5.hpp

    cpp/utils.h
    cpp/utils.cpp

    ${MANIPULATORS_SRCS}
    ${MOTOR_APPLY_METHODS_SRCS}
    ${MULTIVECTOR_PRODUCTS_SRCS}
    ${MULTIVECTOR_SRCS}
    ${ROTOR_APPLY_METHODS_SRCS}

    ${CMAKE_SOURCE_DIR}/dependencies/gafro_robot_descriptions/src/gafro_robot_descriptions/serialization/FilePath.cpp
    ${CMAKE_SOURCE_DIR}/dependencies/gafro_robot_descriptions/src/gafro_robot_descriptions/serialization/SystemSerialization.cpp
    ${CMAKE_SOURCE_DIR}/dependencies/gafro_robot_descriptions/src/gafro_robot_descriptions/serialization/Visual.cpp
)


target_precompile_headers(${LIBRARY_NAME}
    PRIVATE
        cpp/algebra/types.h
        cpp/physics_types.h
        cpp/robots/types.h
        ${GENERATED_DIR}/manipulators.h
        ${GENERATED_DIR}/multivectors.h
)


get_source_file_property(IS_GENERATED ${GENERATED_DIR}/motor_apply_methods.cpp GENERATED)
if(NOT IS_GENERATED)
    set_source_files_properties(${MANIPULATORS_SRCS} PROPERTIES GENERATED TRUE)
    set_source_files_properties(${MOTOR_APPLY_METHODS_SRCS} PROPERTIES GENERATED TRUE)
    set_source_files_properties(${MULTIVECTOR_PRODUCTS_SRCS} PROPERTIES GENERATED TRUE)
    set_source_files_properties(${MULTIVECTOR_SRCS} PROPERTIES GENERATED TRUE)
    set_source_files_properties(${ROTOR_APPLY_METHODS_SRCS} PROPERTIES GENERATED TRUE)
endif()


if (CMAKE_CXX_COMPILER_ID MATCHES "(C|c?)lang")
    target_compile_options(${LIBRARY_NAME} PUBLIC "-Wall" "-Wno-unused-local-typedef" "-Wno-unused-command-line-argument")
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_compile_options(${LIBRARY_NAME} PUBLIC "-Wall" "-Wno-unused-local-typedefs" "-Wno-class-memaccess")
endif()

set_source_files_properties(cpp/robots.cpp PROPERTIES COMPILE_FLAGS "-Wno-array-bounds")

message(STATUS ${gafro_USE_YAML_CPP})
target_include_directories(${LIBRARY_NAME}
    PRIVATE
        ${CMAKE_BINARY_DIR}/generated
        ${CMAKE_SOURCE_DIR}/dependencies/gafro/src
        ${CMAKE_SOURCE_DIR}/dependencies/gafro_robot_descriptions/src
        ${CMAKE_BINARY_DIR}/dependencies/gafro_robot_descriptions/src
        cpp

    PUBLIC
        ${yaml-cpp_SOURCE_DIR}
        ${yaml-cpp_BINARY_DIR}
)

target_link_libraries(${LIBRARY_NAME}
    PRIVATE
        gafro
        yaml-cpp::yaml-cpp
)

add_dependencies(${LIBRARY_NAME} generate_bindings)

set_target_properties(${LIBRARY_NAME}
                      PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${DEST_DIR}"
)


add_custom_target(copy-python-files ALL
                  ${CMAKE_COMMAND} -E copy ${PYTHON_SRCS} ${DEST_DIR}/
                  DEPENDS ${LIBRARY_NAME}
                  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                  VERBATIM
)


install(TARGETS ${LIBRARY_NAME} DESTINATION "${PYTHON_SITE_PACKAGES_INSTALL_DIR}/${PACKAGE_NAME}")
install(FILES ${PYTHON_SRCS} DESTINATION "${PYTHON_SITE_PACKAGES_INSTALL_DIR}/${PACKAGE_NAME}")
install(
    DIRECTORY
        "${DEST_DIR}/assets/"
    DESTINATION
        "${PYTHON_SITE_PACKAGES_INSTALL_DIR}/${PACKAGE_NAME}/assets"
    COMPONENT
        Devel
)
