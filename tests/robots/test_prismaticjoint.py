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

from pygafro import Joint
from pygafro import Motor
from pygafro import MotorGenerator
from pygafro import Rotor
from pygafro import RotorGenerator
from pygafro import System
from pygafro import Translator
from pygafro import TranslatorGenerator


class TestDefaultPrismaticJoint(unittest.TestCase):

    def test_defaults(self):
        system = System()
        joint = system.createPrismaticJoint("joint")

        self.assertTrue(joint.getName() == "joint")
        self.assertTrue(joint.getType() == Joint.PRISMATIC)
        self.assertTrue(joint.getParentLink() is None)
        self.assertTrue(joint.getChildLink() is None)
        self.assertTrue(joint.isActuated())

    def test_hasDefaultFrame(self):
        system = System()
        joint = system.createPrismaticJoint("joint")

        frame = joint.getFrame()

        self.assertTrue(isinstance(frame, Motor))

        rotor = frame.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 1.0)
        self.assertAlmostEqual(rotor.e23(), 0.0)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)

        translator = frame.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], 0.0)
        self.assertAlmostEqual(translator["e2i"], 0.0)
        self.assertAlmostEqual(translator["e3i"], 0.0)

    def test_hasDefaultAxis(self):
        system = System()
        joint = system.createPrismaticJoint("joint")

        axis = joint.getAxis()

        self.assertTrue(isinstance(axis, TranslatorGenerator))

        self.assertAlmostEqual(axis.x(), 0.0)
        self.assertAlmostEqual(axis.y(), 0.0)
        self.assertAlmostEqual(axis.z(), 0.0)

    def test_frame(self):
        system = System()
        joint = system.createPrismaticJoint("joint")

        translator = Translator(TranslatorGenerator([0.0, 0.0, 1.0]))
        rotor = Rotor(RotorGenerator([0.0, 0.0, 1.0]), math.pi / 2.0)
        motor = Motor(rotor, translator)

        joint.setFrame(motor)

        frame = joint.getFrame()

        self.assertTrue(isinstance(frame, Motor))

        rotor2 = frame.getRotor()

        self.assertAlmostEqual(rotor2.scalar(), rotor.scalar())
        self.assertAlmostEqual(rotor2.e23(), rotor.e23())
        self.assertAlmostEqual(rotor2.e13(), rotor.e13())
        self.assertAlmostEqual(rotor2.e12(), rotor.e12())

        translator2 = frame.getTranslator()

        self.assertAlmostEqual(translator2["scalar"], translator["scalar"])
        self.assertAlmostEqual(translator2["e1i"], translator["e1i"])
        self.assertAlmostEqual(translator2["e2i"], translator["e2i"])
        self.assertAlmostEqual(translator2["e3i"], translator["e3i"])

    def test_limits(self):
        system = System()
        joint = system.createPrismaticJoint("joint")

        limits = Joint.Limits()
        limits.positionLower = 1.0
        limits.positionUpper = 2.0
        limits.velocity = 3.0
        limits.torque = 4.0

        joint.setLimits(limits)

        limits2 = joint.getLimits()

        self.assertTrue(isinstance(limits2, Joint.Limits))

        self.assertAlmostEqual(limits.positionLower, 1.0)
        self.assertAlmostEqual(limits.positionUpper, 2.0)
        self.assertAlmostEqual(limits.velocity, 3.0)
        self.assertAlmostEqual(limits.torque, 4.0)

    def test_parentLink(self):
        system = System()
        joint = system.createPrismaticJoint("joint")
        link = system.createLink("link1")

        joint.setParentLink(link)
        self.assertTrue(joint.getParentLink().getName() == "link1")

    def test_childLink(self):
        system = System()
        joint = system.createPrismaticJoint("joint")
        link = system.createLink("link1")

        joint.setChildLink(link)
        self.assertTrue(joint.getChildLink().getName() == "link1")

    def test_axis(self):
        system = System()
        joint = system.createPrismaticJoint("joint")

        generator = TranslatorGenerator([1.0, 2.0, 3.0])
        joint.setAxis(generator)

        axis = joint.getAxis()

        self.assertTrue(isinstance(axis, TranslatorGenerator))

        self.assertAlmostEqual(axis["e1i"], 1.0)
        self.assertAlmostEqual(axis["e2i"], 2.0)
        self.assertAlmostEqual(axis["e3i"], 3.0)

    def test_getTranslator_withDefaultAxis(self):
        system = System()
        joint = system.createPrismaticJoint("joint")

        translator = joint.getTranslator(10.0)

        self.assertTrue(isinstance(translator, Translator))

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], 0.0)
        self.assertAlmostEqual(translator["e2i"], 0.0)
        self.assertAlmostEqual(translator["e3i"], 0.0)

    def test_getTranslator_withCustomAxis(self):
        system = System()
        joint = system.createPrismaticJoint("joint")

        generator = TranslatorGenerator([1.0, 2.0, 3.0])
        joint.setAxis(generator)

        translator = joint.getTranslator(10.0)

        self.assertTrue(isinstance(translator, Translator))

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], -5.0)
        self.assertAlmostEqual(translator["e2i"], -10.0)
        self.assertAlmostEqual(translator["e3i"], -15.0)

    def test_getMotor_withDefaultAxis(self):
        system = System()
        joint = system.createPrismaticJoint("joint")

        motor = joint.getMotor(math.pi / 2.0)

        self.assertTrue(isinstance(motor, Motor))

        rotor = motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 1.0)
        self.assertAlmostEqual(rotor.e23(), 0.0)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)
        self.assertAlmostEqual(rotor.angle(), 0.0)

        translator = motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], 0.0)
        self.assertAlmostEqual(translator["e2i"], 0.0)
        self.assertAlmostEqual(translator["e3i"], 0.0)

    def test_getMotor_withCustomAxis(self):
        system = System()
        joint = system.createPrismaticJoint("joint")

        generator = TranslatorGenerator([1.0, 2.0, 3.0])
        joint.setAxis(generator)

        motor = joint.getMotor(math.pi / 2.0)

        self.assertTrue(isinstance(motor, Motor))

        rotor = motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 1.0)
        self.assertAlmostEqual(rotor.e23(), 0.0)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)
        self.assertAlmostEqual(rotor.angle(), 0.0)

        translator = motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], -math.pi / 4)
        self.assertAlmostEqual(translator["e2i"], -math.pi / 2)
        self.assertAlmostEqual(translator["e3i"], -3 * math.pi / 4)

    def test_getMotorDerivative(self):
        system = System()
        joint = system.createPrismaticJoint("joint")

        self.assertRaises(RuntimeError, joint.getMotorDerivative, math.pi / 2.0)

    def test_getCurrentAxis_withDefaultAxisAndMotor(self):
        system = System()
        joint = system.createPrismaticJoint("joint")

        motor = Motor()

        axis = joint.getCurrentAxis(motor)

        self.assertTrue(isinstance(axis, MotorGenerator))

        rotorGenerator = axis.getRotorGenerator()

        self.assertAlmostEqual(rotorGenerator.e23(), 0.0)
        self.assertAlmostEqual(rotorGenerator.e13(), 0.0)
        self.assertAlmostEqual(rotorGenerator.e12(), 0.0)

        translatorGenerator = axis.getTranslatorGenerator()

        self.assertAlmostEqual(translatorGenerator.x(), 0.0)
        self.assertAlmostEqual(translatorGenerator.y(), 0.0)
        self.assertAlmostEqual(translatorGenerator.z(), 0.0)

    def test_getCurrentAxis_withDefaultAxis(self):
        system = System()
        joint = system.createPrismaticJoint("joint")

        translator = Translator(TranslatorGenerator([0.0, 0.0, 1.0]))
        rotor = Rotor(RotorGenerator([0.0, 0.0, 1.0]), math.pi / 2.0)
        motor = Motor(rotor, translator)

        axis = joint.getCurrentAxis(motor)

        self.assertTrue(isinstance(axis, MotorGenerator))

        rotorGenerator = axis.getRotorGenerator()

        self.assertAlmostEqual(rotorGenerator.e23(), 0.0)
        self.assertAlmostEqual(rotorGenerator.e13(), 0.0)
        self.assertAlmostEqual(rotorGenerator.e12(), 0.0)

        translatorGenerator = axis.getTranslatorGenerator()

        self.assertAlmostEqual(translatorGenerator.x(), 0.0)
        self.assertAlmostEqual(translatorGenerator.y(), 0.0)
        self.assertAlmostEqual(translatorGenerator.z(), 0.0)

    def test_getCurrentAxis_withCustomAxisAndDefaultMotor(self):
        system = System()
        joint = system.createPrismaticJoint("joint")

        generator = TranslatorGenerator([1.0, 2.0, 3.0])
        joint.setAxis(generator)

        motor = Motor()

        axis = joint.getCurrentAxis(motor)

        self.assertTrue(isinstance(axis, MotorGenerator))

        rotorGenerator = axis.getRotorGenerator()

        self.assertAlmostEqual(rotorGenerator.e23(), 0.0)
        self.assertAlmostEqual(rotorGenerator.e13(), 0.0)
        self.assertAlmostEqual(rotorGenerator.e12(), 0.0)

        translatorGenerator = axis.getTranslatorGenerator()

        self.assertAlmostEqual(translatorGenerator.x(), 1.0)
        self.assertAlmostEqual(translatorGenerator.y(), 2.0)
        self.assertAlmostEqual(translatorGenerator.z(), 3.0)

    def test_getCurrentAxis_withCustomAxis(self):
        system = System()
        joint = system.createPrismaticJoint("joint")

        generator = TranslatorGenerator([1.0, 2.0, 3.0])
        joint.setAxis(generator)

        translator = Translator(TranslatorGenerator([0.0, 0.0, 1.0]))
        rotor = Rotor(RotorGenerator([0.0, 0.0, 1.0]), math.pi / 2.0)
        motor = Motor(rotor, translator)

        axis = joint.getCurrentAxis(motor)

        self.assertTrue(isinstance(axis, MotorGenerator))

        rotorGenerator = axis.getRotorGenerator()

        self.assertAlmostEqual(rotorGenerator.e23(), 0.0)
        self.assertAlmostEqual(rotorGenerator.e13(), 0.0)
        self.assertAlmostEqual(rotorGenerator.e12(), 0.0)

        translatorGenerator = axis.getTranslatorGenerator()

        self.assertAlmostEqual(translatorGenerator.x(), -2.0)
        self.assertAlmostEqual(translatorGenerator.y(), 1.0)
        self.assertAlmostEqual(translatorGenerator.z(), 3.0)


class TestPrismaticJointWith6ParametersFirstConfiguration(unittest.TestCase):

    def test_defaults(self):
        system = System()
        joint = system.createPrismaticJoint(
            "joint", [1.0, 2.0, 3.0, math.pi / 2.0, 0.0, 0.0], 1
        )

        self.assertTrue(joint.getName() == "joint")
        self.assertTrue(joint.getType() == Joint.PRISMATIC)
        self.assertTrue(joint.getParentLink() is None)
        self.assertTrue(joint.getChildLink() is None)
        self.assertTrue(joint.isActuated())

    def test_hasDefaultFrame(self):
        system = System()
        joint = system.createPrismaticJoint(
            "joint", [1.0, 2.0, 3.0, math.pi / 2.0, 0.0, 0.0], 1
        )

        frame = joint.getFrame()

        self.assertTrue(isinstance(frame, Motor))

        rotor = frame.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 0.7071067812)
        self.assertAlmostEqual(rotor.e23(), -0.7071067812)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)
        self.assertAlmostEqual(rotor.angle(), math.pi / 2.0)

        translator = frame.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], -0.5)
        self.assertAlmostEqual(translator["e2i"], -1.0)
        self.assertAlmostEqual(translator["e3i"], -1.5)

    def test_hasDefaultAxis(self):
        system = System()
        joint = system.createPrismaticJoint(
            "joint", [1.0, 2.0, 3.0, math.pi / 2.0, 0.0, 0.0], 1
        )

        axis = joint.getAxis()

        self.assertTrue(isinstance(axis, TranslatorGenerator))

        self.assertAlmostEqual(axis.x(), 1.0)
        self.assertAlmostEqual(axis.y(), 0.0)
        self.assertAlmostEqual(axis.z(), 0.0)


class TestPrismaticJointWith6ParametersSecondConfiguration(unittest.TestCase):

    def test_hasDefaultFrame(self):
        system = System()
        joint = system.createPrismaticJoint(
            "joint", [1.0, 2.0, 3.0, 0.0, math.pi / 2.0, 0.0], 2
        )

        frame = joint.getFrame()

        self.assertTrue(isinstance(frame, Motor))

        rotor = frame.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 0.7071067812)
        self.assertAlmostEqual(rotor.e23(), 0.0)
        self.assertAlmostEqual(rotor.e13(), -0.7071067812)
        self.assertAlmostEqual(rotor.e12(), 0.0)
        self.assertAlmostEqual(rotor.angle(), math.pi / 2.0)

        translator = frame.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], -0.5)
        self.assertAlmostEqual(translator["e2i"], -1.0)
        self.assertAlmostEqual(translator["e3i"], -1.5)

    def test_hasDefaultAxis(self):
        system = System()
        joint = system.createPrismaticJoint(
            "joint", [1.0, 2.0, 3.0, 0.0, math.pi / 2.0, 0.0], 2
        )

        axis = joint.getAxis()

        self.assertTrue(isinstance(axis, TranslatorGenerator))

        self.assertAlmostEqual(axis.x(), 0.0)
        self.assertAlmostEqual(axis.y(), 1.0)
        self.assertAlmostEqual(axis.z(), 0.0)


class TestPrismaticJointWith6ParametersThirdConfiguration(unittest.TestCase):

    def test_hasDefaultFrame(self):
        system = System()
        joint = system.createPrismaticJoint(
            "joint", [1.0, 2.0, 3.0, 0.0, 0.0, math.pi / 2.0], -3
        )

        frame = joint.getFrame()

        self.assertTrue(isinstance(frame, Motor))

        rotor = frame.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 0.7071067812)
        self.assertAlmostEqual(rotor.e23(), 0.0)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), -0.7071067812)
        self.assertAlmostEqual(rotor.angle(), math.pi / 2.0)

        translator = frame.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], -0.5)
        self.assertAlmostEqual(translator["e2i"], -1.0)
        self.assertAlmostEqual(translator["e3i"], -1.5)

    def test_hasDefaultAxis(self):
        system = System()
        joint = system.createPrismaticJoint(
            "joint", [1.0, 2.0, 3.0, 0.0, 0.0, math.pi / 2.0], -3
        )

        axis = joint.getAxis()

        self.assertTrue(isinstance(axis, TranslatorGenerator))

        self.assertAlmostEqual(axis.x(), 0.0)
        self.assertAlmostEqual(axis.y(), 0.0)
        self.assertAlmostEqual(axis.z(), -1.0)


if __name__ == "__main__":
    unittest.main()
