#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2025 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: MPL-2.0
#

import copy
import os
import sys

import helpers


def generate(template, nb_fingers, dof):
    fingers = [str(dof)] * nb_fingers
    data = copy.copy(template)
    data = data.replace("FINGERSLIST", ', '.join(fingers))
    data = data.replace("FINGERSSUFFIX", '_'.join(fingers))
    data = data.replace("DOF", str(nb_fingers * dof))
    data = data.replace("NB_FINGERS", str(nb_fingers))

    data = helpers.process_section(
        data, "BEGIN_3_FINGERS", "END_3_FINGERS", nb_fingers == 3
    )

    data = helpers.process_section(
        data, "BEGIN_4_FINGERS", "END_4_FINGERS", nb_fingers == 4
    )

    return data



NB_FINGERS_MAX = 5
DOF_MAX = 4


with open(os.path.join(sys.argv[1], "hands.h"), "w") as output:
    template = helpers.load_template("hands.h")

    output.write(
        """// This file is auto-generated

#include <gafro/gafro.hpp>
"""
    )

    for nb_fingers in range(2, NB_FINGERS_MAX+1):
        for dof in range(1, DOF_MAX+1):
            output.write(generate(template, nb_fingers, dof))


with open(os.path.join(sys.argv[1], "hands.hpp"), "w") as output:
    template = helpers.load_template("hands.hpp")

    output.write(
        """// This file is auto-generated

"""
    )

    for nb_fingers in range(2, NB_FINGERS_MAX+1):
        for dof in range(1, DOF_MAX+1):
            output.write(generate(template, nb_fingers, dof))
            output.write("\n\n")
