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

from pygafro import SingleManipulatorMotorCost


class TestSingleManipulatorMotorCost(unittest.TestCase):

    def setUp(self):
        self.manipulator = helpers.createManipulatorWith3Joints()

        target_position = [0.0, math.pi / 2.0, 0.0]
        ee_target_motor = self.manipulator.getEEMotor(target_position)

        self.cost_function = SingleManipulatorMotorCost(
            self.manipulator, ee_target_motor
        )

    def tearDown(self):
        self.cost_function = None
        self.manipulator = None

    def testGetError(self):
        error = self.cost_function.getError([0.0, 0.0, 0.0])

        self.assertEqual(error.shape, (6,))

        self.assertAlmostEqual(error[0], 0.0)
        self.assertAlmostEqual(error[1], 0.0)
        self.assertAlmostEqual(error[2], -1.5708, places=4)
        self.assertAlmostEqual(error[3], 1.0)
        self.assertAlmostEqual(error[4], -1.0)
        self.assertAlmostEqual(error[5], 0.0)

    def testGetGradientAndHessian(self):
        gradient, hessian = self.cost_function.getGradientAndHessian([0.0, 0.0, 0.0])

        self.assertEqual(gradient.shape, (3,))
        self.assertEqual(hessian.shape, (3, 3))

        self.assertAlmostEqual(gradient[0], -3.5708, places=4)
        self.assertAlmostEqual(gradient[1], -2.5708, places=4)
        self.assertAlmostEqual(gradient[2], -1.5708, places=4)

        self.assertAlmostEqual(hessian[0, 0], 5.0)
        self.assertAlmostEqual(hessian[1, 0], 3.0)
        self.assertAlmostEqual(hessian[2, 0], 1.0)

        self.assertAlmostEqual(hessian[0, 1], 3.0)
        self.assertAlmostEqual(hessian[1, 1], 2.0)
        self.assertAlmostEqual(hessian[2, 1], 1.0)

        self.assertAlmostEqual(hessian[0, 2], 1.0)
        self.assertAlmostEqual(hessian[1, 2], 1.0)
        self.assertAlmostEqual(hessian[2, 2], 1.0)


if __name__ == "__main__":
    unittest.main()
