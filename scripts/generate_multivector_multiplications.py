#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

import itertools
import os
import sys

import helpers


def generate_file(filename, pattern, permutations, function_name):
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
#include "algebra/products_utils.hpp"


void {function_name}(py::module &m)
{{
"""
        )
        for blades1, blades2 in permutations:
            blades1 = "".join(blades1)
            blades2 = "".join(blades2)
            output.write("    ")
            output.write(eval(f"f'{pattern}'"))  # nosec
            output.write("\n")

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


multivectors = []
multivectors.extend(helpers.blades)
multivectors.extend(helpers.multivectors[: helpers.nb_base_multivectors])
multivectors.append("".join(helpers.blades))

all_permutations = list(itertools.product(multivectors, repeat=2))

N = 100

PATTERN_GEOMETRIC_PRODUCT = 'm.def("geometricProduct_{blades1}_{blades2}", &geometricProduct<Multivector_{blades1}, Multivector_{blades2}>);'
PATTERN_INNER_PRODUCT = 'm.def("innerProduct_{blades1}_{blades2}", &innerProduct<Multivector_{blades1}, Multivector_{blades2}>);'
PATTERN_OUTER_PRODUCT = 'm.def("outerProduct_{blades1}_{blades2}", &outerProduct<Multivector_{blades1}, Multivector_{blades2}>);'

nb = 0
for i in range(0, len(all_permutations), N):
    permutations = all_permutations[i : i + N]

    generate_file(
        os.path.join(sys.argv[1], f"geometric_products_{i}.cpp"),
        PATTERN_GEOMETRIC_PRODUCT,
        permutations,
        f"init_geometric_products_{i}",
    )

    generate_file(
        os.path.join(sys.argv[1], f"inner_products_{i}.cpp"),
        PATTERN_INNER_PRODUCT,
        permutations,
        f"init_inner_products_{i}",
    )

    generate_file(
        os.path.join(sys.argv[1], f"outer_products_{i}.cpp"),
        PATTERN_OUTER_PRODUCT,
        permutations,
        f"init_outer_products_{i}",
    )

    nb += 1


generate_index_file(
    os.path.join(sys.argv[1], "geometric_products.cpp"),
    "init_geometric_products",
    len(all_permutations),
)
generate_index_file(
    os.path.join(sys.argv[1], "inner_products.cpp"),
    "init_inner_products",
    len(all_permutations),
)
generate_index_file(
    os.path.join(sys.argv[1], "outer_products.cpp"),
    "init_outer_products",
    len(all_permutations),
)


if nb != 23:
    print(
        "The number of generated product files has changed, update the 'scripts/CMakeLists.txt' file!"
    )
    sys.exit(1)
