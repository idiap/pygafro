#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: MPL-2.0
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
    ${OUTPUT_DIR}/geometric_products_1.cpp
    ${OUTPUT_DIR}/geometric_products_2.cpp
    ${OUTPUT_DIR}/geometric_products_3.cpp
    ${OUTPUT_DIR}/geometric_products_4.cpp
    ${OUTPUT_DIR}/geometric_products_5.cpp
    ${OUTPUT_DIR}/geometric_products_6.cpp
    ${OUTPUT_DIR}/geometric_products_7.cpp
    ${OUTPUT_DIR}/geometric_products_8.cpp
    ${OUTPUT_DIR}/geometric_products_9.cpp
    ${OUTPUT_DIR}/geometric_products_10.cpp
    ${OUTPUT_DIR}/geometric_products_11.cpp
    ${OUTPUT_DIR}/geometric_products_12.cpp
    ${OUTPUT_DIR}/geometric_products_13.cpp
    ${OUTPUT_DIR}/geometric_products_14.cpp
    ${OUTPUT_DIR}/geometric_products_15.cpp
    ${OUTPUT_DIR}/geometric_products_16.cpp
    ${OUTPUT_DIR}/geometric_products_17.cpp
    ${OUTPUT_DIR}/geometric_products_18.cpp
    ${OUTPUT_DIR}/geometric_products_19.cpp
    ${OUTPUT_DIR}/geometric_products_20.cpp
    ${OUTPUT_DIR}/geometric_products_21.cpp
    ${OUTPUT_DIR}/geometric_products_22.cpp
    ${OUTPUT_DIR}/geometric_products_23.cpp
    ${OUTPUT_DIR}/geometric_products_24.cpp
    ${OUTPUT_DIR}/geometric_products_25.cpp
    ${OUTPUT_DIR}/geometric_products_26.cpp
    ${OUTPUT_DIR}/geometric_products_27.cpp
    ${OUTPUT_DIR}/geometric_products_28.cpp
    ${OUTPUT_DIR}/geometric_products_29.cpp

    ${OUTPUT_DIR}/inner_products_0.cpp
    ${OUTPUT_DIR}/inner_products_1.cpp
    ${OUTPUT_DIR}/inner_products_2.cpp
    ${OUTPUT_DIR}/inner_products_3.cpp
    ${OUTPUT_DIR}/inner_products_4.cpp
    ${OUTPUT_DIR}/inner_products_5.cpp
    ${OUTPUT_DIR}/inner_products_6.cpp
    ${OUTPUT_DIR}/inner_products_7.cpp
    ${OUTPUT_DIR}/inner_products_8.cpp
    ${OUTPUT_DIR}/inner_products_9.cpp
    ${OUTPUT_DIR}/inner_products_10.cpp
    ${OUTPUT_DIR}/inner_products_11.cpp
    ${OUTPUT_DIR}/inner_products_12.cpp
    ${OUTPUT_DIR}/inner_products_13.cpp
    ${OUTPUT_DIR}/inner_products_14.cpp
    ${OUTPUT_DIR}/inner_products_15.cpp
    ${OUTPUT_DIR}/inner_products_16.cpp
    ${OUTPUT_DIR}/inner_products_17.cpp
    ${OUTPUT_DIR}/inner_products_18.cpp
    ${OUTPUT_DIR}/inner_products_19.cpp
    ${OUTPUT_DIR}/inner_products_20.cpp
    ${OUTPUT_DIR}/inner_products_21.cpp
    ${OUTPUT_DIR}/inner_products_22.cpp
    ${OUTPUT_DIR}/inner_products_23.cpp
    ${OUTPUT_DIR}/inner_products_24.cpp
    ${OUTPUT_DIR}/inner_products_25.cpp
    ${OUTPUT_DIR}/inner_products_26.cpp
    ${OUTPUT_DIR}/inner_products_27.cpp
    ${OUTPUT_DIR}/inner_products_28.cpp
    ${OUTPUT_DIR}/inner_products_29.cpp

    ${OUTPUT_DIR}/outer_products_0.cpp
    ${OUTPUT_DIR}/outer_products_1.cpp
    ${OUTPUT_DIR}/outer_products_2.cpp
    ${OUTPUT_DIR}/outer_products_3.cpp
    ${OUTPUT_DIR}/outer_products_4.cpp
    ${OUTPUT_DIR}/outer_products_5.cpp
    ${OUTPUT_DIR}/outer_products_6.cpp
    ${OUTPUT_DIR}/outer_products_7.cpp
    ${OUTPUT_DIR}/outer_products_8.cpp
    ${OUTPUT_DIR}/outer_products_9.cpp
    ${OUTPUT_DIR}/outer_products_10.cpp
    ${OUTPUT_DIR}/outer_products_11.cpp
    ${OUTPUT_DIR}/outer_products_12.cpp
    ${OUTPUT_DIR}/outer_products_13.cpp
    ${OUTPUT_DIR}/outer_products_14.cpp
    ${OUTPUT_DIR}/outer_products_15.cpp
    ${OUTPUT_DIR}/outer_products_16.cpp
    ${OUTPUT_DIR}/outer_products_17.cpp
    ${OUTPUT_DIR}/outer_products_18.cpp
    ${OUTPUT_DIR}/outer_products_19.cpp
    ${OUTPUT_DIR}/outer_products_20.cpp
    ${OUTPUT_DIR}/outer_products_21.cpp
    ${OUTPUT_DIR}/outer_products_22.cpp
    ${OUTPUT_DIR}/outer_products_23.cpp
    ${OUTPUT_DIR}/outer_products_24.cpp
    ${OUTPUT_DIR}/outer_products_25.cpp
    ${OUTPUT_DIR}/outer_products_26.cpp
    ${OUTPUT_DIR}/outer_products_27.cpp
    ${OUTPUT_DIR}/outer_products_28.cpp
    ${OUTPUT_DIR}/outer_products_29.cpp

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
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_caleytable.py ${CMAKE_CURRENT_SOURCE_DIR}/templates/geometricproductcayleytable.py ${OUTPUT_DIR}
    DEPENDS generate_caleytable.py helpers.py ${CMAKE_CURRENT_SOURCE_DIR}/templates/geometricproductcayleytable.py
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the Geometric product Caley table"
    VERBATIM
)

add_custom_target(generate_geometric_product_caley_table DEPENDS ${OUTPUT_DIR}/geometricproductcayleytable.py)
add_dependencies(generate_geometric_product_caley_table make_generated_directory)


# Inner product Caley table
add_custom_command(
    OUTPUT ${OUTPUT_DIR}/innerproductcayleytable.py
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_caleytable.py ${CMAKE_CURRENT_SOURCE_DIR}/templates/innerproductcayleytable.py ${OUTPUT_DIR}
    DEPENDS generate_caleytable.py helpers.py ${CMAKE_CURRENT_SOURCE_DIR}/templates/innerproductcayleytable.py
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the Inner product Caley table"
    VERBATIM
)

add_custom_target(generate_inner_product_caley_table DEPENDS ${OUTPUT_DIR}/innerproductcayleytable.py)
add_dependencies(generate_inner_product_caley_table make_generated_directory)


# Outer product Caley table
add_custom_command(
    OUTPUT ${OUTPUT_DIR}/outerproductcayleytable.py
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_caleytable.py ${CMAKE_CURRENT_SOURCE_DIR}/templates/outerproductcayleytable.py ${OUTPUT_DIR}
    DEPENDS generate_caleytable.py helpers.py ${CMAKE_CURRENT_SOURCE_DIR}/templates/outerproductcayleytable.py
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
    COMMENT "Generation of the rotor apply methods"
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


# Quadrupeds
set(QUADRUPEDS_SRCS
    ${OUTPUT_DIR}/quadrupeds.h
    ${OUTPUT_DIR}/quadrupeds.hpp

    CACHE INTERNAL "QUADRUPEDS_SRCS"
)

add_custom_command(
    OUTPUT ${QUADRUPEDS_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_quadrupeds.py ${OUTPUT_DIR}
    DEPENDS generate_quadrupeds.py helpers.py templates/quadrupeds.h templates/quadrupeds.hpp
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the Quadruped bindings"
    VERBATIM
)

add_custom_target(generate_quadrupeds DEPENDS ${QUADRUPEDS_SRCS})
add_dependencies(generate_quadrupeds make_generated_directory)


# Hands
set(HANDS_SRCS
    ${OUTPUT_DIR}/hands.h
    ${OUTPUT_DIR}/hands.hpp

    CACHE INTERNAL "HANDS_SRCS"
)

add_custom_command(
    OUTPUT ${HANDS_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_hands.py ${OUTPUT_DIR}
    DEPENDS generate_hands.py helpers.py templates/hands.h templates/hands.hpp
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the Hand bindings"
    VERBATIM
)

add_custom_target(generate_hands DEPENDS ${HANDS_SRCS})
add_dependencies(generate_hands make_generated_directory)


# SingleManipulatorTargets
set(SINGLEMANIPULATORTARGETS_SRCS
    ${OUTPUT_DIR}/singlemanipulatortargets.h
    ${OUTPUT_DIR}/singlemanipulatortargets.cpp

    ${OUTPUT_DIR}/singlemanipulatortargets_0.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_1.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_2.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_3.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_4.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_5.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_6.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_7.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_8.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_9.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_10.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_11.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_12.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_13.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_14.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_15.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_16.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_17.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_18.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_19.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_20.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_21.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_22.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_23.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_24.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_25.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_26.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_27.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_28.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_29.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_30.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_31.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_32.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_33.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_34.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_35.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_36.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_37.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_38.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_39.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_40.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_41.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_42.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_43.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_44.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_45.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_46.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_47.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_48.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_49.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_50.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_51.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_52.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_53.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_54.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_55.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_56.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_57.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_58.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_59.cpp
    ${OUTPUT_DIR}/singlemanipulatortargets_60.cpp

    CACHE INTERNAL "SINGLEMANIPULATORTARGETS_SRCS"
)

add_custom_command(
    OUTPUT ${SINGLEMANIPULATORTARGETS_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_singlemanipulatortargets.py ${OUTPUT_DIR}
    DEPENDS generate_singlemanipulatortargets.py helpers.py templates/singlemanipulatortargets.h
            templates/singlemanipulatortargets.hpp templates/singlemanipulatortargets_functions.hpp
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the SingleManipulatorTarget bindings"
    VERBATIM
)

add_custom_target(generate_singlemanipulatortargets DEPENDS ${SINGLEMANIPULATORTARGETS_SRCS})
add_dependencies(generate_singlemanipulatortargets make_generated_directory)


# SingleManipulatorMotorCosts
set(SINGLEMANIPULATORMOTORCOSTS_SRCS
    ${OUTPUT_DIR}/singlemanipulatormotorcosts.h
    ${OUTPUT_DIR}/singlemanipulatormotorcosts.cpp

    CACHE INTERNAL "SINGLEMANIPULATORMOTORCOSTS_SRCS"
)

add_custom_command(
    OUTPUT ${SINGLEMANIPULATORMOTORCOSTS_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_singlemanipulatormotorcosts.py ${OUTPUT_DIR}
    DEPENDS generate_singlemanipulatormotorcosts.py helpers.py templates/singlemanipulatormotorcosts.h
            templates/singlemanipulatormotorcosts.hpp templates/singlemanipulatormotorcosts_functions.hpp
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the SingleManipulatorMotoCost bindings"
    VERBATIM
)

add_custom_target(generate_singlemanipulatormotorcosts DEPENDS ${SINGLEMANIPULATORMOTORCOSTS_SRCS})
add_dependencies(generate_singlemanipulatormotorcosts make_generated_directory)


# SingleManipulatorDualTargets
set(SINGLEMANIPULATORDUALTARGETS_SRCS
    ${OUTPUT_DIR}/singlemanipulatordualtargets.h
    ${OUTPUT_DIR}/singlemanipulatordualtargets.cpp

    ${OUTPUT_DIR}/singlemanipulatordualtargets_0.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_1.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_2.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_3.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_4.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_5.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_6.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_7.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_8.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_9.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_10.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_11.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_12.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_13.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_14.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_15.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_16.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_17.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_18.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_19.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_20.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_21.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_22.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_23.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_24.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_25.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_26.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_27.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_28.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_29.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_30.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_31.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_32.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_33.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_34.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_35.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_36.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_37.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_38.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_39.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_40.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_41.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_42.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_43.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_44.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_45.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_46.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_47.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_48.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_49.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_50.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_51.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_52.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_53.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_54.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_55.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_56.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_57.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_58.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_59.cpp
    ${OUTPUT_DIR}/singlemanipulatordualtargets_60.cpp

    CACHE INTERNAL "SINGLEMANIPULATORDUALTARGETS_SRCS"
)

add_custom_command(
    OUTPUT ${SINGLEMANIPULATORDUALTARGETS_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_singlemanipulatordualtargets.py ${OUTPUT_DIR}
    DEPENDS generate_singlemanipulatordualtargets.py helpers.py templates/singlemanipulatordualtargets.h
            templates/singlemanipulatordualtargets.hpp templates/singlemanipulatordualtargets_functions.hpp
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the SingleManipulatorDualTarget bindings"
    VERBATIM
)

add_custom_target(generate_singlemanipulatordualtargets DEPENDS ${SINGLEMANIPULATORDUALTARGETS_SRCS})
add_dependencies(generate_singlemanipulatordualtargets make_generated_directory)


add_custom_target(generate_bindings)
add_dependencies(generate_bindings
    generate_geometric_product_caley_table
    generate_inner_product_caley_table
    generate_manipulators
    generate_quadrupeds
    generate_hands
    generate_motor_apply_methods
    generate_multivectors
    generate_multivector_multiplications
    generate_outer_product_caley_table
    generate_rotor_apply_methods
    generate_singlemanipulatortargets
    generate_singlemanipulatormotorcosts
    generate_singlemanipulatordualtargets
)
