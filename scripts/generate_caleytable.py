#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

import os
import sys

import helpers


def extract(data, start_pos, start_token, end_token):
    start = data.find(start_token, start_pos)
    if start < 0:
        return None, start_pos

    end = data.find(end_token, start + len(start_token))
    if end < 0:
        return None, start_pos

    return (data[start + len(start_token) : end], end + len(end_token))


with open(sys.argv[1], "r") as f:
    cpp = f.read()


filename = os.path.basename(sys.argv[1]).lower()
filename, _ = os.path.splitext(filename)
filename += ".py"


with open(os.path.join(sys.argv[2], filename), "w") as output:
    output.write("# This file is auto-generated\n\n")
    output.write("table = {\n")

    block_start = cpp.find(f"struct {sys.argv[3]}<T, ")

    while block_start > 0:
        blade1, offset = extract(cpp, block_start, "blades::", ",")
        blade2, offset = extract(cpp, offset, "blades::", ">")

        result_blades = []
        line, offset = extract(cpp, offset, "using Type = Multivector<T", ">")
        line += ">"
        offset2 = 0
        while True:
            blade, offset2 = extract(line, offset2, "blades::", ",")
            if blade is None:
                blade, offset2 = extract(line, offset2, "blades::", ">")
                if blade is None:
                    break

            result_blades.append(blade)

        blade1 = helpers.blades.index(blade1)
        blade2 = helpers.blades.index(blade2)
        result_blades = [helpers.blades.index(x) for x in result_blades]

        output.write(f"    ({blade1}, {blade2}): {result_blades},\n")

        block_start = cpp.find(f"struct {sys.argv[3]}<T, ", block_start + 10)

    output.write("}\n")
