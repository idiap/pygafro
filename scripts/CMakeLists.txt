#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

set(OUTPUT_DIR ${CMAKE_BINARY_DIR}/generated)

add_custom_target(make_generated_directory ALL COMMAND ${CMAKE_COMMAND} -E make_directory ${OUTPUT_DIR})


# Multivectors
set(MULTIVECTOR_SRCS
    ${OUTPUT_DIR}/multivectors.h
    ${OUTPUT_DIR}/multivectors.cpp
    ${OUTPUT_DIR}/mv_combinations.py

    ${OUTPUT_DIR}/multivectors_0.cpp
    ${OUTPUT_DIR}/multivectors_3.cpp
    ${OUTPUT_DIR}/multivectors_6.cpp
    ${OUTPUT_DIR}/multivectors_9.cpp
    ${OUTPUT_DIR}/multivectors_12.cpp
    ${OUTPUT_DIR}/multivectors_15.cpp
    ${OUTPUT_DIR}/multivectors_18.cpp
    ${OUTPUT_DIR}/multivectors_21.cpp
    ${OUTPUT_DIR}/multivectors_24.cpp
    ${OUTPUT_DIR}/multivectors_27.cpp
    ${OUTPUT_DIR}/multivectors_30.cpp
    ${OUTPUT_DIR}/multivectors_33.cpp
    ${OUTPUT_DIR}/multivectors_36.cpp
    ${OUTPUT_DIR}/multivectors_39.cpp
    ${OUTPUT_DIR}/multivectors_42.cpp
    ${OUTPUT_DIR}/multivectors_45.cpp
    ${OUTPUT_DIR}/multivectors_48.cpp
    ${OUTPUT_DIR}/multivectors_51.cpp
    ${OUTPUT_DIR}/multivectors_54.cpp
    ${OUTPUT_DIR}/multivectors_57.cpp
    ${OUTPUT_DIR}/multivectors_60.cpp
    ${OUTPUT_DIR}/multivectors_63.cpp
    ${OUTPUT_DIR}/multivectors_66.cpp
    ${OUTPUT_DIR}/multivectors_69.cpp
    ${OUTPUT_DIR}/multivectors_72.cpp

    CACHE INTERNAL "MULTIVECTOR_SRCS"
)

add_custom_command(
    OUTPUT ${MULTIVECTOR_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_multivectors.py ${OUTPUT_DIR}
    DEPENDS generate_multivectors.py helpers.py templates/multivectors.h templates/multivectors.hpp
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the Multivector bindings"
    VERBATIM
)

add_custom_target(generate_multivectors DEPENDS ${MULTIVECTOR_SRCS})
add_dependencies(generate_multivectors make_generated_directory)


# Multivectors multiplications
set(MULTIVECTOR_PRODUCTS_SRCS
    ${OUTPUT_DIR}/geometric_products.cpp
    ${OUTPUT_DIR}/inner_products.cpp
    ${OUTPUT_DIR}/outer_products.cpp

    ${OUTPUT_DIR}/geometric_products_0.cpp
    ${OUTPUT_DIR}/geometric_products_100.cpp
    ${OUTPUT_DIR}/geometric_products_200.cpp
    ${OUTPUT_DIR}/geometric_products_300.cpp
    ${OUTPUT_DIR}/geometric_products_400.cpp
    ${OUTPUT_DIR}/geometric_products_500.cpp
    ${OUTPUT_DIR}/geometric_products_600.cpp
    ${OUTPUT_DIR}/geometric_products_700.cpp
    ${OUTPUT_DIR}/geometric_products_800.cpp
    ${OUTPUT_DIR}/geometric_products_900.cpp
    ${OUTPUT_DIR}/geometric_products_1000.cpp
    ${OUTPUT_DIR}/geometric_products_1100.cpp
    ${OUTPUT_DIR}/geometric_products_1200.cpp
    ${OUTPUT_DIR}/geometric_products_1300.cpp
    ${OUTPUT_DIR}/geometric_products_1400.cpp
    ${OUTPUT_DIR}/geometric_products_1500.cpp
    ${OUTPUT_DIR}/geometric_products_1600.cpp
    ${OUTPUT_DIR}/geometric_products_1700.cpp
    ${OUTPUT_DIR}/geometric_products_1800.cpp
    ${OUTPUT_DIR}/geometric_products_1900.cpp
    ${OUTPUT_DIR}/geometric_products_2000.cpp
    ${OUTPUT_DIR}/geometric_products_2100.cpp
    ${OUTPUT_DIR}/geometric_products_2200.cpp

    ${OUTPUT_DIR}/inner_products_0.cpp
    ${OUTPUT_DIR}/inner_products_100.cpp
    ${OUTPUT_DIR}/inner_products_200.cpp
    ${OUTPUT_DIR}/inner_products_300.cpp
    ${OUTPUT_DIR}/inner_products_400.cpp
    ${OUTPUT_DIR}/inner_products_500.cpp
    ${OUTPUT_DIR}/inner_products_600.cpp
    ${OUTPUT_DIR}/inner_products_700.cpp
    ${OUTPUT_DIR}/inner_products_800.cpp
    ${OUTPUT_DIR}/inner_products_900.cpp
    ${OUTPUT_DIR}/inner_products_1000.cpp
    ${OUTPUT_DIR}/inner_products_1100.cpp
    ${OUTPUT_DIR}/inner_products_1200.cpp
    ${OUTPUT_DIR}/inner_products_1300.cpp
    ${OUTPUT_DIR}/inner_products_1400.cpp
    ${OUTPUT_DIR}/inner_products_1500.cpp
    ${OUTPUT_DIR}/inner_products_1600.cpp
    ${OUTPUT_DIR}/inner_products_1700.cpp
    ${OUTPUT_DIR}/inner_products_1800.cpp
    ${OUTPUT_DIR}/inner_products_1900.cpp
    ${OUTPUT_DIR}/inner_products_2000.cpp
    ${OUTPUT_DIR}/inner_products_2100.cpp
    ${OUTPUT_DIR}/inner_products_2200.cpp

    ${OUTPUT_DIR}/outer_products_0.cpp
    ${OUTPUT_DIR}/outer_products_100.cpp
    ${OUTPUT_DIR}/outer_products_200.cpp
    ${OUTPUT_DIR}/outer_products_300.cpp
    ${OUTPUT_DIR}/outer_products_400.cpp
    ${OUTPUT_DIR}/outer_products_500.cpp
    ${OUTPUT_DIR}/outer_products_600.cpp
    ${OUTPUT_DIR}/outer_products_700.cpp
    ${OUTPUT_DIR}/outer_products_800.cpp
    ${OUTPUT_DIR}/outer_products_900.cpp
    ${OUTPUT_DIR}/outer_products_1000.cpp
    ${OUTPUT_DIR}/outer_products_1100.cpp
    ${OUTPUT_DIR}/outer_products_1200.cpp
    ${OUTPUT_DIR}/outer_products_1300.cpp
    ${OUTPUT_DIR}/outer_products_1400.cpp
    ${OUTPUT_DIR}/outer_products_1500.cpp
    ${OUTPUT_DIR}/outer_products_1600.cpp
    ${OUTPUT_DIR}/outer_products_1700.cpp
    ${OUTPUT_DIR}/outer_products_1800.cpp
    ${OUTPUT_DIR}/outer_products_1900.cpp
    ${OUTPUT_DIR}/outer_products_2000.cpp
    ${OUTPUT_DIR}/outer_products_2100.cpp
    ${OUTPUT_DIR}/outer_products_2200.cpp

    CACHE INTERNAL "MULTIVECTOR_PRODUCTS_SRCS"
)

add_custom_command(
    OUTPUT ${MULTIVECTOR_PRODUCTS_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_multivector_multiplications.py ${OUTPUT_DIR}
    DEPENDS generate_multivector_multiplications.py helpers.py
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the Multivector multiplication bindings"
    VERBATIM
)

add_custom_target(generate_multivector_multiplications DEPENDS ${MULTIVECTOR_PRODUCTS_SRCS})
add_dependencies(generate_multivector_multiplications make_generated_directory)


# Geometric product Caley table
add_custom_command(
    OUTPUT ${OUTPUT_DIR}/geometricproductcayleytable.py
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_caleytable.py ${CMAKE_SOURCE_DIR}/dependencies/gafro/src/gafro/algebra/expressions/GeometricProductCayleyTable.hpp ${OUTPUT_DIR} "CayleyTable"
    DEPENDS generate_caleytable.py helpers.py ${CMAKE_SOURCE_DIR}/dependencies/gafro/src/gafro/algebra/expressions/GeometricProductCayleyTable.hpp
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the Geometric product Caley table"
    VERBATIM
)

add_custom_target(generate_geometric_product_caley_table DEPENDS ${OUTPUT_DIR}/geometricproductcayleytable.py)
add_dependencies(generate_geometric_product_caley_table make_generated_directory)


# Inner product Caley table
add_custom_command(
    OUTPUT ${OUTPUT_DIR}/innerproductcayleytable.py
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_caleytable.py ${CMAKE_SOURCE_DIR}/dependencies/gafro/src/gafro/algebra/expressions/InnerProductCayleyTable.hpp ${OUTPUT_DIR} "InnerProductCayleyTable"
    DEPENDS generate_caleytable.py helpers.py ${CMAKE_SOURCE_DIR}/dependencies/gafro/src/gafro/algebra/expressions/InnerProductCayleyTable.hpp
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the Inner product Caley table"
    VERBATIM
)

add_custom_target(generate_inner_product_caley_table DEPENDS ${OUTPUT_DIR}/innerproductcayleytable.py)
add_dependencies(generate_inner_product_caley_table make_generated_directory)


# Outer product Caley table
add_custom_command(
    OUTPUT ${OUTPUT_DIR}/outerproductcayleytable.py
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_caleytable.py ${CMAKE_SOURCE_DIR}/dependencies/gafro/src/gafro/algebra/expressions/OuterProductCayleyTable.hpp ${OUTPUT_DIR} "OuterProductCayleyTable"
    DEPENDS generate_caleytable.py helpers.py ${CMAKE_SOURCE_DIR}/dependencies/gafro/src/gafro/algebra/expressions/OuterProductCayleyTable.hpp
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the Outer product Caley table"
    VERBATIM
)

add_custom_target(generate_outer_product_caley_table DEPENDS ${OUTPUT_DIR}/outerproductcayleytable.py)
add_dependencies(generate_outer_product_caley_table make_generated_directory)


# Motor apply methods
set(MOTOR_APPLY_METHODS_SRCS
    ${OUTPUT_DIR}/motor_apply_methods.cpp
    ${OUTPUT_DIR}/motor_apply_methods_0.cpp
    ${OUTPUT_DIR}/motor_apply_methods_3.cpp
    ${OUTPUT_DIR}/motor_apply_methods_6.cpp
    ${OUTPUT_DIR}/motor_apply_methods_9.cpp
    ${OUTPUT_DIR}/motor_apply_methods_12.cpp
    ${OUTPUT_DIR}/motor_apply_methods_15.cpp
    ${OUTPUT_DIR}/motor_apply_methods_18.cpp
    ${OUTPUT_DIR}/motor_apply_methods_21.cpp
    ${OUTPUT_DIR}/motor_apply_methods_24.cpp
    ${OUTPUT_DIR}/motor_apply_methods_27.cpp
    ${OUTPUT_DIR}/motor_apply_methods_30.cpp
    ${OUTPUT_DIR}/motor_apply_methods_33.cpp
    ${OUTPUT_DIR}/motor_apply_methods_36.cpp
    ${OUTPUT_DIR}/motor_apply_methods_39.cpp
    ${OUTPUT_DIR}/motor_apply_methods_42.cpp
    ${OUTPUT_DIR}/motor_apply_methods_45.cpp

    CACHE INTERNAL "MOTOR_APPLY_METHODS_SRCS"
)

add_custom_command(
    OUTPUT ${MOTOR_APPLY_METHODS_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_motor_apply_methods.py ${OUTPUT_DIR}
    DEPENDS generate_motor_apply_methods.py helpers.py
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the motor apply methods"
    VERBATIM
)

add_custom_target(generate_motor_apply_methods DEPENDS ${MOTOR_APPLY_METHODS_SRCS})
add_dependencies(generate_motor_apply_methods make_generated_directory)


# Rotor apply methods
set(ROTOR_APPLY_METHODS_SRCS
    ${OUTPUT_DIR}/rotor_apply_methods.cpp
    ${OUTPUT_DIR}/rotor_apply_methods_0.cpp
    ${OUTPUT_DIR}/rotor_apply_methods_3.cpp
    ${OUTPUT_DIR}/rotor_apply_methods_6.cpp
    ${OUTPUT_DIR}/rotor_apply_methods_9.cpp
    ${OUTPUT_DIR}/rotor_apply_methods_12.cpp
    ${OUTPUT_DIR}/rotor_apply_methods_15.cpp
    ${OUTPUT_DIR}/rotor_apply_methods_18.cpp
    ${OUTPUT_DIR}/rotor_apply_methods_21.cpp
    ${OUTPUT_DIR}/rotor_apply_methods_24.cpp
    ${OUTPUT_DIR}/rotor_apply_methods_27.cpp
    ${OUTPUT_DIR}/rotor_apply_methods_30.cpp
    ${OUTPUT_DIR}/rotor_apply_methods_33.cpp
    ${OUTPUT_DIR}/rotor_apply_methods_36.cpp
    ${OUTPUT_DIR}/rotor_apply_methods_39.cpp
    ${OUTPUT_DIR}/rotor_apply_methods_42.cpp
    ${OUTPUT_DIR}/rotor_apply_methods_45.cpp

    CACHE INTERNAL "ROTOR_APPLY_METHODS_SRCS"
)

add_custom_command(
    OUTPUT ${ROTOR_APPLY_METHODS_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_rotor_apply_methods.py ${OUTPUT_DIR}
    DEPENDS generate_rotor_apply_methods.py helpers.py
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the motor apply methods"
    VERBATIM
)

add_custom_target(generate_rotor_apply_methods DEPENDS ${ROTOR_APPLY_METHODS_SRCS})
add_dependencies(generate_rotor_apply_methods make_generated_directory)


# Manipulators
set(MANIPULATORS_SRCS
    ${OUTPUT_DIR}/manipulators.h
    ${OUTPUT_DIR}/manipulators.hpp

    CACHE INTERNAL "MANIPULATORS_SRCS"
)

add_custom_command(
    OUTPUT ${MANIPULATORS_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_manipulators.py ${OUTPUT_DIR}
    DEPENDS generate_manipulators.py helpers.py templates/manipulators.h templates/manipulators.hpp
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the Manipulator bindings"
    VERBATIM
)

add_custom_target(generate_manipulators DEPENDS ${MANIPULATORS_SRCS})
add_dependencies(generate_manipulators make_generated_directory)


add_custom_target(generate_bindings)
add_dependencies(generate_bindings
    generate_geometric_product_caley_table
    generate_inner_product_caley_table
    generate_manipulators
    generate_motor_apply_methods
    generate_multivectors
    generate_multivector_multiplications
    generate_outer_product_caley_table
    generate_rotor_apply_methods
)
