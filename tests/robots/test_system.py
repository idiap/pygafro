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

from pygafro import Inertia
from pygafro import Joint
from pygafro import Motor
from pygafro import MotorGenerator
from pygafro import Point
from pygafro import RotorGenerator
from pygafro import System
from pygafro import Translator
from pygafro import TranslatorGenerator


class TestDefaultSystem(unittest.TestCase):

    def test_defaults(self):
        system = System()

        self.assertTrue(system.getBaseLink() is None)

        links = system.getLinks()
        self.assertEqual(len(links), 0)

        self.assertTrue(system.getLink("link1") is None)

        joints = system.getJoints()
        self.assertEqual(len(joints), 0)

        self.assertTrue(system.getJoint("joint1") is None)

        self.assertFalse(system.hasKinematicChain("joint1"))

        self.assertRaises(RuntimeError, system.getKinematicChain, "chain1")


class TestSystem(unittest.TestCase):

    def setUp(self):
        # Create the system
        self.system = System()

        # Create some links
        link1 = self.system.createLink("link1")
        link2 = self.system.createLink("link2")
        link3 = self.system.createLink("link3")

        # Create some joints
        joint1 = self.system.createRevoluteJoint("joint1")
        joint1.setAxis(RotorGenerator([0.0, 0.0, 1.0]))
        joint1.setFrame(Motor(Translator(TranslatorGenerator([0.0, 1.0, 0.0]))))

        limits = Joint.Limits()
        limits.positionLower = -0.5
        limits.positionUpper = 0.5
        limits.velocity = 1.0
        limits.torque = 1.0

        joint1.setLimits(limits)

        joint2 = self.system.createRevoluteJoint("joint2")
        joint2.setAxis(RotorGenerator([0.0, 0.0, 1.0]))
        joint2.setFrame(Motor(Translator(TranslatorGenerator([0.0, 1.0, 0.0]))))

        limits = Joint.Limits()
        limits.positionLower = -0.8
        limits.positionUpper = 0.8
        limits.velocity = 1.0
        limits.torque = 1.0

        joint2.setLimits(limits)

        joint1.setParentLink(link1)
        link1.addChildJoint(joint1)

        joint1.setChildLink(link2)
        link2.setParentJoint(joint1)

        joint2.setParentLink(link2)
        link2.addChildJoint(joint2)

        joint2.setChildLink(link3)
        link3.setParentJoint(joint2)

        self.system.finalize()

        self.assertTrue(self.system.hasKinematicChain("joint2"))
        self.assertFalse(self.system.hasKinematicChain("joint1"))

    def tearDown(self):
        self.system = None

    def createKinematicChain(self):
        self.chain = self.system.createKinematicChain("chain1")

        self.chain.addActuatedJoint(self.system.getJoint("joint1"))
        self.chain.addActuatedJoint(self.system.getJoint("joint2"))

        translator = Motor(Translator(TranslatorGenerator([0.0, 1.0, 0.0])))
        self.chain.addFixedMotor(translator)

        self.chain.finalize()

        self.assertTrue(self.system.hasKinematicChain("chain1"))

    def test_links(self):
        self.assertEqual(self.system.getBaseLink().getName(), "link1")

        links = self.system.getLinks()
        self.assertEqual(len(links), 3)
        self.assertEqual(links[0].getName(), "link1")
        self.assertEqual(links[1].getName(), "link2")
        self.assertEqual(links[2].getName(), "link3")

        self.assertTrue(self.system.getLink("link1") is not None)
        self.assertTrue(self.system.getLink("link2") is not None)
        self.assertTrue(self.system.getLink("link3") is not None)

    def test_joints(self):
        joints = self.system.getJoints()
        self.assertEqual(len(joints), 2)
        self.assertEqual(joints[0].getName(), "joint1")
        self.assertEqual(joints[1].getName(), "joint2")

        self.assertTrue(self.system.getJoint("joint1") is not None)
        self.assertTrue(self.system.getJoint("joint2") is not None)

    def testRandomConfiguration(self):
        config = self.system.getRandomConfiguration()

        self.assertTrue(isinstance(config, np.ndarray))
        self.assertAlmostEqual(config.shape, (2,))

    def test_setJointLimits_getMin(self):
        self.system.setJointLimits([-1.0, -2.0], [1.0, 2.0])

        limitsMin = self.system.getJointLimitsMin()

        self.assertTrue(isinstance(limitsMin, np.ndarray))
        self.assertAlmostEqual(limitsMin.shape, (2,))
        self.assertAlmostEqual(limitsMin[0], -1.0)
        self.assertAlmostEqual(limitsMin[1], -2.0)

    def test_setJointLimits_getMax(self):
        self.system.setJointLimits([-1.0, -2.0], [1.0, 2.0])

        limitsMax = self.system.getJointLimitsMax()

        self.assertTrue(isinstance(limitsMax, np.ndarray))
        self.assertAlmostEqual(limitsMax.shape, (2,))
        self.assertAlmostEqual(limitsMax[0], 1.0)
        self.assertAlmostEqual(limitsMax[1], 2.0)

    def test_setJointLimits_feasiblePosition(self):
        self.system.setJointLimits([-1.0, -2.0], [1.0, 2.0])

        self.assertTrue(self.system.isJointPositionFeasible([0.0, 0.0]))
        self.assertTrue(self.system.isJointPositionFeasible([-0.5, 1.5]))
        self.assertTrue(self.system.isJointPositionFeasible([0.5, -1.5]))

    def test_setJointLimits_unfeasiblePosition(self):
        self.system.setJointLimits([-1.0, -2.0], [1.0, 2.0])

        self.assertFalse(self.system.isJointPositionFeasible([1.5, 0.0]))
        self.assertFalse(self.system.isJointPositionFeasible([0.0, 2.5]))

    def test_defaultJointLimits_getMin(self):
        limitsMin = self.system.getJointLimitsMin()

        self.assertTrue(isinstance(limitsMin, np.ndarray))
        self.assertAlmostEqual(limitsMin.shape, (2,))
        self.assertAlmostEqual(limitsMin[0], -0.5)
        self.assertAlmostEqual(limitsMin[1], -0.8)

    def test_defaultJointLimits_getMax(self):
        limitsMax = self.system.getJointLimitsMax()

        self.assertTrue(isinstance(limitsMax, np.ndarray))
        self.assertAlmostEqual(limitsMax.shape, (2,))
        self.assertAlmostEqual(limitsMax[0], 0.5)
        self.assertAlmostEqual(limitsMax[1], 0.8)

    def test_defaultJointLimits_feasiblePosition(self):
        self.assertTrue(self.system.isJointPositionFeasible([0.0, 0.0]))
        self.assertTrue(self.system.isJointPositionFeasible([-0.2, 0.5]))

    def test_defaultJointLimits_unfeasiblePosition(self):
        self.assertFalse(self.system.isJointPositionFeasible([1.5, 0.0]))
        self.assertFalse(self.system.isJointPositionFeasible([0.0, 2.5]))

    def test_getKinematicChain(self):
        self.createKinematicChain()

        chain = self.system.getKinematicChain("chain1")

        self.assertEqual(chain.getDoF(), 2)

        motors = chain.getFixedMotors()

        self.assertTrue(isinstance(motors, dict))
        self.assertEqual(len(motors), 1)
        self.assertTrue(1 in motors)

        joints = chain.getActuatedJoints()

        self.assertTrue(isinstance(joints, list))
        self.assertEqual(len(joints), 2)
        self.assertEqual(joints[0].getName(), "joint1")
        self.assertEqual(joints[1].getName(), "joint2")

    def test_computeKinematicChainMotor(self):
        self.createKinematicChain()

        motor = self.system.computeKinematicChainMotor("chain1", [0.0, math.pi / 2.0])

        self.assertAlmostEqual(motor["scalar"], 0.7071067812)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.7071067812)
        self.assertAlmostEqual(motor["e1i"], -0.3535533906)
        self.assertAlmostEqual(motor["e2i"], -1.0606601718)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

    def test_computeKinematicChainAnalyticJacobian(self):
        self.createKinematicChain()

        jacobian = self.system.computeKinematicChainAnalyticJacobian(
            "chain1", [0.0, math.pi / 2.0]
        )

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

    def test_computeKinematicChainGeometricJacobian(self):
        self.createKinematicChain()

        jacobian = self.system.computeKinematicChainGeometricJacobian(
            "chain1", [0.0, math.pi / 2.0]
        )

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

    def test_computeKinematicChainGeometricJacobianBody(self):
        self.createKinematicChain()

        jacobian = self.system.computeKinematicChainGeometricJacobianBody(
            "chain1", [0.0, math.pi / 2.0]
        )

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


class TestSystemDynamics(unittest.TestCase):

    def setUp(self):
        # Create the system
        self.system = System()

        # Create some links
        com = Translator(TranslatorGenerator([0.0, 0.0, 0.0]))

        link1 = self.system.createLink("link1")
        link1.setMass(0.1)
        link1.setCenterOfMass(com)
        link1.setInertia(Inertia(0.1, np.eye(3)))
        link1.setAxis(MotorGenerator([0.0, 0.0, 1.0, 0.0, 0.0, 0.0]))

        link2 = self.system.createLink("link2")
        link2.setMass(0.1)
        link2.setCenterOfMass(com)
        link2.setInertia(Inertia(0.1, np.eye(3)))
        link2.setAxis(MotorGenerator([0.0, 0.0, 1.0, 0.0, 0.0, 0.0]))

        link3 = self.system.createLink("link3")
        link3.setMass(0.1)
        link3.setCenterOfMass(com)
        link3.setInertia(Inertia(0.1, np.eye(3)))
        link3.setAxis(MotorGenerator([0.0, 0.0, 1.0, 0.0, 0.0, 0.0]))

        link4 = self.system.createLink("link4")
        link4.setMass(0.1)
        link4.setCenterOfMass(com)
        link4.setInertia(Inertia(0.1, np.eye(3)))
        link4.setAxis(MotorGenerator([0.0, 0.0, 1.0, 0.0, 0.0, 0.0]))

        # Create some joints
        t = Translator(TranslatorGenerator([0.0, 1.0, 0.0]))

        joint1 = self.system.createRevoluteJoint("joint1")
        joint1.setAxis(RotorGenerator([0.0, 0.0, 1.0]))
        joint1.setFrame(Motor(t))

        limits = Joint.Limits()
        limits.positionLower = -0.5
        limits.positionUpper = 0.5
        limits.velocity = 1.0
        limits.torque = 1.0

        joint1.setLimits(limits)

        joint2 = self.system.createRevoluteJoint("joint2")
        joint2.setAxis(RotorGenerator([0.0, 0.0, 1.0]))
        joint2.setFrame(Motor(t))

        limits = Joint.Limits()
        limits.positionLower = -0.8
        limits.positionUpper = 0.8
        limits.velocity = 1.0
        limits.torque = 1.0

        joint2.setLimits(limits)

        joint3 = self.system.createRevoluteJoint("joint3")
        joint3.setAxis(RotorGenerator([0.0, 0.0, 1.0]))
        joint3.setFrame(Motor(t))

        limits = Joint.Limits()
        limits.positionLower = -0.8
        limits.positionUpper = 0.8
        limits.velocity = 1.0
        limits.torque = 1.0

        joint3.setLimits(limits)

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

        self.system.finalize()

        self.assertTrue(self.system.hasKinematicChain("joint3"))

    def tearDown(self):
        self.system = None

    def testInverseDynamics(self):
        position = [0.0, 0.1, 0.0]
        velocity = [0.1, 0.4, 0.0]
        acceleration = [-0.2, 0.8, 0.0]

        torques = self.system.computeInverseDynamics(position, velocity, acceleration)

        self.assertTrue(isinstance(torques, list))
        self.assertEqual(len(torques), 3)

        self.assertAlmostEqual(torques[0], 1.0574, places=4)
        self.assertAlmostEqual(torques[1], 1.2402, places=4)
        self.assertAlmostEqual(torques[2], 0.6, places=4)

    def testInverseDynamicsWithShorterKinematicChain(self):
        chain = self.system.createKinematicChain("chain2")

        chain.addActuatedJoint(self.system.getJoint("joint1"))
        chain.addActuatedJoint(self.system.getJoint("joint2"))

        chain.finalize()

        position = [0.0, 0.1]
        velocity = [0.1, 0.4]
        acceleration = [-0.2, 0.8]

        torques = self.system.computeInverseDynamics(position, velocity, acceleration)

        self.assertTrue(isinstance(torques, list))
        self.assertEqual(len(torques), 2)

        self.assertAlmostEqual(torques[0], 1.0574, places=4)
        self.assertAlmostEqual(torques[1], 1.2402, places=4)

    def testInverseDynamicsWithTooMuchDOF(self):
        position = [0.0] * 20
        velocity = [0.0] * 20
        acceleration = [0.0] * 20

        self.assertRaises(
            RuntimeError,
            self.system.computeInverseDynamics,
            position,
            velocity,
            acceleration,
        )

    def testInverseDynamicsWithNotEnoughDOF(self):
        position = [0.0] * 2
        velocity = [0.0] * 2
        acceleration = [0.0] * 2

        self.assertRaises(
            RuntimeError,
            self.system.computeInverseDynamics,
            position,
            velocity,
            acceleration,
        )

    def testForwardDynamics(self):
        position = [0.0, 0.1, 0.0]
        velocity = [0.1, 0.4, 0.0]
        torques = [1.0574, 1.2402, 0.6]

        acceleration = self.system.computeForwardDynamics(position, velocity, torques)

        self.assertTrue(isinstance(acceleration, list))
        self.assertEqual(len(acceleration), 3)

        self.assertAlmostEqual(acceleration[0], -0.2, places=4)
        self.assertAlmostEqual(acceleration[1], 0.8, places=4)
        self.assertAlmostEqual(acceleration[2], 0.0, places=4)

    def testForwardDynamicsWithShorterKinematicChain(self):
        chain = self.system.createKinematicChain("chain2")

        chain.addActuatedJoint(self.system.getJoint("joint1"))
        chain.addActuatedJoint(self.system.getJoint("joint2"))

        chain.finalize()

        position = [0.0, 0.1]
        velocity = [0.1, 0.4]
        torques = [1.0574, 1.2402]

        acceleration = self.system.computeForwardDynamics(position, velocity, torques)

        self.assertTrue(isinstance(acceleration, list))
        self.assertEqual(len(acceleration), 2)

        self.assertAlmostEqual(acceleration[0], -0.2, places=4)
        self.assertAlmostEqual(acceleration[1], 0.8, places=4)

    def testForwardDynamicsWithTooMuchDOF(self):
        position = [0.0] * 20
        velocity = [0.0] * 20
        torques = [0.0] * 20

        self.assertRaises(
            RuntimeError,
            self.system.computeForwardDynamics,
            position,
            velocity,
            torques,
        )

    def testForwardDynamicsWithNotEnoughDOF(self):
        position = [0.0] * 2
        velocity = [0.0] * 2
        torques = [0.0] * 2

        self.assertRaises(
            RuntimeError,
            self.system.computeForwardDynamics,
            position,
            velocity,
            torques,
        )


class TestSystemWithFixedJoints(unittest.TestCase):

    def setUp(self):
        # Create the system
        self.system = System()

        # Create some links
        com = Translator(TranslatorGenerator([0.0, 0.5, 0.0]))
        inertia = Inertia(1.0, 0.1, 0.0, 0.0, 0.1, 0.0, 0.01)

        link0 = self.system.createLink("link0")
        link0.setMass(1.0)
        link0.setCenterOfMass(com)
        link0.setInertia(inertia)

        link1 = self.system.createLink("link1")
        link1.setMass(1.0)
        link1.setCenterOfMass(com)
        link1.setInertia(inertia)

        link2 = self.system.createLink("link2")
        link2.setMass(1.0)
        link2.setCenterOfMass(com)
        link2.setInertia(inertia)

        link3 = self.system.createLink("link3")
        link3.setMass(1.0)
        link3.setCenterOfMass(com)
        link3.setInertia(inertia)

        link4 = self.system.createLink("link4")
        link4.setMass(1.0)
        link4.setCenterOfMass(com)
        link4.setInertia(inertia)

        link5 = self.system.createLink("link5")
        link5.setMass(1.0)
        link5.setCenterOfMass(com)
        link5.setInertia(inertia)

        link6 = self.system.createLink("link6")
        link6.setMass(1.0)
        link6.setCenterOfMass(com)
        link6.setInertia(inertia)

        link7 = self.system.createLink("link7")
        link7.setMass(1.0)
        link7.setCenterOfMass(com)
        link7.setInertia(inertia)

        # Create the fixed joints
        tx = Translator(TranslatorGenerator([1.0, 0.0, 0.0]))
        ty = Translator(TranslatorGenerator([0.0, 1.0, 0.0]))

        fixed_joint1 = self.system.createFixedJoint("fixed_joint1")
        fixed_joint1.setFrame(Motor(ty))

        fixed_joint3 = self.system.createFixedJoint("fixed_joint3")
        fixed_joint3.setFrame(Motor(ty))

        fixed_joint5 = self.system.createFixedJoint("fixed_joint5")
        fixed_joint5.setFrame(Motor(tx))

        fixed_joint6 = self.system.createFixedJoint("fixed_joint6")
        fixed_joint6.setFrame(Motor(tx))

        # Create the revolute joints
        axis = RotorGenerator([0.0, 0.0, 1.0])

        joint2 = self.system.createRevoluteJoint("joint2")
        joint2.setAxis(axis)
        joint2.setFrame(Motor(ty))

        limits = Joint.Limits()
        limits.positionLower = -0.5
        limits.positionUpper = 0.5
        limits.velocity = 1.0
        limits.torque = 1.0

        joint2.setLimits(limits)

        joint4 = self.system.createRevoluteJoint("joint4")
        joint4.setAxis(axis)
        joint4.setFrame(Motor(ty))

        limits = Joint.Limits()
        limits.positionLower = -0.6
        limits.positionUpper = 0.6
        limits.velocity = 1.0
        limits.torque = 1.0

        joint4.setLimits(limits)

        joint7 = self.system.createRevoluteJoint("joint7")
        joint7.setAxis(axis)
        joint7.setFrame(Motor(tx))

        limits = Joint.Limits()
        limits.positionLower = -0.7
        limits.positionUpper = 0.7
        limits.velocity = 1.0
        limits.torque = 1.0

        joint7.setLimits(limits)

        # Specify the hierarchy
        fixed_joint1.setParentLink(link0)
        link0.addChildJoint(fixed_joint1)

        fixed_joint1.setChildLink(link1)
        link1.setParentJoint(fixed_joint1)

        joint2.setParentLink(link1)
        link1.addChildJoint(joint2)

        joint2.setChildLink(link2)
        link2.setParentJoint(joint2)

        fixed_joint3.setParentLink(link2)
        link2.addChildJoint(fixed_joint3)

        fixed_joint3.setChildLink(link3)
        link3.setParentJoint(fixed_joint3)

        joint4.setParentLink(link3)
        link3.addChildJoint(joint4)

        joint4.setChildLink(link4)
        link4.setParentJoint(joint4)

        fixed_joint5.setParentLink(link4)
        link4.addChildJoint(fixed_joint5)

        fixed_joint5.setChildLink(link5)
        link5.setParentJoint(fixed_joint5)

        fixed_joint6.setParentLink(link5)
        link5.addChildJoint(fixed_joint6)

        fixed_joint6.setChildLink(link6)
        link6.setParentJoint(fixed_joint6)

        joint7.setParentLink(link6)
        link6.addChildJoint(joint7)

        joint7.setChildLink(link7)
        link7.setParentJoint(joint7)

        self.system.finalize()

        self.assertTrue(self.system.hasKinematicChain("joint7"))

    def tearDown(self):
        self.system = None

    def testLinkAxes(self):
        for name in ["link0", "link1", "link3", "link5", "link6"]:
            link = self.system.getLink(name)
            axis = link.getAxis()

            self.assertAlmostEqual(axis["e23"], 0.0)
            self.assertAlmostEqual(axis["e13"], 0.0)
            self.assertAlmostEqual(axis["e12"], 0.0)
            self.assertAlmostEqual(axis["e1i"], 0.0)
            self.assertAlmostEqual(axis["e2i"], 0.0)
            self.assertAlmostEqual(axis["e3i"], 0.0)

        for name in ["link2", "link4", "link7"]:
            link = self.system.getLink(name)
            axis = link.getAxis()

            self.assertAlmostEqual(axis["e23"], 0.0)
            self.assertAlmostEqual(axis["e13"], 0.0)
            self.assertAlmostEqual(axis["e12"], 1.0)
            self.assertAlmostEqual(axis["e1i"], -0.5)
            self.assertAlmostEqual(axis["e2i"], 0.0)
            self.assertAlmostEqual(axis["e3i"], 0.0)

    def testRandomConfiguration(self):
        config = self.system.getRandomConfiguration()

        self.assertTrue(isinstance(config, np.ndarray))
        self.assertAlmostEqual(config.shape, (3,))

    def test_setJointLimits_getMin(self):
        self.system.setJointLimits([-1.0, -2.0, -3.0], [1.0, 2.0, 3.0])

        limitsMin = self.system.getJointLimitsMin()

        self.assertTrue(isinstance(limitsMin, np.ndarray))
        self.assertAlmostEqual(limitsMin.shape, (3,))
        self.assertAlmostEqual(limitsMin[0], -1.0)
        self.assertAlmostEqual(limitsMin[1], -2.0)
        self.assertAlmostEqual(limitsMin[2], -3.0)

    def test_setJointLimits_getMax(self):
        self.system.setJointLimits([-1.0, -2.0, -3.0], [1.0, 2.0, 3.0])

        limitsMax = self.system.getJointLimitsMax()

        self.assertTrue(isinstance(limitsMax, np.ndarray))
        self.assertAlmostEqual(limitsMax.shape, (3,))
        self.assertAlmostEqual(limitsMax[0], 1.0)
        self.assertAlmostEqual(limitsMax[1], 2.0)
        self.assertAlmostEqual(limitsMax[2], 3.0)

    def test_setJointLimits_feasiblePosition(self):
        self.system.setJointLimits([-1.0, -2.0, -3.0], [1.0, 2.0, 3.0])

        self.assertTrue(self.system.isJointPositionFeasible([0.0, 0.0, 0.0]))
        self.assertTrue(self.system.isJointPositionFeasible([-0.5, 1.5, 2.5]))
        self.assertTrue(self.system.isJointPositionFeasible([0.5, -1.5, -2.5]))

    def test_setJointLimits_unfeasiblePosition(self):
        self.system.setJointLimits([-1.0, -2.0, -3.0], [1.0, 2.0, 3.0])

        self.assertFalse(self.system.isJointPositionFeasible([1.5, 0.0, 0.0]))
        self.assertFalse(self.system.isJointPositionFeasible([0.0, 2.5, 0.0]))
        self.assertFalse(self.system.isJointPositionFeasible([0.0, 0.0, 3.5]))

    def test_defaultJointLimits_getMin(self):
        limitsMin = self.system.getJointLimitsMin()

        self.assertTrue(isinstance(limitsMin, np.ndarray))
        self.assertAlmostEqual(limitsMin.shape, (3,))
        self.assertAlmostEqual(limitsMin[0], -0.5)
        self.assertAlmostEqual(limitsMin[1], -0.6)
        self.assertAlmostEqual(limitsMin[2], -0.7)

    def test_defaultJointLimits_getMax(self):
        limitsMax = self.system.getJointLimitsMax()

        self.assertTrue(isinstance(limitsMax, np.ndarray))
        self.assertAlmostEqual(limitsMax.shape, (3,))
        self.assertAlmostEqual(limitsMax[0], 0.5)
        self.assertAlmostEqual(limitsMax[1], 0.6)
        self.assertAlmostEqual(limitsMax[2], 0.7)

    def test_defaultJointLimits_feasiblePosition(self):
        self.assertTrue(self.system.isJointPositionFeasible([0.0, 0.0, 0.0]))
        self.assertTrue(self.system.isJointPositionFeasible([-0.2, 0.5, 0.6]))
        self.assertTrue(self.system.isJointPositionFeasible([0.2, -0.5, -0.6]))

    def test_defaultJointLimits_unfeasiblePosition(self):
        self.assertFalse(self.system.isJointPositionFeasible([1.5, 0.0, 0.0]))
        self.assertFalse(self.system.isJointPositionFeasible([0.0, 2.5, 0.0]))
        self.assertFalse(self.system.isJointPositionFeasible([0.0, 0.0, 3.5]))

    def testComputeEndEffectorPosition1(self):
        position = [0.0, 0.0, 0.0]
        motor = self.system.computeKinematicChainMotor("joint7", position)

        self.assertTrue(isinstance(motor, Motor))

        point = motor.apply(Point(0.0, 0.0, 0.0))

        self.assertAlmostEqual(point["e1"], 3.0)
        self.assertAlmostEqual(point["e2"], 4.0)
        self.assertAlmostEqual(point["e3"], 0.0)
        self.assertAlmostEqual(point["ei"], 12.5)
        self.assertAlmostEqual(point["e0"], 1.0)

    def testComputeEndEffectorPosition2(self):
        position = [0.0, math.pi / 2.0, 0.0]
        motor = self.system.computeKinematicChainMotor("joint7", position)

        self.assertTrue(isinstance(motor, Motor))

        point = motor.apply(Point(0.0, 0.0, 0.0))

        self.assertAlmostEqual(point["e1"], 0.0)
        self.assertAlmostEqual(point["e2"], 7.0)
        self.assertAlmostEqual(point["e3"], 0.0)
        self.assertAlmostEqual(point["ei"], 24.5)
        self.assertAlmostEqual(point["e0"], 1.0)

    def testGetJointTorques(self):
        position = [0.0, 0.1, 0.0]
        velocity = [0.1, 0.4, 0.0]
        acceleration = [-0.2, 0.8, 0.0]

        torques = self.system.computeInverseDynamics(position, velocity, acceleration)

        self.assertTrue(isinstance(torques, list))
        self.assertEqual(len(torques), 3)

        self.assertAlmostEqual(torques[0], 4.7830207575, places=4)
        self.assertAlmostEqual(torques[1], 3.7083281023, places=4)
        self.assertAlmostEqual(torques[2], 0.1819987506, places=4)

    def testGetJointAccelerations(self):
        position = [0.0, 0.1, 0.0]
        velocity = [0.1, 0.4, 0.0]
        torques = [4.7830207575, 3.7083281023, 0.1819987506]

        acceleration = self.system.computeForwardDynamics(position, velocity, torques)

        self.assertTrue(isinstance(acceleration, list))
        self.assertEqual(len(acceleration), 3)

        self.assertAlmostEqual(acceleration[0], -0.2, places=4)
        self.assertAlmostEqual(acceleration[1], 0.8, places=4)
        self.assertAlmostEqual(acceleration[2], 0.0, places=4)


class TestSystemWith7Joints(unittest.TestCase):

    def setUp(self):
        # Create the system
        self.system = System()

        # Create some links
        com = Translator(TranslatorGenerator([0.0, 0.5, 0.0]))
        inertia = Inertia(1.0, 0.1, 0.0, 0.0, 0.1, 0.0, 0.01)

        link0 = self.system.createLink("link0")
        link0.setMass(1.0)
        link0.setCenterOfMass(com)
        link0.setInertia(inertia)

        link1 = self.system.createLink("link1")
        link1.setMass(1.0)
        link1.setCenterOfMass(com)
        link1.setInertia(inertia)

        link2 = self.system.createLink("link2")
        link2.setMass(1.0)
        link2.setCenterOfMass(com)
        link2.setInertia(inertia)

        link3 = self.system.createLink("link3")
        link3.setMass(1.0)
        link3.setCenterOfMass(com)
        link3.setInertia(inertia)

        link4 = self.system.createLink("link4")
        link4.setMass(1.0)
        link4.setCenterOfMass(com)
        link4.setInertia(inertia)

        link5 = self.system.createLink("link5")
        link5.setMass(1.0)
        link5.setCenterOfMass(com)
        link5.setInertia(inertia)

        link6 = self.system.createLink("link6")
        link6.setMass(1.0)
        link6.setCenterOfMass(com)
        link6.setInertia(inertia)

        link7 = self.system.createLink("link7")
        link7.setMass(1.0)
        link7.setCenterOfMass(com)
        link7.setInertia(inertia)

        # Create the revolute joints
        tx = Translator(TranslatorGenerator([1.0, 0.0, 0.0]))
        ty = Translator(TranslatorGenerator([0.0, 1.0, 0.0]))
        axis = RotorGenerator([0.0, 0.0, 1.0])

        joint1 = self.system.createRevoluteJoint("joint1")
        joint1.setAxis(axis)
        joint1.setFrame(Motor(ty))

        joint2 = self.system.createRevoluteJoint("joint2")
        joint2.setAxis(axis)
        joint2.setFrame(Motor(ty))

        joint3 = self.system.createRevoluteJoint("joint3")
        joint3.setAxis(axis)
        joint3.setFrame(Motor(ty))

        joint4 = self.system.createRevoluteJoint("joint4")
        joint4.setAxis(axis)
        joint4.setFrame(Motor(ty))

        joint5 = self.system.createRevoluteJoint("joint5")
        joint5.setAxis(axis)
        joint5.setFrame(Motor(tx))

        joint6 = self.system.createRevoluteJoint("joint6")
        joint6.setAxis(axis)
        joint6.setFrame(Motor(tx))

        joint7 = self.system.createRevoluteJoint("joint7")
        joint7.setAxis(axis)
        joint7.setFrame(Motor(tx))

        # Specify the hierarchy
        joint1.setParentLink(link0)
        link0.addChildJoint(joint1)

        joint1.setChildLink(link1)
        link1.setParentJoint(joint1)

        joint2.setParentLink(link1)
        link1.addChildJoint(joint2)

        joint2.setChildLink(link2)
        link2.setParentJoint(joint2)

        joint3.setParentLink(link2)
        link2.addChildJoint(joint3)

        joint3.setChildLink(link3)
        link3.setParentJoint(joint3)

        joint4.setParentLink(link3)
        link3.addChildJoint(joint4)

        joint4.setChildLink(link4)
        link4.setParentJoint(joint4)

        joint5.setParentLink(link4)
        link4.addChildJoint(joint5)

        joint5.setChildLink(link5)
        link5.setParentJoint(joint5)

        joint6.setParentLink(link5)
        link5.addChildJoint(joint6)

        joint6.setChildLink(link6)
        link6.setParentJoint(joint6)

        joint7.setParentLink(link6)
        link6.addChildJoint(joint7)

        joint7.setChildLink(link7)
        link7.setParentJoint(joint7)

        self.system.finalize()

        self.assertTrue(self.system.hasKinematicChain("joint7"))

    def tearDown(self):
        self.system = None

    def testLinkAxes(self):
        for name in ["link0"]:
            link = self.system.getLink(name)
            axis = link.getAxis()

            self.assertAlmostEqual(axis["e23"], 0.0)
            self.assertAlmostEqual(axis["e13"], 0.0)
            self.assertAlmostEqual(axis["e12"], 0.0)
            self.assertAlmostEqual(axis["e1i"], 0.0)
            self.assertAlmostEqual(axis["e2i"], 0.0)
            self.assertAlmostEqual(axis["e3i"], 0.0)

        for name in ["link1", "link2", "link3", "link4", "link5", "link6", "link7"]:
            link = self.system.getLink(name)
            axis = link.getAxis()

            self.assertAlmostEqual(axis["e23"], 0.0)
            self.assertAlmostEqual(axis["e13"], 0.0)
            self.assertAlmostEqual(axis["e12"], 1.0)
            self.assertAlmostEqual(axis["e1i"], -0.5)
            self.assertAlmostEqual(axis["e2i"], 0.0)
            self.assertAlmostEqual(axis["e3i"], 0.0)

    def testRandomConfiguration(self):
        config = self.system.getRandomConfiguration()

        self.assertTrue(isinstance(config, np.ndarray))
        self.assertAlmostEqual(config.shape, (7,))

    def testComputeEndEffectorPosition1(self):
        position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        motor = self.system.computeKinematicChainMotor("joint7", position)

        self.assertTrue(isinstance(motor, Motor))

        point = motor.apply(Point(0.0, 0.0, 0.0))

        self.assertAlmostEqual(point["e1"], 3.0)
        self.assertAlmostEqual(point["e2"], 4.0)
        self.assertAlmostEqual(point["e3"], 0.0)
        self.assertAlmostEqual(point["ei"], 12.5)
        self.assertAlmostEqual(point["e0"], 1.0)

    def testComputeEndEffectorPosition2(self):
        position = [0.0, 0.0, 0.0, math.pi / 2.0, 0.0, 0.0, 0.0]
        motor = self.system.computeKinematicChainMotor("joint7", position)

        self.assertTrue(isinstance(motor, Motor))

        point = motor.apply(Point(0.0, 0.0, 0.0))

        self.assertAlmostEqual(point["e1"], 0.0)
        self.assertAlmostEqual(point["e2"], 7.0)
        self.assertAlmostEqual(point["e3"], 0.0)
        self.assertAlmostEqual(point["ei"], 24.5)
        self.assertAlmostEqual(point["e0"], 1.0)

    def testGetJointTorques(self):
        position = [0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0]
        velocity = [0.0, 0.1, 0.0, 0.4, 0.0, 0.0, 0.0]
        acceleration = [0.0, -0.2, 0.0, 0.8, 0.0, 0.0, 0.0]

        torques = self.system.computeInverseDynamics(position, velocity, acceleration)

        self.assertTrue(isinstance(torques, list))
        self.assertEqual(len(torques), 7)

        self.assertAlmostEqual(torques[0], 11.157, places=4)
        self.assertAlmostEqual(torques[1], 10.161, places=4)
        self.assertAlmostEqual(torques[2], 9.11698, places=4)
        self.assertAlmostEqual(torques[3], 7.87299, places=4)
        self.assertAlmostEqual(torques[4], 4.86949, places=4)
        self.assertAlmostEqual(torques[5], 2.15616, places=4)
        self.assertAlmostEqual(torques[6], 0.332998, places=4)

    def testGetJointAccelerations(self):
        position = [0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0]
        velocity = [0.0, 0.1, 0.0, 0.4, 0.0, 0.0, 0.0]
        torques = [11.157, 10.161, 9.11698, 7.87299, 4.86949, 2.15616, 0.332998]

        acceleration = self.system.computeForwardDynamics(position, velocity, torques)

        self.assertTrue(isinstance(acceleration, list))
        self.assertEqual(len(acceleration), 7)

        self.assertAlmostEqual(acceleration[0], 0.0, places=3)
        self.assertAlmostEqual(acceleration[1], -0.2, places=3)
        self.assertAlmostEqual(acceleration[2], 0.0, places=3)
        self.assertAlmostEqual(acceleration[3], 0.8, places=3)
        self.assertAlmostEqual(acceleration[4], 0.0, places=3)
        self.assertAlmostEqual(acceleration[5], 0.0, places=3)
        self.assertAlmostEqual(acceleration[6], 0.0, places=3)


if __name__ == "__main__":
    unittest.main()
