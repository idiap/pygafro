#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

import unittest

import numpy as np

from pygafro import Multivector
from pygafro import Vector


class TestVector(unittest.TestCase):

    def test_defaultCreation(self):
        vector = Vector()

        self.assertAlmostEqual(vector["e1"], 0.0)
        self.assertAlmostEqual(vector["e2"], 0.0)
        self.assertAlmostEqual(vector["e3"], 0.0)

    def test_creationFromParameters(self):
        vector = Vector(1.0, 2.0, 3.0)

        self.assertAlmostEqual(vector["e1"], 1.0)
        self.assertAlmostEqual(vector["e2"], 2.0)
        self.assertAlmostEqual(vector["e3"], 3.0)

    def test_creationFromVector(self):
        vector = Vector(1.0, 2.0, 3.0)
        vector2 = Vector(vector)

        self.assertAlmostEqual(vector2["e1"], 1.0)
        self.assertAlmostEqual(vector2["e2"], 2.0)
        self.assertAlmostEqual(vector2["e3"], 3.0)

    def test_creationFromMultivector(self):
        mv = Multivector.create(["e1", "e2", "e3"], [1.0, 2.0, 3.0])
        vector = Vector(mv)

        self.assertAlmostEqual(vector["e1"], 1.0)
        self.assertAlmostEqual(vector["e2"], 2.0)
        self.assertAlmostEqual(vector["e3"], 3.0)

    def test_creationFromNumpyArray(self):
        vector = Vector(np.array([1.0, 2.0, 3.0]))

        self.assertAlmostEqual(vector["e1"], 1.0)
        self.assertAlmostEqual(vector["e2"], 2.0)
        self.assertAlmostEqual(vector["e3"], 3.0)

    def test_creationFromArray(self):
        vector = Vector([1.0, 2.0, 3.0])

        self.assertAlmostEqual(vector["e1"], 1.0)
        self.assertAlmostEqual(vector["e2"], 2.0)
        self.assertAlmostEqual(vector["e3"], 3.0)

    def test_addition(self):
        vector1 = Vector(1.0, 2.0, 3.0)
        vector2 = Vector(10.0, 20.0, 30.0)

        vector = vector1 + vector2

        self.assertTrue(isinstance(vector, Vector))

        self.assertAlmostEqual(vector["e1"], 11.0)
        self.assertAlmostEqual(vector["e2"], 22.0)
        self.assertAlmostEqual(vector["e3"], 33.0)

    def test_addition2(self):
        vector1 = Vector(1.0, 2.0, 3.0)
        mv = Multivector.create(["e1", "e2", "e3"], [10.0, 20.0, 30.0])

        vector = vector1 + mv

        self.assertTrue(isinstance(vector, Vector))

        self.assertAlmostEqual(vector["e1"], 11.0)
        self.assertAlmostEqual(vector["e2"], 22.0)
        self.assertAlmostEqual(vector["e3"], 33.0)

    def test_substraction(self):
        vector1 = Vector(10.0, 20.0, 30.0)
        vector2 = Vector(1.0, 2.0, 3.0)

        vector = vector1 - vector2

        self.assertTrue(isinstance(vector, Vector))

        self.assertAlmostEqual(vector["e1"], 9.0)
        self.assertAlmostEqual(vector["e2"], 18.0)
        self.assertAlmostEqual(vector["e3"], 27.0)

    def test_substraction2(self):
        vector1 = Vector(10.0, 20.0, 30.0)
        mv = Multivector.create(["e1", "e2", "e3"], [1.0, 2.0, 3.0])

        vector = vector1 - mv

        self.assertTrue(isinstance(vector, Vector))

        self.assertAlmostEqual(vector["e1"], 9.0)
        self.assertAlmostEqual(vector["e2"], 18.0)
        self.assertAlmostEqual(vector["e3"], 27.0)


if __name__ == "__main__":
    unittest.main()
