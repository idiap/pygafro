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
from pygafro import Point


class TestPoint(unittest.TestCase):

    def test_defaultCreation(self):
        point = Point()

        self.assertAlmostEqual(point["e1"], 0.0)
        self.assertAlmostEqual(point["e2"], 0.0)
        self.assertAlmostEqual(point["e3"], 0.0)
        self.assertAlmostEqual(point["ei"], 0.0)
        self.assertAlmostEqual(point["e0"], 1.0)

    def test_creationFromParameters(self):
        point = Point(1.0, 2.0, 3.0)

        self.assertAlmostEqual(point["e1"], 1.0)
        self.assertAlmostEqual(point["e2"], 2.0)
        self.assertAlmostEqual(point["e3"], 3.0)
        self.assertAlmostEqual(point["ei"], 7.0)
        self.assertAlmostEqual(point["e0"], 1.0)

    def test_creationFromPoint(self):
        point = Point(1.0, 2.0, 3.0)
        point2 = Point(point)

        self.assertAlmostEqual(point2["e1"], 1.0)
        self.assertAlmostEqual(point2["e2"], 2.0)
        self.assertAlmostEqual(point2["e3"], 3.0)
        self.assertAlmostEqual(point2["ei"], 7.0)
        self.assertAlmostEqual(point2["e0"], 1.0)

    def test_creationFromMultivector(self):
        mv = Multivector.create(
            ["e1", "e2", "e3", "ei", "e0"], [1.0, 2.0, 3.0, 7.0, 1.0]
        )
        point = Point(mv)

        self.assertAlmostEqual(point["e1"], 1.0)
        self.assertAlmostEqual(point["e2"], 2.0)
        self.assertAlmostEqual(point["e3"], 3.0)
        self.assertAlmostEqual(point["ei"], 7.0)
        self.assertAlmostEqual(point["e0"], 1.0)

    def test_creationFromNumpyArray(self):
        point = Point(np.array([1.0, 2.0, 3.0, 7.0, 1.0]))

        self.assertAlmostEqual(point["e1"], 1.0)
        self.assertAlmostEqual(point["e2"], 2.0)
        self.assertAlmostEqual(point["e3"], 3.0)
        self.assertAlmostEqual(point["ei"], 7.0)
        self.assertAlmostEqual(point["e0"], 1.0)

    def test_creationFromArray(self):
        point = Point([1.0, 2.0, 3.0, 7.0, 1.0])

        self.assertAlmostEqual(point["e1"], 1.0)
        self.assertAlmostEqual(point["e2"], 2.0)
        self.assertAlmostEqual(point["e3"], 3.0)
        self.assertAlmostEqual(point["ei"], 7.0)
        self.assertAlmostEqual(point["e0"], 1.0)

    def test_addition(self):
        point1 = Point(1.0, 2.0, 3.0)
        point2 = Point(10.0, 20.0, 30.0)

        point = point1 + point2

        self.assertTrue(isinstance(point, Point))

        self.assertAlmostEqual(point["e1"], 11.0)
        self.assertAlmostEqual(point["e2"], 22.0)
        self.assertAlmostEqual(point["e3"], 33.0)
        self.assertAlmostEqual(point["ei"], 707.0)
        self.assertAlmostEqual(point["e0"], 2.0)

    def test_addition2(self):
        point1 = Point(1.0, 2.0, 3.0)
        mv = Multivector.create(
            ["e1", "e2", "e3", "ei", "e0"], [10.0, 20.0, 30.0, 700.0, 1.0]
        )

        point = point1 + mv

        self.assertTrue(isinstance(point, Point))

        self.assertAlmostEqual(point["e1"], 11.0)
        self.assertAlmostEqual(point["e2"], 22.0)
        self.assertAlmostEqual(point["e3"], 33.0)
        self.assertAlmostEqual(point["ei"], 707.0)
        self.assertAlmostEqual(point["e0"], 2.0)

    def test_substraction(self):
        point1 = Point(10.0, 20.0, 30.0)
        point2 = Point(1.0, 2.0, 3.0)

        point = point1 - point2

        self.assertTrue(isinstance(point, Point))

        self.assertAlmostEqual(point["e1"], 9.0)
        self.assertAlmostEqual(point["e2"], 18.0)
        self.assertAlmostEqual(point["e3"], 27.0)
        self.assertAlmostEqual(point["ei"], 693.0)
        self.assertAlmostEqual(point["e0"], 0.0)

    def test_substraction2(self):
        point1 = Point(10.0, 20.0, 30.0)
        mv = Multivector.create(
            ["e1", "e2", "e3", "ei", "e0"], [1.0, 2.0, 3.0, 7.0, 1.0]
        )

        point = point1 - mv

        self.assertTrue(isinstance(point, Point))

        self.assertAlmostEqual(point["e1"], 9.0)
        self.assertAlmostEqual(point["e2"], 18.0)
        self.assertAlmostEqual(point["e3"], 27.0)
        self.assertAlmostEqual(point["ei"], 693.0)
        self.assertAlmostEqual(point["e0"], 0.0)


if __name__ == "__main__":
    unittest.main()
