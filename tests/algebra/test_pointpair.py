#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

import math
import unittest

from pygafro import Multivector
from pygafro import Point
from pygafro import PointPair


class TestPointPair(unittest.TestCase):

    def test_defaultCreation(self):
        pair = PointPair()

        self.assertAlmostEqual(pair["e23"], 0.0)
        self.assertAlmostEqual(pair["e13"], 0.0)
        self.assertAlmostEqual(pair["e12"], 0.0)
        self.assertAlmostEqual(pair["e1i"], 0.0)
        self.assertAlmostEqual(pair["e2i"], 0.0)
        self.assertAlmostEqual(pair["e3i"], 0.0)
        self.assertAlmostEqual(pair["e01"], 0.0)
        self.assertAlmostEqual(pair["e02"], 0.0)
        self.assertAlmostEqual(pair["e03"], 0.0)
        self.assertAlmostEqual(pair["e0i"], 0.0)

        p1 = pair.getPoint1()

        self.assertTrue(isinstance(p1, Point))

        self.assertTrue(math.isnan(p1["e1"]))
        self.assertTrue(math.isnan(p1["e2"]))
        self.assertTrue(math.isnan(p1["e3"]))
        self.assertTrue(math.isnan(p1["ei"]))
        self.assertTrue(math.isnan(p1["e0"]))

        p2 = pair.getPoint2()

        self.assertTrue(isinstance(p2, Point))

        self.assertTrue(math.isnan(p2["e1"]))
        self.assertTrue(math.isnan(p2["e2"]))
        self.assertTrue(math.isnan(p2["e3"]))
        self.assertTrue(math.isnan(p2["ei"]))
        self.assertTrue(math.isnan(p2["e0"]))

    def test_creationFromPoints(self):
        p1 = Point(1.0, 2.0, 3.0)
        p2 = Point(4.0, 5.0, 6.0)

        pair = PointPair(p1, p2)

        self.assertAlmostEqual(pair["e23"], -3.0)
        self.assertAlmostEqual(pair["e13"], -6.0)
        self.assertAlmostEqual(pair["e12"], -3.0)
        self.assertAlmostEqual(pair["e1i"], 10.5)
        self.assertAlmostEqual(pair["e2i"], 42.0)
        self.assertAlmostEqual(pair["e3i"], 73.5)
        self.assertAlmostEqual(pair["e01"], 3.0)
        self.assertAlmostEqual(pair["e02"], 3.0)
        self.assertAlmostEqual(pair["e03"], 3.0)
        self.assertAlmostEqual(pair["e0i"], 31.5)

        p1b = pair.getPoint1()

        self.assertTrue(isinstance(p1b, Point))

        self.assertAlmostEqual(p1b["e1"], p1["e1"])
        self.assertAlmostEqual(p1b["e2"], p1["e2"])
        self.assertAlmostEqual(p1b["e3"], p1["e3"])
        self.assertAlmostEqual(p1b["ei"], p1["ei"])
        self.assertAlmostEqual(p1b["e0"], p1["e0"])

        p2b = pair.getPoint2()

        self.assertTrue(isinstance(p2b, Point))

        self.assertAlmostEqual(p2b["e1"], p2["e1"])
        self.assertAlmostEqual(p2b["e2"], p2["e2"])
        self.assertAlmostEqual(p2b["e3"], p2["e3"])
        self.assertAlmostEqual(p2b["ei"], p2["ei"])
        self.assertAlmostEqual(p2b["e0"], p2["e0"])

    def test_creationFromPair(self):
        p1 = Point(1.0, 2.0, 3.0)
        p2 = Point(4.0, 5.0, 6.0)

        pair = PointPair(p1, p2)
        pair2 = PointPair(pair)

        self.assertAlmostEqual(pair2["e23"], -3.0)
        self.assertAlmostEqual(pair2["e13"], -6.0)
        self.assertAlmostEqual(pair2["e12"], -3.0)
        self.assertAlmostEqual(pair2["e1i"], 10.5)
        self.assertAlmostEqual(pair2["e2i"], 42.0)
        self.assertAlmostEqual(pair2["e3i"], 73.5)
        self.assertAlmostEqual(pair2["e01"], 3.0)
        self.assertAlmostEqual(pair2["e02"], 3.0)
        self.assertAlmostEqual(pair2["e03"], 3.0)
        self.assertAlmostEqual(pair2["e0i"], 31.5)

    def test_creationFromMultivector(self):
        mv = Multivector.create(
            ["e23", "e13", "e12", "e1i", "e2i", "e3i", "e01", "e02", "e03", "e0i"],
            [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
        )
        pair = PointPair(mv)

        self.assertAlmostEqual(pair["e23"], 1.0)
        self.assertAlmostEqual(pair["e13"], 2.0)
        self.assertAlmostEqual(pair["e12"], 3.0)
        self.assertAlmostEqual(pair["e1i"], 4.0)
        self.assertAlmostEqual(pair["e2i"], 5.0)
        self.assertAlmostEqual(pair["e3i"], 6.0)
        self.assertAlmostEqual(pair["e01"], 7.0)
        self.assertAlmostEqual(pair["e02"], 8.0)
        self.assertAlmostEqual(pair["e03"], 9.0)
        self.assertAlmostEqual(pair["e0i"], 10.0)

    def test_addition(self):
        p1 = Point(1.0, 2.0, 3.0)
        p2 = Point(4.0, 5.0, 6.0)
        p3 = Point(10.0, 20.0, 30.0)
        p4 = Point(40.0, 50.0, 60.0)

        pair1 = PointPair(p1, p2)
        pair2 = PointPair(p3, p4)

        pair = pair1 + pair2

        self.assertTrue(isinstance(pair, PointPair))

        self.assertAlmostEqual(pair["e23"], -303.0)
        self.assertAlmostEqual(pair["e13"], -606.0)
        self.assertAlmostEqual(pair["e12"], -303.0)
        self.assertAlmostEqual(pair["e1i"], 10510.5)
        self.assertAlmostEqual(pair["e2i"], 42042.0)
        self.assertAlmostEqual(pair["e3i"], 73573.5)
        self.assertAlmostEqual(pair["e01"], 33.0)
        self.assertAlmostEqual(pair["e02"], 33.0)
        self.assertAlmostEqual(pair["e03"], 33.0)
        self.assertAlmostEqual(pair["e0i"], 3181.5)

    def test_addition2(self):
        p1 = Point(1.0, 2.0, 3.0)
        p2 = Point(4.0, 5.0, 6.0)

        pair1 = PointPair(p1, p2)

        mv = Multivector.create(
            ["e23", "e13", "e12", "e1i", "e2i", "e3i", "e01", "e02", "e03", "e0i"],
            [
                -300.0,
                -600.0,
                -300.0,
                10500.0,
                42000.0,
                73500.0,
                30.0,
                30.0,
                30.0,
                3150.0,
            ],
        )

        pair = pair1 + mv

        self.assertTrue(isinstance(pair, PointPair))

        self.assertAlmostEqual(pair["e23"], -303.0)
        self.assertAlmostEqual(pair["e13"], -606.0)
        self.assertAlmostEqual(pair["e12"], -303.0)
        self.assertAlmostEqual(pair["e1i"], 10510.5)
        self.assertAlmostEqual(pair["e2i"], 42042.0)
        self.assertAlmostEqual(pair["e3i"], 73573.5)
        self.assertAlmostEqual(pair["e01"], 33.0)
        self.assertAlmostEqual(pair["e02"], 33.0)
        self.assertAlmostEqual(pair["e03"], 33.0)
        self.assertAlmostEqual(pair["e0i"], 3181.5)

    def test_substraction(self):
        p1 = Point(1.0, 2.0, 3.0)
        p2 = Point(4.0, 5.0, 6.0)
        p3 = Point(10.0, 20.0, 30.0)
        p4 = Point(40.0, 50.0, 60.0)

        pair1 = PointPair(p1, p2)
        pair2 = PointPair(p3, p4)

        pair = pair1 - pair2

        self.assertTrue(isinstance(pair, PointPair))

        self.assertAlmostEqual(pair["e23"], 297.0)
        self.assertAlmostEqual(pair["e13"], 594.0)
        self.assertAlmostEqual(pair["e12"], 297.0)
        self.assertAlmostEqual(pair["e1i"], -10489.5)
        self.assertAlmostEqual(pair["e2i"], -41958.0)
        self.assertAlmostEqual(pair["e3i"], -73426.5)
        self.assertAlmostEqual(pair["e01"], -27.0)
        self.assertAlmostEqual(pair["e02"], -27.0)
        self.assertAlmostEqual(pair["e03"], -27.0)
        self.assertAlmostEqual(pair["e0i"], -3118.5)

    def test_substraction2(self):
        p1 = Point(1.0, 2.0, 3.0)
        p2 = Point(4.0, 5.0, 6.0)

        pair1 = PointPair(p1, p2)

        mv = Multivector.create(
            ["e23", "e13", "e12", "e1i", "e2i", "e3i", "e01", "e02", "e03", "e0i"],
            [
                -300.0,
                -600.0,
                -300.0,
                10500.0,
                42000.0,
                73500.0,
                30.0,
                30.0,
                30.0,
                3150.0,
            ],
        )

        pair = pair1 - mv

        self.assertTrue(isinstance(pair, PointPair))

        self.assertAlmostEqual(pair["e23"], 297.0)
        self.assertAlmostEqual(pair["e13"], 594.0)
        self.assertAlmostEqual(pair["e12"], 297.0)
        self.assertAlmostEqual(pair["e1i"], -10489.5)
        self.assertAlmostEqual(pair["e2i"], -41958.0)
        self.assertAlmostEqual(pair["e3i"], -73426.5)
        self.assertAlmostEqual(pair["e01"], -27.0)
        self.assertAlmostEqual(pair["e02"], -27.0)
        self.assertAlmostEqual(pair["e03"], -27.0)
        self.assertAlmostEqual(pair["e0i"], -3118.5)


if __name__ == "__main__":
    unittest.main()
