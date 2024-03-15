#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

import unittest

from pygafro import Circle
from pygafro import Multivector
from pygafro import Plane
from pygafro import Point


class TestCircle(unittest.TestCase):

    def test_creationFromPoints(self):
        p1 = Point(1.0, 0.0, 0.0)
        p2 = Point(0.0, 1.0, 0.0)
        p3 = Point(-1.0, 0.0, 0.0)

        circle = Circle(p1, p2, p3)

        self.assertAlmostEqual(circle["e123"], 0.0)
        self.assertAlmostEqual(circle["e12i"], 1.0)
        self.assertAlmostEqual(circle["e13i"], 0.0)
        self.assertAlmostEqual(circle["e23i"], 0.0)
        self.assertAlmostEqual(circle["e012"], 2.0)
        self.assertAlmostEqual(circle["e013"], 0.0)
        self.assertAlmostEqual(circle["e023"], 0.0)
        self.assertAlmostEqual(circle["e01i"], 0.0)
        self.assertAlmostEqual(circle["e02i"], 0.0)
        self.assertAlmostEqual(circle["e03i"], 0.0)

        center = circle.getCenter()

        self.assertTrue(isinstance(center, Point))

        self.assertAlmostEqual(center["e1"], 0.0)
        self.assertAlmostEqual(center["e2"], 0.0)
        self.assertAlmostEqual(center["e3"], 0.0)
        self.assertAlmostEqual(center["ei"], 0.0)
        self.assertAlmostEqual(center["e0"], 1.0)

        plane = circle.getPlane()

        self.assertTrue(isinstance(plane, Plane))

        self.assertAlmostEqual(plane["e123i"], 0.0)
        self.assertAlmostEqual(plane["e012i"], 2.0)
        self.assertAlmostEqual(plane["e023i"], 0.0)
        self.assertAlmostEqual(plane["e013i"], 0.0)

    def test_creationFromCircle(self):
        p1 = Point(1.0, 0.0, 0.0)
        p2 = Point(0.0, 1.0, 0.0)
        p3 = Point(-1.0, 0.0, 0.0)

        circle = Circle(p1, p2, p3)
        circle2 = Circle(circle)

        self.assertAlmostEqual(circle2["e123"], 0.0)
        self.assertAlmostEqual(circle2["e12i"], 1.0)
        self.assertAlmostEqual(circle2["e13i"], 0.0)
        self.assertAlmostEqual(circle2["e23i"], 0.0)
        self.assertAlmostEqual(circle2["e012"], 2.0)
        self.assertAlmostEqual(circle2["e013"], 0.0)
        self.assertAlmostEqual(circle2["e023"], 0.0)
        self.assertAlmostEqual(circle2["e01i"], 0.0)
        self.assertAlmostEqual(circle2["e02i"], 0.0)
        self.assertAlmostEqual(circle2["e03i"], 0.0)

    def test_creationFromMultivector(self):
        mv = Multivector.create(
            [
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
            ],
            [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
        )

        circle = Circle(mv)

        self.assertAlmostEqual(circle["e123"], 1.0)
        self.assertAlmostEqual(circle["e12i"], 2.0)
        self.assertAlmostEqual(circle["e13i"], 3.0)
        self.assertAlmostEqual(circle["e23i"], 4.0)
        self.assertAlmostEqual(circle["e012"], 5.0)
        self.assertAlmostEqual(circle["e013"], 6.0)
        self.assertAlmostEqual(circle["e023"], 7.0)
        self.assertAlmostEqual(circle["e01i"], 8.0)
        self.assertAlmostEqual(circle["e02i"], 9.0)
        self.assertAlmostEqual(circle["e03i"], 10.0)

    def test_addition(self):
        p1 = Point(1.0, 0.0, 0.0)
        p2 = Point(0.0, 1.0, 0.0)
        p3 = Point(-1.0, 0.0, 0.0)

        p4 = Point(1.0, 0.0, 0.0)
        p5 = Point(0.0, 1.0, 3.0)
        p6 = Point(-1.0, 0.0, 0.0)

        circle1 = Circle(p1, p2, p3)
        circle2 = Circle(p4, p5, p6)

        circle = circle1 + circle2

        self.assertTrue(isinstance(circle, Circle))

        self.assertAlmostEqual(circle["e123"], 0.0)
        self.assertAlmostEqual(circle["e12i"], 2.0)
        self.assertAlmostEqual(circle["e13i"], 3.0)
        self.assertAlmostEqual(circle["e23i"], 0.0)
        self.assertAlmostEqual(circle["e012"], 4.0)
        self.assertAlmostEqual(circle["e013"], 6.0)
        self.assertAlmostEqual(circle["e023"], 0.0)
        self.assertAlmostEqual(circle["e01i"], 9.0)
        self.assertAlmostEqual(circle["e02i"], 0.0)
        self.assertAlmostEqual(circle["e03i"], 0.0)

    def test_addition2(self):
        p1 = Point(1.0, 0.0, 0.0)
        p2 = Point(0.0, 1.0, 0.0)
        p3 = Point(-1.0, 0.0, 0.0)

        circle1 = Circle(p1, p2, p3)

        mv = Multivector.create(
            [
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
            ],
            [0.0, 1.0, 3.0, 0.0, 2.0, 6.0, 0.0, 9.0, 0.0, 0.0],
        )

        circle = circle1 + mv

        self.assertTrue(isinstance(circle, Circle))

        self.assertAlmostEqual(circle["e123"], 0.0)
        self.assertAlmostEqual(circle["e12i"], 2.0)
        self.assertAlmostEqual(circle["e13i"], 3.0)
        self.assertAlmostEqual(circle["e23i"], 0.0)
        self.assertAlmostEqual(circle["e012"], 4.0)
        self.assertAlmostEqual(circle["e013"], 6.0)
        self.assertAlmostEqual(circle["e023"], 0.0)
        self.assertAlmostEqual(circle["e01i"], 9.0)
        self.assertAlmostEqual(circle["e02i"], 0.0)
        self.assertAlmostEqual(circle["e03i"], 0.0)

    def test_substraction(self):
        p1 = Point(1.0, 0.0, 0.0)
        p2 = Point(0.0, 1.0, 0.0)
        p3 = Point(-1.0, 0.0, 0.0)

        p4 = Point(1.0, 0.0, 0.0)
        p5 = Point(0.0, 1.0, 3.0)
        p6 = Point(-1.0, 0.0, 0.0)

        circle1 = Circle(p1, p2, p3)
        circle2 = Circle(p4, p5, p6)

        circle = circle1 - circle2

        self.assertTrue(isinstance(circle, Circle))

        self.assertAlmostEqual(circle["e123"], 0.0)
        self.assertAlmostEqual(circle["e12i"], 0.0)
        self.assertAlmostEqual(circle["e13i"], -3.0)
        self.assertAlmostEqual(circle["e23i"], 0.0)
        self.assertAlmostEqual(circle["e012"], 0.0)
        self.assertAlmostEqual(circle["e013"], -6.0)
        self.assertAlmostEqual(circle["e023"], 0.0)
        self.assertAlmostEqual(circle["e01i"], -9.0)
        self.assertAlmostEqual(circle["e02i"], 0.0)
        self.assertAlmostEqual(circle["e03i"], 0.0)

    def test_substraction2(self):
        p1 = Point(1.0, 0.0, 0.0)
        p2 = Point(0.0, 1.0, 0.0)
        p3 = Point(-1.0, 0.0, 0.0)

        circle1 = Circle(p1, p2, p3)

        mv = Multivector.create(
            [
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
            ],
            [0.0, 1.0, 3.0, 0.0, 2.0, 6.0, 0.0, 9.0, 0.0, 0.0],
        )

        circle = circle1 - mv

        self.assertTrue(isinstance(circle, Circle))

        self.assertAlmostEqual(circle["e123"], 0.0)
        self.assertAlmostEqual(circle["e12i"], 0.0)
        self.assertAlmostEqual(circle["e13i"], -3.0)
        self.assertAlmostEqual(circle["e23i"], 0.0)
        self.assertAlmostEqual(circle["e012"], 0.0)
        self.assertAlmostEqual(circle["e013"], -6.0)
        self.assertAlmostEqual(circle["e023"], 0.0)
        self.assertAlmostEqual(circle["e01i"], -9.0)
        self.assertAlmostEqual(circle["e02i"], 0.0)
        self.assertAlmostEqual(circle["e03i"], 0.0)


if __name__ == "__main__":
    unittest.main()
