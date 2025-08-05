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


def generate(template, dof, tool, target):
    data = copy.copy(template)
    data = data.replace("DOF", str(dof))
    data = data.replace("TOOL", tool)
    data = data.replace("TARGET", target)
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

#include "singlemanipulatortargets.h"


"""
        )

        for dof, tool, target in entries:
            output.write(generate(template_functions, dof, tool, target))
            output.write("\n\n")

        output.write(f"""
void {function_name}(py::module &m)
{{
"""
        )
        for dof, tool, target in entries:
            output.write(generate(template, dof, tool, target))
            output.write("\n\n")

        output.write("}\n")


def generate_index_file(filename, function_name, count):
    with open(filename, "w") as output:
        output.write(
            """// This file is auto-generated

#include <pybind11/pybind11.h>


namespace py = pybind11;

"""
        )

        for i in range(0, count):
            output.write(f"void {function_name}_{i}(py::module &);\n")

        output.write("\n\n")

        output.write(f"void {function_name}(py::module &m)\n")
        output.write("{\n")

        for i in range(0, count):
            output.write(f"    {function_name}_{i}(m);\n")

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


entries = []

for dof in range(1, 12):
    for tool in tools:
        for target in tools:
            entries.append((dof, tool, target))


N = len(tools) * 2
count = len(entries)


with open(os.path.join(sys.argv[1], "singlemanipulatortargets.h"), "w") as output:
    template = helpers.load_template("singlemanipulatortargets.h")

    output.write(
        """// This file is auto-generated

#include <gafro/gafro.hpp>
"""
    )

    for dof, tool, target in entries:
        output.write(generate(template, dof, tool, target))


template = helpers.load_template("singlemanipulatortargets.hpp")
template_functions = helpers.load_template("singlemanipulatortargets_functions.hpp")

nb = 0
for i in range(0, count, N):
    generate_file(
        os.path.join(sys.argv[1], f"singlemanipulatortargets_{nb}.cpp"),
        f"init_singlemanipulatortargets_{nb}",
        template,
        template_functions,
        entries[i : i + N],
    )
    nb += 1


generate_index_file(
    os.path.join(sys.argv[1], "singlemanipulatortargets.cpp"), "init_singlemanipulatortargets", nb
)


if nb != 61:
    print(
        "The number of generated 'singlemanipulatortargets' files has changed, update the 'scripts/CMakeLists.txt' file!"
    )
    sys.exit(1)
