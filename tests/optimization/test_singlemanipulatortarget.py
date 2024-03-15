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
from pygafro import SingleManipulatorTarget
from pygafro import Sphere


class TestSingleManipulatorTargetPointToolPointTarget(unittest.TestCase):

    def setUp(self):
        self.manipulator = helpers.createManipulatorWith3Joints()

        target_position = [0.0, math.pi / 2.0, 0.0]
        ee_target_point = self.manipulator.getEEMotor(target_position).apply(Point())

        self.cost_function = SingleManipulatorTarget(
            self.manipulator, Point(), ee_target_point
        )

    def tearDown(self):
        self.cost_function = None
        self.manipulator = None

    def testGetValue(self):
        self.assertAlmostEqual(self.cost_function.getValue([0.0, 0.0, 0.0]), 37.5)
        self.assertAlmostEqual(
            self.cost_function.getValue([0.2, 0.0, 0.0]), 24.145, places=3
        )
        self.assertAlmostEqual(
            self.cost_function.getValue([0.0, math.pi / 4.0, 0.0]), 9.9895, places=3
        )
        self.assertAlmostEqual(
            self.cost_function.getValue([0.0, math.pi / 2.0, 0.0]), 0.0
        )

    def testGetError(self):
        error = self.cost_function.getError([0.0, 0.0, 0.0])

        self.assertEqual(error.shape, (10,))

        self.assertAlmostEqual(error[0], 0.0)
        self.assertAlmostEqual(error[1], 0.0)
        self.assertAlmostEqual(error[2], -3.0)
        self.assertAlmostEqual(error[3], -4.5)
        self.assertAlmostEqual(error[4], 1.5)
        self.assertAlmostEqual(error[5], 0.0)
        self.assertAlmostEqual(error[6], 1.0)
        self.assertAlmostEqual(error[7], 1.0)
        self.assertAlmostEqual(error[8], 0.0)
        self.assertAlmostEqual(error[9], 2.0)

        error = self.cost_function.getError([0.0, math.pi / 4.0, 0.0])

        self.assertEqual(error.shape, (10,))

        self.assertAlmostEqual(error[0], 0.0)
        self.assertAlmostEqual(error[1], 0.0)
        self.assertAlmostEqual(error[2], -1.29289, places=5)
        self.assertAlmostEqual(error[3], -2.14645, places=5)
        self.assertAlmostEqual(error[4], 1.06066, places=5)
        self.assertAlmostEqual(error[5], 0.0)
        self.assertAlmostEqual(error[6], 0.292893, places=5)
        self.assertAlmostEqual(error[7], 0.707107, places=5)
        self.assertAlmostEqual(error[8], 0.0)
        self.assertAlmostEqual(error[9], 1.41421, places=5)

        error = self.cost_function.getError([0.0, math.pi / 2.0, 0.0])

        self.assertEqual(error.shape, (10,))

        self.assertAlmostEqual(error[0], 0.0)
        self.assertAlmostEqual(error[1], 0.0)
        self.assertAlmostEqual(error[2], 0.0)
        self.assertAlmostEqual(error[3], 0.0)
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
        self.assertAlmostEqual(jacobian[2, 0], 8.0)
        self.assertAlmostEqual(jacobian[3, 0], 10.0)
        self.assertAlmostEqual(jacobian[4, 0], 0.0)
        self.assertAlmostEqual(jacobian[5, 0], 0.0)
        self.assertAlmostEqual(jacobian[6, 0], -4.0)
        self.assertAlmostEqual(jacobian[7, 0], 0.0)
        self.assertAlmostEqual(jacobian[8, 0], 0.0)
        self.assertAlmostEqual(jacobian[9, 0], 0.0)

        self.assertAlmostEqual(jacobian[0, 1], 0.0)
        self.assertAlmostEqual(jacobian[1, 1], 0.0)
        self.assertAlmostEqual(jacobian[2, 1], 4.0)
        self.assertAlmostEqual(jacobian[3, 1], 5.0)
        self.assertAlmostEqual(jacobian[4, 1], 0.0)
        self.assertAlmostEqual(jacobian[5, 1], 0.0)
        self.assertAlmostEqual(jacobian[6, 1], -2.0)
        self.assertAlmostEqual(jacobian[7, 1], 0.0)
        self.assertAlmostEqual(jacobian[8, 1], 0.0)
        self.assertAlmostEqual(jacobian[9, 1], 0.0)

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

        self.assertAlmostEqual(gradient[0], -73.0)
        self.assertAlmostEqual(gradient[1], -36.5)
        self.assertAlmostEqual(gradient[2], 0.0)

    def testGetGradientAndHessian(self):
        gradient, hessian = self.cost_function.getGradientAndHessian([0.0, 0.0, 0.0])

        self.assertEqual(gradient.shape, (3,))
        self.assertEqual(hessian.shape, (3, 3))

        self.assertAlmostEqual(gradient[0], -73.0)
        self.assertAlmostEqual(gradient[1], -36.5)
        self.assertAlmostEqual(gradient[2], 0.0)

        self.assertAlmostEqual(hessian[0, 0], 180.0)
        self.assertAlmostEqual(hessian[1, 0], 90.0)
        self.assertAlmostEqual(hessian[2, 0], 0.0)

        self.assertAlmostEqual(hessian[0, 1], 90.0)
        self.assertAlmostEqual(hessian[1, 1], 45.0)
        self.assertAlmostEqual(hessian[2, 1], 0.0)

        self.assertAlmostEqual(hessian[0, 2], 0.0)
        self.assertAlmostEqual(hessian[1, 2], 0.0)
        self.assertAlmostEqual(hessian[2, 2], 0.0)


class TestSingleManipulatorTargetPointToolSphereTarget(unittest.TestCase):

    def setUp(self):
        self.manipulator = helpers.createManipulatorWith3Joints()

        target_position = [0.0, math.pi / 2.0, 0.0]
        ee_target_sphere = self.manipulator.getEEMotor(target_position).apply(
            Sphere(Point(), 0.1)
        )

        self.cost_function = SingleManipulatorTarget(
            self.manipulator, Point(), ee_target_sphere
        )

    def tearDown(self):
        self.cost_function = None
        self.manipulator = None

    def testGetValue(self):
        self.assertAlmostEqual(self.cost_function.getValue([0.0, 0.0, 0.0]), 0.990025)
        self.assertAlmostEqual(
            self.cost_function.getValue([0.2, 0.0, 0.0]), 0.4064, places=4
        )
        self.assertAlmostEqual(
            self.cost_function.getValue([0.0, math.pi / 4.0, 0.0]), 0.0828, places=3
        )
        self.assertAlmostEqual(
            self.cost_function.getValue([0.0, math.pi / 2.0, 0.0]), 0.000025
        )

    def testGetError(self):
        error = self.cost_function.getError([0.0, 0.0, 0.0])

        self.assertEqual(error.shape, (1,))

        self.assertAlmostEqual(error[0], -0.995)

    def testGetJacobian(self):
        jacobian = self.cost_function.getJacobian([0.0, 0.0, 0.0])

        self.assertEqual(jacobian.shape, (1, 3))

        self.assertAlmostEqual(jacobian[0, 0], 4.0)
        self.assertAlmostEqual(jacobian[0, 1], 2.0)
        self.assertAlmostEqual(jacobian[0, 2], 0.0)

        jacobian = self.cost_function.getJacobian([0.0, math.pi / 4.0, 0.0])

        self.assertAlmostEqual(jacobian[0, 0], 2.0)
        self.assertAlmostEqual(jacobian[0, 1], 1.41421, places=5)
        self.assertAlmostEqual(jacobian[0, 2], 0.0)

        jacobian = self.cost_function.getJacobian([0.0, math.pi / 2.0, 0.0])

        self.assertAlmostEqual(jacobian[0, 0], 0.0)
        self.assertAlmostEqual(jacobian[0, 1], 0.0)
        self.assertAlmostEqual(jacobian[0, 2], 0.0)

    def testGetGradient(self):
        gradient = self.cost_function.getGradient([0.0, 0.0, 0.0])

        self.assertEqual(gradient.shape, (3,))

        self.assertAlmostEqual(gradient[0], -3.98)
        self.assertAlmostEqual(gradient[1], -1.99)
        self.assertAlmostEqual(gradient[2], 0.0)

        gradient = self.cost_function.getGradient([0.0, math.pi / 4.0, 0.0])

        self.assertAlmostEqual(gradient[0], -0.575786, places=6)
        self.assertAlmostEqual(gradient[1], -0.407142, places=6)
        self.assertAlmostEqual(gradient[2], 0.0)

        gradient = self.cost_function.getGradient([0.0, math.pi / 2.0, 0.0])

        self.assertAlmostEqual(gradient[0], 0.0)
        self.assertAlmostEqual(gradient[1], 0.0)
        self.assertAlmostEqual(gradient[2], 0.0)

    def testGetGradientAndHessian(self):
        gradient, hessian = self.cost_function.getGradientAndHessian([0.0, 0.0, 0.0])

        self.assertEqual(gradient.shape, (3,))
        self.assertEqual(hessian.shape, (3, 3))

        self.assertAlmostEqual(gradient[0], -3.98)
        self.assertAlmostEqual(gradient[1], -1.99)
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

        gradient, hessian = self.cost_function.getGradientAndHessian(
            [0.0, math.pi / 4.0, 0.0]
        )

        self.assertAlmostEqual(gradient[0], -0.575786, places=6)
        self.assertAlmostEqual(gradient[1], -0.407142, places=6)
        self.assertAlmostEqual(gradient[2], 0.0)

        self.assertAlmostEqual(hessian[0, 0], 4.0)
        self.assertAlmostEqual(hessian[1, 0], 2.82843, places=5)
        self.assertAlmostEqual(hessian[2, 0], 0.0)

        self.assertAlmostEqual(hessian[0, 1], 2.82843, places=5)
        self.assertAlmostEqual(hessian[1, 1], 2.0)
        self.assertAlmostEqual(hessian[2, 1], 0.0)

        self.assertAlmostEqual(hessian[0, 2], 0.0)
        self.assertAlmostEqual(hessian[1, 2], 0.0)
        self.assertAlmostEqual(hessian[2, 2], 0.0)

        gradient, hessian = self.cost_function.getGradientAndHessian(
            [0.0, math.pi / 2.0, 0.0]
        )

        self.assertAlmostEqual(gradient[0], 0.0)
        self.assertAlmostEqual(gradient[1], 0.0)
        self.assertAlmostEqual(gradient[2], 0.0)

        self.assertAlmostEqual(hessian[0, 0], 0.0)
        self.assertAlmostEqual(hessian[1, 0], 0.0)
        self.assertAlmostEqual(hessian[2, 0], 0.0)

        self.assertAlmostEqual(hessian[0, 1], 0.0)
        self.assertAlmostEqual(hessian[1, 1], 0.0)
        self.assertAlmostEqual(hessian[2, 1], 0.0)

        self.assertAlmostEqual(hessian[0, 2], 0.0)
        self.assertAlmostEqual(hessian[1, 2], 0.0)
        self.assertAlmostEqual(hessian[2, 2], 0.0)


if __name__ == "__main__":
    unittest.main()
