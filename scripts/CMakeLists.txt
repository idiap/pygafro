#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: MPL-2.0
#

set(OUTPUT_DIR ${CMAKE_BINARY_DIR}/generated)

add_custom_target(make_generated_directory ALL
    COMMAND ${CMAKE_COMMAND} -E make_directory ${OUTPUT_DIR}
    COMMAND ${CMAKE_COMMAND} -E make_directory ${OUTPUT_DIR}/algebra
    COMMAND ${CMAKE_COMMAND} -E make_directory ${OUTPUT_DIR}/optimization
    COMMAND ${CMAKE_COMMAND} -E make_directory ${OUTPUT_DIR}/robots
)


# Multivectors
set(MULTIVECTOR_SRCS
    ${OUTPUT_DIR}/algebra/multivectors.h
    ${OUTPUT_DIR}/algebra/multivectors.cpp
    ${OUTPUT_DIR}/algebra/mv_combinations.py

    ${OUTPUT_DIR}/algebra/multivectors_0.cpp
    ${OUTPUT_DIR}/algebra/multivectors_1.cpp
    ${OUTPUT_DIR}/algebra/multivectors_2.cpp
    ${OUTPUT_DIR}/algebra/multivectors_3.cpp
    ${OUTPUT_DIR}/algebra/multivectors_4.cpp
    ${OUTPUT_DIR}/algebra/multivectors_5.cpp
    ${OUTPUT_DIR}/algebra/multivectors_6.cpp
    ${OUTPUT_DIR}/algebra/multivectors_7.cpp
    ${OUTPUT_DIR}/algebra/multivectors_8.cpp
    ${OUTPUT_DIR}/algebra/multivectors_9.cpp
    ${OUTPUT_DIR}/algebra/multivectors_10.cpp
    ${OUTPUT_DIR}/algebra/multivectors_11.cpp
    ${OUTPUT_DIR}/algebra/multivectors_12.cpp
    ${OUTPUT_DIR}/algebra/multivectors_13.cpp
    ${OUTPUT_DIR}/algebra/multivectors_14.cpp
    ${OUTPUT_DIR}/algebra/multivectors_15.cpp
    ${OUTPUT_DIR}/algebra/multivectors_16.cpp
    ${OUTPUT_DIR}/algebra/multivectors_17.cpp
    ${OUTPUT_DIR}/algebra/multivectors_18.cpp

    CACHE INTERNAL "MULTIVECTOR_SRCS"
)

add_custom_command(
    OUTPUT ${MULTIVECTOR_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_multivectors.py ${OUTPUT_DIR}/algebra
    DEPENDS generate_multivectors.py helpers.py templates/multivectors.h templates/multivectors.hpp
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the Multivector bindings"
    VERBATIM
)

add_custom_target(generate_multivectors DEPENDS ${MULTIVECTOR_SRCS})
add_dependencies(generate_multivectors make_generated_directory)


# Multivectors multiplications
set(MULTIVECTOR_PRODUCTS_SRCS
    ${OUTPUT_DIR}/algebra/geometric_products.cpp
    ${OUTPUT_DIR}/algebra/inner_products.cpp
    ${OUTPUT_DIR}/algebra/outer_products.cpp

    ${OUTPUT_DIR}/algebra/geometric_products_0.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_1.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_2.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_3.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_4.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_5.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_6.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_7.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_8.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_9.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_10.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_11.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_12.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_13.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_14.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_15.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_16.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_17.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_18.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_19.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_20.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_21.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_22.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_23.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_24.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_25.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_26.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_27.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_28.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_29.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_30.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_31.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_32.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_33.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_34.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_35.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_36.cpp
    ${OUTPUT_DIR}/algebra/geometric_products_37.cpp

    ${OUTPUT_DIR}/algebra/inner_products_0.cpp
    ${OUTPUT_DIR}/algebra/inner_products_1.cpp
    ${OUTPUT_DIR}/algebra/inner_products_2.cpp
    ${OUTPUT_DIR}/algebra/inner_products_3.cpp
    ${OUTPUT_DIR}/algebra/inner_products_4.cpp
    ${OUTPUT_DIR}/algebra/inner_products_5.cpp
    ${OUTPUT_DIR}/algebra/inner_products_6.cpp
    ${OUTPUT_DIR}/algebra/inner_products_7.cpp
    ${OUTPUT_DIR}/algebra/inner_products_8.cpp
    ${OUTPUT_DIR}/algebra/inner_products_9.cpp
    ${OUTPUT_DIR}/algebra/inner_products_10.cpp
    ${OUTPUT_DIR}/algebra/inner_products_11.cpp
    ${OUTPUT_DIR}/algebra/inner_products_12.cpp
    ${OUTPUT_DIR}/algebra/inner_products_13.cpp
    ${OUTPUT_DIR}/algebra/inner_products_14.cpp
    ${OUTPUT_DIR}/algebra/inner_products_15.cpp
    ${OUTPUT_DIR}/algebra/inner_products_16.cpp
    ${OUTPUT_DIR}/algebra/inner_products_17.cpp
    ${OUTPUT_DIR}/algebra/inner_products_18.cpp
    ${OUTPUT_DIR}/algebra/inner_products_19.cpp
    ${OUTPUT_DIR}/algebra/inner_products_20.cpp
    ${OUTPUT_DIR}/algebra/inner_products_21.cpp
    ${OUTPUT_DIR}/algebra/inner_products_22.cpp
    ${OUTPUT_DIR}/algebra/inner_products_23.cpp
    ${OUTPUT_DIR}/algebra/inner_products_24.cpp
    ${OUTPUT_DIR}/algebra/inner_products_25.cpp
    ${OUTPUT_DIR}/algebra/inner_products_26.cpp
    ${OUTPUT_DIR}/algebra/inner_products_27.cpp
    ${OUTPUT_DIR}/algebra/inner_products_28.cpp
    ${OUTPUT_DIR}/algebra/inner_products_29.cpp
    ${OUTPUT_DIR}/algebra/inner_products_30.cpp
    ${OUTPUT_DIR}/algebra/inner_products_31.cpp
    ${OUTPUT_DIR}/algebra/inner_products_32.cpp
    ${OUTPUT_DIR}/algebra/inner_products_33.cpp
    ${OUTPUT_DIR}/algebra/inner_products_34.cpp
    ${OUTPUT_DIR}/algebra/inner_products_35.cpp
    ${OUTPUT_DIR}/algebra/inner_products_36.cpp
    ${OUTPUT_DIR}/algebra/inner_products_37.cpp

    ${OUTPUT_DIR}/algebra/outer_products_0.cpp
    ${OUTPUT_DIR}/algebra/outer_products_1.cpp
    ${OUTPUT_DIR}/algebra/outer_products_2.cpp
    ${OUTPUT_DIR}/algebra/outer_products_3.cpp
    ${OUTPUT_DIR}/algebra/outer_products_4.cpp
    ${OUTPUT_DIR}/algebra/outer_products_5.cpp
    ${OUTPUT_DIR}/algebra/outer_products_6.cpp
    ${OUTPUT_DIR}/algebra/outer_products_7.cpp
    ${OUTPUT_DIR}/algebra/outer_products_8.cpp
    ${OUTPUT_DIR}/algebra/outer_products_9.cpp
    ${OUTPUT_DIR}/algebra/outer_products_10.cpp
    ${OUTPUT_DIR}/algebra/outer_products_11.cpp
    ${OUTPUT_DIR}/algebra/outer_products_12.cpp
    ${OUTPUT_DIR}/algebra/outer_products_13.cpp
    ${OUTPUT_DIR}/algebra/outer_products_14.cpp
    ${OUTPUT_DIR}/algebra/outer_products_15.cpp
    ${OUTPUT_DIR}/algebra/outer_products_16.cpp
    ${OUTPUT_DIR}/algebra/outer_products_17.cpp
    ${OUTPUT_DIR}/algebra/outer_products_18.cpp
    ${OUTPUT_DIR}/algebra/outer_products_19.cpp
    ${OUTPUT_DIR}/algebra/outer_products_20.cpp
    ${OUTPUT_DIR}/algebra/outer_products_21.cpp
    ${OUTPUT_DIR}/algebra/outer_products_22.cpp
    ${OUTPUT_DIR}/algebra/outer_products_23.cpp
    ${OUTPUT_DIR}/algebra/outer_products_24.cpp
    ${OUTPUT_DIR}/algebra/outer_products_25.cpp
    ${OUTPUT_DIR}/algebra/outer_products_26.cpp
    ${OUTPUT_DIR}/algebra/outer_products_27.cpp
    ${OUTPUT_DIR}/algebra/outer_products_28.cpp
    ${OUTPUT_DIR}/algebra/outer_products_29.cpp
    ${OUTPUT_DIR}/algebra/outer_products_30.cpp
    ${OUTPUT_DIR}/algebra/outer_products_31.cpp
    ${OUTPUT_DIR}/algebra/outer_products_32.cpp
    ${OUTPUT_DIR}/algebra/outer_products_33.cpp
    ${OUTPUT_DIR}/algebra/outer_products_34.cpp
    ${OUTPUT_DIR}/algebra/outer_products_35.cpp
    ${OUTPUT_DIR}/algebra/outer_products_36.cpp
    ${OUTPUT_DIR}/algebra/outer_products_37.cpp

    CACHE INTERNAL "MULTIVECTOR_PRODUCTS_SRCS"
)

add_custom_command(
    OUTPUT ${MULTIVECTOR_PRODUCTS_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_multivector_multiplications.py ${OUTPUT_DIR}/algebra
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
    ${OUTPUT_DIR}/algebra/motor_apply_methods.cpp
    ${OUTPUT_DIR}/algebra/motor_apply_methods_0.cpp
    ${OUTPUT_DIR}/algebra/motor_apply_methods_1.cpp
    ${OUTPUT_DIR}/algebra/motor_apply_methods_2.cpp
    ${OUTPUT_DIR}/algebra/motor_apply_methods_3.cpp
    ${OUTPUT_DIR}/algebra/motor_apply_methods_4.cpp
    ${OUTPUT_DIR}/algebra/motor_apply_methods_5.cpp
    ${OUTPUT_DIR}/algebra/motor_apply_methods_6.cpp
    ${OUTPUT_DIR}/algebra/motor_apply_methods_7.cpp
    ${OUTPUT_DIR}/algebra/motor_apply_methods_8.cpp
    ${OUTPUT_DIR}/algebra/motor_apply_methods_9.cpp
    ${OUTPUT_DIR}/algebra/motor_apply_methods_10.cpp
    ${OUTPUT_DIR}/algebra/motor_apply_methods_11.cpp
    ${OUTPUT_DIR}/algebra/motor_apply_methods_12.cpp
    ${OUTPUT_DIR}/algebra/motor_apply_methods_13.cpp
    ${OUTPUT_DIR}/algebra/motor_apply_methods_14.cpp
    ${OUTPUT_DIR}/algebra/motor_apply_methods_15.cpp
    ${OUTPUT_DIR}/algebra/motor_apply_methods_16.cpp
    ${OUTPUT_DIR}/algebra/motor_apply_methods_17.cpp
    ${OUTPUT_DIR}/algebra/motor_apply_methods_18.cpp

    CACHE INTERNAL "MOTOR_APPLY_METHODS_SRCS"
)

add_custom_command(
    OUTPUT ${MOTOR_APPLY_METHODS_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_motor_apply_methods.py ${OUTPUT_DIR}/algebra
    DEPENDS generate_motor_apply_methods.py helpers.py
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the motor apply methods"
    VERBATIM
)

add_custom_target(generate_motor_apply_methods DEPENDS ${MOTOR_APPLY_METHODS_SRCS})
add_dependencies(generate_motor_apply_methods make_generated_directory)


# Rotor apply methods
set(ROTOR_APPLY_METHODS_SRCS
    ${OUTPUT_DIR}/algebra/rotor_apply_methods.cpp
    ${OUTPUT_DIR}/algebra/rotor_apply_methods_0.cpp
    ${OUTPUT_DIR}/algebra/rotor_apply_methods_1.cpp
    ${OUTPUT_DIR}/algebra/rotor_apply_methods_2.cpp
    ${OUTPUT_DIR}/algebra/rotor_apply_methods_3.cpp
    ${OUTPUT_DIR}/algebra/rotor_apply_methods_4.cpp
    ${OUTPUT_DIR}/algebra/rotor_apply_methods_5.cpp
    ${OUTPUT_DIR}/algebra/rotor_apply_methods_6.cpp
    ${OUTPUT_DIR}/algebra/rotor_apply_methods_7.cpp
    ${OUTPUT_DIR}/algebra/rotor_apply_methods_8.cpp
    ${OUTPUT_DIR}/algebra/rotor_apply_methods_9.cpp
    ${OUTPUT_DIR}/algebra/rotor_apply_methods_10.cpp
    ${OUTPUT_DIR}/algebra/rotor_apply_methods_11.cpp
    ${OUTPUT_DIR}/algebra/rotor_apply_methods_12.cpp
    ${OUTPUT_DIR}/algebra/rotor_apply_methods_13.cpp
    ${OUTPUT_DIR}/algebra/rotor_apply_methods_14.cpp
    ${OUTPUT_DIR}/algebra/rotor_apply_methods_15.cpp
    ${OUTPUT_DIR}/algebra/rotor_apply_methods_16.cpp
    ${OUTPUT_DIR}/algebra/rotor_apply_methods_17.cpp
    ${OUTPUT_DIR}/algebra/rotor_apply_methods_18.cpp

    CACHE INTERNAL "ROTOR_APPLY_METHODS_SRCS"
)

add_custom_command(
    OUTPUT ${ROTOR_APPLY_METHODS_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_rotor_apply_methods.py ${OUTPUT_DIR}/algebra
    DEPENDS generate_rotor_apply_methods.py helpers.py
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the rotor apply methods"
    VERBATIM
)

add_custom_target(generate_rotor_apply_methods DEPENDS ${ROTOR_APPLY_METHODS_SRCS})
add_dependencies(generate_rotor_apply_methods make_generated_directory)


# Manipulators
set(MANIPULATORS_SRCS
    ${OUTPUT_DIR}/robots/manipulators.h
    ${OUTPUT_DIR}/robots/manipulators.hpp

    CACHE INTERNAL "MANIPULATORS_SRCS"
)

add_custom_command(
    OUTPUT ${MANIPULATORS_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_manipulators.py ${OUTPUT_DIR}/robots
    DEPENDS generate_manipulators.py helpers.py templates/manipulators.h templates/manipulators.hpp
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the Manipulator bindings"
    VERBATIM
)

add_custom_target(generate_manipulators DEPENDS ${MANIPULATORS_SRCS})
add_dependencies(generate_manipulators make_generated_directory)


# Quadrupeds
set(QUADRUPEDS_SRCS
    ${OUTPUT_DIR}/robots/quadrupeds.h
    ${OUTPUT_DIR}/robots/quadrupeds.hpp

    CACHE INTERNAL "QUADRUPEDS_SRCS"
)

add_custom_command(
    OUTPUT ${QUADRUPEDS_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_quadrupeds.py ${OUTPUT_DIR}/robots
    DEPENDS generate_quadrupeds.py helpers.py templates/quadrupeds.h templates/quadrupeds.hpp
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the Quadruped bindings"
    VERBATIM
)

add_custom_target(generate_quadrupeds DEPENDS ${QUADRUPEDS_SRCS})
add_dependencies(generate_quadrupeds make_generated_directory)


# Hands
set(HANDS_SRCS
    ${OUTPUT_DIR}/robots/hands.h
    ${OUTPUT_DIR}/robots/hands.hpp

    CACHE INTERNAL "HANDS_SRCS"
)

add_custom_command(
    OUTPUT ${HANDS_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_hands.py ${OUTPUT_DIR}/robots
    DEPENDS generate_hands.py helpers.py templates/hands.h templates/hands.hpp
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Generation of the Hand bindings"
    VERBATIM
)

add_custom_target(generate_hands DEPENDS ${HANDS_SRCS})
add_dependencies(generate_hands make_generated_directory)


# SingleManipulatorTargets
set(SINGLEMANIPULATORTARGETS_SRCS
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets.h
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets.cpp

    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_0.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_1.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_2.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_3.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_4.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_5.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_6.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_7.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_8.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_9.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_10.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_11.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_12.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_13.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_14.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_15.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_16.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_17.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_18.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_19.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_20.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_21.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_22.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_23.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_24.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_25.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_26.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_27.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_28.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_29.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_30.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_31.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_32.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_33.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_34.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_35.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_36.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_37.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_38.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_39.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_40.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_41.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_42.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_43.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_44.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_45.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_46.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_47.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_48.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_49.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_50.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_51.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_52.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_53.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_54.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_55.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_56.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_57.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_58.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_59.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatortargets_60.cpp

    CACHE INTERNAL "SINGLEMANIPULATORTARGETS_SRCS"
)

add_custom_command(
    OUTPUT ${SINGLEMANIPULATORTARGETS_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_singlemanipulatortargets.py ${OUTPUT_DIR}/optimization
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
    ${OUTPUT_DIR}/optimization/singlemanipulatormotorcosts.h
    ${OUTPUT_DIR}/optimization/singlemanipulatormotorcosts.cpp

    CACHE INTERNAL "SINGLEMANIPULATORMOTORCOSTS_SRCS"
)

add_custom_command(
    OUTPUT ${SINGLEMANIPULATORMOTORCOSTS_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_singlemanipulatormotorcosts.py ${OUTPUT_DIR}/optimization
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
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets.h
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets.cpp

    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_0.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_1.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_2.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_3.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_4.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_5.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_6.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_7.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_8.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_9.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_10.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_11.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_12.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_13.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_14.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_15.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_16.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_17.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_18.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_19.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_20.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_21.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_22.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_23.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_24.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_25.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_26.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_27.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_28.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_29.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_30.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_31.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_32.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_33.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_34.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_35.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_36.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_37.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_38.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_39.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_40.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_41.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_42.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_43.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_44.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_45.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_46.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_47.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_48.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_49.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_50.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_51.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_52.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_53.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_54.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_55.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_56.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_57.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_58.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_59.cpp
    ${OUTPUT_DIR}/optimization/singlemanipulatordualtargets_60.cpp

    CACHE INTERNAL "SINGLEMANIPULATORDUALTARGETS_SRCS"
)

add_custom_command(
    OUTPUT ${SINGLEMANIPULATORDUALTARGETS_SRCS}
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generate_singlemanipulatordualtargets.py ${OUTPUT_DIR}/optimization
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
