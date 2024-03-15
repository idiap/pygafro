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

from pygafro import FrankaEmikaRobot
from pygafro import Point


class TestFrankaEmikaRobot(unittest.TestCase):

    def testRandomConfiguration(self):
        robot = FrankaEmikaRobot()

        config = robot.getRandomConfiguration()

        self.assertTrue(isinstance(config, np.ndarray))
        self.assertAlmostEqual(config.shape, (7,))

    def test_setJointLimits_getMin(self):
        robot = FrankaEmikaRobot()

        limitsMin = robot.getSystem().getJointLimitsMin()

        self.assertTrue(isinstance(limitsMin, np.ndarray))
        self.assertAlmostEqual(limitsMin.shape, (9,))
        self.assertAlmostEqual(limitsMin[0], -2.8973)
        self.assertAlmostEqual(limitsMin[1], -1.7628)
        self.assertAlmostEqual(limitsMin[2], -2.8973)
        self.assertAlmostEqual(limitsMin[3], -3.0718)
        self.assertAlmostEqual(limitsMin[4], -2.8973)
        self.assertAlmostEqual(limitsMin[5], -0.0175)
        self.assertAlmostEqual(limitsMin[6], -2.8973)
        self.assertAlmostEqual(limitsMin[7], 0.0)
        self.assertAlmostEqual(limitsMin[8], 0.0)

    def test_setJointLimits_getMax(self):
        robot = FrankaEmikaRobot()

        limitsMax = robot.getSystem().getJointLimitsMax()

        self.assertTrue(isinstance(limitsMax, np.ndarray))
        self.assertAlmostEqual(limitsMax.shape, (9,))
        self.assertAlmostEqual(limitsMax[0], 2.8973)
        self.assertAlmostEqual(limitsMax[1], 1.7628)
        self.assertAlmostEqual(limitsMax[2], 2.8973)
        self.assertAlmostEqual(limitsMax[3], -0.0698)
        self.assertAlmostEqual(limitsMax[4], 2.8973)
        self.assertAlmostEqual(limitsMax[5], 3.7525)
        self.assertAlmostEqual(limitsMax[6], 2.8973)
        self.assertAlmostEqual(limitsMax[7], 0.04)
        self.assertAlmostEqual(limitsMax[8], 0.04)

    def testConfiguration1(self):
        robot = FrankaEmikaRobot()

        configuration = [0.5, -0.3, 0.0, -1.8, 0.0, 1.5, 1.0]

        ee_motor = robot.getEEMotor(configuration)

        ee_point = ee_motor.apply(Point(0.0, 0.0, 0.0))

        self.assertAlmostEqual(ee_point["e0"], 1.0)
        self.assertAlmostEqual(ee_point["e1"], 0.3954677774)
        self.assertAlmostEqual(ee_point["e2"], 0.2160450314)
        self.assertAlmostEqual(ee_point["e3"], 0.5583231694)
        self.assertAlmostEqual(ee_point["ei"], 0.25739749)

    def testConfiguration2(self):
        robot = FrankaEmikaRobot()

        configuration = [-0.5, -0.3, 0.0, -1.8, 0.0, 1.5, 1.0]

        ee_motor = robot.getEEMotor(configuration)

        ee_point = ee_motor.apply(Point(0.0, 0.0, 0.0))

        self.assertAlmostEqual(ee_point["e0"], 1.0)
        self.assertAlmostEqual(ee_point["e1"], 0.3954677774)
        self.assertAlmostEqual(ee_point["e2"], -0.2160450314)
        self.assertAlmostEqual(ee_point["e3"], 0.5583231694)
        self.assertAlmostEqual(ee_point["ei"], 0.25739749)

    def testInverseDynamics1(self):
        robot = FrankaEmikaRobot()

        position = [
            0.680375,
            -0.211234,
            0.566198,
            0.59688,
            0.823295,
            -0.604897,
            -0.329554,
        ]
        velocity = [
            0.536459,
            -0.444451,
            0.10794,
            -0.0452059,
            0.257742,
            -0.270431,
            0.0268018,
        ]
        acceleration = [
            0.904459,
            0.83239,
            0.271423,
            0.434594,
            -0.716795,
            0.213938,
            -0.967399,
        ]

        torque = robot.getJointTorques(position, velocity, acceleration)

        self.assertTrue(isinstance(torque, np.ndarray))
        self.assertEqual(torque.shape, (7,))

        self.assertAlmostEqual(torque[0], 0.982722, places=4)
        self.assertAlmostEqual(torque[1], 17.4042, places=4)
        self.assertAlmostEqual(torque[2], 1.11406, places=4)
        self.assertAlmostEqual(torque[3], -15.77, places=4)
        self.assertAlmostEqual(torque[4], -0.736949, places=4)
        self.assertAlmostEqual(torque[5], 1.60781, places=4)
        self.assertAlmostEqual(torque[6], 0.0118833, places=4)

    def testInverseDynamics2(self):
        robot = FrankaEmikaRobot()

        position = [
            0.997849,
            -0.563486,
            0.0258648,
            0.678224,
            0.22528,
            -0.407937,
            0.275105,
        ]
        velocity = [
            0.0485744,
            -0.012834,
            0.94555,
            -0.414966,
            0.542715,
            0.05349,
            0.539828,
        ]
        acceleration = [
            -0.199543,
            0.783059,
            -0.433371,
            -0.295083,
            0.615449,
            0.838053,
            -0.860489,
        ]

        torque = robot.getJointTorques(position, velocity, acceleration)

        self.assertTrue(isinstance(torque, np.ndarray))
        self.assertEqual(torque.shape, (7,))

        self.assertAlmostEqual(torque[0], -0.75037, places=4)
        self.assertAlmostEqual(torque[1], 31.4451, places=4)
        self.assertAlmostEqual(torque[2], -0.868337, places=4)
        self.assertAlmostEqual(torque[3], -18.6992, places=4)
        self.assertAlmostEqual(torque[4], -0.884175, places=4)
        self.assertAlmostEqual(torque[5], 2.8628, places=4)
        self.assertAlmostEqual(torque[6], -0.0235222, places=4)

    def testInverseDynamics3(self):
        robot = FrankaEmikaRobot()

        position = [0.17728, 0.314608, 0.717353, -0.12088, 0.84794, -0.203127, 0.629534]
        velocity = [
            0.368437,
            0.821944,
            -0.0350187,
            -0.56835,
            0.900505,
            0.840257,
            -0.70468,
        ]
        acceleration = [
            0.762124,
            0.282161,
            -0.136093,
            0.239193,
            -0.437881,
            0.572004,
            -0.385084,
        ]

        torque = robot.getJointTorques(position, velocity, acceleration)

        self.assertTrue(isinstance(torque, np.ndarray))
        self.assertEqual(torque.shape, (7,))

        self.assertAlmostEqual(torque[0], 0.914278, places=4)
        self.assertAlmostEqual(torque[1], -17.4753, places=4)
        self.assertAlmostEqual(torque[2], 1.51745, places=4)
        self.assertAlmostEqual(torque[3], 1.16747, places=4)
        self.assertAlmostEqual(torque[4], 0.675721, places=4)
        self.assertAlmostEqual(torque[5], 1.59136, places=4)
        self.assertAlmostEqual(torque[6], 0.00452535, places=4)

    def testInverseDynamics4(self):
        robot = FrankaEmikaRobot()

        position = [
            -0.639255,
            -0.673737,
            -0.21662,
            0.826053,
            0.63939,
            -0.281809,
            0.10497,
        ]
        velocity = [
            0.15886,
            -0.0948483,
            0.374775,
            -0.80072,
            0.061616,
            0.514588,
            -0.39141,
        ]
        acceleration = [
            0.984457,
            0.153942,
            0.755228,
            0.495619,
            0.25782,
            -0.929158,
            0.495606,
        ]

        torque = robot.getJointTorques(position, velocity, acceleration)

        self.assertTrue(isinstance(torque, np.ndarray))
        self.assertEqual(torque.shape, (7,))

        self.assertAlmostEqual(torque[0], 1.4954, places=4)
        self.assertAlmostEqual(torque[1], 32.1859, places=4)
        self.assertAlmostEqual(torque[2], -1.63865, places=4)
        self.assertAlmostEqual(torque[3], -17.4762, places=4)
        self.assertAlmostEqual(torque[4], -1.35407, places=4)
        self.assertAlmostEqual(torque[5], 1.99246, places=4)
        self.assertAlmostEqual(torque[6], -0.0101391, places=4)

    def testInverseForwardDynamics(self):
        robot = FrankaEmikaRobot()

        for i in range(10):
            position = np.random.rand(7)
            velocity = np.random.rand(7)
            acceleration = np.random.rand(7)

            torque = robot.getJointTorques(position, velocity, acceleration)

            acceleration_computed = robot.getJointAccelerations(
                position, velocity, torque
            )

            self.assertTrue(isinstance(acceleration_computed, np.ndarray))
            self.assertEqual(acceleration_computed.shape, (7,))

            self.assertAlmostEqual(acceleration[0], acceleration_computed[0])
            self.assertAlmostEqual(acceleration[1], acceleration_computed[1])
            self.assertAlmostEqual(acceleration[2], acceleration_computed[2])
            self.assertAlmostEqual(acceleration[3], acceleration_computed[3])
            self.assertAlmostEqual(acceleration[4], acceleration_computed[4])
            self.assertAlmostEqual(acceleration[5], acceleration_computed[5])
            self.assertAlmostEqual(acceleration[6], acceleration_computed[6])


if __name__ == "__main__":
    unittest.main()
