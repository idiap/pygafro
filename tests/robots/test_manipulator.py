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
import numpy as np

from pygafro import Inertia
from pygafro import Joint
from pygafro import Line
from pygafro import Motor
from pygafro import MotorGenerator
from pygafro import Point
from pygafro import RotorGenerator
from pygafro import System
from pygafro import Translator
from pygafro import TranslatorGenerator
from pygafro import createManipulator


class TestManipulatorConfiguration1With3Joints(unittest.TestCase):

    def setUp(self):
        self.manipulator = helpers.createManipulatorWith3Joints()

    def tearDown(self):
        self.manipulator = None

    def testRandomConfiguration(self):
        config = self.manipulator.getRandomConfiguration()

        self.assertTrue(isinstance(config, np.ndarray))
        self.assertAlmostEqual(config.shape, (3,))

    def test_getEndEffectorKinematicChain(self):
        chain = self.manipulator.getEEKinematicChain()

        self.assertTrue(chain is not None)
        self.assertEqual(chain.getDoF(), 3)

    def test_computeEndEffectorMotor(self):
        position = [0.0, math.pi / 2.0, 0.0]
        motor = self.manipulator.getEEMotor(position)

        self.assertAlmostEqual(motor["scalar"], 0.7071067812)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.7071067812)
        self.assertAlmostEqual(motor["e1i"], -0.3535533906)
        self.assertAlmostEqual(motor["e2i"], -1.0606601718)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

    def test_computeEndEffectorAnalyticJacobian(self):
        position = [0.0, math.pi / 2.0, 0.0]

        jacobian = self.manipulator.getEEAnalyticJacobian(position)

        self.assertTrue(isinstance(jacobian, list))
        self.assertEqual(len(jacobian), 3)

        self.assertAlmostEqual(jacobian[0]["scalar"], -0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], -0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e1i"], 0.1767766953)
        self.assertAlmostEqual(jacobian[0]["e2i"], 0.1767766953)
        self.assertAlmostEqual(jacobian[0]["e3i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e123i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["scalar"], -0.3535533906)
        self.assertAlmostEqual(jacobian[1]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e12"], -0.3535533906)
        self.assertAlmostEqual(jacobian[1]["e1i"], -0.1767766953)
        self.assertAlmostEqual(jacobian[1]["e2i"], 0.5303300859)
        self.assertAlmostEqual(jacobian[1]["e3i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e123i"], 0.0)

        self.assertAlmostEqual(jacobian[2]["scalar"], -0.3535533906)
        self.assertAlmostEqual(jacobian[2]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e12"], -0.3535533906)
        self.assertAlmostEqual(jacobian[2]["e1i"], -0.5303300859)
        self.assertAlmostEqual(jacobian[2]["e2i"], 0.1767766953)
        self.assertAlmostEqual(jacobian[2]["e3i"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e123i"], 0.0)

    def test_computeEndEffectorGeometricJacobian(self):
        position = [0.0, math.pi / 2.0, 0.0]

        jacobian = self.manipulator.getEEGeometricJacobian(position)

        self.assertTrue(isinstance(jacobian, list))
        self.assertEqual(len(jacobian), 3)

        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e1i"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e3i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[1]["e1i"], 2.0)
        self.assertAlmostEqual(jacobian[1]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e3i"], 0.0)

        self.assertAlmostEqual(jacobian[2]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[2]["e1i"], 2.0)
        self.assertAlmostEqual(jacobian[2]["e2i"], 1.0)
        self.assertAlmostEqual(jacobian[2]["e3i"], 0.0)

    def test_computeEndEffectorFrameJacobian(self):
        position = [0.0, math.pi / 2.0, 0.0]

        jacobian = self.manipulator.getEEFrameJacobian(position)

        self.assertTrue(isinstance(jacobian, list))
        self.assertEqual(len(jacobian), 3)

        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e1i"], -1.0)
        self.assertAlmostEqual(jacobian[0]["e2i"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e3i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[1]["e1i"], -1.0)
        self.assertAlmostEqual(jacobian[1]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e3i"], 0.0)

        self.assertAlmostEqual(jacobian[2]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[2]["e1i"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e3i"], 0.0)

    def test_computeEndEffectorPrimitiveJacobian_Point(self):
        position = [0.0, math.pi / 2.0, 0.0]

        primitive = Point(1.0, 0.0, 0.0)

        jacobian = self.manipulator.getEEPrimitiveJacobian(position, primitive)

        self.assertTrue(isinstance(jacobian, list))
        self.assertEqual(len(jacobian), 3)

        self.assertAlmostEqual(jacobian[0]["e1"], -2.0)
        self.assertAlmostEqual(jacobian[0]["e2"], -1.0)
        self.assertAlmostEqual(jacobian[0]["e3"], 0.0)
        self.assertAlmostEqual(jacobian[0]["ei"], -1.0)
        self.assertAlmostEqual(jacobian[0]["e0"], 0.0)

        self.assertAlmostEqual(jacobian[1]["e1"], -1.0)
        self.assertAlmostEqual(jacobian[1]["e2"], -1.0)
        self.assertAlmostEqual(jacobian[1]["e3"], 0.0)
        self.assertAlmostEqual(jacobian[1]["ei"], -2.0)
        self.assertAlmostEqual(jacobian[1]["e0"], 0.0)

        self.assertAlmostEqual(jacobian[2]["e1"], -1.0)
        self.assertAlmostEqual(jacobian[2]["e2"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e3"], 0.0)
        self.assertAlmostEqual(jacobian[2]["ei"], 1.0)
        self.assertAlmostEqual(jacobian[2]["e0"], 0.0)

    def test_computeEndEffectorPrimitiveJacobian_Line(self):
        position = [0.0, math.pi / 2.0, 0.0]

        primitive = Line(Point(0.0, 0.0, 0.0), Point(1.0, 0.0, 0.0))

        jacobian = self.manipulator.getEEPrimitiveJacobian(position, primitive)

        self.assertTrue(isinstance(jacobian, list))
        self.assertEqual(len(jacobian), 3)

        self.assertAlmostEqual(jacobian[0]["e12i"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e13i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e23i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e01i"], -1.0)
        self.assertAlmostEqual(jacobian[0]["e02i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e03i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["e12i"], 2.0)
        self.assertAlmostEqual(jacobian[1]["e13i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e23i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e01i"], -1.0)
        self.assertAlmostEqual(jacobian[1]["e02i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e03i"], 0.0)

        self.assertAlmostEqual(jacobian[2]["e12i"], 2.0)
        self.assertAlmostEqual(jacobian[2]["e13i"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e23i"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e01i"], -1.0)
        self.assertAlmostEqual(jacobian[2]["e02i"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e03i"], 0.0)

    def test_getJointTorques(self):
        position = [0.0, 0.1, 0.0]
        velocity = [0.1, 0.4, 0.0]
        acceleration = [-0.2, 0.8, 0.0]

        torques = self.manipulator.getJointTorques(position, velocity, acceleration)

        self.assertTrue(isinstance(torques, np.ndarray))
        self.assertEqual(len(torques), 3)

        self.assertAlmostEqual(torques[0], 1.0574, places=4)
        self.assertAlmostEqual(torques[1], 1.2402, places=4)
        self.assertAlmostEqual(torques[2], 0.6, places=4)

    def test_getJointAccelerations(self):
        position = [0.0, 0.1, 0.0]
        velocity = [0.1, 0.4, 0.0]
        torques = [1.0574, 1.2402, 0.6]

        acceleration = self.manipulator.getJointAccelerations(
            position, velocity, torques
        )

        self.assertTrue(isinstance(acceleration, np.ndarray))
        self.assertEqual(acceleration.shape, (3,))

        self.assertAlmostEqual(acceleration[0], -0.2, places=4)
        self.assertAlmostEqual(acceleration[1], 0.8, places=4)
        self.assertAlmostEqual(acceleration[2], 0.0, places=4)


class TestManipulatorConfiguration1With2Joints(unittest.TestCase):

    def setUp(self):
        self.manipulator = createManipulator(
            helpers.createSystemWith3Joints(), 2, "joint2"
        )

    def tearDown(self):
        self.manipulator = None

    def testRandomConfiguration(self):
        config = self.manipulator.getRandomConfiguration()

        self.assertTrue(isinstance(config, np.ndarray))
        self.assertAlmostEqual(config.shape, (2,))

    def test_getEndEffectorKinematicChain(self):
        chain = self.manipulator.getEEKinematicChain()

        self.assertTrue(chain is not None)
        self.assertEqual(chain.getDoF(), 2)

    def test_computeEndEffectorMotor(self):
        position = [0.0, math.pi / 2.0]
        motor = self.manipulator.getEEMotor(position)

        self.assertAlmostEqual(motor["scalar"], 0.7071067812)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.7071067812)
        self.assertAlmostEqual(motor["e1i"], -0.7071067812)
        self.assertAlmostEqual(motor["e2i"], -0.7071067812)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

    def test_computeEndEffectorAnalyticJacobian(self):
        position = [0.0, math.pi / 2.0]

        jacobian = self.manipulator.getEEAnalyticJacobian(position)

        self.assertTrue(isinstance(jacobian, list))
        self.assertEqual(len(jacobian), 2)

        self.assertAlmostEqual(jacobian[0]["scalar"], -0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], -0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e1i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e3i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e123i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["scalar"], -0.3535533906)
        self.assertAlmostEqual(jacobian[1]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e12"], -0.3535533906)
        self.assertAlmostEqual(jacobian[1]["e1i"], -0.3535533906)
        self.assertAlmostEqual(jacobian[1]["e2i"], 0.3535533906)
        self.assertAlmostEqual(jacobian[1]["e3i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e123i"], 0.0)

    def test_computeEndEffectorGeometricJacobian(self):
        position = [0.0, math.pi / 2.0]

        jacobian = self.manipulator.getEEGeometricJacobian(position)

        self.assertTrue(isinstance(jacobian, list))
        self.assertEqual(len(jacobian), 2)

        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e1i"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e3i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[1]["e1i"], 2.0)
        self.assertAlmostEqual(jacobian[1]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e3i"], 0.0)

    def test_computeEndEffectorFrameJacobian(self):
        position = [0.0, math.pi / 2.0]

        jacobian = self.manipulator.getEEFrameJacobian(position)

        self.assertTrue(isinstance(jacobian, list))
        self.assertEqual(len(jacobian), 2)

        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e1i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e2i"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e3i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[1]["e1i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e3i"], 0.0)

    def test_getJointTorques(self):
        position = [0.0, 0.1]
        velocity = [0.1, 0.4]
        acceleration = [-0.2, 0.8]

        torques = self.manipulator.getJointTorques(position, velocity, acceleration)

        self.assertTrue(isinstance(torques, np.ndarray))
        self.assertEqual(len(torques), 2)

        self.assertAlmostEqual(torques[0], 1.0574, places=4)
        self.assertAlmostEqual(torques[1], 1.2402, places=4)

    def test_getJointAccelerations(self):
        position = [0.0, 0.1]
        velocity = [0.1, 0.4]
        torques = [1.0574, 1.2402]

        acceleration = self.manipulator.getJointAccelerations(
            position, velocity, torques
        )

        self.assertTrue(isinstance(acceleration, np.ndarray))
        self.assertEqual(acceleration.shape, (2,))

        self.assertAlmostEqual(acceleration[0], -0.2, places=4)
        self.assertAlmostEqual(acceleration[1], 0.8, places=4)


class TestManipulatorConfiguration2(unittest.TestCase):

    def setUp(self):
        # Create the system
        system = System()

        # Create some links
        com = Translator(TranslatorGenerator([0.0, 0.0, 0.0]))

        link1 = system.createLink("link1")
        link1.setMass(0.1)
        link1.setCenterOfMass(com)
        link1.setInertia(Inertia(0.1, np.eye(3)))
        link1.setAxis(MotorGenerator([0.0, 0.0, 1.0, 0.0, 0.0, 0.0]))

        link2 = system.createLink("link2")
        link2.setMass(0.1)
        link2.setCenterOfMass(com)
        link2.setInertia(Inertia(0.1, np.eye(3)))
        link2.setAxis(MotorGenerator([0.0, 0.0, 1.0, 0.0, 0.0, 0.0]))

        link3 = system.createLink("link3")
        link3.setMass(0.1)
        link3.setCenterOfMass(com)
        link3.setInertia(Inertia(0.1, np.eye(3)))
        link3.setAxis(MotorGenerator([0.0, 0.0, 1.0, 0.0, 0.0, 0.0]))

        link4 = system.createLink("link4")
        link4.setMass(0.1)
        link4.setCenterOfMass(com)
        link4.setInertia(Inertia(0.1, np.eye(3)))
        link4.setAxis(MotorGenerator([0.0, 0.0, 1.0, 0.0, 0.0, 0.0]))

        # Create some joints
        t = Translator(TranslatorGenerator([0.0, 1.0, 0.0]))

        joint1 = system.createRevoluteJoint("joint1")
        joint1.setAxis(RotorGenerator([0.0, 0.0, 1.0]))
        joint1.setFrame(Motor(t))

        limits = Joint.Limits()
        limits.positionLower = -0.5
        limits.positionUpper = 0.5
        limits.velocity = 1.0
        limits.torque = 1.0

        joint1.setLimits(limits)

        joint2 = system.createRevoluteJoint("joint2")
        joint2.setAxis(RotorGenerator([0.0, 0.0, 1.0]))
        joint2.setFrame(Motor(t))

        limits = Joint.Limits()
        limits.positionLower = -0.8
        limits.positionUpper = 0.8
        limits.velocity = 1.0
        limits.torque = 1.0

        joint2.setLimits(limits)

        joint3 = system.createFixedJoint("joint3")
        joint3.setFrame(Motor(t))

        joint1.setParentLink(link1)
        link1.addChildJoint(joint1)

        joint1.setChildLink(link2)
        link2.setParentJoint(joint1)

        joint2.setParentLink(link2)
        link2.addChildJoint(joint2)

        joint2.setChildLink(link3)
        link3.setParentJoint(joint2)

        joint3.setParentLink(link3)
        link3.addChildJoint(joint3)

        joint3.setChildLink(link4)
        link4.setParentJoint(joint3)

        # Create the manipulator
        self.manipulator = createManipulator(system, 2, "joint3")

    def tearDown(self):
        self.manipulator = None

    def testRandomConfiguration(self):
        config = self.manipulator.getRandomConfiguration()

        self.assertTrue(isinstance(config, np.ndarray))
        self.assertAlmostEqual(config.shape, (2,))

    def test_getEndEffectorKinematicChain(self):
        chain = self.manipulator.getEEKinematicChain()

        self.assertTrue(chain is not None)
        self.assertEqual(chain.getDoF(), 2)

    def test_computeEndEffectorMotor(self):
        position = [0.0, math.pi / 2.0]
        motor = self.manipulator.getEEMotor(position)

        self.assertAlmostEqual(motor["scalar"], 0.7071067812)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.7071067812)
        self.assertAlmostEqual(motor["e1i"], -0.3535533906)
        self.assertAlmostEqual(motor["e2i"], -1.0606601718)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

    def test_computeEndEffectorAnalyticJacobian(self):
        position = [0.0, math.pi / 2.0]

        jacobian = self.manipulator.getEEAnalyticJacobian(position)

        self.assertTrue(isinstance(jacobian, list))
        self.assertEqual(len(jacobian), 2)

        self.assertAlmostEqual(jacobian[0]["scalar"], -0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], -0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e1i"], 0.1767766953)
        self.assertAlmostEqual(jacobian[0]["e2i"], 0.1767766953)
        self.assertAlmostEqual(jacobian[0]["e3i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e123i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["scalar"], -0.3535533906)
        self.assertAlmostEqual(jacobian[1]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e12"], -0.3535533906)
        self.assertAlmostEqual(jacobian[1]["e1i"], -0.1767766953)
        self.assertAlmostEqual(jacobian[1]["e2i"], 0.5303300859)
        self.assertAlmostEqual(jacobian[1]["e3i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e123i"], 0.0)

    def test_computeEndEffectorGeometricJacobian(self):
        position = [0.0, math.pi / 2.0]

        jacobian = self.manipulator.getEEGeometricJacobian(position)

        self.assertTrue(isinstance(jacobian, list))
        self.assertEqual(len(jacobian), 2)

        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e1i"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e3i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[1]["e1i"], 2.0)
        self.assertAlmostEqual(jacobian[1]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e3i"], 0.0)

    def test_computeEndEffectorFrameJacobian(self):
        position = [0.0, math.pi / 2.0]

        jacobian = self.manipulator.getEEFrameJacobian(position)

        self.assertTrue(isinstance(jacobian, list))
        self.assertEqual(len(jacobian), 2)

        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e1i"], -1.0)
        self.assertAlmostEqual(jacobian[0]["e2i"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e3i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[1]["e1i"], -1.0)
        self.assertAlmostEqual(jacobian[1]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e3i"], 0.0)

    def test_computeEndEffectorPrimitiveJacobian_Point(self):
        position = [0.0, math.pi / 2.0, 0.0]

        primitive = Point(1.0, 0.0, 0.0)

        jacobian = self.manipulator.getEEPrimitiveJacobian(position, primitive)

        self.assertTrue(isinstance(jacobian, list))
        self.assertEqual(len(jacobian), 2)

        self.assertAlmostEqual(jacobian[0]["e1"], -2.0)
        self.assertAlmostEqual(jacobian[0]["e2"], -1.0)
        self.assertAlmostEqual(jacobian[0]["e3"], 0.0)
        self.assertAlmostEqual(jacobian[0]["ei"], -1.0)
        self.assertAlmostEqual(jacobian[0]["e0"], 0.0)

        self.assertAlmostEqual(jacobian[1]["e1"], -1.0)
        self.assertAlmostEqual(jacobian[1]["e2"], -1.0)
        self.assertAlmostEqual(jacobian[1]["e3"], 0.0)
        self.assertAlmostEqual(jacobian[1]["ei"], -2.0)
        self.assertAlmostEqual(jacobian[1]["e0"], 0.0)

    def test_computeEndEffectorPrimitiveJacobian_Line(self):
        position = [0.0, math.pi / 2.0, 0.0]

        primitive = Line(Point(0.0, 0.0, 0.0), Point(1.0, 0.0, 0.0))

        jacobian = self.manipulator.getEEPrimitiveJacobian(position, primitive)

        self.assertTrue(isinstance(jacobian, list))
        self.assertEqual(len(jacobian), 2)

        self.assertAlmostEqual(jacobian[0]["e12i"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e13i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e23i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e01i"], -1.0)
        self.assertAlmostEqual(jacobian[0]["e02i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e03i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["e12i"], 2.0)
        self.assertAlmostEqual(jacobian[1]["e13i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e23i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e01i"], -1.0)
        self.assertAlmostEqual(jacobian[1]["e02i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e03i"], 0.0)

    def test_getJointTorques(self):
        position = [0.0, 0.1]
        velocity = [0.1, 0.4]
        acceleration = [-0.2, 0.8]

        torques = self.manipulator.getJointTorques(position, velocity, acceleration)

        self.assertTrue(isinstance(torques, np.ndarray))
        self.assertEqual(len(torques), 2)

        self.assertAlmostEqual(torques[0], 1.0574, places=4)
        self.assertAlmostEqual(torques[1], 1.2402, places=4)

    def test_getJointAccelerations(self):
        position = [0.0, 0.1]
        velocity = [0.1, 0.4]
        torques = [1.0574, 1.2402]

        acceleration = self.manipulator.getJointAccelerations(
            position, velocity, torques
        )

        self.assertTrue(isinstance(acceleration, np.ndarray))
        self.assertEqual(acceleration.shape, (2,))

        self.assertAlmostEqual(acceleration[0], -0.2, places=4)
        self.assertAlmostEqual(acceleration[1], 0.8, places=4)


if __name__ == "__main__":
    unittest.main()
