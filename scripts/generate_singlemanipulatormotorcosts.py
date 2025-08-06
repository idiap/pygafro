#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: MPL-2.0
#

import copy
import os
import sys

import helpers


def generate(template, dof):
    data = copy.copy(template)
    data = data.replace("DOF", str(dof))
    return data


def generate_file(filename, function_name, template, template_functions, entries):
    with open(filename, "w") as output:
        output.write(
            f"""// This file is auto-generated

#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>

#include <gafro/gafro.hpp>


namespace py = pybind11;
using namespace gafro;

#include "singlemanipulatormotorcosts.h"


"""
        )

        for dof in entries:
            output.write(generate(template_functions, dof))
            output.write("\n\n")

        output.write(f"""
void {function_name}(py::module &m)
{{
"""
        )
        for dof in entries:
            output.write(generate(template, dof))
            output.write("\n\n")

        output.write("}\n")



tools = [
    'Circle', 
    'DirectionVector', 
    'Line', 
    'Motor', 
    'Plane', 
    'Point', 
    'PointPair', 
    'Rotor', 
    'Sphere', 
    'Translator', 
    'Vector', 
]


entries = list(range(1, 12))


with open(os.path.join(sys.argv[1], "singlemanipulatormotorcosts.h"), "w") as output:
    template = helpers.load_template("singlemanipulatormotorcosts.h")

    output.write(
        """// This file is auto-generated

#include <gafro/gafro.hpp>
"""
    )

    for dof in entries:
        output.write(generate(template, dof))


template = helpers.load_template("singlemanipulatormotorcosts.hpp")
template_functions = helpers.load_template("singlemanipulatormotorcosts_functions.hpp")

generate_file(
    os.path.join(sys.argv[1], f"singlemanipulatormotorcosts.cpp"),
    f"init_singlemanipulatormotorcosts",
    template,
    template_functions,
    entries,
)
