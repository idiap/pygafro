#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

import itertools
import os

blades = [
    "scalar",
    "e1",
    "e2",
    "e3",
    "ei",
    "e0",
    "e23",
    "e13",
    "e12",
    "e1i",
    "e2i",
    "e3i",
    "e01",
    "e02",
    "e03",
    "e0i",
    "e123",
    "e12i",
    "e13i",
    "e23i",
    "e012",
    "e013",
    "e023",
    "e01i",
    "e02i",
    "e03i",
    "e123i",
    "e0123",
    "e012i",
    "e023i",
    "e013i",
    "e0123i",
]


multivectors = [
    ["e1", "e2", "e3", "ei", "e0"],
    ["e1", "e2", "e3"],
    ["e123", "e12i", "e13i", "e23i", "e012", "e013", "e023", "e01i", "e02i", "e03i"],
    ["e123i", "e0123", "e012i", "e023i", "e013i"],
    ["e123i", "e012i", "e023i", "e013i"],
    ["e12i", "e13i", "e23i", "e01i", "e02i", "e03i"],
    ["e1i", "e2i", "e3i"],
    ["e23", "e13", "e12", "e01", "e02", "e03"],
    ["e23", "e13", "e12", "e1i", "e2i", "e3i", "e01", "e02", "e03", "e0i"],
    ["e23", "e13", "e12", "e1i", "e2i", "e3i"],
    ["e23", "e13", "e12"],
    ["scalar", "e1i", "e2i", "e3i"],
    ["scalar", "e23", "e13", "e12", "e1i", "e2i", "e3i", "e123i"],
    ["scalar", "e23", "e13", "e12"],
]


nb_base_multivectors = len(multivectors)


blades_ranges = [
    (0, 5),
    (6, 15),
    (16, 25),
    (26, 30),
    (31, 31),
]


combinations = []
for k in range(1, len(blades_ranges) + 1):
    combinations.extend(itertools.combinations(blades_ranges, k))

for combination in combinations:
    b = [blades[n] for x in combination for n in range(x[0], x[1] + 1)]
    if (b not in multivectors) and (len(b) > 1):
        multivectors.append(b)


specific_multivector_classes = [
    "Circle",
    "DirectionVector",
    "Line",
    "Plane",
    "Point",
    "PointPair",
    "Sphere",
    "Vector",
]


def load_template(filename):
    with open(os.path.join("templates", filename), "r") as f:
        return f.read()


def get_multivector_class_name(blades):
    return "Multivector_" + "".join(blades)


def process_section(data, start_token, end_token, keep):
    if not keep:
        start = data.find(start_token)
        if start < 0:
            return data
        end = data.find(end_token, start) + len(end_token) + 1
        data = data[:start] + data[end:]
    else:
        data = data.replace(start_token + "\n", "")
        data = data.replace(end_token + "\n", "")

    return data
