#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2025 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: MPL-2.0
#

import os
import sys

import helpers


with open(sys.argv[1], "r") as f:
    template = f.read().split('\n')


filename = os.path.basename(sys.argv[1]).lower()


with open(os.path.join(sys.argv[2], filename), "w") as output:
    output.write("# This file is auto-generated\n\n")
    output.write("table = {\n")

    for line in template:
        if (len(line) == 0) or (line[0] == '#'):
            continue

        parts = line.split(': ')
        blade1, blade2 = parts[0].split(', ')
        result_blades = parts[1].split(', ')

        blade1 = helpers.blades.index(blade1)
        blade2 = helpers.blades.index(blade2)
        result_blades = [helpers.blades.index(x) for x in result_blades if x != '']

        output.write(f"    ({blade1}, {blade2}): {result_blades},\n")

    output.write("}\n")
