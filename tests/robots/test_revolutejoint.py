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


class TestDefaultRevoluteJoint(unittest.TestCase):

    def test_defaults(self):
        system = System()
        joint = system.createRevoluteJoint("joint")

        self.assertTrue(joint.getName() == "joint")
        self.assertTrue(joint.getType() == Joint.REVOLUTE)
        self.assertTrue(joint.getParentLink() is None)
        self.assertTrue(joint.getChildLink() is None)
        self.assertTrue(joint.isActuated())

    def test_hasDefaultFrame(self):
        system = System()
        joint = system.createRevoluteJoint("joint")

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
        joint = system.createRevoluteJoint("joint")

        axis = joint.getAxis()

        self.assertTrue(isinstance(axis, RotorGenerator))

        self.assertAlmostEqual(axis.e23(), 0.0)
        self.assertAlmostEqual(axis.e13(), 0.0)
        self.assertAlmostEqual(axis.e12(), 0.0)

    def test_frame(self):
        system = System()
        joint = system.createRevoluteJoint("joint")

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
        joint = system.createRevoluteJoint("joint")

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
        joint = system.createRevoluteJoint("joint")
        link = system.createLink("link1")

        joint.setParentLink(link)
        self.assertTrue(joint.getParentLink().getName() == "link1")

    def test_childLink(self):
        system = System()
        joint = system.createRevoluteJoint("joint")
        link = system.createLink("link1")

        joint.setChildLink(link)
        self.assertTrue(joint.getChildLink().getName() == "link1")

    def test_axis(self):
        system = System()
        joint = system.createRevoluteJoint("joint")

        generator = RotorGenerator([1.0, 2.0, 3.0])
        joint.setAxis(generator)

        axis = joint.getAxis()

        self.assertTrue(isinstance(axis, RotorGenerator))

        self.assertAlmostEqual(axis.e23(), 1.0)
        self.assertAlmostEqual(axis.e13(), 2.0)
        self.assertAlmostEqual(axis.e12(), 3.0)

    def test_getRotor_withDefaultAxis(self):
        system = System()
        joint = system.createRevoluteJoint("joint")

        rotor = joint.getRotor(math.pi / 2.0)

        self.assertTrue(isinstance(rotor, Rotor))

        self.assertAlmostEqual(rotor.scalar(), 0.7071067812)
        self.assertAlmostEqual(rotor.e23(), 0.0)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)
        self.assertAlmostEqual(rotor.angle(), math.pi / 2.0)

    def test_getRotor_withCustomAxis(self):
        system = System()
        joint = system.createRevoluteJoint("joint")

        generator = RotorGenerator([1.0, 0.0, 0.0])
        joint.setAxis(generator)

        rotor = joint.getRotor(math.pi / 2.0)

        self.assertTrue(isinstance(rotor, Rotor))

        self.assertAlmostEqual(rotor.scalar(), 0.7071067812)
        self.assertAlmostEqual(rotor.e23(), -0.7071067812)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)
        self.assertAlmostEqual(rotor.angle(), math.pi / 2.0)

    def test_getMotor_withDefaultAxis(self):
        system = System()
        joint = system.createRevoluteJoint("joint")

        motor = joint.getMotor(math.pi / 2.0)

        self.assertTrue(isinstance(motor, Motor))

        rotor = motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 0.7071067812)
        self.assertAlmostEqual(rotor.e23(), 0.0)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)
        self.assertAlmostEqual(rotor.angle(), math.pi / 2.0)

        translator = motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 0.5)
        self.assertAlmostEqual(translator["e1i"], 0.0)
        self.assertAlmostEqual(translator["e2i"], 0.0)
        self.assertAlmostEqual(translator["e3i"], 0.0)

    def test_getMotor_withCustomAxis(self):
        system = System()
        joint = system.createRevoluteJoint("joint")

        generator = RotorGenerator([1.0, 0.0, 0.0])
        joint.setAxis(generator)

        motor = joint.getMotor(math.pi / 2.0)

        self.assertTrue(isinstance(motor, Motor))

        rotor = motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 0.7071067812)
        self.assertAlmostEqual(rotor.e23(), -0.7071067812)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)
        self.assertAlmostEqual(rotor.angle(), math.pi / 2.0)

        translator = motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], 0.0)
        self.assertAlmostEqual(translator["e2i"], 0.0)
        self.assertAlmostEqual(translator["e3i"], 0.0)

    def test_getMotorDerivative_withDefaultAxisAndFrame(self):
        system = System()
        joint = system.createRevoluteJoint("joint")

        motor = joint.getMotorDerivative(math.pi / 2.0)

        self.assertTrue(isinstance(motor, Motor))

        rotor = motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 0.0)
        self.assertAlmostEqual(rotor.e23(), 0.0)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)
        self.assertAlmostEqual(rotor.angle(), math.pi)

        translator = motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 0.0)
        self.assertAlmostEqual(translator["e1i"], 0.0)
        self.assertAlmostEqual(translator["e2i"], 0.0)
        self.assertAlmostEqual(translator["e3i"], 0.0)

    def test_getMotorDerivative_withCustomAxis(self):
        system = System()
        joint = system.createRevoluteJoint("joint")

        generator = RotorGenerator([1.0, 0.0, 0.0])
        joint.setAxis(generator)

        motor = joint.getMotorDerivative(math.pi / 2.0)

        self.assertTrue(isinstance(motor, Motor))

        rotor = motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), -0.3535533906)
        self.assertAlmostEqual(rotor.e23(), -0.3535533906)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)
        self.assertAlmostEqual(rotor.angle(), 3.8643269014)

        translator = motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 0.25)
        self.assertAlmostEqual(translator["e1i"], 0.0)
        self.assertAlmostEqual(translator["e2i"], 0.0)
        self.assertAlmostEqual(translator["e3i"], 0.0)

    def test_getMotorDerivative_withCustomFrame(self):
        system = System()
        joint = system.createRevoluteJoint("joint")

        translator2 = Translator(TranslatorGenerator([0.0, 0.0, 1.0]))
        rotor2 = Rotor(RotorGenerator([0.0, 0.0, 1.0]), math.pi / 2.0)
        frame = Motor(rotor2, translator2)

        joint.setFrame(frame)

        motor = joint.getMotorDerivative(math.pi / 2.0)

        self.assertTrue(isinstance(motor, Motor))

        rotor = motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 0.0)
        self.assertAlmostEqual(rotor.e23(), 0.0)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)
        self.assertAlmostEqual(rotor.angle(), math.pi)

        translator = motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 0.0)
        self.assertAlmostEqual(translator["e1i"], 0.0)
        self.assertAlmostEqual(translator["e2i"], 0.0)
        self.assertAlmostEqual(translator["e3i"], 0.0)

    def test_getMotorDerivative_withCustomAxisAndFrame(self):
        system = System()
        joint = system.createRevoluteJoint("joint")

        generator = RotorGenerator([1.0, 0.0, 0.0])
        joint.setAxis(generator)

        translator2 = Translator(TranslatorGenerator([0.0, 0.0, 1.0]))
        rotor2 = Rotor(RotorGenerator([0.0, 0.0, 1.0]), math.pi / 2.0)
        frame = Motor(rotor2, translator2)

        joint.setFrame(frame)

        motor = joint.getMotorDerivative(math.pi / 2.0)

        self.assertTrue(isinstance(motor, Motor))

        rotor = motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), -0.25)
        self.assertAlmostEqual(rotor.e23(), -0.25)
        self.assertAlmostEqual(rotor.e13(), 0.25)
        self.assertAlmostEqual(rotor.e12(), 0.25)
        self.assertAlmostEqual(rotor.angle(), 3.6469531639)

        translator = motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 0.25)
        self.assertAlmostEqual(translator["e1i"], 0.0)
        self.assertAlmostEqual(translator["e2i"], 0.0)
        self.assertAlmostEqual(translator["e3i"], -0.125)

    def test_getCurrentAxis_withDefaultAxisAndMotor(self):
        system = System()
        joint = system.createRevoluteJoint("joint")

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
        joint = system.createRevoluteJoint("joint")

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
        joint = system.createRevoluteJoint("joint")

        generator = RotorGenerator([1.0, 0.0, 0.0])
        joint.setAxis(generator)

        motor = Motor()

        axis = joint.getCurrentAxis(motor)

        self.assertTrue(isinstance(axis, MotorGenerator))

        rotorGenerator = axis.getRotorGenerator()

        self.assertAlmostEqual(rotorGenerator.e23(), 1.0)
        self.assertAlmostEqual(rotorGenerator.e13(), 0.0)
        self.assertAlmostEqual(rotorGenerator.e12(), 0.0)

        translatorGenerator = axis.getTranslatorGenerator()

        self.assertAlmostEqual(translatorGenerator.x(), 0.0)
        self.assertAlmostEqual(translatorGenerator.y(), 0.0)
        self.assertAlmostEqual(translatorGenerator.z(), 0.0)

    def test_getCurrentAxis_withCustomAxis(self):
        system = System()
        joint = system.createRevoluteJoint("joint")

        generator = RotorGenerator([1.0, 0.0, 0.0])
        joint.setAxis(generator)

        translator = Translator(TranslatorGenerator([0.0, 0.0, 1.0]))
        rotor = Rotor(RotorGenerator([0.0, 0.0, 1.0]), math.pi / 2.0)
        motor = Motor(rotor, translator)

        axis = joint.getCurrentAxis(motor)

        self.assertTrue(isinstance(axis, MotorGenerator))

        rotorGenerator = axis.getRotorGenerator()

        self.assertAlmostEqual(rotorGenerator.e23(), 0.0)
        self.assertAlmostEqual(rotorGenerator.e13(), -1.0)
        self.assertAlmostEqual(rotorGenerator.e12(), 0.0)

        translatorGenerator = axis.getTranslatorGenerator()

        self.assertAlmostEqual(translatorGenerator.x(), -1.0)
        self.assertAlmostEqual(translatorGenerator.y(), 0.0)
        self.assertAlmostEqual(translatorGenerator.z(), 0.0)


class TestRevoluteJointWith3Parameters(unittest.TestCase):

    def test_defaults(self):
        system = System()
        joint = system.createRevoluteJoint("joint", [1.0, 2.0, math.pi / 2.0])

        self.assertTrue(joint.getName() == "joint")
        self.assertTrue(joint.getType() == Joint.REVOLUTE)
        self.assertTrue(joint.getParentLink() is None)
        self.assertTrue(joint.getChildLink() is None)
        self.assertTrue(joint.isActuated())

    def test_hasDefaultFrame(self):
        system = System()
        joint = system.createRevoluteJoint("joint", [1.0, 2.0, math.pi / 2.0])

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
        self.assertAlmostEqual(translator["e2i"], 1.0)
        self.assertAlmostEqual(translator["e3i"], 0.0)

    def test_hasDefaultAxis(self):
        system = System()
        joint = system.createRevoluteJoint("joint", [1.0, 2.0, math.pi / 2.0])

        axis = joint.getAxis()

        self.assertTrue(isinstance(axis, RotorGenerator))

        self.assertAlmostEqual(axis.e23(), 0.0)
        self.assertAlmostEqual(axis.e13(), 0.0)
        self.assertAlmostEqual(axis.e12(), 1.0)


class TestRevoluteJointWith6ParametersFirstConfiguration(unittest.TestCase):

    def test_defaults(self):
        system = System()
        joint = system.createRevoluteJoint(
            "joint", [1.0, 2.0, 3.0, math.pi / 2.0, 0.0, 0.0], 1
        )

        self.assertTrue(joint.getName() == "joint")
        self.assertTrue(joint.getType() == Joint.REVOLUTE)
        self.assertTrue(joint.getParentLink() is None)
        self.assertTrue(joint.getChildLink() is None)
        self.assertTrue(joint.isActuated())

    def test_hasDefaultFrame(self):
        system = System()
        joint = system.createRevoluteJoint(
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
        joint = system.createRevoluteJoint(
            "joint", [1.0, 2.0, 3.0, math.pi / 2.0, 0.0, 0.0], 1
        )

        axis = joint.getAxis()

        self.assertTrue(isinstance(axis, RotorGenerator))

        self.assertAlmostEqual(axis.e23(), 1.0)
        self.assertAlmostEqual(axis.e13(), 0.0)
        self.assertAlmostEqual(axis.e12(), 0.0)


class TestRevoluteJointWith6ParametersSecondConfiguration(unittest.TestCase):

    def test_hasDefaultFrame(self):
        system = System()
        joint = system.createRevoluteJoint(
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
        joint = system.createRevoluteJoint(
            "joint", [1.0, 2.0, 3.0, 0.0, math.pi / 2.0, 0.0], 2
        )

        axis = joint.getAxis()

        self.assertTrue(isinstance(axis, RotorGenerator))

        self.assertAlmostEqual(axis.e23(), 0.0)
        self.assertAlmostEqual(axis.e13(), 1.0)
        self.assertAlmostEqual(axis.e12(), 0.0)


class TestRevoluteJointWith6ParametersThirdConfiguration(unittest.TestCase):

    def test_hasDefaultFrame(self):
        system = System()
        joint = system.createRevoluteJoint(
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
        joint = system.createRevoluteJoint(
            "joint", [1.0, 2.0, 3.0, 0.0, 0.0, math.pi / 2.0], -3
        )

        axis = joint.getAxis()

        self.assertTrue(isinstance(axis, RotorGenerator))

        self.assertAlmostEqual(axis.e23(), 0.0)
        self.assertAlmostEqual(axis.e13(), 0.0)
        self.assertAlmostEqual(axis.e12(), -1.0)


if __name__ == "__main__":
    unittest.main()
