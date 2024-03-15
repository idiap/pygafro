#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

import unittest

from pygafro import Multivector
from pygafro import RotorGenerator


class TestRotorGenerator(unittest.TestCase):

    def test_defaultCreation(self):
        generator = RotorGenerator()

        self.assertAlmostEqual(generator.e23(), 0.0)
        self.assertAlmostEqual(generator.e13(), 0.0)
        self.assertAlmostEqual(generator.e12(), 0.0)

    def test_creationFromMultivector(self):
        mv = Multivector.create(["e23", "e13", "e12"], [1.0, 2.0, 3.0])
        generator = RotorGenerator(mv)

        self.assertAlmostEqual(generator.e23(), mv["e23"])
        self.assertAlmostEqual(generator.e13(), mv["e13"])
        self.assertAlmostEqual(generator.e12(), mv["e12"])

    def test_creationFromGenerator(self):
        generator1 = RotorGenerator([1.0, 2.0, 3.0])
        generator2 = RotorGenerator(generator1)

        self.assertAlmostEqual(generator2.e23(), generator1.e23())
        self.assertAlmostEqual(generator2.e13(), generator1.e13())
        self.assertAlmostEqual(generator2.e12(), generator1.e12())

    def test_creationFromParameters(self):
        generator = RotorGenerator([1.0, 2.0, 3.0])

        self.assertAlmostEqual(generator.e23(), 1.0)
        self.assertAlmostEqual(generator.e13(), 2.0)
        self.assertAlmostEqual(generator.e12(), 3.0)

        self.assertAlmostEqual(generator.e23(), generator["e23"])
        self.assertAlmostEqual(generator.e13(), generator["e13"])
        self.assertAlmostEqual(generator.e12(), generator["e12"])


if __name__ == "__main__":
    unittest.main()
