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


with open(os.path.join(sys.argv[1], "quadrupeds.h"), "w") as output:
    template = helpers.load_template("quadrupeds.h")

    output.write(
        """// This file is auto-generated

#include <gafro/gafro.hpp>
"""
    )

    for dof in range(1, 12):
        output.write(generate(template, dof))


with open(os.path.join(sys.argv[1], "quadrupeds.hpp"), "w") as output:
    template = helpers.load_template("quadrupeds.hpp")

    output.write(
        """// This file is auto-generated

"""
    )

    for dof in range(1, 12):
        output.write(generate(template, dof))
        output.write("\n\n")
