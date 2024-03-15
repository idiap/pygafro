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
from pygafro import Multivector
from pygafro import Rotor
from pygafro import RotorGenerator
from pygafro import Translator
from pygafro import TranslatorGenerator
from pygafro import Twist
from pygafro import Wrench


class TestDefaultTwist(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.twist = Twist()

    def test_blades(self):
        self.assertAlmostEqual(self.twist["e23"], 0.0)
        self.assertAlmostEqual(self.twist["e13"], 0.0)
        self.assertAlmostEqual(self.twist["e12"], 0.0)
        self.assertAlmostEqual(self.twist["e1i"], 0.0)
        self.assertAlmostEqual(self.twist["e2i"], 0.0)
        self.assertAlmostEqual(self.twist["e3i"], 0.0)

    def test_getMultivector(self):
        mv = self.twist.multivector()

        self.assertTrue(mv.size() == self.twist.size())

        self.assertAlmostEqual(mv["e23"], 0.0)
        self.assertAlmostEqual(mv["e13"], 0.0)
        self.assertAlmostEqual(mv["e12"], 0.0)
        self.assertAlmostEqual(mv["e1i"], 0.0)
        self.assertAlmostEqual(mv["e2i"], 0.0)
        self.assertAlmostEqual(mv["e3i"], 0.0)

    def test_getAngular(self):
        angular = self.twist.getAngular()

        self.assertTrue(angular.size() == 3)

        self.assertAlmostEqual(angular["e23"], 0.0)
        self.assertAlmostEqual(angular["e13"], 0.0)
        self.assertAlmostEqual(angular["e12"], 0.0)

    def test_getLinear(self):
        linear = self.twist.getLinear()

        self.assertTrue(linear.size() == 3)

        self.assertAlmostEqual(linear["e1i"], 0.0)
        self.assertAlmostEqual(linear["e2i"], 0.0)
        self.assertAlmostEqual(linear["e3i"], 0.0)


class TestTwistCreationFromParameters(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.twist = Twist([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])

    def test_blades(self):
        self.assertAlmostEqual(self.twist["e23"], 1.0)
        self.assertAlmostEqual(self.twist["e13"], 2.0)
        self.assertAlmostEqual(self.twist["e12"], 3.0)
        self.assertAlmostEqual(self.twist["e1i"], 4.0)
        self.assertAlmostEqual(self.twist["e2i"], 5.0)
        self.assertAlmostEqual(self.twist["e3i"], 6.0)

    def test_getMultivector(self):
        mv = self.twist.multivector()

        self.assertTrue(mv.size() == self.twist.size())

        self.assertAlmostEqual(mv["e23"], 1.0)
        self.assertAlmostEqual(mv["e13"], 2.0)
        self.assertAlmostEqual(mv["e12"], 3.0)
        self.assertAlmostEqual(mv["e1i"], 4.0)
        self.assertAlmostEqual(mv["e2i"], 5.0)
        self.assertAlmostEqual(mv["e3i"], 6.0)

    def test_getAngular(self):
        angular = self.twist.getAngular()

        self.assertTrue(angular.size() == 3)

        self.assertAlmostEqual(angular["e23"], 1.0)
        self.assertAlmostEqual(angular["e13"], 2.0)
        self.assertAlmostEqual(angular["e12"], 3.0)

    def test_getLinear(self):
        linear = self.twist.getLinear()

        self.assertTrue(linear.size() == 3)

        self.assertAlmostEqual(linear["e1i"], 4.0)
        self.assertAlmostEqual(linear["e2i"], 5.0)
        self.assertAlmostEqual(linear["e3i"], 6.0)


class TestTwistCreationFromTwist(unittest.TestCase):

    def test_creation(self):
        twist1 = Twist([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        twist2 = Twist(twist1)

        self.assertAlmostEqual(twist2["e23"], 1.0)
        self.assertAlmostEqual(twist2["e13"], 2.0)
        self.assertAlmostEqual(twist2["e12"], 3.0)
        self.assertAlmostEqual(twist2["e1i"], 4.0)
        self.assertAlmostEqual(twist2["e2i"], 5.0)
        self.assertAlmostEqual(twist2["e3i"], 6.0)


class TestTwistCreationFromMultivector(unittest.TestCase):

    def test_creation(self):
        mv = Multivector.create(
            ["e23", "e13", "e12", "e1i", "e2i", "e3i"], [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        )
        twist = Twist(mv)

        self.assertAlmostEqual(twist["e23"], 1.0)
        self.assertAlmostEqual(twist["e13"], 2.0)
        self.assertAlmostEqual(twist["e12"], 3.0)
        self.assertAlmostEqual(twist["e1i"], 4.0)
        self.assertAlmostEqual(twist["e2i"], 5.0)
        self.assertAlmostEqual(twist["e3i"], 6.0)


class TestTwistTransformByMotor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.twist = Twist([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])

    def test_default(self):
        motor = Motor()

        twist = self.twist.transform(motor)

        self.assertTrue(isinstance(twist, Twist))

        self.assertAlmostEqual(twist["e23"], 1.0)
        self.assertAlmostEqual(twist["e13"], 2.0)
        self.assertAlmostEqual(twist["e12"], 3.0)
        self.assertAlmostEqual(twist["e1i"], 4.0)
        self.assertAlmostEqual(twist["e2i"], 5.0)
        self.assertAlmostEqual(twist["e3i"], 6.0)

    def test_withTranslation(self):
        translator = Translator(TranslatorGenerator([0.0, 0.0, 1.0]))
        motor = Motor(translator)

        twist = self.twist.transform(motor)

        self.assertTrue(isinstance(twist, Twist))

        self.assertAlmostEqual(twist["e23"], 1.0)
        self.assertAlmostEqual(twist["e13"], 2.0)
        self.assertAlmostEqual(twist["e12"], 3.0)
        self.assertAlmostEqual(twist["e1i"], 6.0)
        self.assertAlmostEqual(twist["e2i"], 6.0)
        self.assertAlmostEqual(twist["e3i"], 6.0)

    def test_withRotation(self):
        rotor = Rotor(RotorGenerator([0.0, 0.0, 1.0]), math.pi / 2.0)
        motor = Motor(rotor)

        twist = self.twist.transform(motor)

        self.assertTrue(isinstance(twist, Twist))

        self.assertAlmostEqual(twist["e23"], 2.0)
        self.assertAlmostEqual(twist["e13"], -1.0)
        self.assertAlmostEqual(twist["e12"], 3.0)
        self.assertAlmostEqual(twist["e1i"], -5.0)
        self.assertAlmostEqual(twist["e2i"], 4.0)
        self.assertAlmostEqual(twist["e3i"], 6.0)

    def test_withTranslationAndRotation(self):
        translator = Translator(TranslatorGenerator([0.0, 0.0, 1.0]))
        rotor = Rotor(RotorGenerator([0.0, 0.0, 1.0]), math.pi / 2.0)
        motor = Motor(translator, rotor)

        twist = self.twist.transform(motor)

        self.assertTrue(isinstance(twist, Twist))

        self.assertAlmostEqual(twist["e23"], 2.0)
        self.assertAlmostEqual(twist["e13"], -1.0)
        self.assertAlmostEqual(twist["e12"], 3.0)
        self.assertAlmostEqual(twist["e1i"], -6.0)
        self.assertAlmostEqual(twist["e2i"], 6.0)
        self.assertAlmostEqual(twist["e3i"], 6.0)


class TestTwistOperations(unittest.TestCase):

    def test_addition(self):
        twist = Twist([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        twist2 = Twist([10.0, 20.0, 30.0, 40.0, 50.0, 60.0])

        twist += twist2

        self.assertAlmostEqual(twist["e23"], 11.0)
        self.assertAlmostEqual(twist["e13"], 22.0)
        self.assertAlmostEqual(twist["e12"], 33.0)
        self.assertAlmostEqual(twist["e1i"], 44.0)
        self.assertAlmostEqual(twist["e2i"], 55.0)
        self.assertAlmostEqual(twist["e3i"], 66.0)

    def test_commutation(self):
        twist = Twist([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        wrench = Wrench([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])

        wrench2 = twist.commute(wrench)

        self.assertAlmostEqual(wrench2["e23"], 0.0)
        self.assertAlmostEqual(wrench2["e13"], 0.0)
        self.assertAlmostEqual(wrench2["e12"], 0.0)
        self.assertAlmostEqual(wrench2["e01"], 27.0)
        self.assertAlmostEqual(wrench2["e02"], -6.0)
        self.assertAlmostEqual(wrench2["e03"], -13.0)


if __name__ == "__main__":
    unittest.main()
