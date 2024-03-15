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
from pygafro import Point
from pygafro import Sphere


class TestSphere(unittest.TestCase):

    def test_creationFromCenterAndRadius_unitAtOrigin(self):
        center = Point(0.0, 0.0, 0.0)

        sphere = Sphere(center, 1.0)

        self.assertAlmostEqual(sphere["e123i"], 0.5)
        self.assertAlmostEqual(sphere["e0123"], -1.0)
        self.assertAlmostEqual(sphere["e012i"], 0.0)
        self.assertAlmostEqual(sphere["e023i"], 0.0)
        self.assertAlmostEqual(sphere["e013i"], 0.0)

        self.assertAlmostEqual(sphere.getRadius(), 1.0)

        centerResult = sphere.getCenter()

        self.assertAlmostEqual(centerResult["e1"], 0.0)
        self.assertAlmostEqual(centerResult["e2"], 0.0)
        self.assertAlmostEqual(centerResult["e3"], 0.0)
        self.assertAlmostEqual(centerResult["ei"], 0.0)
        self.assertAlmostEqual(centerResult["e0"], 1.0)

    def test_creationFromCenterAndRadius_other(self):
        center = Point(1.0, 2.0, 3.0)

        sphere = Sphere(center, 2.0)

        self.assertAlmostEqual(sphere["e123i"], -5.0)
        self.assertAlmostEqual(sphere["e0123"], -1.0)
        self.assertAlmostEqual(sphere["e012i"], -3.0)
        self.assertAlmostEqual(sphere["e023i"], -1.0)
        self.assertAlmostEqual(sphere["e013i"], 2.0)

        self.assertAlmostEqual(sphere.getRadius(), 2.0)

        centerResult = sphere.getCenter()

        self.assertAlmostEqual(centerResult["e1"], 1.0)
        self.assertAlmostEqual(centerResult["e2"], 2.0)
        self.assertAlmostEqual(centerResult["e3"], 3.0)
        self.assertAlmostEqual(centerResult["ei"], 7.0)
        self.assertAlmostEqual(centerResult["e0"], 1.0)

    def test_creationFromPoints(self):
        p1 = Point(1.0, 0.0, 0.0)
        p2 = Point(0.0, 1.0, 0.0)
        p3 = Point(-1.0, 0.0, 0.0)
        p4 = Point(0.0, 0.0, 1.0)

        sphere = Sphere(p1, p2, p3, p4)

        self.assertAlmostEqual(sphere["e123i"], -1.0)
        self.assertAlmostEqual(sphere["e0123"], 2.0)
        self.assertAlmostEqual(sphere["e012i"], 0.0)
        self.assertAlmostEqual(sphere["e023i"], 0.0)
        self.assertAlmostEqual(sphere["e013i"], 0.0)

        self.assertAlmostEqual(sphere.getRadius(), 1.0)

        centerResult = sphere.getCenter()

        self.assertAlmostEqual(centerResult["e1"], 0.0)
        self.assertAlmostEqual(centerResult["e2"], 0.0)
        self.assertAlmostEqual(centerResult["e3"], 0.0)
        self.assertAlmostEqual(centerResult["ei"], 0.0)
        self.assertAlmostEqual(centerResult["e0"], 1.0)

    def test_creationFromSphere(self):
        center = Point(0.0, 0.0, 0.0)

        sphere = Sphere(center, 1.0)
        sphere2 = Sphere(sphere)

        self.assertAlmostEqual(sphere2["e123i"], 0.5)
        self.assertAlmostEqual(sphere2["e0123"], -1.0)
        self.assertAlmostEqual(sphere2["e012i"], 0.0)
        self.assertAlmostEqual(sphere2["e023i"], 0.0)
        self.assertAlmostEqual(sphere2["e013i"], 0.0)

    def test_creationFromMultivector(self):
        mv = Multivector.create(
            ["e123i", "e0123", "e012i", "e023i", "e013i"], [1.0, 2.0, 3.0, 4.0, 5.0]
        )
        sphere = Sphere(mv)

        self.assertAlmostEqual(sphere["e123i"], 1.0)
        self.assertAlmostEqual(sphere["e0123"], 2.0)
        self.assertAlmostEqual(sphere["e012i"], 3.0)
        self.assertAlmostEqual(sphere["e023i"], 4.0)
        self.assertAlmostEqual(sphere["e013i"], 5.0)

    def test_addition(self):
        center1 = Point(0.0, 0.0, 0.0)
        center2 = Point(1.0, 0.0, 0.0)

        sphere1 = Sphere(center1, 1.0)
        sphere2 = Sphere(center2, 2.0)

        sphere = sphere1 + sphere2

        self.assertTrue(isinstance(sphere, Sphere))

        self.assertAlmostEqual(sphere["e123i"], 2.0)
        self.assertAlmostEqual(sphere["e0123"], -2.0)
        self.assertAlmostEqual(sphere["e012i"], 0.0)
        self.assertAlmostEqual(sphere["e023i"], -1.0)
        self.assertAlmostEqual(sphere["e013i"], 0.0)

    def test_addition2(self):
        center1 = Point(0.0, 0.0, 0.0)
        sphere1 = Sphere(center1, 1.0)

        mv = Multivector.create(
            ["e123i", "e0123", "e012i", "e023i", "e013i"], [1.5, -1.0, 0.0, -1.0, 0.0]
        )

        sphere = sphere1 + mv

        self.assertTrue(isinstance(sphere, Sphere))

        self.assertAlmostEqual(sphere["e123i"], 2.0)
        self.assertAlmostEqual(sphere["e0123"], -2.0)
        self.assertAlmostEqual(sphere["e012i"], 0.0)
        self.assertAlmostEqual(sphere["e023i"], -1.0)
        self.assertAlmostEqual(sphere["e013i"], 0.0)

    def test_substraction(self):
        center1 = Point(0.0, 0.0, 0.0)
        center2 = Point(1.0, 0.0, 0.0)

        sphere1 = Sphere(center1, 1.0)
        sphere2 = Sphere(center2, 2.0)

        sphere = sphere1 - sphere2

        self.assertTrue(isinstance(sphere, Sphere))

        self.assertAlmostEqual(sphere["e123i"], -1.0)
        self.assertAlmostEqual(sphere["e0123"], 0.0)
        self.assertAlmostEqual(sphere["e012i"], 0.0)
        self.assertAlmostEqual(sphere["e023i"], 1.0)
        self.assertAlmostEqual(sphere["e013i"], 0.0)

    def test_substraction2(self):
        center1 = Point(0.0, 0.0, 0.0)
        sphere1 = Sphere(center1, 1.0)

        mv = Multivector.create(
            ["e123i", "e0123", "e012i", "e023i", "e013i"], [1.5, -1.0, 0.0, -1.0, 0.0]
        )

        sphere = sphere1 - mv

        self.assertTrue(isinstance(sphere, Sphere))

        self.assertAlmostEqual(sphere["e123i"], -1.0)
        self.assertAlmostEqual(sphere["e0123"], 0.0)
        self.assertAlmostEqual(sphere["e012i"], 0.0)
        self.assertAlmostEqual(sphere["e023i"], 1.0)
        self.assertAlmostEqual(sphere["e013i"], 0.0)


if __name__ == "__main__":
    unittest.main()
