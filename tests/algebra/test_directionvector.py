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

from pygafro import DirectionVector
from pygafro import Multivector


class TestDirectionVector(unittest.TestCase):

    def test_defaultCreation(self):
        vector = DirectionVector()

        self.assertAlmostEqual(vector["e1i"], 0.0)
        self.assertAlmostEqual(vector["e2i"], 0.0)
        self.assertAlmostEqual(vector["e3i"], 0.0)

    def test_creationFromParameters(self):
        vector = DirectionVector(1.0, 2.0, 3.0)

        self.assertAlmostEqual(vector["e1i"], 1.0)
        self.assertAlmostEqual(vector["e2i"], 2.0)
        self.assertAlmostEqual(vector["e3i"], 3.0)

    def test_creationFromDirectionVector(self):
        vector = DirectionVector(1.0, 2.0, 3.0)
        vector2 = DirectionVector(vector)

        self.assertAlmostEqual(vector2["e1i"], 1.0)
        self.assertAlmostEqual(vector2["e2i"], 2.0)
        self.assertAlmostEqual(vector2["e3i"], 3.0)

    def test_creationFromMultivector(self):
        mv = Multivector.create(["e1i", "e2i", "e3i"], [1.0, 2.0, 3.0])
        vector = DirectionVector(mv)

        self.assertAlmostEqual(vector["e1i"], 1.0)
        self.assertAlmostEqual(vector["e2i"], 2.0)
        self.assertAlmostEqual(vector["e3i"], 3.0)

    def test_creationFromNumpyArray(self):
        vector = DirectionVector(np.array([1.0, 2.0, 3.0]))

        self.assertAlmostEqual(vector["e1i"], 1.0)
        self.assertAlmostEqual(vector["e2i"], 2.0)
        self.assertAlmostEqual(vector["e3i"], 3.0)

    def test_creationFromArray(self):
        vector = DirectionVector([1.0, 2.0, 3.0])

        self.assertAlmostEqual(vector["e1i"], 1.0)
        self.assertAlmostEqual(vector["e2i"], 2.0)
        self.assertAlmostEqual(vector["e3i"], 3.0)

    def test_addition(self):
        vector1 = DirectionVector(1.0, 2.0, 3.0)
        vector2 = DirectionVector(10.0, 20.0, 30.0)

        vector = vector1 + vector2

        self.assertTrue(isinstance(vector, DirectionVector))

        self.assertAlmostEqual(vector["e1i"], 11.0)
        self.assertAlmostEqual(vector["e2i"], 22.0)
        self.assertAlmostEqual(vector["e3i"], 33.0)

    def test_addition2(self):
        vector1 = DirectionVector(1.0, 2.0, 3.0)
        mv = Multivector.create(["e1i", "e2i", "e3i"], [10.0, 20.0, 30.0])

        vector = vector1 + mv

        self.assertTrue(isinstance(vector, DirectionVector))

        self.assertAlmostEqual(vector["e1i"], 11.0)
        self.assertAlmostEqual(vector["e2i"], 22.0)
        self.assertAlmostEqual(vector["e3i"], 33.0)

    def test_substraction(self):
        vector1 = DirectionVector(10.0, 20.0, 30.0)
        vector2 = DirectionVector(1.0, 2.0, 3.0)

        vector = vector1 - vector2

        self.assertTrue(isinstance(vector, DirectionVector))

        self.assertAlmostEqual(vector["e1i"], 9.0)
        self.assertAlmostEqual(vector["e2i"], 18.0)
        self.assertAlmostEqual(vector["e3i"], 27.0)

    def test_substraction2(self):
        vector1 = DirectionVector(10.0, 20.0, 30.0)
        mv = Multivector.create(["e1i", "e2i", "e3i"], [1.0, 2.0, 3.0])

        vector = vector1 - mv

        self.assertTrue(isinstance(vector, DirectionVector))

        self.assertAlmostEqual(vector["e1i"], 9.0)
        self.assertAlmostEqual(vector["e2i"], 18.0)
        self.assertAlmostEqual(vector["e3i"], 27.0)


if __name__ == "__main__":
    unittest.main()
