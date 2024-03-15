#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

import unittest

from pygafro import Line
from pygafro import Multivector
from pygafro import Point


class TestLine(unittest.TestCase):

    def test_creationFromPoints_origin(self):
        p1 = Point(0.0, 0.0, 0.0)
        p2 = Point(1.0, 2.0, 3.0)

        line = Line(p1, p2)

        self.assertAlmostEqual(line["e12i"], 0.0)
        self.assertAlmostEqual(line["e13i"], 0.0)
        self.assertAlmostEqual(line["e23i"], 0.0)
        self.assertAlmostEqual(line["e01i"], 1.0)
        self.assertAlmostEqual(line["e02i"], 2.0)
        self.assertAlmostEqual(line["e03i"], 3.0)

    def test_creationFromPoints_arbitrary(self):
        p1 = Point(1.0, 2.0, 3.0)
        p2 = Point(4.0, 5.0, 6.0)

        line = Line(p1, p2)

        self.assertAlmostEqual(line["e12i"], -3.0)
        self.assertAlmostEqual(line["e13i"], -6.0)
        self.assertAlmostEqual(line["e23i"], -3.0)
        self.assertAlmostEqual(line["e01i"], 3.0)
        self.assertAlmostEqual(line["e02i"], 3.0)
        self.assertAlmostEqual(line["e03i"], 3.0)

    def test_creationFromLine(self):
        p1 = Point(1.0, 2.0, 3.0)
        p2 = Point(4.0, 5.0, 6.0)

        line = Line(p1, p2)
        line2 = Line(line)

        self.assertAlmostEqual(line2["e12i"], -3.0)
        self.assertAlmostEqual(line2["e13i"], -6.0)
        self.assertAlmostEqual(line2["e23i"], -3.0)
        self.assertAlmostEqual(line2["e01i"], 3.0)
        self.assertAlmostEqual(line2["e02i"], 3.0)
        self.assertAlmostEqual(line2["e03i"], 3.0)

    def test_creationFromMultivector(self):
        mv = Multivector.create(
            ["e12i", "e13i", "e23i", "e01i", "e02i", "e03i"],
            [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
        )
        line = Line(mv)

        self.assertAlmostEqual(line["e12i"], 1.0)
        self.assertAlmostEqual(line["e13i"], 2.0)
        self.assertAlmostEqual(line["e23i"], 3.0)
        self.assertAlmostEqual(line["e01i"], 4.0)
        self.assertAlmostEqual(line["e02i"], 5.0)
        self.assertAlmostEqual(line["e03i"], 6.0)

    def test_addition(self):
        p1 = Point(1.0, 2.0, 3.0)
        p2 = Point(4.0, 5.0, 6.0)
        p3 = Point(10.0, 20.0, 30.0)
        p4 = Point(40.0, 50.0, 60.0)

        line1 = Line(p1, p2)
        line2 = Line(p3, p4)

        line = line1 + line2

        self.assertTrue(isinstance(line, Line))

        self.assertAlmostEqual(line["e12i"], -303.0)
        self.assertAlmostEqual(line["e13i"], -606.0)
        self.assertAlmostEqual(line["e23i"], -303.0)
        self.assertAlmostEqual(line["e01i"], 33.0)
        self.assertAlmostEqual(line["e02i"], 33.0)
        self.assertAlmostEqual(line["e03i"], 33.0)

    def test_addition2(self):
        p1 = Point(1.0, 2.0, 3.0)
        p2 = Point(4.0, 5.0, 6.0)

        mv = Multivector.create(
            ["e12i", "e13i", "e23i", "e01i", "e02i", "e03i"],
            [-300.0, -600.0, -300.0, 30.0, 30.0, 30.0],
        )

        line1 = Line(p1, p2)
        line2 = Line(mv)

        line = line1 + line2

        self.assertTrue(isinstance(line, Line))

        self.assertAlmostEqual(line["e12i"], -303.0)
        self.assertAlmostEqual(line["e13i"], -606.0)
        self.assertAlmostEqual(line["e23i"], -303.0)
        self.assertAlmostEqual(line["e01i"], 33.0)
        self.assertAlmostEqual(line["e02i"], 33.0)
        self.assertAlmostEqual(line["e03i"], 33.0)

    def test_substraction(self):
        p1 = Point(10.0, 20.0, 30.0)
        p2 = Point(40.0, 50.0, 60.0)
        p3 = Point(1.0, 2.0, 3.0)
        p4 = Point(4.0, 5.0, 6.0)

        line1 = Line(p1, p2)
        line2 = Line(p3, p4)

        line = line1 - line2

        self.assertTrue(isinstance(line, Line))

        self.assertAlmostEqual(line["e12i"], -297.0)
        self.assertAlmostEqual(line["e13i"], -594.0)
        self.assertAlmostEqual(line["e23i"], -297.0)
        self.assertAlmostEqual(line["e01i"], 27.0)
        self.assertAlmostEqual(line["e02i"], 27.0)
        self.assertAlmostEqual(line["e03i"], 27.0)

    def test_substraction2(self):
        p1 = Point(10.0, 20.0, 30.0)
        p2 = Point(40.0, 50.0, 60.0)
        mv = Multivector.create(
            ["e12i", "e13i", "e23i", "e01i", "e02i", "e03i"],
            [-3.0, -6.0, -3.0, 3.0, 3.0, 3.0],
        )

        line1 = Line(p1, p2)
        line2 = Line(mv)

        line = line1 - line2

        self.assertTrue(isinstance(line, Line))

        self.assertAlmostEqual(line["e12i"], -297.0)
        self.assertAlmostEqual(line["e13i"], -594.0)
        self.assertAlmostEqual(line["e23i"], -297.0)
        self.assertAlmostEqual(line["e01i"], 27.0)
        self.assertAlmostEqual(line["e02i"], 27.0)
        self.assertAlmostEqual(line["e03i"], 27.0)


if __name__ == "__main__":
    unittest.main()
