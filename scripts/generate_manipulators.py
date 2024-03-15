#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

import copy
import os
import sys

import helpers


def generate(template, dof):
    data = copy.copy(template)
    data = data.replace("DOF", str(dof))
    return data


with open(os.path.join(sys.argv[1], "manipulators.h"), "w") as output:
    template = helpers.load_template("manipulators.h")

    output.write(
        """// This file is auto-generated

#include <gafro/gafro.hpp>
"""
    )

    for dof in range(1, 12):
        output.write(generate(template, dof))


with open(os.path.join(sys.argv[1], "manipulators.hpp"), "w") as output:
    template = helpers.load_template("manipulators.hpp")

    output.write(
        """// This file is auto-generated

"""
    )

    for dof in range(1, 12):
        output.write(generate(template, dof))
        output.write("\n\n")
