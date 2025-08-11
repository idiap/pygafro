#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: MPL-2.0
#

import os
import sys

import helpers


def generate_file(filename, multivectors, function_name):
    with open(filename, "w") as output:
        output.write(
            f"""// This file is auto-generated

#include <pybind11/pybind11.h>

#include <gafro/gafro.hpp>


namespace py = pybind11;
using namespace gafro;

#include "multivectors.h"
#include "algebra/rotor_utils.hpp"


void {function_name}(py::class_<gafro::Rotor<double>, Multivector_scalare12e13e23> &c)
{{
"""
        )
        for mv in multivectors:
            output.write(f'    c.def("apply", &rotor_apply<{mv}>);\n')

        output.write("}\n")


def generate_index_file(filename, function_name, count):
    with open(filename, "w") as output:
        output.write(
            """// This file is auto-generated

#include <pybind11/pybind11.h>

#include <gafro/gafro.hpp>


namespace py = pybind11;
using namespace gafro;

#include "multivectors.h"

"""
        )

        for i in range(0, count):
            output.write(
                f"void {function_name}_{i}(py::class_<gafro::Rotor<double>, Multivector_scalare12e13e23> &);\n"
            )

        output.write("\n\n")

        output.write(
            f"void {function_name}(py::class_<gafro::Rotor<double>, Multivector_scalare12e13e23> &c)\n"
        )
        output.write("{\n")

        for i in range(0, count):
            output.write(f"    {function_name}_{i}(c);\n")

        output.write("}\n")


multivectors = helpers.blades.copy()
multivectors.extend(helpers.multivectors)


N = 3
count = len(multivectors)

nb = 0
for i in range(0, count, N):
    mvs = [
        helpers.get_multivector_class_name(blades) for blades in multivectors[i : i + N]
    ]
    generate_file(
        os.path.join(sys.argv[1], f"rotor_apply_methods_{nb}.cpp"),
        mvs,
        f"init_rotor_apply_methods_{nb}",
    )
    nb += 1


generate_index_file(
    os.path.join(sys.argv[1], "rotor_apply_methods.cpp"),
    "init_rotor_apply_methods",
    nb,
)


if nb != 19:
    print(
        "The number of 'rotor apply methods' files has changed, update the 'scripts/CMakeLists.txt' file!"
    )
    sys.exit(1)
