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


class TestDefaultFixedJoint(unittest.TestCase):

    def test_defaults(self):
        system = System()
        joint = system.createFixedJoint("joint")

        self.assertTrue(joint.getName() == "joint")
        self.assertTrue(joint.getType() == Joint.FIXED)
        self.assertTrue(joint.getParentLink() is None)
        self.assertTrue(joint.getChildLink() is None)
        self.assertFalse(joint.isActuated())

    def test_hasDefaultFrame(self):
        system = System()
        joint = system.createFixedJoint("joint")

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

    def test_frame(self):
        system = System()
        joint = system.createFixedJoint("joint")

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
        joint = system.createFixedJoint("joint")

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
        joint = system.createFixedJoint("joint")
        link = system.createLink("link1")

        joint.setParentLink(link)
        self.assertTrue(joint.getParentLink().getName() == "link1")

    def test_childLink(self):
        system = System()
        joint = system.createFixedJoint("joint")
        link = system.createLink("link1")

        joint.setChildLink(link)
        self.assertTrue(joint.getChildLink().getName() == "link1")

    def test_getMotor(self):
        system = System()
        joint = system.createFixedJoint("joint")

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

    def test_getMotorDerivative_withDefaultFrame(self):
        system = System()
        joint = system.createFixedJoint("joint")

        motor = joint.getMotorDerivative(math.pi / 2.0)

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

    def test_getMotorDerivative_withCustomFrame(self):
        system = System()
        joint = system.createFixedJoint("joint")

        translator2 = Translator(TranslatorGenerator([0.0, 0.0, 1.0]))
        rotor2 = Rotor(RotorGenerator([0.0, 0.0, 1.0]), math.pi / 2.0)
        frame = Motor(rotor2, translator2)

        joint.setFrame(frame)

        motor = joint.getMotorDerivative(math.pi / 2.0)

        self.assertTrue(isinstance(motor, Motor))

        rotor = motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 0.7071067812)
        self.assertAlmostEqual(rotor.e23(), 0.0)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), -0.7071067812)
        self.assertAlmostEqual(rotor.angle(), math.pi / 2.0)

        translator = motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], 0.0)
        self.assertAlmostEqual(translator["e2i"], 0.0)
        self.assertAlmostEqual(translator["e3i"], -0.5)

    def test_getCurrentAxis_withDefaultMotor(self):
        system = System()
        joint = system.createFixedJoint("joint")

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

    def test_getCurrentAxis_withCustomMotor(self):
        system = System()
        joint = system.createFixedJoint("joint")

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


if __name__ == "__main__":
    unittest.main()
