#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: MPL-2.0
#

set(DEST_DIR "${CMAKE_CURRENT_BINARY_DIR}/pygafro")
set(GENERATED_DIR ${CMAKE_BINARY_DIR}/generated)

file(
    COPY "${FETCHCONTENT_BASE_DIR}/gafro_robot_descriptions-src/assets/"
    DESTINATION "${DEST_DIR}/assets/"
    FILES_MATCHING
        PATTERN "*.yaml"
        PATTERN "meshes" EXCLUDE
        PATTERN "materials" EXCLUDE
)


set(PYTHON_SRCS
    __init__.py
    manipulator.py
    multivector.py
    singlemanipulatortarget.py
    singlemanipulatordualtarget.py
    singlemanipulatormotorcost.py
    utils.py
    ${CMAKE_BINARY_DIR}/generated/algebra/mv_combinations.py
    ${CMAKE_BINARY_DIR}/generated/geometricproductcayleytable.py
    ${CMAKE_BINARY_DIR}/generated/innerproductcayleytable.py
    ${CMAKE_BINARY_DIR}/generated/outerproductcayleytable.py
)


set(PRECOMPILED_HEADERS
    cpp/algebra/types.h
    cpp/physics_types.h
    cpp/robots/types.h
    ${GENERATED_DIR}/algebra/multivectors.h
)


set(INCLUDE_DIRS
    ${CMAKE_BINARY_DIR}/generated
    ${CMAKE_BINARY_DIR}/generated/algebra
    ${CMAKE_BINARY_DIR}/generated/optimization
    ${CMAKE_BINARY_DIR}/generated/robots
    ${FETCHCONTENT_BASE_DIR}/gafro-src/src
    ${FETCHCONTENT_BASE_DIR}/gafro_robot_descriptions-src/src
    ${FETCHCONTENT_BASE_DIR}/eigen3-src/
    cpp
)


get_source_file_property(IS_GENERATED ${GENERATED_DIR}/motor_apply_methods.cpp GENERATED)
if(NOT IS_GENERATED)
    set_source_files_properties(${MANIPULATORS_SRCS} PROPERTIES GENERATED TRUE)
    set_source_files_properties(${MOTOR_APPLY_METHODS_SRCS} PROPERTIES GENERATED TRUE)
    set_source_files_properties(${MULTIVECTOR_PRODUCTS_SRCS} PROPERTIES GENERATED TRUE)
    set_source_files_properties(${MULTIVECTOR_SRCS} PROPERTIES GENERATED TRUE)
    set_source_files_properties(${ROTOR_APPLY_METHODS_SRCS} PROPERTIES GENERATED TRUE)
    set_source_files_properties(${SINGLEMANIPULATORTARGETS_SRCS} PROPERTIES GENERATED TRUE)
    set_source_files_properties(${SINGLEMANIPULATORMOTORCOSTS_SRCS} PROPERTIES GENERATED TRUE)
    set_source_files_properties(${SINGLEMANIPULATORDUALTARGETS_SRCS} PROPERTIES GENERATED TRUE)
endif()


if (CMAKE_CXX_COMPILER_ID MATCHES "(C|c?)lang")
    add_compile_options("-Wall" "-Wno-unused-local-typedef" "-Wno-unused-command-line-argument")
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    add_compile_options("-Wall" "-Wno-unused-local-typedefs" "-Wno-class-memaccess")
endif()

add_compile_options("-Wno-unused-but-set-variable" "-fPIC")

set_source_files_properties(cpp/robots.cpp PROPERTIES COMPILE_FLAGS "-Wno-array-bounds")


###########################################################
# Build a static library with the optimization classes
add_library(pygafro-optimization STATIC
    ${SINGLEMANIPULATORTARGETS_SRCS}
    ${SINGLEMANIPULATORMOTORCOSTS_SRCS}
    ${SINGLEMANIPULATORDUALTARGETS_SRCS}
)

target_include_directories(pygafro-optimization
    PRIVATE
        ${INCLUDE_DIRS}
        ${PYBIND11_INCLUDE_DIR}
        ${PYTHON_INCLUDE_DIRS}

    PUBLIC
        ${yaml-cpp_SOURCE_DIR}
        ${yaml-cpp_BINARY_DIR}
)

target_link_libraries(pygafro-optimization
    PRIVATE
        gafro
        yaml-cpp::yaml-cpp
)

target_precompile_headers(pygafro-optimization
    PRIVATE
        ${PRECOMPILED_HEADERS}
        ${GENERATED_DIR}/robots/manipulators.h
        ${GENERATED_DIR}/optimization/singlemanipulatortargets.h
        ${GENERATED_DIR}/optimization/singlemanipulatormotorcosts.h
        ${GENERATED_DIR}/optimization/singlemanipulatordualtargets.h
)

add_dependencies(pygafro-optimization generate_bindings)


###########################################################
# Build a static library with the robot classes
add_library(pygafro-robots STATIC
    cpp/robots.cpp
    cpp/robots/types.h
    cpp/robots/AnymalC.hpp
    cpp/robots/FixedJoint.hpp
    cpp/robots/FrankaEmikaRobot.hpp
    cpp/robots/Hand.hpp
    cpp/robots/Joint.hpp
    cpp/robots/KinematicChain.hpp
    cpp/robots/KukaIIWA7.hpp
    cpp/robots/KukaIIWA14.hpp
    cpp/robots/LeapHand.hpp
    cpp/robots/Link.hpp
    cpp/robots/Manipulator.hpp
    cpp/robots/Planar3DoF.hpp
    cpp/robots/PrismaticJoint.hpp
    cpp/robots/Quadruped.hpp
    cpp/robots/RevoluteJoint.hpp
    cpp/robots/System.hpp
    cpp/robots/UFactoryLite6.hpp
    cpp/robots/UR5.hpp

    ${MANIPULATORS_SRCS}
)

target_include_directories(pygafro-robots
    PRIVATE
        ${INCLUDE_DIRS}
        ${PYBIND11_INCLUDE_DIR}
        ${PYTHON_INCLUDE_DIRS}

    PUBLIC
        ${yaml-cpp_SOURCE_DIR}
        ${yaml-cpp_BINARY_DIR}
)

target_link_libraries(pygafro-robots
    PRIVATE
        gafro
        yaml-cpp::yaml-cpp
)

target_precompile_headers(pygafro-robots
    PRIVATE
        ${PRECOMPILED_HEADERS}
        ${GENERATED_DIR}/robots/manipulators.h
)

add_dependencies(pygafro-robots generate_bindings)


###########################################################
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

    cpp/utils.h
    cpp/utils.cpp

    ${MOTOR_APPLY_METHODS_SRCS}
    ${MULTIVECTOR_PRODUCTS_SRCS}
    ${MULTIVECTOR_SRCS}
    ${ROTOR_APPLY_METHODS_SRCS}

    "${FETCHCONTENT_BASE_DIR}/gafro_robot_descriptions-src/src/gafro_robot_descriptions/serialization/FilePath.cpp"
    "${FETCHCONTENT_BASE_DIR}/gafro_robot_descriptions-src/src/gafro_robot_descriptions/serialization/SystemSerialization.cpp"
    "${FETCHCONTENT_BASE_DIR}/gafro_robot_descriptions-src/src/gafro_robot_descriptions/serialization/Visual.cpp"
)


target_precompile_headers(${LIBRARY_NAME}
    PRIVATE
        ${PRECOMPILED_HEADERS}
)

target_include_directories(${LIBRARY_NAME}
    PRIVATE
        ${INCLUDE_DIRS}

    PUBLIC
        ${yaml-cpp_SOURCE_DIR}
        ${yaml-cpp_BINARY_DIR}
)

target_link_libraries(${LIBRARY_NAME}
    PRIVATE
        gafro
        yaml-cpp::yaml-cpp
        pygafro-optimization
        pygafro-robots
)

add_dependencies(${LIBRARY_NAME} generate_bindings)

set_target_properties(${LIBRARY_NAME}
                      PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${DEST_DIR}"
)


###########################################################

add_custom_target(copy-python-files ALL
                  ${CMAKE_COMMAND} -E copy ${PYTHON_SRCS} ${DEST_DIR}/
                  DEPENDS ${LIBRARY_NAME}
                  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                  VERBATIM
)


install(TARGETS ${LIBRARY_NAME} DESTINATION "${PYTHON_SITE_PACKAGES_INSTALL_DIR}${PACKAGE_NAME}")
install(FILES ${PYTHON_SRCS} DESTINATION "${PYTHON_SITE_PACKAGES_INSTALL_DIR}${PACKAGE_NAME}")
install(
    DIRECTORY
        "${DEST_DIR}/assets/"
    DESTINATION
        "${PYTHON_SITE_PACKAGES_INSTALL_DIR}${PACKAGE_NAME}/assets"
    COMPONENT
        Devel
)
