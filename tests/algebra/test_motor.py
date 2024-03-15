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

from pygafro import Line
from pygafro import Motor
from pygafro import MotorGenerator
from pygafro import Multivector
from pygafro import Plane
from pygafro import Point
from pygafro import Rotor
from pygafro import RotorGenerator
from pygafro import Sphere
from pygafro import Translator
from pygafro import TranslatorGenerator


class TestDefaultMotor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.motor = Motor()

    def test_rotor(self):
        rotor = self.motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 1.0)
        self.assertAlmostEqual(rotor.e23(), 0.0)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)

    def test_translator(self):
        translator = self.motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], 0.0)
        self.assertAlmostEqual(translator["e2i"], 0.0)
        self.assertAlmostEqual(translator["e3i"], 0.0)

    def test_log(self):
        log = self.motor.log()

        self.assertAlmostEqual(log.get_e23(), 0.0)
        self.assertAlmostEqual(log.get_e13(), 0.0)
        self.assertAlmostEqual(log.get_e12(), 0.0)
        self.assertAlmostEqual(log.get_e1i(), 0.0)
        self.assertAlmostEqual(log.get_e2i(), 0.0)
        self.assertAlmostEqual(log.get_e3i(), 0.0)

    def test_logJacobian(self):
        jacobian = self.motor.logJacobian()

        self.assertTrue(isinstance(jacobian, np.ndarray))
        self.assertEqual(jacobian.shape, (6, 8))

        self.assertAlmostEqual(jacobian[0, 0], 0.0)
        self.assertAlmostEqual(jacobian[0, 1], 0.0)
        self.assertAlmostEqual(jacobian[0, 2], 0.0)
        self.assertAlmostEqual(jacobian[0, 3], 0.0)
        self.assertAlmostEqual(jacobian[0, 4], 0.0)
        self.assertAlmostEqual(jacobian[0, 5], 0.0)
        self.assertAlmostEqual(jacobian[0, 6], 0.0)
        self.assertAlmostEqual(jacobian[0, 7], 0.0)

        self.assertAlmostEqual(jacobian[1, 0], 0.0)
        self.assertAlmostEqual(jacobian[1, 1], 0.0)
        self.assertAlmostEqual(jacobian[1, 2], 0.0)
        self.assertAlmostEqual(jacobian[1, 3], 0.0)
        self.assertAlmostEqual(jacobian[1, 4], 0.0)
        self.assertAlmostEqual(jacobian[1, 5], 0.0)
        self.assertAlmostEqual(jacobian[1, 6], 0.0)
        self.assertAlmostEqual(jacobian[1, 7], 0.0)

        self.assertAlmostEqual(jacobian[2, 0], 0.0)
        self.assertAlmostEqual(jacobian[2, 1], 0.0)
        self.assertAlmostEqual(jacobian[2, 2], 0.0)
        self.assertAlmostEqual(jacobian[2, 3], 0.0)
        self.assertAlmostEqual(jacobian[2, 4], 0.0)
        self.assertAlmostEqual(jacobian[2, 5], 0.0)
        self.assertAlmostEqual(jacobian[2, 6], 0.0)
        self.assertAlmostEqual(jacobian[2, 7], 0.0)

        self.assertAlmostEqual(jacobian[3, 0], 0.0)
        self.assertAlmostEqual(jacobian[3, 1], 0.0)
        self.assertAlmostEqual(jacobian[3, 2], 0.0)
        self.assertAlmostEqual(jacobian[3, 3], 0.0)
        self.assertAlmostEqual(jacobian[3, 4], -2.0)
        self.assertAlmostEqual(jacobian[3, 5], 0.0)
        self.assertAlmostEqual(jacobian[3, 6], 0.0)
        self.assertAlmostEqual(jacobian[3, 7], 0.0)

        self.assertAlmostEqual(jacobian[4, 0], 0.0)
        self.assertAlmostEqual(jacobian[4, 1], 0.0)
        self.assertAlmostEqual(jacobian[4, 2], 0.0)
        self.assertAlmostEqual(jacobian[4, 3], 0.0)
        self.assertAlmostEqual(jacobian[4, 4], 0.0)
        self.assertAlmostEqual(jacobian[4, 5], -2.0)
        self.assertAlmostEqual(jacobian[4, 6], 0.0)
        self.assertAlmostEqual(jacobian[4, 7], 0.0)

        self.assertAlmostEqual(jacobian[5, 0], 0.0)
        self.assertAlmostEqual(jacobian[5, 1], 0.0)
        self.assertAlmostEqual(jacobian[5, 2], 0.0)
        self.assertAlmostEqual(jacobian[5, 3], 0.0)
        self.assertAlmostEqual(jacobian[5, 4], 0.0)
        self.assertAlmostEqual(jacobian[5, 5], 0.0)
        self.assertAlmostEqual(jacobian[5, 6], -2.0)
        self.assertAlmostEqual(jacobian[5, 7], 0.0)

    def test_applyToPoint_origin(self):
        point = Point()
        result = self.motor.apply(point)

        self.assertTrue(isinstance(result, Point))

        self.assertAlmostEqual(result["e0"], point["e0"])
        self.assertAlmostEqual(result["e1"], point["e1"])
        self.assertAlmostEqual(result["e2"], point["e2"])
        self.assertAlmostEqual(result["e3"], point["e3"])
        self.assertAlmostEqual(result["ei"], point["ei"])

    def test_applyToPoint_other(self):
        point = Point(1.0, 2.0, 3.0)
        result = self.motor.apply(point)

        self.assertTrue(isinstance(result, Point))

        self.assertAlmostEqual(result["e0"], point["e0"])
        self.assertAlmostEqual(result["e1"], point["e1"])
        self.assertAlmostEqual(result["e2"], point["e2"])
        self.assertAlmostEqual(result["e3"], point["e3"])
        self.assertAlmostEqual(result["ei"], point["ei"])

    def test_applyToLine(self):
        p1 = Point()
        p2 = Point(1.0, 0.0, 0.0)
        line = Line(p1, p2)

        result = self.motor.apply(line)

        self.assertTrue(isinstance(result, Line))

        self.assertAlmostEqual(result["e12i"], line["e12i"])
        self.assertAlmostEqual(result["e13i"], line["e13i"])
        self.assertAlmostEqual(result["e23i"], line["e23i"])
        self.assertAlmostEqual(result["e01i"], line["e01i"])
        self.assertAlmostEqual(result["e02i"], line["e02i"])
        self.assertAlmostEqual(result["e03i"], line["e03i"])

    def test_applyToPlane(self):
        p1 = Point(0.0, 0.0, 0.0)
        p2 = Point(1.0, 0.0, 0.0)
        p3 = Point(0.0, 1.0, 0.0)
        plane = Plane(p1, p2, p3)

        result = self.motor.apply(plane)

        self.assertTrue(isinstance(result, Plane))

        self.assertAlmostEqual(result["e123i"], plane["e123i"])
        self.assertAlmostEqual(result["e012i"], plane["e012i"])
        self.assertAlmostEqual(result["e023i"], plane["e023i"])
        self.assertAlmostEqual(result["e013i"], plane["e013i"])

    def test_applyToSphere(self):
        center = Point(1.0, 0.0, 0.0)
        sphere = Sphere(center, 0.5)

        result = self.motor.apply(sphere)

        self.assertTrue(isinstance(result, Sphere))

        resultCenter = result.getCenter()

        self.assertTrue(isinstance(resultCenter, Point))

        self.assertAlmostEqual(resultCenter["e0"], center["e0"])
        self.assertAlmostEqual(resultCenter["e1"], center["e1"])
        self.assertAlmostEqual(resultCenter["e2"], center["e2"])
        self.assertAlmostEqual(resultCenter["e3"], center["e3"])
        self.assertAlmostEqual(resultCenter["ei"], center["ei"])

        self.assertAlmostEqual(result.getRadius(), sphere.getRadius())


class TestMotorWithTranslation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.translator = Translator(TranslatorGenerator([0.0, 0.0, 1.0]))
        cls.motor = Motor(cls.translator)

    def test_rotor(self):
        rotor = self.motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 1.0)
        self.assertAlmostEqual(rotor.e23(), 0.0)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)

    def test_translator(self):
        translator = self.motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], self.translator["scalar"])
        self.assertAlmostEqual(translator["e1i"], self.translator["e1i"])
        self.assertAlmostEqual(translator["e2i"], self.translator["e2i"])
        self.assertAlmostEqual(translator["e3i"], self.translator["e3i"])

    def test_log(self):
        log = self.motor.log()

        self.assertAlmostEqual(log.get_e23(), 0.0)
        self.assertAlmostEqual(log.get_e13(), 0.0)
        self.assertAlmostEqual(log.get_e12(), 0.0)
        self.assertAlmostEqual(log.get_e1i(), 0.0)
        self.assertAlmostEqual(log.get_e2i(), 0.0)
        self.assertAlmostEqual(log.get_e3i(), 1.0)

    def test_logJacobian(self):
        jacobian = self.motor.logJacobian()

        self.assertTrue(isinstance(jacobian, np.ndarray))
        self.assertEqual(jacobian.shape, (6, 8))

        self.assertAlmostEqual(jacobian[0, 0], 0.0)
        self.assertAlmostEqual(jacobian[0, 1], 0.0)
        self.assertAlmostEqual(jacobian[0, 2], 0.0)
        self.assertAlmostEqual(jacobian[0, 3], 0.0)
        self.assertAlmostEqual(jacobian[0, 4], 0.0)
        self.assertAlmostEqual(jacobian[0, 5], 0.0)
        self.assertAlmostEqual(jacobian[0, 6], 0.0)
        self.assertAlmostEqual(jacobian[0, 7], 0.0)

        self.assertAlmostEqual(jacobian[1, 0], 0.0)
        self.assertAlmostEqual(jacobian[1, 1], 0.0)
        self.assertAlmostEqual(jacobian[1, 2], 0.0)
        self.assertAlmostEqual(jacobian[1, 3], 0.0)
        self.assertAlmostEqual(jacobian[1, 4], 0.0)
        self.assertAlmostEqual(jacobian[1, 5], 0.0)
        self.assertAlmostEqual(jacobian[1, 6], 0.0)
        self.assertAlmostEqual(jacobian[1, 7], 0.0)

        self.assertAlmostEqual(jacobian[2, 0], 0.0)
        self.assertAlmostEqual(jacobian[2, 1], 0.0)
        self.assertAlmostEqual(jacobian[2, 2], 0.0)
        self.assertAlmostEqual(jacobian[2, 3], 0.0)
        self.assertAlmostEqual(jacobian[2, 4], 0.0)
        self.assertAlmostEqual(jacobian[2, 5], 0.0)
        self.assertAlmostEqual(jacobian[2, 6], 0.0)
        self.assertAlmostEqual(jacobian[2, 7], 0.0)

        self.assertAlmostEqual(jacobian[3, 0], 0.0)
        self.assertAlmostEqual(jacobian[3, 1], 0.0)
        self.assertAlmostEqual(jacobian[3, 2], 1.0)
        self.assertAlmostEqual(jacobian[3, 3], 0.0)
        self.assertAlmostEqual(jacobian[3, 4], -2.0)
        self.assertAlmostEqual(jacobian[3, 5], 0.0)
        self.assertAlmostEqual(jacobian[3, 6], 0.0)
        self.assertAlmostEqual(jacobian[3, 7], 0.0)

        self.assertAlmostEqual(jacobian[4, 0], 0.0)
        self.assertAlmostEqual(jacobian[4, 1], 1.0)
        self.assertAlmostEqual(jacobian[4, 2], 0.0)
        self.assertAlmostEqual(jacobian[4, 3], 0.0)
        self.assertAlmostEqual(jacobian[4, 4], 0.0)
        self.assertAlmostEqual(jacobian[4, 5], -2.0)
        self.assertAlmostEqual(jacobian[4, 6], 0.0)
        self.assertAlmostEqual(jacobian[4, 7], 0.0)

        self.assertAlmostEqual(jacobian[5, 0], 1.0)
        self.assertAlmostEqual(jacobian[5, 1], 0.0)
        self.assertAlmostEqual(jacobian[5, 2], 0.0)
        self.assertAlmostEqual(jacobian[5, 3], 0.0)
        self.assertAlmostEqual(jacobian[5, 4], 0.0)
        self.assertAlmostEqual(jacobian[5, 5], 0.0)
        self.assertAlmostEqual(jacobian[5, 6], -2.0)
        self.assertAlmostEqual(jacobian[5, 7], 0.0)

    def test_applyToPoint_origin(self):
        point = Point()
        result = self.motor.apply(point)

        self.assertTrue(isinstance(result, Point))

        self.assertAlmostEqual(result["e0"], 1.0)
        self.assertAlmostEqual(result["e1"], 0.0)
        self.assertAlmostEqual(result["e2"], 0.0)
        self.assertAlmostEqual(result["e3"], 1.0)
        self.assertAlmostEqual(result["ei"], 0.5)

    def test_applyToPoint_other(self):
        point = Point(1.0, 2.0, 3.0)
        result = self.motor.apply(point)

        self.assertTrue(isinstance(result, Point))

        self.assertAlmostEqual(result["e0"], 1.0)
        self.assertAlmostEqual(result["e1"], 1.0)
        self.assertAlmostEqual(result["e2"], 2.0)
        self.assertAlmostEqual(result["e3"], 4.0)
        self.assertAlmostEqual(result["ei"], 10.5)

    def test_applyToLine(self):
        p1 = Point()
        p2 = Point(1.0, 0.0, 0.0)
        line = Line(p1, p2)

        result = self.motor.apply(line)

        self.assertTrue(isinstance(result, Line))

        self.assertAlmostEqual(result["e12i"], line["e12i"])
        self.assertAlmostEqual(result["e13i"], -1.0)
        self.assertAlmostEqual(result["e23i"], line["e23i"])
        self.assertAlmostEqual(result["e01i"], line["e01i"])
        self.assertAlmostEqual(result["e02i"], line["e02i"])
        self.assertAlmostEqual(result["e03i"], line["e03i"])

    def test_applyToPlane(self):
        p1 = Point(0.0, 0.0, 0.0)
        p2 = Point(1.0, 0.0, 0.0)
        p3 = Point(0.0, 1.0, 0.0)
        plane = Plane(p1, p2, p3)

        result = self.motor.apply(plane)

        self.assertTrue(isinstance(result, Plane))

        self.assertAlmostEqual(result["e123i"], 1.0)
        self.assertAlmostEqual(result["e012i"], plane["e012i"])
        self.assertAlmostEqual(result["e023i"], plane["e023i"])
        self.assertAlmostEqual(result["e013i"], plane["e013i"])

    def test_applyToSphere(self):
        center = Point(1.0, 0.0, 0.0)
        sphere = Sphere(center, 0.5)

        result = self.motor.apply(sphere)

        self.assertTrue(isinstance(result, Sphere))

        resultCenter = result.getCenter()

        self.assertTrue(isinstance(resultCenter, Point))

        self.assertAlmostEqual(resultCenter["e0"], center["e0"])
        self.assertAlmostEqual(resultCenter["e1"], center["e1"])
        self.assertAlmostEqual(resultCenter["e2"], center["e2"])
        self.assertAlmostEqual(resultCenter["e3"], 1.0)
        self.assertAlmostEqual(resultCenter["ei"], 1.0)

        self.assertAlmostEqual(result.getRadius(), sphere.getRadius())


class TestMotorWithRotation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rotor = Rotor(RotorGenerator([0.0, 0.0, 1.0]), math.pi / 2.0)
        cls.motor = Motor(cls.rotor)

    def test_rotor(self):
        rotor = self.motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), self.rotor.scalar())
        self.assertAlmostEqual(rotor.e23(), self.rotor.e23())
        self.assertAlmostEqual(rotor.e13(), self.rotor.e13())
        self.assertAlmostEqual(rotor.e12(), self.rotor.e12())

    def test_translator(self):
        translator = self.motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], 0.0)
        self.assertAlmostEqual(translator["e2i"], 0.0)
        self.assertAlmostEqual(translator["e3i"], 0.0)

    def test_log(self):
        log = self.motor.log()

        self.assertAlmostEqual(log.get_e23(), 0.0)
        self.assertAlmostEqual(log.get_e13(), 0.0)
        self.assertAlmostEqual(log.get_e12(), 1.5707963266)
        self.assertAlmostEqual(log.get_e1i(), 0.0)
        self.assertAlmostEqual(log.get_e2i(), 0.0)
        self.assertAlmostEqual(log.get_e3i(), 0.0)

    def test_logJacobian(self):
        jacobian = self.motor.logJacobian()

        self.assertTrue(isinstance(jacobian, np.ndarray))
        self.assertEqual(jacobian.shape, (6, 8))

        self.assertAlmostEqual(jacobian[0, 0], 0.0)
        self.assertAlmostEqual(jacobian[0, 1], -2.22144, places=5)
        self.assertAlmostEqual(jacobian[0, 2], 0.0)
        self.assertAlmostEqual(jacobian[0, 3], 0.0)
        self.assertAlmostEqual(jacobian[0, 4], 0.0)
        self.assertAlmostEqual(jacobian[0, 5], 0.0)
        self.assertAlmostEqual(jacobian[0, 6], 0.0)
        self.assertAlmostEqual(jacobian[0, 7], 0.0)

        self.assertAlmostEqual(jacobian[1, 0], 0.0)
        self.assertAlmostEqual(jacobian[1, 1], 0.0)
        self.assertAlmostEqual(jacobian[1, 2], -2.22144, places=5)
        self.assertAlmostEqual(jacobian[1, 3], 0.0)
        self.assertAlmostEqual(jacobian[1, 4], 0.0)
        self.assertAlmostEqual(jacobian[1, 5], 0.0)
        self.assertAlmostEqual(jacobian[1, 6], 0.0)
        self.assertAlmostEqual(jacobian[1, 7], 0.0)

        self.assertAlmostEqual(jacobian[2, 0], -0.606986, places=5)
        self.assertAlmostEqual(jacobian[2, 1], 0.0)
        self.assertAlmostEqual(jacobian[2, 2], 0.0)
        self.assertAlmostEqual(jacobian[2, 3], -2.22144, places=5)
        self.assertAlmostEqual(jacobian[2, 4], 0.0)
        self.assertAlmostEqual(jacobian[2, 5], 0.0)
        self.assertAlmostEqual(jacobian[2, 6], 0.0)
        self.assertAlmostEqual(jacobian[2, 7], 0.0)

        self.assertAlmostEqual(jacobian[3, 0], 0.0)
        self.assertAlmostEqual(jacobian[3, 1], 0.0)
        self.assertAlmostEqual(jacobian[3, 2], 0.0)
        self.assertAlmostEqual(jacobian[3, 3], 0.0)
        self.assertAlmostEqual(jacobian[3, 4], -1.41421, places=5)
        self.assertAlmostEqual(jacobian[3, 5], 1.41421, places=5)
        self.assertAlmostEqual(jacobian[3, 6], 0.0)
        self.assertAlmostEqual(jacobian[3, 7], 0.0)

        self.assertAlmostEqual(jacobian[4, 0], 0.0)
        self.assertAlmostEqual(jacobian[4, 1], 0.0)
        self.assertAlmostEqual(jacobian[4, 2], 0.0)
        self.assertAlmostEqual(jacobian[4, 3], 0.0)
        self.assertAlmostEqual(jacobian[4, 4], -1.41421, places=5)
        self.assertAlmostEqual(jacobian[4, 5], -1.41421, places=5)
        self.assertAlmostEqual(jacobian[4, 6], 0.0)
        self.assertAlmostEqual(jacobian[4, 7], 0.0)

        self.assertAlmostEqual(jacobian[5, 0], 0.0)
        self.assertAlmostEqual(jacobian[5, 1], 0.0)
        self.assertAlmostEqual(jacobian[5, 2], 0.0)
        self.assertAlmostEqual(jacobian[5, 3], 0.0)
        self.assertAlmostEqual(jacobian[5, 4], 0.0)
        self.assertAlmostEqual(jacobian[5, 5], 0.0)
        self.assertAlmostEqual(jacobian[5, 6], -1.41421, places=5)
        self.assertAlmostEqual(jacobian[5, 7], 1.41421, places=5)

    def test_applyToPoint_origin(self):
        point = Point()
        result = self.motor.apply(point)

        self.assertTrue(isinstance(result, Point))

        self.assertAlmostEqual(result["e0"], point["e0"])
        self.assertAlmostEqual(result["e1"], point["e1"])
        self.assertAlmostEqual(result["e2"], point["e2"])
        self.assertAlmostEqual(result["e3"], point["e3"])
        self.assertAlmostEqual(result["ei"], point["ei"])

    def test_applyToPoint_other(self):
        point = Point(1.0, 2.0, 3.0)
        result = self.motor.apply(point)

        self.assertTrue(isinstance(result, Point))

        self.assertAlmostEqual(result["e0"], 1.0)
        self.assertAlmostEqual(result["e1"], -2.0)
        self.assertAlmostEqual(result["e2"], 1.0)
        self.assertAlmostEqual(result["e3"], 3.0)
        self.assertAlmostEqual(result["ei"], 7.0)

    def test_applyToLine(self):
        p1 = Point()
        p2 = Point(1.0, 0.0, 0.0)
        line = Line(p1, p2)

        result = self.motor.apply(line)

        self.assertTrue(isinstance(result, Line))

        self.assertAlmostEqual(result["e12i"], line["e12i"])
        self.assertAlmostEqual(result["e13i"], line["e13i"])
        self.assertAlmostEqual(result["e23i"], line["e23i"])
        self.assertAlmostEqual(result["e01i"], 0.0)
        self.assertAlmostEqual(result["e02i"], 1.0)
        self.assertAlmostEqual(result["e03i"], line["e03i"])

    def test_applyToPlane(self):
        p1 = Point(0.0, 0.0, 0.0)
        p2 = Point(1.0, 0.0, 0.0)
        p3 = Point(0.0, 1.0, 0.0)
        plane = Plane(p1, p2, p3)

        result = self.motor.apply(plane)

        self.assertTrue(isinstance(result, Plane))

        self.assertAlmostEqual(result["e123i"], plane["e123i"])
        self.assertAlmostEqual(result["e012i"], plane["e012i"])
        self.assertAlmostEqual(result["e023i"], plane["e023i"])
        self.assertAlmostEqual(result["e013i"], plane["e013i"])

    def test_applyToSphere(self):
        center = Point(1.0, 0.0, 0.0)
        sphere = Sphere(center, 0.5)

        result = self.motor.apply(sphere)

        self.assertTrue(isinstance(result, Sphere))

        resultCenter = result.getCenter()

        self.assertTrue(isinstance(resultCenter, Point))

        self.assertAlmostEqual(resultCenter["e0"], center["e0"])
        self.assertAlmostEqual(resultCenter["e1"], 0.0)
        self.assertAlmostEqual(resultCenter["e2"], 1.0)
        self.assertAlmostEqual(resultCenter["e3"], center["e3"])
        self.assertAlmostEqual(resultCenter["ei"], center["ei"])

        self.assertAlmostEqual(result.getRadius(), sphere.getRadius())


class TestMotorWithTranslationAndRotation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.translator = Translator(TranslatorGenerator([0.0, 0.0, 1.0]))
        cls.rotor = Rotor(RotorGenerator([0.0, 0.0, 1.0]), math.pi / 2.0)
        cls.motor = Motor(cls.translator, cls.rotor)

    def test_rotor(self):
        rotor = self.motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), self.rotor.scalar())
        self.assertAlmostEqual(rotor.e23(), self.rotor.e23())
        self.assertAlmostEqual(rotor.e13(), self.rotor.e13())
        self.assertAlmostEqual(rotor.e12(), self.rotor.e12())

    def test_translator(self):
        translator = self.motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], self.translator["scalar"])
        self.assertAlmostEqual(translator["e1i"], self.translator["e1i"])
        self.assertAlmostEqual(translator["e2i"], self.translator["e2i"])
        self.assertAlmostEqual(translator["e3i"], self.translator["e3i"])

    def test_log(self):
        log = self.motor.log()

        self.assertAlmostEqual(log.get_e23(), 0.0)
        self.assertAlmostEqual(log.get_e13(), 0.0)
        self.assertAlmostEqual(log.get_e12(), 1.5707963266)
        self.assertAlmostEqual(log.get_e1i(), 0.0)
        self.assertAlmostEqual(log.get_e2i(), 0.0)
        self.assertAlmostEqual(log.get_e3i(), 1.0)

    def test_logJacobian(self):
        jacobian = self.motor.logJacobian()

        self.assertTrue(isinstance(jacobian, np.ndarray))
        self.assertEqual(jacobian.shape, (6, 8))

        self.assertAlmostEqual(jacobian[0, 0], 0.0)
        self.assertAlmostEqual(jacobian[0, 1], -2.22144, places=5)
        self.assertAlmostEqual(jacobian[0, 2], 0.0)
        self.assertAlmostEqual(jacobian[0, 3], 0.0)
        self.assertAlmostEqual(jacobian[0, 4], 0.0)
        self.assertAlmostEqual(jacobian[0, 5], 0.0)
        self.assertAlmostEqual(jacobian[0, 6], 0.0)
        self.assertAlmostEqual(jacobian[0, 7], 0.0)

        self.assertAlmostEqual(jacobian[1, 0], 0.0)
        self.assertAlmostEqual(jacobian[1, 1], 0.0)
        self.assertAlmostEqual(jacobian[1, 2], -2.22144, places=5)
        self.assertAlmostEqual(jacobian[1, 3], 0.0)
        self.assertAlmostEqual(jacobian[1, 4], 0.0)
        self.assertAlmostEqual(jacobian[1, 5], 0.0)
        self.assertAlmostEqual(jacobian[1, 6], 0.0)
        self.assertAlmostEqual(jacobian[1, 7], 0.0)

        self.assertAlmostEqual(jacobian[2, 0], -0.606986, places=5)
        self.assertAlmostEqual(jacobian[2, 1], 0.0)
        self.assertAlmostEqual(jacobian[2, 2], 0.0)
        self.assertAlmostEqual(jacobian[2, 3], -2.22144, places=5)
        self.assertAlmostEqual(jacobian[2, 4], 0.0)
        self.assertAlmostEqual(jacobian[2, 5], 0.0)
        self.assertAlmostEqual(jacobian[2, 6], 0.0)
        self.assertAlmostEqual(jacobian[2, 7], 0.0)

        self.assertAlmostEqual(jacobian[3, 0], 0.0)
        self.assertAlmostEqual(jacobian[3, 1], -0.707107, places=5)
        self.assertAlmostEqual(jacobian[3, 2], 0.707107, places=5)
        self.assertAlmostEqual(jacobian[3, 3], 0.0)
        self.assertAlmostEqual(jacobian[3, 4], -1.41421, places=5)
        self.assertAlmostEqual(jacobian[3, 5], 1.41421, places=5)
        self.assertAlmostEqual(jacobian[3, 6], 0.0)
        self.assertAlmostEqual(jacobian[3, 7], 0.0)

        self.assertAlmostEqual(jacobian[4, 0], 0.0)
        self.assertAlmostEqual(jacobian[4, 1], 0.707107, places=5)
        self.assertAlmostEqual(jacobian[4, 2], 0.707107, places=5)
        self.assertAlmostEqual(jacobian[4, 3], 0.0)
        self.assertAlmostEqual(jacobian[4, 4], -1.41421, places=5)
        self.assertAlmostEqual(jacobian[4, 5], -1.41421, places=5)
        self.assertAlmostEqual(jacobian[4, 6], 0.0)
        self.assertAlmostEqual(jacobian[4, 7], 0.0)

        self.assertAlmostEqual(jacobian[5, 0], 0.707107, places=5)
        self.assertAlmostEqual(jacobian[5, 1], 0.0)
        self.assertAlmostEqual(jacobian[5, 2], 0.0)
        self.assertAlmostEqual(jacobian[5, 3], -0.707107, places=5)
        self.assertAlmostEqual(jacobian[5, 4], 0.0)
        self.assertAlmostEqual(jacobian[5, 5], 0.0)
        self.assertAlmostEqual(jacobian[5, 6], -1.41421, places=5)
        self.assertAlmostEqual(jacobian[5, 7], 1.41421, places=5)

    def test_applyToPoint_origin(self):
        point = Point()
        result = self.motor.apply(point)

        self.assertTrue(isinstance(result, Point))

        self.assertAlmostEqual(result["e0"], 1.0)
        self.assertAlmostEqual(result["e1"], 0.0)
        self.assertAlmostEqual(result["e2"], 0.0)
        self.assertAlmostEqual(result["e3"], 1.0)
        self.assertAlmostEqual(result["ei"], 0.5)

    def test_applyToPoint_other(self):
        point = Point(1.0, 2.0, 3.0)
        result = self.motor.apply(point)

        self.assertTrue(isinstance(result, Point))

        self.assertAlmostEqual(result["e0"], 1.0)
        self.assertAlmostEqual(result["e1"], -2.0)
        self.assertAlmostEqual(result["e2"], 1.0)
        self.assertAlmostEqual(result["e3"], 4.0)
        self.assertAlmostEqual(result["ei"], 10.5)

    def test_applyToLine(self):
        p1 = Point()
        p2 = Point(1.0, 0.0, 0.0)
        line = Line(p1, p2)

        result = self.motor.apply(line)

        self.assertTrue(isinstance(result, Line))

        self.assertAlmostEqual(result["e12i"], 0.0)
        self.assertAlmostEqual(result["e13i"], 0.0)
        self.assertAlmostEqual(result["e23i"], -1.0)
        self.assertAlmostEqual(result["e01i"], 0.0)
        self.assertAlmostEqual(result["e02i"], 1.0)
        self.assertAlmostEqual(result["e03i"], 0.0)

    def test_applyToPlane(self):
        p1 = Point(0.0, 0.0, 0.0)
        p2 = Point(1.0, 0.0, 0.0)
        p3 = Point(0.0, 1.0, 0.0)
        plane = Plane(p1, p2, p3)

        result = self.motor.apply(plane)

        self.assertTrue(isinstance(result, Plane))

        self.assertAlmostEqual(result["e123i"], 1.0)
        self.assertAlmostEqual(result["e012i"], plane["e012i"])
        self.assertAlmostEqual(result["e023i"], plane["e023i"])
        self.assertAlmostEqual(result["e013i"], plane["e013i"])

    def test_applyToSphere(self):
        center = Point(1.0, 0.0, 0.0)
        sphere = Sphere(center, 0.5)

        result = self.motor.apply(sphere)

        self.assertTrue(isinstance(result, Sphere))

        resultCenter = result.getCenter()

        self.assertTrue(isinstance(resultCenter, Point))

        self.assertAlmostEqual(resultCenter["e0"], 1.0)
        self.assertAlmostEqual(resultCenter["e1"], 0.0)
        self.assertAlmostEqual(resultCenter["e2"], 1.0)
        self.assertAlmostEqual(resultCenter["e3"], 1.0)
        self.assertAlmostEqual(resultCenter["ei"], 1.0)

        self.assertAlmostEqual(result.getRadius(), sphere.getRadius())


class TestMotorWithRotationAndTranslation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.translator = Translator(TranslatorGenerator([0.0, 0.0, 1.0]))
        cls.rotor = Rotor(RotorGenerator([0.0, 0.0, 1.0]), math.pi / 2.0)
        cls.motor = Motor(cls.rotor, cls.translator)

    def test_rotor(self):
        rotor = self.motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), self.rotor.scalar())
        self.assertAlmostEqual(rotor.e23(), self.rotor.e23())
        self.assertAlmostEqual(rotor.e13(), self.rotor.e13())
        self.assertAlmostEqual(rotor.e12(), self.rotor.e12())

    def test_translator(self):
        translator = self.motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], self.translator["scalar"])
        self.assertAlmostEqual(translator["e1i"], self.translator["e1i"])
        self.assertAlmostEqual(translator["e2i"], self.translator["e2i"])
        self.assertAlmostEqual(translator["e3i"], self.translator["e3i"])


class TestMotor(unittest.TestCase):

    def test_creationFromMultivector(self):
        mv = Multivector.create(
            ["scalar", "e23", "e13", "e12", "e1i", "e2i", "e3i", "e123i"],
            [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
        )
        motor = Motor(mv)

        self.assertAlmostEqual(motor["scalar"], 1.0)
        self.assertAlmostEqual(motor["e23"], 2.0)
        self.assertAlmostEqual(motor["e13"], 3.0)
        self.assertAlmostEqual(motor["e12"], 4.0)
        self.assertAlmostEqual(motor["e1i"], 5.0)
        self.assertAlmostEqual(motor["e2i"], 6.0)
        self.assertAlmostEqual(motor["e3i"], 7.0)
        self.assertAlmostEqual(motor["e123i"], 8.0)

    def test_creationFromGenerator(self):
        generator = MotorGenerator([math.pi / 2.0, 0.0, 0.0, 1.0, 2.0, 3.0])
        motor = Motor(generator)

        rotor = motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 0.7071067812)
        self.assertAlmostEqual(rotor.e23(), -0.7071067812)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)

        translator = motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], -0.5)
        self.assertAlmostEqual(translator["e2i"], -1.0)
        self.assertAlmostEqual(translator["e3i"], -1.5)

    def test_creationFromMotor(self):
        generator = MotorGenerator([math.pi / 2.0, 0.0, 0.0, 1.0, 2.0, 3.0])
        motor1 = Motor(generator)
        motor2 = Motor(motor1)

        rotor = motor2.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 0.7071067812)
        self.assertAlmostEqual(rotor.e23(), -0.7071067812)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)

        translator = motor2.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], -0.5)
        self.assertAlmostEqual(translator["e2i"], -1.0)
        self.assertAlmostEqual(translator["e3i"], -1.5)

    def test_randomCreation(self):
        # We can only check that it compiles and doesn't throw any exception
        motor = Motor.Random()
        rotor = motor.getRotor()  # noqa
        translator = motor.getTranslator()  # noqa

    def test_unitCreation(self):
        motor = Motor.Unit()

        rotor = motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 1.0)
        self.assertAlmostEqual(rotor.e23(), 0.0)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)

        translator = motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], 0.0)
        self.assertAlmostEqual(translator["e2i"], 0.0)
        self.assertAlmostEqual(translator["e3i"], 0.0)

    def test_exponential(self):
        generator = MotorGenerator([math.pi / 2.0, 0.0, 0.0, 1.0, 2.0, 3.0])

        exp = Motor.exp(generator)

        self.assertAlmostEqual(exp.get_scalar(), 0.7071067812)
        self.assertAlmostEqual(exp.get_e23(), -0.7071067812)
        self.assertAlmostEqual(exp.get_e13(), 0.0)
        self.assertAlmostEqual(exp.get_e12(), 0.0)
        self.assertAlmostEqual(exp.get_e1i(), -0.3535533906)
        self.assertAlmostEqual(exp.get_e2i(), -1.767766953)
        self.assertAlmostEqual(exp.get_e3i(), -0.3535533906)
        self.assertAlmostEqual(exp.get_e123i(), 0.3535533906)


class TestMotorsCombination(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.xTranslator = Translator(TranslatorGenerator([1.0, 0.0, 0.0]))
        cls.yTranslator = Translator(TranslatorGenerator([0.0, 1.0, 0.0]))
        cls.rotor = Rotor([0.7071067812, -0.7071067812, 0.0, 0.0])

    def test_twoTranslations(self):
        motor = Motor(self.xTranslator)
        motor2 = Motor(self.yTranslator)

        motor *= motor2

        rotor = motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 1.0)
        self.assertAlmostEqual(rotor.e23(), 0.0)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)

        translator = motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], -0.5)
        self.assertAlmostEqual(translator["e2i"], -0.5)
        self.assertAlmostEqual(translator["e3i"], 0.0)

    def test_twoRotations(self):
        motor = Motor(self.rotor)
        motor2 = Motor(self.rotor)

        motor *= motor2

        rotor = motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 0.0)
        self.assertAlmostEqual(rotor.e23(), -1.0)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)

        translator = motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], 0.0)
        self.assertAlmostEqual(translator["e2i"], 0.0)
        self.assertAlmostEqual(translator["e3i"], 0.0)

    def test_translationTimesRotation(self):
        motor = Motor(self.xTranslator)
        motor2 = Motor(self.rotor)

        motor *= motor2

        rotor = motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 0.7071067812)
        self.assertAlmostEqual(rotor.e23(), -0.7071067812)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)

        translator = motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], -0.5)
        self.assertAlmostEqual(translator["e2i"], 0.0)
        self.assertAlmostEqual(translator["e3i"], 0.0)

    def test_rotationTimesTranslation(self):
        motor = Motor(self.rotor)
        motor2 = Motor(self.xTranslator)

        motor *= motor2

        rotor = motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 0.7071067812)
        self.assertAlmostEqual(rotor.e23(), -0.7071067812)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)

        translator = motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], -0.5)
        self.assertAlmostEqual(translator["e2i"], 0.0)
        self.assertAlmostEqual(translator["e3i"], 0.0)

    def test_complex(self):
        motor = Motor(self.xTranslator, self.rotor)
        motor2 = Motor(self.xTranslator, self.rotor)

        motor *= motor2

        rotor = motor.getRotor()

        self.assertAlmostEqual(rotor.scalar(), 0.0)
        self.assertAlmostEqual(rotor.e23(), -1.0)
        self.assertAlmostEqual(rotor.e13(), 0.0)
        self.assertAlmostEqual(rotor.e12(), 0.0)

        translator = motor.getTranslator()

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], -1.0)
        self.assertAlmostEqual(translator["e2i"], 0.0)
        self.assertAlmostEqual(translator["e3i"], 0.0)


if __name__ == "__main__":
    unittest.main()
