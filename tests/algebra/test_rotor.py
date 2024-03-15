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

import numpy as np

from pygafro import Line
from pygafro import Multivector
from pygafro import Plane
from pygafro import Point
from pygafro import Rotor
from pygafro import RotorGenerator
from pygafro import Sphere


class TestRotor(unittest.TestCase):

    def test_defaultCreation(self):
        rotor = Rotor()

        self.assertAlmostEqual(rotor["scalar"], 1.0)
        self.assertAlmostEqual(rotor["e23"], 0.0)
        self.assertAlmostEqual(rotor["e13"], 0.0)
        self.assertAlmostEqual(rotor["e12"], 0.0)
        self.assertAlmostEqual(rotor.angle(), 0.0)

    def test_creationFromMultivector_noAngle(self):
        mv = Multivector.create(["scalar", "e23", "e13", "e12"], [1.0, 1.0, 0.0, 0.0])
        rotor = Rotor(mv)

        self.assertAlmostEqual(rotor["scalar"], 1.0)
        self.assertAlmostEqual(rotor["e23"], 1.0)
        self.assertAlmostEqual(rotor["e13"], 0.0)
        self.assertAlmostEqual(rotor["e12"], 0.0)
        self.assertAlmostEqual(rotor.angle(), 0.0)

    def test_creationFromMultivector_withAngle(self):
        mv = Multivector.create(
            ["scalar", "e23", "e13", "e12"], [0.7071067812, -0.7071067812, 0.0, 0.0]
        )
        rotor = Rotor(mv)

        self.assertAlmostEqual(rotor["scalar"], 0.7071067812)
        self.assertAlmostEqual(rotor["e23"], -0.7071067812)
        self.assertAlmostEqual(rotor["e13"], 0.0)
        self.assertAlmostEqual(rotor["e12"], 0.0)
        self.assertAlmostEqual(rotor.angle(), math.pi / 2.0)

    def test_creationFromGenerator(self):
        generator = RotorGenerator([1.0, 0.0, 0.0])
        rotor = Rotor(generator, math.pi / 2.0)

        self.assertAlmostEqual(rotor["scalar"], 0.7071067812)
        self.assertAlmostEqual(rotor["e23"], -0.7071067812)
        self.assertAlmostEqual(rotor["e13"], 0.0)
        self.assertAlmostEqual(rotor["e12"], 0.0)
        self.assertAlmostEqual(rotor.angle(), math.pi / 2.0)

    def test_creationFromParameters_noAngle(self):
        rotor = Rotor([1.0, 1.0, 0.0, 0.0])

        self.assertAlmostEqual(rotor["scalar"], 1.0)
        self.assertAlmostEqual(rotor["e23"], 1.0)
        self.assertAlmostEqual(rotor["e13"], 0.0)
        self.assertAlmostEqual(rotor["e12"], 0.0)
        self.assertAlmostEqual(rotor.angle(), 0.0)

    def test_creationFromParameters_withAngle(self):
        rotor = Rotor([0.7071067812, -0.7071067812, 0.0, 0.0])

        self.assertAlmostEqual(rotor["scalar"], 0.7071067812)
        self.assertAlmostEqual(rotor["e23"], -0.7071067812)
        self.assertAlmostEqual(rotor["e13"], 0.0)
        self.assertAlmostEqual(rotor["e12"], 0.0)
        self.assertAlmostEqual(rotor.angle(), math.pi / 2.0)

    def test_creationFromQuaternion(self):
        rotor = Rotor.fromQuaternion(np.array([0.7071067812, 0.7071067812, 0.0, 0.0]))

        self.assertAlmostEqual(rotor["scalar"], 0.7071067812)
        self.assertAlmostEqual(rotor["e23"], -0.7071067812)
        self.assertAlmostEqual(rotor["e13"], 0.0)
        self.assertAlmostEqual(rotor["e12"], 0.0)
        self.assertAlmostEqual(rotor.angle(), math.pi / 2.0)

    def test_log_noAngle(self):
        generator = RotorGenerator([1.0, 0.0, 0.0])
        rotor = Rotor(generator, 0.0)

        log = rotor.log()

        self.assertTrue(isinstance(log, RotorGenerator))

        self.assertAlmostEqual(log.e23(), 0.0)
        self.assertAlmostEqual(log.e13(), 0.0)
        self.assertAlmostEqual(log.e12(), 0.0)

    def test_log_withAngle(self):
        generator = RotorGenerator([1.0, 0.0, 0.0])
        rotor = Rotor(generator, math.pi / 2.0)

        log = rotor.log()

        self.assertTrue(isinstance(log, RotorGenerator))

        self.assertAlmostEqual(log.e23(), math.pi / 2.0)
        self.assertAlmostEqual(log.e13(), 0.0)
        self.assertAlmostEqual(log.e12(), 0.0)

    def test_quaternion_noAngle(self):
        generator = RotorGenerator([1.0, 0.0, 0.0])
        rotor = Rotor(generator, 0.0)

        quaternion = rotor.quaternion()

        self.assertTrue(isinstance(quaternion, np.ndarray))
        self.assertEqual(quaternion.shape, (4,))

        self.assertAlmostEqual(quaternion[0], 1.0)
        self.assertAlmostEqual(quaternion[1], 0.0)
        self.assertAlmostEqual(quaternion[2], 0.0)
        self.assertAlmostEqual(quaternion[3], 0.0)

    def test_quaternion_withAngle(self):
        generator = RotorGenerator([1.0, 0.0, 0.0])
        rotor = Rotor(generator, math.pi / 2.0)

        quaternion = rotor.quaternion()

        self.assertTrue(isinstance(quaternion, np.ndarray))
        self.assertEqual(quaternion.shape, (4,))

        self.assertAlmostEqual(quaternion[0], 0.7071067812)
        self.assertAlmostEqual(quaternion[1], 0.7071067812)
        self.assertAlmostEqual(quaternion[2], 0.0)
        self.assertAlmostEqual(quaternion[3], 0.0)

    def test_rotationMatrix_noAngle(self):
        generator = RotorGenerator([1.0, 0.0, 0.0])
        rotor = Rotor(generator, 0.0)

        matrix = rotor.toRotationMatrix()

        self.assertTrue(isinstance(matrix, np.ndarray))
        self.assertEqual(matrix.shape, (3, 3))

        self.assertAlmostEqual(matrix[0, 0], 1.0)
        self.assertAlmostEqual(matrix[0, 1], 0.0)
        self.assertAlmostEqual(matrix[0, 2], 0.0)
        self.assertAlmostEqual(matrix[1, 0], 0.0)
        self.assertAlmostEqual(matrix[1, 1], 1.0)
        self.assertAlmostEqual(matrix[1, 2], 0.0)
        self.assertAlmostEqual(matrix[2, 0], 0.0)
        self.assertAlmostEqual(matrix[2, 1], 0.0)
        self.assertAlmostEqual(matrix[2, 2], 1.0)

    def test_rotationMatrix_withAngle(self):
        generator = RotorGenerator([1.0, 0.0, 0.0])
        rotor = Rotor(generator, math.pi / 2.0)

        matrix = rotor.toRotationMatrix()

        self.assertTrue(isinstance(matrix, np.ndarray))
        self.assertEqual(matrix.shape, (3, 3))

        self.assertAlmostEqual(matrix[0, 0], 1.0)
        self.assertAlmostEqual(matrix[0, 1], 0.0)
        self.assertAlmostEqual(matrix[0, 2], 0.0)
        self.assertAlmostEqual(matrix[1, 0], 0.0)
        self.assertAlmostEqual(matrix[1, 1], 0.0)
        self.assertAlmostEqual(matrix[1, 2], -1.0)
        self.assertAlmostEqual(matrix[2, 0], 0.0)
        self.assertAlmostEqual(matrix[2, 1], 1.0)
        self.assertAlmostEqual(matrix[2, 2], 0.0)

    def test_applyToPoint_origin(self):
        generator = RotorGenerator([0.0, 0.0, 1.0])
        rotor = Rotor(generator, math.pi / 2.0)

        point = Point()
        result = rotor.apply(point)

        self.assertTrue(isinstance(result, Point))

        self.assertAlmostEqual(result["e0"], point["e0"])
        self.assertAlmostEqual(result["e1"], point["e1"])
        self.assertAlmostEqual(result["e2"], point["e2"])
        self.assertAlmostEqual(result["e3"], point["e3"])
        self.assertAlmostEqual(result["ei"], point["ei"])

    def test_applyToPoint_other(self):
        generator = RotorGenerator([0.0, 0.0, 1.0])
        rotor = Rotor(generator, math.pi / 2.0)

        point = Point(1.0, 2.0, 3.0)
        result = rotor.apply(point)

        self.assertTrue(isinstance(result, Point))

        self.assertAlmostEqual(result["e0"], 1.0)
        self.assertAlmostEqual(result["e1"], -2.0)
        self.assertAlmostEqual(result["e2"], 1.0)
        self.assertAlmostEqual(result["e3"], 3.0)
        self.assertAlmostEqual(result["ei"], 7.0)

    def test_applyToLine(self):
        generator = RotorGenerator([0.0, 0.0, 1.0])
        rotor = Rotor(generator, math.pi / 2.0)

        p1 = Point()
        p2 = Point(1.0, 0.0, 0.0)
        line = Line(p1, p2)

        result = rotor.apply(line)

        self.assertTrue(isinstance(result, Line))

        self.assertAlmostEqual(result["e12i"], line["e12i"])
        self.assertAlmostEqual(result["e13i"], line["e13i"])
        self.assertAlmostEqual(result["e23i"], line["e23i"])
        self.assertAlmostEqual(result["e01i"], 0.0)
        self.assertAlmostEqual(result["e02i"], 1.0)
        self.assertAlmostEqual(result["e03i"], line["e03i"])

    def test_applyToPlane(self):
        generator = RotorGenerator([0.0, 0.0, 1.0])
        rotor = Rotor(generator, math.pi / 2.0)

        p1 = Point(0.0, 0.0, 0.0)
        p2 = Point(1.0, 0.0, 0.0)
        p3 = Point(0.0, 1.0, 0.0)
        plane = Plane(p1, p2, p3)

        result = rotor.apply(plane)

        self.assertTrue(isinstance(result, Plane))

        self.assertAlmostEqual(result["e123i"], plane["e123i"])
        self.assertAlmostEqual(result["e012i"], plane["e012i"])
        self.assertAlmostEqual(result["e023i"], plane["e023i"])
        self.assertAlmostEqual(result["e013i"], plane["e013i"])

    def test_applyToSphere(self):
        generator = RotorGenerator([0.0, 0.0, 1.0])
        rotor = Rotor(generator, math.pi / 2.0)

        center = Point(1.0, 0.0, 0.0)
        sphere = Sphere(center, 0.5)

        result = rotor.apply(sphere)

        self.assertTrue(isinstance(result, Sphere))

        resultCenter = result.getCenter()

        self.assertTrue(isinstance(resultCenter, Point))

        self.assertAlmostEqual(resultCenter["e0"], center["e0"])
        self.assertAlmostEqual(resultCenter["e1"], 0.0)
        self.assertAlmostEqual(resultCenter["e2"], 1.0)
        self.assertAlmostEqual(resultCenter["e3"], center["e3"])
        self.assertAlmostEqual(resultCenter["ei"], center["ei"])

        self.assertAlmostEqual(result.getRadius(), sphere.getRadius())

    def test_exponential(self):
        generator = RotorGenerator([1.0, 0.0, 0.0])

        exp = Rotor.exp(generator)

        self.assertAlmostEqual(exp["scalar"], 0.877583, places=5)
        self.assertAlmostEqual(exp["e23"], -0.479426, places=5)
        self.assertAlmostEqual(exp["e13"], 0.0)
        self.assertAlmostEqual(exp["e12"], 0.0)


if __name__ == "__main__":
    unittest.main()
