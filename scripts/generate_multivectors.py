#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

import copy
import json
import os
import sys

import helpers


def generate_multivector_class(
    template, blades, include_norm_methods=True, include_dual_method=True
):
    data = copy.copy(template)

    multivector_class_name = helpers.get_multivector_class_name(blades)
    data = data.replace("MULTIVECTOR_CLASS_NAME", multivector_class_name)

    if len(blades) > 0:
        data = data.replace(
            "BLADES", ", ".join([f"gafro::blades::{x}" for x in blades])
        )
    else:
        data = data.replace(", BLADES", "")

    multivector_set_methods = ""
    multivector_get_methods = ""
    for blade in blades:
        multivector_set_methods += (
            f"    DECLARE_MULTIVECTOR_SET_METHOD({multivector_class_name}, {blade})\n"
        )
        multivector_get_methods += (
            f"    DECLARE_MULTIVECTOR_GET_METHOD({multivector_class_name}, {blade})\n"
        )

    data = data.replace("    MULTIVECTOR_SET_METHODS\n", multivector_set_methods)
    data = data.replace("    MULTIVECTOR_GET_METHODS\n", multivector_get_methods)

    data = helpers.process_section(
        data, "BEGIN_NORM_METHODS", "END_NORM_METHODS", include_norm_methods
    )

    data = helpers.process_section(
        data, "BEGIN_DUAL_METHOD", "END_DUAL_METHOD", include_dual_method
    )

    return data


def generate_file(filename, function_name, template, entries):
    with open(filename, "w") as output:
        output.write(
            f"""// This file is auto-generated

#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>

#include <gafro/gafro.hpp>


namespace py = pybind11;
using namespace gafro;

#include "multivectors.h"
#include "algebra/multivector_utils.hpp"


#define DECLARE_MULTIVECTOR_SET_METHOD(MultivectorClass, blade) .def("set_" #blade, &MultivectorClass::set<blades::blade>)
#define DECLARE_MULTIVECTOR_GET_METHOD(MultivectorClass, blade) .def("get_" #blade, &MultivectorClass::get<blades::blade>)


void {function_name}(py::module &m)
{{
"""
        )
        for blades, include_norm_methods, include_dual_method in entries:
            output.write(
                generate_multivector_class(
                    template,
                    blades,
                    include_norm_methods=include_norm_methods,
                    include_dual_method=include_dual_method,
                )
            )
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

        for i in range(0, count, N):
            output.write(f"void {function_name}_{i}(py::module &);\n")

        output.write("\n\n")

        output.write(f"void {function_name}(py::module &m)\n")
        output.write("{\n")

        for i in range(0, count, N):
            output.write(f"    {function_name}_{i}(m);\n")

        output.write("}\n")


exclusion_norm_methods = [
    "ei",
    "e0",
    "e1i",
    "e2i",
    "e3i",
    "e01",
    "e02",
    "e03",
    "e12i",
    "e13i",
    "e23i",
    "e012",
    "e013",
    "e023",
    "e123i",
    "e0123",
]


multivectors_without_norm_methods = [
    ["e1i", "e2i", "e3i"],
]


entries = [([], False, False)]

entries.extend(
    [([blade], blade not in exclusion_norm_methods, True) for blade in helpers.blades]
)
entries.extend(
    [
        (blades, blades not in multivectors_without_norm_methods, True)
        for blades in helpers.multivectors
    ]
)


N = 3
count = len(entries)


with open(os.path.join(sys.argv[1], "multivectors.h"), "w") as output:
    template = helpers.load_template("multivectors.h")

    output.write(
        """// This file is auto-generated

#include <gafro/gafro.hpp>
"""
    )

    for blades, include_norm_methods, include_dual_method in entries:
        output.write(
            generate_multivector_class(
                template,
                blades,
                include_norm_methods=include_norm_methods,
                include_dual_method=include_dual_method,
            )
        )


template = helpers.load_template("multivectors.hpp")

nb = 0
for i in range(0, count, N):
    generate_file(
        os.path.join(sys.argv[1], f"multivectors_{i}.cpp"),
        f"init_multivectors_{i}",
        template,
        entries[i : i + N],
    )
    nb += 1


generate_index_file(
    os.path.join(sys.argv[1], "multivectors.cpp"), "init_multivectors", count
)


with open(os.path.join(sys.argv[1], "mv_combinations.py"), "w") as output:
    output.write("# This file is auto-generated\n\n")
    output.write("combinations = " + json.dumps(helpers.multivectors, indent=4))


if nb != 25:
    print(
        "The number of generated 'multivector' files has changed, update the 'scripts/CMakeLists.txt' file!"
    )
    sys.exit(1)
