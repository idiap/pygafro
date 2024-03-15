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

from pygafro import Motor
from pygafro import RotorGenerator
from pygafro import System
from pygafro import Translator
from pygafro import TranslatorGenerator


class TestDefaultKinematicChain(unittest.TestCase):

    def test_defaults(self):
        system = System()

        chain = system.createKinematicChain("default")

        self.assertEqual(chain.getDoF(), 0)

        motors = chain.getFixedMotors()

        self.assertTrue(isinstance(motors, dict))
        self.assertEqual(len(motors), 0)

        joints = chain.getActuatedJoints()

        self.assertTrue(isinstance(joints, list))
        self.assertEqual(len(joints), 0)


class TestKinematicChainWithJoints(unittest.TestCase):

    def setUp(self):
        translator = Motor(Translator(TranslatorGenerator([0.0, 1.0, 0.0])))
        generator = RotorGenerator([0.0, 0.0, 1.0])

        self.system = System()

        joint1 = self.system.createRevoluteJoint("joint1")
        joint1.setAxis(generator)

        joint2 = self.system.createRevoluteJoint("joint2")
        joint2.setFrame(translator)
        joint2.setAxis(generator)

        joint3 = self.system.createRevoluteJoint("joint3")
        joint3.setFrame(translator)
        joint3.setAxis(generator)

        self.chain = self.system.createKinematicChain("default")
        self.chain.addActuatedJoint(joint1)
        self.chain.addActuatedJoint(joint2)
        self.chain.addActuatedJoint(joint3)

    def tearDown(self):
        self.chain = None
        self.system = None

    def test_defaults(self):
        self.assertEqual(self.chain.getDoF(), 3)

        motors = self.chain.getFixedMotors()

        self.assertTrue(isinstance(motors, dict))
        self.assertEqual(len(motors), 0)

        joints = self.chain.getActuatedJoints()

        self.assertTrue(isinstance(joints, list))
        self.assertEqual(len(joints), 3)
        self.assertEqual(joints[0].getName(), "joint1")
        self.assertEqual(joints[1].getName(), "joint2")
        self.assertEqual(joints[2].getName(), "joint3")

    def test_setFixedMotors(self):
        fixedMotors = {
            0: Motor(),
            1: Motor(),
            3: Motor(),
        }

        self.chain.setFixedMotors(fixedMotors)

        motors = self.chain.getFixedMotors()

        self.assertTrue(isinstance(motors, dict))
        self.assertEqual(len(motors), 3)
        self.assertTrue(0 in motors)
        self.assertTrue(1 in motors)
        self.assertTrue(3 in motors)

    def test_computeMotor(self):
        motor = self.chain.computeMotor([0.0, 0.0, math.pi / 2.0])

        self.assertAlmostEqual(motor["scalar"], 0.7071067812)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.7071067812)
        self.assertAlmostEqual(motor["e1i"], -0.7071067812)
        self.assertAlmostEqual(motor["e2i"], -0.7071067812)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

    def test_computeMotors(self):
        joints = self.chain.getActuatedJoints()

        for i in range(3):
            motor = self.chain.computeMotor(i, math.pi / 2.0)
            ref = joints[i].getMotor(math.pi / 2.0)

            self.assertAlmostEqual(motor["scalar"], ref["scalar"])
            self.assertAlmostEqual(motor["e23"], ref["e23"])
            self.assertAlmostEqual(motor["e13"], ref["e13"])
            self.assertAlmostEqual(motor["e12"], ref["e12"])
            self.assertAlmostEqual(motor["e1i"], ref["e1i"])
            self.assertAlmostEqual(motor["e2i"], ref["e2i"])
            self.assertAlmostEqual(motor["e3i"], ref["e3i"])
            self.assertAlmostEqual(motor["e123i"], ref["e123i"])

    def test_computeMotorDerivatives(self):
        joints = self.chain.getActuatedJoints()

        for i in range(3):
            motor = self.chain.computeMotorDerivative(i, math.pi / 2.0)
            ref = joints[i].getMotorDerivative(math.pi / 2.0)

            self.assertAlmostEqual(motor["scalar"], ref["scalar"])
            self.assertAlmostEqual(motor["e23"], ref["e23"])
            self.assertAlmostEqual(motor["e13"], ref["e13"])
            self.assertAlmostEqual(motor["e12"], ref["e12"])
            self.assertAlmostEqual(motor["e1i"], ref["e1i"])
            self.assertAlmostEqual(motor["e2i"], ref["e2i"])
            self.assertAlmostEqual(motor["e3i"], ref["e3i"])
            self.assertAlmostEqual(motor["e123i"], ref["e123i"])

    def test_computeAnalyticJacobian(self):
        jacobian = self.chain.computeAnalyticJacobian([0.0, 0.0, math.pi / 2.0])

        self.assertTrue(isinstance(jacobian, list))
        self.assertEqual(len(jacobian), 3)

        self.assertAlmostEqual(jacobian[0]["scalar"], -0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], -0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e1i"], 0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e2i"], -0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e3i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e123i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["scalar"], -0.3535533906)
        self.assertAlmostEqual(jacobian[1]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e12"], -0.3535533906)
        self.assertAlmostEqual(jacobian[1]["e1i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e3i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e123i"], 0.0)

        self.assertAlmostEqual(jacobian[2]["scalar"], -0.3535533906)
        self.assertAlmostEqual(jacobian[2]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e12"], -0.3535533906)
        self.assertAlmostEqual(jacobian[2]["e1i"], -0.3535533906)
        self.assertAlmostEqual(jacobian[2]["e2i"], 0.3535533906)
        self.assertAlmostEqual(jacobian[2]["e3i"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e123i"], 0.0)

    def test_computeGeometricJacobian(self):
        jacobian = self.chain.computeGeometricJacobian([0.0, 0.0, math.pi / 2.0])

        self.assertTrue(isinstance(jacobian, list))
        self.assertEqual(len(jacobian), 3)

        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e1i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e3i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[1]["e1i"], 1.0)
        self.assertAlmostEqual(jacobian[1]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e3i"], 0.0)

        self.assertAlmostEqual(jacobian[2]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[2]["e1i"], 2.0)
        self.assertAlmostEqual(jacobian[2]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e3i"], 0.0)

    def test_computeGeometricJacobianBody(self):
        translator = Motor(Translator(TranslatorGenerator([0.0, 1.0, 0.0])))
        self.chain.addFixedMotor(translator)

        jacobian = self.chain.computeGeometricJacobianBody([0.0, 0.0, math.pi / 2.0])

        self.assertTrue(isinstance(jacobian, list))
        self.assertEqual(len(jacobian), 3)

        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e1i"], -1.0)
        self.assertAlmostEqual(jacobian[0]["e2i"], 2.0)
        self.assertAlmostEqual(jacobian[0]["e3i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[1]["e1i"], -1.0)
        self.assertAlmostEqual(jacobian[1]["e2i"], 1.0)
        self.assertAlmostEqual(jacobian[1]["e3i"], 0.0)

        self.assertAlmostEqual(jacobian[2]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[2]["e1i"], -1.0)
        self.assertAlmostEqual(jacobian[2]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e3i"], 0.0)


class TestKinematicChainWithFixedMotors(unittest.TestCase):

    def setUp(self):
        translator = Motor(Translator(TranslatorGenerator([0.0, 1.0, 0.0])))
        generator = RotorGenerator([0.0, 0.0, 1.0])

        self.system = System()

        joint1 = self.system.createRevoluteJoint("joint1")
        joint1.setAxis(generator)

        joint2 = self.system.createRevoluteJoint("joint2")
        joint2.setAxis(generator)

        joint3 = self.system.createRevoluteJoint("joint3")
        joint3.setAxis(generator)

        self.chain = self.system.createKinematicChain("default")
        self.chain.addActuatedJoint(joint1)
        self.chain.addFixedMotor(translator)
        self.chain.addActuatedJoint(joint2)
        self.chain.addFixedMotor(translator)
        self.chain.addActuatedJoint(joint3)

    def tearDown(self):
        self.chain = None
        self.system = None

    def test_defaults(self):
        self.assertEqual(self.chain.getDoF(), 3)

        motors = self.chain.getFixedMotors()

        self.assertTrue(isinstance(motors, dict))
        self.assertEqual(len(motors), 2)

        joints = self.chain.getActuatedJoints()

        self.assertTrue(isinstance(joints, list))
        self.assertEqual(len(joints), 3)
        self.assertEqual(joints[0].getName(), "joint1")
        self.assertEqual(joints[1].getName(), "joint2")
        self.assertEqual(joints[2].getName(), "joint3")

    def test_computeMotor(self):
        motor = self.chain.computeMotor([0.0, 0.0, math.pi / 2.0])

        self.assertAlmostEqual(motor["scalar"], 0.7071067812)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.7071067812)
        self.assertAlmostEqual(motor["e1i"], -0.7071067812)
        self.assertAlmostEqual(motor["e2i"], -0.7071067812)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

    def test_computeMotors(self):
        motor = self.chain.computeMotor(0, math.pi / 2.0)

        self.assertAlmostEqual(motor["scalar"], 0.7071067812)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.7071067812)
        self.assertAlmostEqual(motor["e1i"], 0.3535533906)
        self.assertAlmostEqual(motor["e2i"], -0.3535533906)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

        motor = self.chain.computeMotor(1, math.pi / 2.0)

        self.assertAlmostEqual(motor["scalar"], 0.7071067812)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.7071067812)
        self.assertAlmostEqual(motor["e1i"], 0.3535533906)
        self.assertAlmostEqual(motor["e2i"], -0.3535533906)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

        motor = self.chain.computeMotor(2, math.pi / 2.0)

        self.assertAlmostEqual(motor["scalar"], 0.7071067812)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.7071067812)
        self.assertAlmostEqual(motor["e1i"], 0.0)
        self.assertAlmostEqual(motor["e2i"], 0.0)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

    def test_computeMotorDerivatives(self):
        motor = self.chain.computeMotorDerivative(0, math.pi / 2.0)

        self.assertAlmostEqual(motor["scalar"], -0.3535533906)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.3535533906)
        self.assertAlmostEqual(motor["e1i"], 0.1767766953)
        self.assertAlmostEqual(motor["e2i"], 0.1767766953)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

        motor = self.chain.computeMotorDerivative(1, math.pi / 2.0)

        self.assertAlmostEqual(motor["scalar"], -0.3535533906)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.3535533906)
        self.assertAlmostEqual(motor["e1i"], 0.1767766953)
        self.assertAlmostEqual(motor["e2i"], 0.1767766953)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

        motor = self.chain.computeMotorDerivative(2, math.pi / 2.0)

        self.assertAlmostEqual(motor["scalar"], -0.3535533906)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.3535533906)
        self.assertAlmostEqual(motor["e1i"], 0.0)
        self.assertAlmostEqual(motor["e2i"], 0.0)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

    def test_computeAnalyticJacobian(self):
        jacobian = self.chain.computeAnalyticJacobian([0.0, 0.0, math.pi / 2.0])

        self.assertTrue(isinstance(jacobian, list))
        self.assertEqual(len(jacobian), 3)

        self.assertAlmostEqual(jacobian[0]["scalar"], -0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], -0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e1i"], 0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e2i"], -0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e3i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e123i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["scalar"], -0.3535533906)
        self.assertAlmostEqual(jacobian[1]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e12"], -0.3535533906)
        self.assertAlmostEqual(jacobian[1]["e1i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e3i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e123i"], 0.0)

        self.assertAlmostEqual(jacobian[2]["scalar"], -0.3535533906)
        self.assertAlmostEqual(jacobian[2]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e12"], -0.3535533906)
        self.assertAlmostEqual(jacobian[2]["e1i"], -0.3535533906)
        self.assertAlmostEqual(jacobian[2]["e2i"], 0.3535533906)
        self.assertAlmostEqual(jacobian[2]["e3i"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e123i"], 0.0)

    def test_computeGeometricJacobian(self):
        jacobian = self.chain.computeGeometricJacobian([0.0, 0.0, math.pi / 2.0])

        self.assertTrue(isinstance(jacobian, list))
        self.assertEqual(len(jacobian), 3)

        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e1i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e3i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[1]["e1i"], 1.0)
        self.assertAlmostEqual(jacobian[1]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e3i"], 0.0)

        self.assertAlmostEqual(jacobian[2]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[2]["e1i"], 2.0)
        self.assertAlmostEqual(jacobian[2]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e3i"], 0.0)

    def test_computeGeometricJacobianBody(self):
        translator = Motor(Translator(TranslatorGenerator([0.0, 1.0, 0.0])))
        self.chain.addFixedMotor(translator)

        jacobian = self.chain.computeGeometricJacobianBody([0.0, 0.0, math.pi / 2.0])

        self.assertTrue(isinstance(jacobian, list))
        self.assertEqual(len(jacobian), 3)

        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e1i"], -1.0)
        self.assertAlmostEqual(jacobian[0]["e2i"], 0.0)
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
        self.assertAlmostEqual(jacobian[2]["e1i"], -1.0)
        self.assertAlmostEqual(jacobian[2]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e3i"], 0.0)


class TestConstKinematicChainWithJoints(unittest.TestCase):

    def setUp(self):
        translator = Motor(Translator(TranslatorGenerator([0.0, 1.0, 0.0])))
        generator = RotorGenerator([0.0, 0.0, 1.0])

        self.system = System()

        joint1 = self.system.createRevoluteJoint("joint1")
        joint1.setAxis(generator)

        joint2 = self.system.createRevoluteJoint("joint2")
        joint2.setFrame(translator)
        joint2.setAxis(generator)

        joint3 = self.system.createRevoluteJoint("joint3")
        joint3.setFrame(translator)
        joint3.setAxis(generator)

        chain = self.system.createKinematicChain("chain1")
        chain.addActuatedJoint(joint1)
        chain.addActuatedJoint(joint2)
        chain.addActuatedJoint(joint3)

        self.chain = self.system.getKinematicChain("chain1")

    def tearDown(self):
        self.chain = None
        self.system = None

    def test_defaults(self):
        self.assertEqual(self.chain.getDoF(), 3)

        motors = self.chain.getFixedMotors()

        self.assertTrue(isinstance(motors, dict))
        self.assertEqual(len(motors), 0)

        joints = self.chain.getActuatedJoints()

        self.assertTrue(isinstance(joints, list))
        self.assertEqual(len(joints), 3)
        self.assertEqual(joints[0].getName(), "joint1")
        self.assertEqual(joints[1].getName(), "joint2")
        self.assertEqual(joints[2].getName(), "joint3")

    def test_computeMotor(self):
        motor = self.chain.computeMotor([0.0, 0.0, math.pi / 2.0])

        self.assertAlmostEqual(motor["scalar"], 0.7071067812)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.7071067812)
        self.assertAlmostEqual(motor["e1i"], -0.7071067812)
        self.assertAlmostEqual(motor["e2i"], -0.7071067812)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

    def test_computeMotors(self):
        joints = self.chain.getActuatedJoints()

        for i in range(3):
            motor = self.chain.computeMotor(i, math.pi / 2.0)
            ref = joints[i].getMotor(math.pi / 2.0)

            self.assertAlmostEqual(motor["scalar"], ref["scalar"])
            self.assertAlmostEqual(motor["e23"], ref["e23"])
            self.assertAlmostEqual(motor["e13"], ref["e13"])
            self.assertAlmostEqual(motor["e12"], ref["e12"])
            self.assertAlmostEqual(motor["e1i"], ref["e1i"])
            self.assertAlmostEqual(motor["e2i"], ref["e2i"])
            self.assertAlmostEqual(motor["e3i"], ref["e3i"])
            self.assertAlmostEqual(motor["e123i"], ref["e123i"])

    def test_computeMotorDerivatives(self):
        joints = self.chain.getActuatedJoints()

        for i in range(3):
            motor = self.chain.computeMotorDerivative(i, math.pi / 2.0)
            ref = joints[i].getMotorDerivative(math.pi / 2.0)

            self.assertAlmostEqual(motor["scalar"], ref["scalar"])
            self.assertAlmostEqual(motor["e23"], ref["e23"])
            self.assertAlmostEqual(motor["e13"], ref["e13"])
            self.assertAlmostEqual(motor["e12"], ref["e12"])
            self.assertAlmostEqual(motor["e1i"], ref["e1i"])
            self.assertAlmostEqual(motor["e2i"], ref["e2i"])
            self.assertAlmostEqual(motor["e3i"], ref["e3i"])
            self.assertAlmostEqual(motor["e123i"], ref["e123i"])

    def test_computeAnalyticJacobian(self):
        jacobian = self.chain.computeAnalyticJacobian([0.0, 0.0, math.pi / 2.0])

        self.assertAlmostEqual(jacobian[0]["scalar"], -0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], -0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e1i"], 0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e2i"], -0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e3i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e123i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["scalar"], -0.3535533906)
        self.assertAlmostEqual(jacobian[1]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e12"], -0.3535533906)
        self.assertAlmostEqual(jacobian[1]["e1i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e3i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e123i"], 0.0)

        self.assertAlmostEqual(jacobian[2]["scalar"], -0.3535533906)
        self.assertAlmostEqual(jacobian[2]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e12"], -0.3535533906)
        self.assertAlmostEqual(jacobian[2]["e1i"], -0.3535533906)
        self.assertAlmostEqual(jacobian[2]["e2i"], 0.3535533906)
        self.assertAlmostEqual(jacobian[2]["e3i"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e123i"], 0.0)

    def test_computeGeometricJacobian(self):
        jacobian = self.chain.computeGeometricJacobian([0.0, 0.0, math.pi / 2.0])

        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e1i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e3i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[1]["e1i"], 1.0)
        self.assertAlmostEqual(jacobian[1]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e3i"], 0.0)

        self.assertAlmostEqual(jacobian[2]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[2]["e1i"], 2.0)
        self.assertAlmostEqual(jacobian[2]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e3i"], 0.0)


class TestConstKinematicChainWithFixedMotors(unittest.TestCase):

    def setUp(self):
        translator = Motor(Translator(TranslatorGenerator([0.0, 1.0, 0.0])))
        generator = RotorGenerator([0.0, 0.0, 1.0])

        self.system = System()

        joint1 = self.system.createRevoluteJoint("joint1")
        joint1.setAxis(generator)

        joint2 = self.system.createRevoluteJoint("joint2")
        joint2.setAxis(generator)

        joint3 = self.system.createRevoluteJoint("joint3")
        joint3.setAxis(generator)

        chain = self.system.createKinematicChain("chain1")
        chain.addActuatedJoint(joint1)
        chain.addFixedMotor(translator)
        chain.addActuatedJoint(joint2)
        chain.addFixedMotor(translator)
        chain.addActuatedJoint(joint3)
        chain.addFixedMotor(translator)

        self.chain = self.system.getKinematicChain("chain1")

    def tearDown(self):
        self.chain = None
        self.system = None

    def test_defaults(self):
        self.assertEqual(self.chain.getDoF(), 3)

        motors = self.chain.getFixedMotors()

        self.assertTrue(isinstance(motors, dict))
        self.assertEqual(len(motors), 3)

        joints = self.chain.getActuatedJoints()

        self.assertTrue(isinstance(joints, list))
        self.assertEqual(len(joints), 3)
        self.assertEqual(joints[0].getName(), "joint1")
        self.assertEqual(joints[1].getName(), "joint2")
        self.assertEqual(joints[2].getName(), "joint3")

    def test_computeMotor(self):
        motor = self.chain.computeMotor([0.0, 0.0, math.pi / 2.0])

        self.assertAlmostEqual(motor["scalar"], 0.7071067812)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.7071067812)
        self.assertAlmostEqual(motor["e1i"], -0.3535533906)
        self.assertAlmostEqual(motor["e2i"], -1.0606601717798214)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

    def test_computeMotors(self):
        motor = self.chain.computeMotor(0, math.pi / 2.0)

        self.assertAlmostEqual(motor["scalar"], 0.7071067812)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.7071067812)
        self.assertAlmostEqual(motor["e1i"], 0.3535533906)
        self.assertAlmostEqual(motor["e2i"], -0.3535533906)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

        motor = self.chain.computeMotor(1, math.pi / 2.0)

        self.assertAlmostEqual(motor["scalar"], 0.7071067812)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.7071067812)
        self.assertAlmostEqual(motor["e1i"], 0.3535533906)
        self.assertAlmostEqual(motor["e2i"], -0.3535533906)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

        motor = self.chain.computeMotor(2, math.pi / 2.0)

        self.assertAlmostEqual(motor["scalar"], 0.7071067812)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.7071067812)
        self.assertAlmostEqual(motor["e1i"], 0.3535533906)
        self.assertAlmostEqual(motor["e2i"], -0.3535533906)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

    def test_computeMotorDerivatives(self):
        motor = self.chain.computeMotorDerivative(0, math.pi / 2.0)

        self.assertAlmostEqual(motor["scalar"], -0.3535533906)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.3535533906)
        self.assertAlmostEqual(motor["e1i"], 0.1767766953)
        self.assertAlmostEqual(motor["e2i"], 0.1767766953)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

        motor = self.chain.computeMotorDerivative(1, math.pi / 2.0)

        self.assertAlmostEqual(motor["scalar"], -0.3535533906)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.3535533906)
        self.assertAlmostEqual(motor["e1i"], 0.1767766953)
        self.assertAlmostEqual(motor["e2i"], 0.1767766953)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

        motor = self.chain.computeMotorDerivative(2, math.pi / 2.0)

        self.assertAlmostEqual(motor["scalar"], -0.3535533906)
        self.assertAlmostEqual(motor["e23"], 0.0)
        self.assertAlmostEqual(motor["e13"], 0.0)
        self.assertAlmostEqual(motor["e12"], -0.3535533906)
        self.assertAlmostEqual(motor["e1i"], 0.1767766952966369)
        self.assertAlmostEqual(motor["e2i"], 0.1767766952966369)
        self.assertAlmostEqual(motor["e3i"], 0.0)
        self.assertAlmostEqual(motor["e123i"], 0.0)

    def test_computeAnalyticJacobian(self):
        jacobian = self.chain.computeAnalyticJacobian([0.0, 0.0, math.pi / 2.0])

        self.assertAlmostEqual(jacobian[0]["scalar"], -0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], -0.3535533906)
        self.assertAlmostEqual(jacobian[0]["e1i"], 0.5303300858899107)
        self.assertAlmostEqual(jacobian[0]["e2i"], -0.17677669529663687)
        self.assertAlmostEqual(jacobian[0]["e3i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e123i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["scalar"], -0.3535533906)
        self.assertAlmostEqual(jacobian[1]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e12"], -0.3535533906)
        self.assertAlmostEqual(jacobian[1]["e1i"], 0.1767766952966369)
        self.assertAlmostEqual(jacobian[1]["e2i"], 0.1767766952966369)
        self.assertAlmostEqual(jacobian[1]["e3i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e123i"], 0.0)

        self.assertAlmostEqual(jacobian[2]["scalar"], -0.3535533906)
        self.assertAlmostEqual(jacobian[2]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e12"], -0.3535533906)
        self.assertAlmostEqual(jacobian[2]["e1i"], -0.1767766952966369)
        self.assertAlmostEqual(jacobian[2]["e2i"], 0.5303300858899106)
        self.assertAlmostEqual(jacobian[2]["e3i"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e123i"], 0.0)

    def test_computeGeometricJacobian(self):
        jacobian = self.chain.computeGeometricJacobian([0.0, 0.0, math.pi / 2.0])

        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e1i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e3i"], 0.0)

        self.assertAlmostEqual(jacobian[1]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[1]["e1i"], 1.0)
        self.assertAlmostEqual(jacobian[1]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[1]["e3i"], 0.0)

        self.assertAlmostEqual(jacobian[2]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[2]["e1i"], 2.0)
        self.assertAlmostEqual(jacobian[2]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e3i"], 0.0)

    def test_computeGeometricJacobianBody(self):
        jacobian = self.chain.computeGeometricJacobianBody([0.0, 0.0, math.pi / 2.0])

        self.assertAlmostEqual(jacobian[0]["e23"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e13"], 0.0)
        self.assertAlmostEqual(jacobian[0]["e12"], 1.0)
        self.assertAlmostEqual(jacobian[0]["e1i"], -1.0)
        self.assertAlmostEqual(jacobian[0]["e2i"], 0.0)
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
        self.assertAlmostEqual(jacobian[2]["e1i"], -1.0)
        self.assertAlmostEqual(jacobian[2]["e2i"], 0.0)
        self.assertAlmostEqual(jacobian[2]["e3i"], 0.0)


if __name__ == "__main__":
    unittest.main()
