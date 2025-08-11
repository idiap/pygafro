#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: MPL-2.0
#

import itertools
import os

# Note: the order is very important here
blades = [
    "scalar",   # 0
    "e0",
    "e1",
    "e01",
    "e2",
    "e02",      # 5
    "e12",
    "e012",
    "e3",
    "e03",
    "e13",      # 10
    "e013",
    "e23",
    "e023",
    "e123",
    "e0123",    # 15
    "ei",
    "e0i",
    "e1i",
    "e01i",
    "e2i",      # 20
    "e02i",
    "e12i",
    "e012i",
    "e3i",
    "e03i",     # 25
    "e13i",
    "e013i",
    "e23i",
    "e023i",
    "e123i",    # 30
    "e0123i",
]


multivectors = [
    ["e0", "e1", "e2", "e3", "ei"],
    ["e1", "e2", "e3"],
    ["e123", "e12i", "e13i", "e23i", "e012", "e013", "e023", "e01i", "e02i", "e03i"],
    ["e123i", "e0123", "e012i", "e023i", "e013i"],
    ["e123i", "e012i", "e023i", "e013i"],
    ["e01i", "e02i", "e12i", "e03i", "e13i", "e23i"],
    ["e1i", "e2i", "e3i"],
    ["e23", "e13", "e12", "e01", "e02", "e03"],
    ["e23", "e13", "e12", "e1i", "e2i", "e3i", "e01", "e02", "e03", "e0i"],
    ["e23", "e13", "e12", "e1i", "e2i", "e3i"],
    ["e23", "e13", "e12"],
    ["scalar", "e1i", "e2i", "e3i"],
    ["scalar", "e12", "e13", "e23", "e1i", "e2i", "e3i", "e123i"],
    ["scalar", "e23", "e13", "e12"],
    ["scalar", "e01", "e02", "e12", "e03", "e13", "e23", "e0123", "e0i", "e1i", "e2i", "e012i", "e3i", "e013i", "e023i", "e123i"],
    ["e012i", "e013i", "e023i"],
    ["e12i", "e13i", "e23i"],
    ["e12i", "e13i", "e23i", "e0123i"],
    ["e01i", "e02i", "e03i"],
    ["e01i", "e02i", "e03i", "e0123i"],
    ["e1", "e2", "e3", "ei"],
    ["ei", "e01i", "e02i", "e12i", "e03i", "e13i", "e23i", "e0123i"],
]

multivectors.append(blades.copy())

for entry in multivectors:
    entry.sort(key=lambda x: blades.index(x))


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
