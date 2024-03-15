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
from pygafro import Multivector_e1e2e3
from pygafro import Plane
from pygafro import Point


class TestPlane(unittest.TestCase):

    def test_creationFromPoints_origin(self):
        p1 = Point(0.0, 0.0, 0.0)
        p2 = Point(0.0, 1.0, 0.0)
        p3 = Point(0.0, 0.0, 1.0)

        plane = Plane(p1, p2, p3)

        self.assertAlmostEqual(plane["e123i"], 0.0)
        self.assertAlmostEqual(plane["e012i"], 0.0)
        self.assertAlmostEqual(plane["e023i"], 1.0)
        self.assertAlmostEqual(plane["e013i"], 0.0)

        normal = plane.getNormal()

        self.assertTrue(isinstance(normal, Multivector_e1e2e3))

        self.assertAlmostEqual(normal["e1"], 1.0)
        self.assertAlmostEqual(normal["e2"], 0.0)
        self.assertAlmostEqual(normal["e3"], 0.0)

    def test_creationFromPoints_arbitrary(self):
        p1 = Point(1.0, 0.0, 0.0)
        p2 = Point(0.0, 1.0, 0.0)
        p3 = Point(0.0, 2.0, 3.0)

        plane = Plane(p1, p2, p3)

        self.assertAlmostEqual(plane["e123i"], 3.0)
        self.assertAlmostEqual(plane["e012i"], -1.0)
        self.assertAlmostEqual(plane["e023i"], 3.0)
        self.assertAlmostEqual(plane["e013i"], -3.0)

        normal = plane.getNormal()

        self.assertTrue(isinstance(normal, Multivector_e1e2e3))

        self.assertAlmostEqual(normal["e1"], 3.0)
        self.assertAlmostEqual(normal["e2"], 3.0)
        self.assertAlmostEqual(normal["e3"], -1.0)

    def test_creationFromPlane(self):
        p1 = Point(0.0, 0.0, 0.0)
        p2 = Point(0.0, 1.0, 0.0)
        p3 = Point(0.0, 0.0, 1.0)

        plane = Plane(p1, p2, p3)
        plane2 = Plane(plane)

        self.assertAlmostEqual(plane2["e123i"], 0.0)
        self.assertAlmostEqual(plane2["e012i"], 0.0)
        self.assertAlmostEqual(plane2["e023i"], 1.0)
        self.assertAlmostEqual(plane2["e013i"], 0.0)

    def test_creationFromMultivector(self):
        mv = Multivector.create(
            ["e123i", "e012i", "e023i", "e013i"], [1.0, 2.0, 3.0, 4.0]
        )
        plane = Plane(mv)

        self.assertAlmostEqual(plane["e123i"], 1.0)
        self.assertAlmostEqual(plane["e012i"], 2.0)
        self.assertAlmostEqual(plane["e023i"], 3.0)
        self.assertAlmostEqual(plane["e013i"], 4.0)

    def test_addition(self):
        p1 = Point(0.0, 0.0, 0.0)
        p2 = Point(0.0, 1.0, 0.0)
        p3 = Point(0.0, 0.0, 1.0)

        p4 = Point(1.0, 0.0, 0.0)
        p5 = Point(0.0, 1.0, 0.0)
        p6 = Point(0.0, 2.0, 3.0)

        plane1 = Plane(p1, p2, p3)
        plane2 = Plane(p4, p5, p6)

        plane = plane1 + plane2

        self.assertTrue(isinstance(plane, Plane))

        self.assertAlmostEqual(plane["e123i"], 3.0)
        self.assertAlmostEqual(plane["e012i"], -1.0)
        self.assertAlmostEqual(plane["e023i"], 4.0)
        self.assertAlmostEqual(plane["e013i"], -3.0)

    def test_addition2(self):
        p1 = Point(0.0, 0.0, 0.0)
        p2 = Point(0.0, 1.0, 0.0)
        p3 = Point(0.0, 0.0, 1.0)

        plane1 = Plane(p1, p2, p3)

        mv = Multivector.create(
            ["e123i", "e012i", "e023i", "e013i"], [3.0, -1.0, 3.0, -3.0]
        )

        plane = plane1 + mv

        self.assertTrue(isinstance(plane, Plane))

        self.assertAlmostEqual(plane["e123i"], 3.0)
        self.assertAlmostEqual(plane["e012i"], -1.0)
        self.assertAlmostEqual(plane["e023i"], 4.0)
        self.assertAlmostEqual(plane["e013i"], -3.0)

    def test_substraction(self):
        p1 = Point(0.0, 0.0, 0.0)
        p2 = Point(0.0, 1.0, 0.0)
        p3 = Point(0.0, 0.0, 1.0)

        p4 = Point(1.0, 0.0, 0.0)
        p5 = Point(0.0, 1.0, 0.0)
        p6 = Point(0.0, 2.0, 3.0)

        plane1 = Plane(p1, p2, p3)
        plane2 = Plane(p4, p5, p6)

        plane = plane1 - plane2

        self.assertTrue(isinstance(plane, Plane))

        self.assertAlmostEqual(plane["e123i"], -3.0)
        self.assertAlmostEqual(plane["e012i"], 1.0)
        self.assertAlmostEqual(plane["e023i"], -2.0)
        self.assertAlmostEqual(plane["e013i"], 3.0)

    def test_substraction2(self):
        p1 = Point(0.0, 0.0, 0.0)
        p2 = Point(0.0, 1.0, 0.0)
        p3 = Point(0.0, 0.0, 1.0)

        plane1 = Plane(p1, p2, p3)

        mv = Multivector.create(
            ["e123i", "e012i", "e023i", "e013i"], [3.0, -1.0, 3.0, -3.0]
        )

        plane = plane1 - mv

        self.assertTrue(isinstance(plane, Plane))

        self.assertAlmostEqual(plane["e123i"], -3.0)
        self.assertAlmostEqual(plane["e012i"], 1.0)
        self.assertAlmostEqual(plane["e023i"], -2.0)
        self.assertAlmostEqual(plane["e013i"], 3.0)


if __name__ == "__main__":
    unittest.main()
