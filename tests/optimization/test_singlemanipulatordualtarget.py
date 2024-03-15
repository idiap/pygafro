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

import helpers

from pygafro import Point
from pygafro import SingleManipulatorDualTarget
from pygafro import Sphere


class TestSingleManipulatorDualTargetPointToolPointTarget(unittest.TestCase):

    def setUp(self):
        self.manipulator = helpers.createManipulatorWith3Joints()

        target_position = [0.0, math.pi / 2.0, 0.0]
        ee_target_point = self.manipulator.getEEMotor(target_position).apply(Point())

        self.cost_function = SingleManipulatorDualTarget(
            self.manipulator, Point(), ee_target_point
        )

    def tearDown(self):
        self.cost_function = None
        self.manipulator = None

    def testGetValue(self):
        self.assertAlmostEqual(self.cost_function.getValue([0.0, 0.0, 0.0]), 1.0)
        self.assertAlmostEqual(
            self.cost_function.getValue([0.2, 0.0, 0.0]), 0.41284, places=3
        )
        self.assertAlmostEqual(
            self.cost_function.getValue([0.0, math.pi / 4.0, 0.0]), 0.0857, places=3
        )
        self.assertAlmostEqual(
            self.cost_function.getValue([0.0, math.pi / 2.0, 0.0]), 0.0
        )

    def testGetError(self):
        error = self.cost_function.getError([0.0, 0.0, 0.0])

        self.assertEqual(error.shape, (1,))

        self.assertAlmostEqual(error[0], 1.0)

        error = self.cost_function.getError([0.0, math.pi / 4.0, 0.0])

        self.assertEqual(error.shape, (1,))

        self.assertAlmostEqual(error[0], 0.29289, places=4)

        error = self.cost_function.getError([0.0, math.pi / 2.0, 0.0])

        self.assertEqual(error.shape, (1,))

        self.assertAlmostEqual(error[0], 0.0)

    def testGetJacobian(self):
        jacobian = self.cost_function.getJacobian([0.0, 0.0, 0.0])

        self.assertEqual(jacobian.shape, (1, 3))

        self.assertAlmostEqual(jacobian[0, 0], -4.0)
        self.assertAlmostEqual(jacobian[0, 1], -2.0)
        self.assertAlmostEqual(jacobian[0, 2], 0.0)

    def testGetGradient(self):
        gradient = self.cost_function.getGradient([0.0, 0.0, 0.0])

        self.assertEqual(gradient.shape, (3,))

        self.assertAlmostEqual(gradient[0], -4.0)
        self.assertAlmostEqual(gradient[1], -2.0)
        self.assertAlmostEqual(gradient[2], 0.0)

    def testGetGradientAndHessian(self):
        gradient, hessian = self.cost_function.getGradientAndHessian([0.0, 0.0, 0.0])

        self.assertEqual(gradient.shape, (3,))
        self.assertEqual(hessian.shape, (3, 3))

        self.assertAlmostEqual(gradient[0], -4.0)
        self.assertAlmostEqual(gradient[1], -2.0)
        self.assertAlmostEqual(gradient[2], 0.0)

        self.assertAlmostEqual(hessian[0, 0], 16.0)
        self.assertAlmostEqual(hessian[1, 0], 8.0)
        self.assertAlmostEqual(hessian[2, 0], 0.0)

        self.assertAlmostEqual(hessian[0, 1], 8.0)
        self.assertAlmostEqual(hessian[1, 1], 4.0)
        self.assertAlmostEqual(hessian[2, 1], 0.0)

        self.assertAlmostEqual(hessian[0, 2], 0.0)
        self.assertAlmostEqual(hessian[1, 2], 0.0)
        self.assertAlmostEqual(hessian[2, 2], 0.0)


class TestSingleManipulatorDualTargetPointToolSphereTarget(unittest.TestCase):

    def setUp(self):
        self.manipulator = helpers.createManipulatorWith3Joints()

        target_position = [0.0, math.pi / 2.0, 0.0]
        ee_target_sphere = self.manipulator.getEEMotor(target_position).apply(
            Sphere(Point(), 0.1)
        )

        self.cost_function = SingleManipulatorDualTarget(
            self.manipulator, Point(), ee_target_sphere
        )

    def tearDown(self):
        self.cost_function = None
        self.manipulator = None

    def testGetValue(self):
        self.assertAlmostEqual(self.cost_function.getValue([0.0, 0.0, 0.0]), 37.56525)
        self.assertAlmostEqual(
            self.cost_function.getValue([0.2, 0.0, 0.0]), 24.2237, places=3
        )
        self.assertAlmostEqual(
            self.cost_function.getValue([0.0, math.pi / 4.0, 0.0]), 10.0478, places=4
        )
        self.assertAlmostEqual(
            self.cost_function.getValue([0.0, math.pi / 2.0, 0.0]), 0.00015
        )

    def testGetError(self):
        error = self.cost_function.getError([0.0, 0.0, 0.0])

        self.assertEqual(error.shape, (10,))

        self.assertAlmostEqual(error[0], 2.005)
        self.assertAlmostEqual(error[1], 0.0)
        self.assertAlmostEqual(error[2], -1.515)
        self.assertAlmostEqual(error[3], -4.5)
        self.assertAlmostEqual(error[4], 0.0)
        self.assertAlmostEqual(error[5], -1.0)
        self.assertAlmostEqual(error[6], 1.0)
        self.assertAlmostEqual(error[7], 0.0)
        self.assertAlmostEqual(error[8], 0.0)
        self.assertAlmostEqual(error[9], -3.0)

        error = self.cost_function.getError([0.0, math.pi / 4.0, 0.0])

        self.assertAlmostEqual(error[0], 1.41921, places=5)
        self.assertAlmostEqual(error[1], 0.0)
        self.assertAlmostEqual(error[2], -1.0742, places=5)
        self.assertAlmostEqual(error[3], -2.14998, places=5)
        self.assertAlmostEqual(error[4], 0.0)
        self.assertAlmostEqual(error[5], -0.707107, places=5)
        self.assertAlmostEqual(error[6], 0.292893, places=5)
        self.assertAlmostEqual(error[7], 0.0)
        self.assertAlmostEqual(error[8], 0.0)
        self.assertAlmostEqual(error[9], -1.29289, places=5)

        error = self.cost_function.getError([0.0, math.pi / 2.0, 0.0])

        self.assertAlmostEqual(error[0], 0.005)
        self.assertAlmostEqual(error[1], 0.0)
        self.assertAlmostEqual(error[2], -0.01)
        self.assertAlmostEqual(error[3], -0.005)
        self.assertAlmostEqual(error[4], 0.0)
        self.assertAlmostEqual(error[5], 0.0)
        self.assertAlmostEqual(error[6], 0.0)
        self.assertAlmostEqual(error[7], 0.0)
        self.assertAlmostEqual(error[8], 0.0)
        self.assertAlmostEqual(error[9], 0.0)

    def testGetJacobian(self):
        jacobian = self.cost_function.getJacobian([0.0, 0.0, 0.0])

        self.assertEqual(jacobian.shape, (10, 3))

        self.assertAlmostEqual(jacobian[0, 0], 0.0)
        self.assertAlmostEqual(jacobian[1, 0], 0.0)
        self.assertAlmostEqual(jacobian[2, 0], 0.0)
        self.assertAlmostEqual(jacobian[3, 0], 9.98)
        self.assertAlmostEqual(jacobian[4, 0], 0.0)
        self.assertAlmostEqual(jacobian[5, 0], 0.0)
        self.assertAlmostEqual(jacobian[6, 0], -4.0)
        self.assertAlmostEqual(jacobian[7, 0], 0.0)
        self.assertAlmostEqual(jacobian[8, 0], 0.0)
        self.assertAlmostEqual(jacobian[9, 0], 8.0)

        self.assertAlmostEqual(jacobian[0, 1], 0.0)
        self.assertAlmostEqual(jacobian[1, 1], 0.0)
        self.assertAlmostEqual(jacobian[2, 1], 0.0)
        self.assertAlmostEqual(jacobian[3, 1], 4.99)
        self.assertAlmostEqual(jacobian[4, 1], 0.0)
        self.assertAlmostEqual(jacobian[5, 1], 0.0)
        self.assertAlmostEqual(jacobian[6, 1], -2.0)
        self.assertAlmostEqual(jacobian[7, 1], 0.0)
        self.assertAlmostEqual(jacobian[8, 1], 0.0)
        self.assertAlmostEqual(jacobian[9, 1], 4.0)

        self.assertAlmostEqual(jacobian[0, 2], 0.0)
        self.assertAlmostEqual(jacobian[1, 2], 0.0)
        self.assertAlmostEqual(jacobian[2, 2], 0.0)
        self.assertAlmostEqual(jacobian[3, 2], 0.0)
        self.assertAlmostEqual(jacobian[4, 2], 0.0)
        self.assertAlmostEqual(jacobian[5, 2], 0.0)
        self.assertAlmostEqual(jacobian[6, 2], 0.0)
        self.assertAlmostEqual(jacobian[7, 2], 0.0)
        self.assertAlmostEqual(jacobian[8, 2], 0.0)
        self.assertAlmostEqual(jacobian[9, 2], 0.0)

        jacobian = self.cost_function.getJacobian([0.0, math.pi / 4.0, 0.0])

        self.assertAlmostEqual(jacobian[0, 0], -1.41421, places=5)
        self.assertAlmostEqual(jacobian[1, 0], 0.0)
        self.assertAlmostEqual(jacobian[2, 0], -0.700036, places=5)
        self.assertAlmostEqual(jacobian[3, 0], 9.93268, places=5)
        self.assertAlmostEqual(jacobian[4, 0], 0.0)
        self.assertAlmostEqual(jacobian[5, 0], 1.41421, places=5)
        self.assertAlmostEqual(jacobian[6, 0], -3.41421, places=5)
        self.assertAlmostEqual(jacobian[7, 0], 0.0)
        self.assertAlmostEqual(jacobian[8, 0], 0.0)
        self.assertAlmostEqual(jacobian[9, 0], 8.24264, places=5)

        self.assertAlmostEqual(jacobian[0, 1], -2.82843, places=5)
        self.assertAlmostEqual(jacobian[1, 1], 0.0)
        self.assertAlmostEqual(jacobian[2, 1], 2.12839, places=5)
        self.assertAlmostEqual(jacobian[3, 1], 6.35689, places=5)
        self.assertAlmostEqual(jacobian[4, 1], 0.0)
        self.assertAlmostEqual(jacobian[5, 1], 1.41421, places=5)
        self.assertAlmostEqual(jacobian[6, 1], -1.41421, places=5)
        self.assertAlmostEqual(jacobian[7, 1], 0.0)
        self.assertAlmostEqual(jacobian[8, 1], 0.0)
        self.assertAlmostEqual(jacobian[9, 1], 4.24264, places=5)

        self.assertAlmostEqual(jacobian[0, 2], 0.0)
        self.assertAlmostEqual(jacobian[1, 2], 0.0)
        self.assertAlmostEqual(jacobian[2, 2], 0.0)
        self.assertAlmostEqual(jacobian[3, 2], 0.0)
        self.assertAlmostEqual(jacobian[4, 2], 0.0)
        self.assertAlmostEqual(jacobian[5, 2], 0.0)
        self.assertAlmostEqual(jacobian[6, 2], 0.0)
        self.assertAlmostEqual(jacobian[7, 2], 0.0)
        self.assertAlmostEqual(jacobian[8, 2], 0.0)
        self.assertAlmostEqual(jacobian[9, 2], 0.0)

        jacobian = self.cost_function.getJacobian([0.0, math.pi / 2.0, 0.0])

        self.assertAlmostEqual(jacobian[0, 0], -2.0)
        self.assertAlmostEqual(jacobian[1, 0], 0.0)
        self.assertAlmostEqual(jacobian[2, 0], -0.99)
        self.assertAlmostEqual(jacobian[3, 0], 6.99)
        self.assertAlmostEqual(jacobian[4, 0], 0.0)
        self.assertAlmostEqual(jacobian[5, 0], 2.0)
        self.assertAlmostEqual(jacobian[6, 0], -2.0)
        self.assertAlmostEqual(jacobian[7, 0], 0.0)
        self.assertAlmostEqual(jacobian[8, 0], 0.0)
        self.assertAlmostEqual(jacobian[9, 0], 6.0)

        self.assertAlmostEqual(jacobian[0, 1], -4.0)
        self.assertAlmostEqual(jacobian[1, 1], 0.0)
        self.assertAlmostEqual(jacobian[2, 1], 3.01)
        self.assertAlmostEqual(jacobian[3, 1], 4.0)
        self.assertAlmostEqual(jacobian[4, 1], 0.0)
        self.assertAlmostEqual(jacobian[5, 1], 2.0)
        self.assertAlmostEqual(jacobian[6, 1], 0.0)
        self.assertAlmostEqual(jacobian[7, 1], 0.0)
        self.assertAlmostEqual(jacobian[8, 1], 0.0)
        self.assertAlmostEqual(jacobian[9, 1], 2.0)

        self.assertAlmostEqual(jacobian[0, 2], 0.0)
        self.assertAlmostEqual(jacobian[1, 2], 0.0)
        self.assertAlmostEqual(jacobian[2, 2], 0.0)
        self.assertAlmostEqual(jacobian[3, 2], 0.0)
        self.assertAlmostEqual(jacobian[4, 2], 0.0)
        self.assertAlmostEqual(jacobian[5, 2], 0.0)
        self.assertAlmostEqual(jacobian[6, 2], 0.0)
        self.assertAlmostEqual(jacobian[7, 2], 0.0)
        self.assertAlmostEqual(jacobian[8, 2], 0.0)
        self.assertAlmostEqual(jacobian[9, 2], 0.0)

    def testGetGradient(self):
        gradient = self.cost_function.getGradient([0.0, 0.0, 0.0])

        self.assertEqual(gradient.shape, (3,))

        self.assertAlmostEqual(gradient[0], -72.91)
        self.assertAlmostEqual(gradient[1], -36.455)
        self.assertAlmostEqual(gradient[2], 0.0)

        gradient = self.cost_function.getGradient([0.0, math.pi / 4.0, 0.0])

        self.assertAlmostEqual(gradient[0], -35.267, places=3)
        self.assertAlmostEqual(gradient[1], -26.8671, places=3)
        self.assertAlmostEqual(gradient[2], 0.0)

        gradient = self.cost_function.getGradient([0.0, math.pi / 2.0, 0.0])

        self.assertAlmostEqual(gradient[0], -0.03505)
        self.assertAlmostEqual(gradient[1], -0.0701)
        self.assertAlmostEqual(gradient[2], 0.0)

    def testGetGradientAndHessian(self):
        gradient, hessian = self.cost_function.getGradientAndHessian([0.0, 0.0, 0.0])

        self.assertEqual(gradient.shape, (3,))
        self.assertEqual(hessian.shape, (3, 3))

        self.assertAlmostEqual(gradient[0], -72.91)
        self.assertAlmostEqual(gradient[1], -36.455)
        self.assertAlmostEqual(gradient[2], 0.0)

        self.assertAlmostEqual(hessian[0, 0], 179.6, places=3)
        self.assertAlmostEqual(hessian[1, 0], 89.8002)
        self.assertAlmostEqual(hessian[2, 0], 0.0)

        self.assertAlmostEqual(hessian[0, 1], 89.8002)
        self.assertAlmostEqual(hessian[1, 1], 44.9001)
        self.assertAlmostEqual(hessian[2, 1], 0.0)

        self.assertAlmostEqual(hessian[0, 2], 0.0)
        self.assertAlmostEqual(hessian[1, 2], 0.0)
        self.assertAlmostEqual(hessian[2, 2], 0.0)

        gradient, hessian = self.cost_function.getGradientAndHessian(
            [0.0, math.pi / 4.0, 0.0]
        )

        self.assertAlmostEqual(gradient[0], -35.267, places=3)
        self.assertAlmostEqual(gradient[1], -26.8671, places=3)
        self.assertAlmostEqual(gradient[2], 0.0)

        self.assertAlmostEqual(hessian[0, 0], 182.746, places=3)
        self.assertAlmostEqual(hessian[1, 0], 107.45, places=3)
        self.assertAlmostEqual(hessian[2, 0], 0.0)

        self.assertAlmostEqual(hessian[0, 1], 107.45, places=3)
        self.assertAlmostEqual(hessian[1, 1], 74.9401)
        self.assertAlmostEqual(hessian[2, 1], 0.0)

        self.assertAlmostEqual(hessian[0, 2], 0.0)
        self.assertAlmostEqual(hessian[1, 2], 0.0)
        self.assertAlmostEqual(hessian[2, 2], 0.0)

        gradient, hessian = self.cost_function.getGradientAndHessian(
            [0.0, math.pi / 2.0, 0.0]
        )

        self.assertAlmostEqual(gradient[0], -0.03505)
        self.assertAlmostEqual(gradient[1], -0.0701)
        self.assertAlmostEqual(gradient[2], 0.0)

        self.assertAlmostEqual(hessian[0, 0], 97.8402, places=3)
        self.assertAlmostEqual(hessian[1, 0], 48.9801, places=3)
        self.assertAlmostEqual(hessian[2, 0], 0.0)

        self.assertAlmostEqual(hessian[0, 1], 48.9801, places=3)
        self.assertAlmostEqual(hessian[1, 1], 49.0601)
        self.assertAlmostEqual(hessian[2, 1], 0.0)

        self.assertAlmostEqual(hessian[0, 2], 0.0)
        self.assertAlmostEqual(hessian[1, 2], 0.0)
        self.assertAlmostEqual(hessian[2, 2], 0.0)


if __name__ == "__main__":
    unittest.main()
