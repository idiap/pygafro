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

from pygafro import UR5
from pygafro import Point


class TestUR5(unittest.TestCase):

    def testRandomConfiguration(self):
        robot = UR5()

        config = robot.getRandomConfiguration()

        self.assertTrue(isinstance(config, np.ndarray))
        self.assertAlmostEqual(config.shape, (6,))

    def test_setJointLimits_getMin(self):
        robot = UR5()

        limitsMin = robot.getSystem().getJointLimitsMin()

        self.assertTrue(isinstance(limitsMin, np.ndarray))
        self.assertAlmostEqual(limitsMin.shape, (6,))
        self.assertAlmostEqual(limitsMin[0], -6.28319, places=5)
        self.assertAlmostEqual(limitsMin[1], -6.28319, places=5)
        self.assertAlmostEqual(limitsMin[2], -6.28319, places=5)
        self.assertAlmostEqual(limitsMin[3], -6.28319, places=5)
        self.assertAlmostEqual(limitsMin[4], -6.28319, places=5)
        self.assertAlmostEqual(limitsMin[5], -6.28319, places=5)

    def test_setJointLimits_getMax(self):
        robot = UR5()

        limitsMax = robot.getSystem().getJointLimitsMax()

        self.assertTrue(isinstance(limitsMax, np.ndarray))
        self.assertAlmostEqual(limitsMax.shape, (6,))
        self.assertAlmostEqual(limitsMax[0], 6.28319, places=5)
        self.assertAlmostEqual(limitsMax[1], 6.28319, places=5)
        self.assertAlmostEqual(limitsMax[2], 6.28319, places=5)
        self.assertAlmostEqual(limitsMax[3], 6.28319, places=5)
        self.assertAlmostEqual(limitsMax[4], 6.28319, places=5)
        self.assertAlmostEqual(limitsMax[5], 6.28319, places=5)

    def testConfiguration1(self):
        robot = UR5()

        configuration = [0.5, -0.3, 0.0, -1.8, 0.0, 1.5]

        ee_motor = robot.getEEMotor(configuration)

        ee_point = ee_motor.apply(Point(0.0, 0.0, 0.0))

        self.assertAlmostEqual(ee_point["e0"], 1.0)
        self.assertAlmostEqual(ee_point["e1"], 0.1918632812)
        self.assertAlmostEqual(ee_point["e2"], 0.3229715006)
        self.assertAlmostEqual(ee_point["e3"], 0.8221240619)
        self.assertAlmostEqual(ee_point["ei"], 0.408505041)

    def testConfiguration2(self):
        robot = UR5()

        configuration = [-0.5, -0.3, 0.0, -1.8, 0.0, 1.5]

        ee_motor = robot.getEEMotor(configuration)

        ee_point = ee_motor.apply(Point(0.0, 0.0, 0.0))

        self.assertAlmostEqual(ee_point["e0"], 1.0)
        self.assertAlmostEqual(ee_point["e1"], 0.3754353199)
        self.assertAlmostEqual(ee_point["e2"], 0.0130548624)
        self.assertAlmostEqual(ee_point["e3"], 0.8221240619)
        self.assertAlmostEqual(ee_point["ei"], 0.408505041)

    def testInverseDynamics1(self):
        robot = UR5()

        position = [0.680375, -0.211234, 0.566198, 0.59688, 0.823295, -0.604897]
        velocity = [0.536459, -0.444451, 0.10794, -0.0452059, 0.257742, -0.270431]
        acceleration = [0.904459, 0.83239, 0.271423, 0.434594, -0.716795, 0.213938]

        torque = robot.getJointTorques(position, velocity, acceleration)

        self.assertTrue(isinstance(torque, np.ndarray))
        self.assertEqual(torque.shape, (6,))

        self.assertAlmostEqual(torque[0], 0.932673, places=6)
        self.assertAlmostEqual(torque[1], 7.69722, places=5)
        self.assertAlmostEqual(torque[2], -3.88589, places=5)
        self.assertAlmostEqual(torque[3], 0.303155, places=6)
        self.assertAlmostEqual(torque[4], -0.0102582, places=6)
        self.assertAlmostEqual(torque[5], 0.0339077, places=6)

    def testInverseDynamics2(self):
        robot = UR5()

        position = [0.997849, -0.563486, 0.0258648, 0.678224, 0.22528, -0.407937]
        velocity = [0.0485744, -0.012834, 0.94555, -0.414966, 0.542715, 0.05349]
        acceleration = [-0.199543, 0.783059, -0.433371, -0.295083, 0.615449, 0.838053]

        torque = robot.getJointTorques(position, velocity, acceleration)

        self.assertTrue(isinstance(torque, np.ndarray))
        self.assertEqual(torque.shape, (6,))

        self.assertAlmostEqual(torque[0], 0.0825726, places=7)
        self.assertAlmostEqual(torque[1], 33.5392, places=4)
        self.assertAlmostEqual(torque[2], 8.77025, places=5)
        self.assertAlmostEqual(torque[3], 0.0112162, places=7)
        self.assertAlmostEqual(torque[4], 0.104304, places=6)
        self.assertAlmostEqual(torque[5], 0.0114626, places=7)

    def testInverseDynamics3(self):
        robot = UR5()

        position = [0.17728, 0.314608, 0.717353, -0.12088, 0.84794, -0.203127]
        velocity = [0.368437, 0.821944, -0.0350187, -0.56835, 0.900505, 0.840257]
        acceleration = [0.762124, 0.282161, -0.136093, 0.239193, -0.437881, 0.572004]

        torque = robot.getJointTorques(position, velocity, acceleration)

        self.assertTrue(isinstance(torque, np.ndarray))
        self.assertEqual(torque.shape, (6,))

        self.assertAlmostEqual(torque[0], 1.88672, places=5)
        self.assertAlmostEqual(torque[1], -25.9083, places=4)
        self.assertAlmostEqual(torque[2], -12.9013, places=4)
        self.assertAlmostEqual(torque[3], 0.0445212, places=7)
        self.assertAlmostEqual(torque[4], -0.00248806, places=8)
        self.assertAlmostEqual(torque[5], 0.0193007, places=7)

    def testInverseDynamics4(self):
        robot = UR5()

        position = [-0.639255, -0.673737, -0.21662, 0.826053, 0.63939, -0.281809]
        velocity = [0.15886, -0.0948483, 0.374775, -0.80072, 0.061616, 0.514588]
        acceleration = [0.984457, 0.153942, 0.755228, 0.495619, 0.25782, -0.929158]

        torque = robot.getJointTorques(position, velocity, acceleration)

        self.assertTrue(isinstance(torque, np.ndarray))
        self.assertEqual(torque.shape, (6,))

        self.assertAlmostEqual(torque[0], 2.4801, places=4)
        self.assertAlmostEqual(torque[1], 41.6159, places=4)
        self.assertAlmostEqual(torque[2], 13.2428, places=4)
        self.assertAlmostEqual(torque[3], 0.342344, places=6)
        self.assertAlmostEqual(torque[4], 0.302564, places=6)
        self.assertAlmostEqual(torque[5], 0.00335514, places=8)

    def testInverseForwardDynamics(self):
        robot = UR5()

        for i in range(10):
            position = np.random.rand(6)
            velocity = np.random.rand(6)
            acceleration = np.random.rand(6)

            torque = robot.getJointTorques(position, velocity, acceleration)

            acceleration_computed = robot.getJointAccelerations(
                position, velocity, torque
            )

            self.assertTrue(isinstance(acceleration_computed, np.ndarray))
            self.assertEqual(acceleration_computed.shape, (6,))

            self.assertAlmostEqual(acceleration[0], acceleration_computed[0])
            self.assertAlmostEqual(acceleration[1], acceleration_computed[1])
            self.assertAlmostEqual(acceleration[2], acceleration_computed[2])
            self.assertAlmostEqual(acceleration[3], acceleration_computed[3])
            self.assertAlmostEqual(acceleration[4], acceleration_computed[4])
            self.assertAlmostEqual(acceleration[5], acceleration_computed[5])


if __name__ == "__main__":
    unittest.main()
