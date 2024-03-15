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
from pygafro import Motor
from pygafro import Multivector
from pygafro import Rotor
from pygafro import RotorGenerator
from pygafro import Translator
from pygafro import TranslatorGenerator
from pygafro import Twist
from pygafro import Wrench


class TestInertia(unittest.TestCase):

    def test_defaultCreation(self):
        inertia = Inertia()  # noqa
        # Note: Eigen matrices aren't initialised by default, we can't test the values in inertia.getTensor()

    def test_zeroInertia(self):
        inertia = Inertia.Zero()

        tensor = inertia.getTensor()

        self.assertTrue(isinstance(tensor, np.ndarray))
        self.assertTrue(tensor.shape == (6, 6))

        for i in range(6):
            for j in range(6):
                self.assertAlmostEqual(tensor[i, j], 0.0)

    def checkTensor(self, inertia):
        tensor = inertia.getTensor()

        self.assertTrue(isinstance(tensor, np.ndarray))
        self.assertTrue(tensor.shape == (6, 6))

        self.assertAlmostEqual(tensor[0, 0], 1.0)
        self.assertAlmostEqual(tensor[0, 1], 0.0)
        self.assertAlmostEqual(tensor[0, 2], 0.0)
        self.assertAlmostEqual(tensor[1, 0], 0.0)
        self.assertAlmostEqual(tensor[1, 1], 1.0)
        self.assertAlmostEqual(tensor[1, 2], 0.0)
        self.assertAlmostEqual(tensor[2, 0], 0.0)
        self.assertAlmostEqual(tensor[2, 1], 0.0)
        self.assertAlmostEqual(tensor[2, 2], 1.0)

        self.assertAlmostEqual(tensor[3, 3], 10.0)
        self.assertAlmostEqual(tensor[3, 4], 0.0)
        self.assertAlmostEqual(tensor[3, 5], 0.0)
        self.assertAlmostEqual(tensor[4, 3], 0.0)
        self.assertAlmostEqual(tensor[4, 4], 10.0)
        self.assertAlmostEqual(tensor[4, 5], 0.0)
        self.assertAlmostEqual(tensor[5, 3], 0.0)
        self.assertAlmostEqual(tensor[5, 4], 0.0)
        self.assertAlmostEqual(tensor[5, 5], 10.0)

    def checkElements(self, inertia):
        element = inertia.getElement23()

        self.assertAlmostEqual(element["e23"], 1.0)
        self.assertAlmostEqual(element["e13"], 0.0)
        self.assertAlmostEqual(element["e12"], 0.0)
        self.assertAlmostEqual(element["e01"], 0.0)
        self.assertAlmostEqual(element["e02"], 0.0)
        self.assertAlmostEqual(element["e03"], 0.0)

        element = inertia.getElement13()

        self.assertAlmostEqual(element["e23"], 0.0)
        self.assertAlmostEqual(element["e13"], 1.0)
        self.assertAlmostEqual(element["e12"], 0.0)
        self.assertAlmostEqual(element["e01"], 0.0)
        self.assertAlmostEqual(element["e02"], 0.0)
        self.assertAlmostEqual(element["e03"], 0.0)

        element = inertia.getElement12()

        self.assertAlmostEqual(element["e23"], 0.0)
        self.assertAlmostEqual(element["e13"], 0.0)
        self.assertAlmostEqual(element["e12"], 1.0)
        self.assertAlmostEqual(element["e01"], 0.0)
        self.assertAlmostEqual(element["e02"], 0.0)
        self.assertAlmostEqual(element["e03"], 0.0)

        element = inertia.getElement01()

        self.assertAlmostEqual(element["e23"], 0.0)
        self.assertAlmostEqual(element["e13"], 0.0)
        self.assertAlmostEqual(element["e12"], 0.0)
        self.assertAlmostEqual(element["e01"], 10.0)
        self.assertAlmostEqual(element["e02"], 0.0)
        self.assertAlmostEqual(element["e03"], 0.0)

        element = inertia.getElement02()

        self.assertAlmostEqual(element["e23"], 0.0)
        self.assertAlmostEqual(element["e13"], 0.0)
        self.assertAlmostEqual(element["e12"], 0.0)
        self.assertAlmostEqual(element["e01"], 0.0)
        self.assertAlmostEqual(element["e02"], 10.0)
        self.assertAlmostEqual(element["e03"], 0.0)

        element = inertia.getElement03()

        self.assertAlmostEqual(element["e23"], 0.0)
        self.assertAlmostEqual(element["e13"], 0.0)
        self.assertAlmostEqual(element["e12"], 0.0)
        self.assertAlmostEqual(element["e01"], 0.0)
        self.assertAlmostEqual(element["e02"], 0.0)
        self.assertAlmostEqual(element["e03"], 10.0)

    def test_creation_from_parameters(self):
        inertia = Inertia(10.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0)

        self.checkTensor(inertia)
        self.checkElements(inertia)

    def test_creation_from_tensor(self):
        inertia = Inertia(10.0, np.eye(3))

        self.checkTensor(inertia)
        self.checkElements(inertia)

    def test_creation_from_elements(self):
        elements = [
            Multivector.create(
                ["e23", "e13", "e12", "e01", "e02", "e03"],
                [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            ),
            Multivector.create(
                ["e23", "e13", "e12", "e01", "e02", "e03"],
                [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            ),
            Multivector.create(
                ["e23", "e13", "e12", "e01", "e02", "e03"],
                [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
            ),
            Multivector.create(
                ["e23", "e13", "e12", "e01", "e02", "e03"],
                [0.0, 0.0, 0.0, 10.0, 0.0, 0.0],
            ),
            Multivector.create(
                ["e23", "e13", "e12", "e01", "e02", "e03"],
                [0.0, 0.0, 0.0, 0.0, 10.0, 0.0],
            ),
            Multivector.create(
                ["e23", "e13", "e12", "e01", "e02", "e03"],
                [0.0, 0.0, 0.0, 0.0, 0.0, 10.0],
            ),
        ]

        inertia = Inertia(elements)

        self.checkTensor(inertia)
        self.checkElements(inertia)

    def test_addition_of_inertia_inplace_operator(self):
        inertia = Inertia(10.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
        inertia2 = Inertia(20.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0)

        inertia += inertia2

        tensor = inertia.getTensor()

        self.assertTrue(isinstance(tensor, np.ndarray))
        self.assertTrue(tensor.shape == (6, 6))

        self.assertAlmostEqual(tensor[0, 0], 11.0)
        self.assertAlmostEqual(tensor[0, 1], -22.0)
        self.assertAlmostEqual(tensor[0, 2], 33.0)
        self.assertAlmostEqual(tensor[1, 0], -22.0)
        self.assertAlmostEqual(tensor[1, 1], 44.0)
        self.assertAlmostEqual(tensor[1, 2], -55.0)
        self.assertAlmostEqual(tensor[2, 0], 33.0)
        self.assertAlmostEqual(tensor[2, 1], -55.0)
        self.assertAlmostEqual(tensor[2, 2], 66.0)

        self.assertAlmostEqual(tensor[3, 3], 30.0)
        self.assertAlmostEqual(tensor[3, 4], 0.0)
        self.assertAlmostEqual(tensor[3, 5], 0.0)
        self.assertAlmostEqual(tensor[4, 3], 0.0)
        self.assertAlmostEqual(tensor[4, 4], 30.0)
        self.assertAlmostEqual(tensor[4, 5], 0.0)
        self.assertAlmostEqual(tensor[5, 3], 0.0)
        self.assertAlmostEqual(tensor[5, 4], 0.0)
        self.assertAlmostEqual(tensor[5, 5], 30.0)

        for i in range(3):
            for j in range(3, 6):
                self.assertAlmostEqual(tensor[i, j], 0.0)
                self.assertAlmostEqual(tensor[j, i], 0.0)

    def test_addition_of_inertia_binary_operator(self):
        inertia = Inertia(10.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0)
        inertia2 = Inertia(20.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0)

        inertia3 = inertia + inertia2

        tensor = inertia3.getTensor()

        self.assertTrue(isinstance(tensor, np.ndarray))
        self.assertTrue(tensor.shape == (6, 6))

        self.assertAlmostEqual(tensor[0, 0], 11.0)
        self.assertAlmostEqual(tensor[0, 1], -22.0)
        self.assertAlmostEqual(tensor[0, 2], 33.0)
        self.assertAlmostEqual(tensor[1, 0], -22.0)
        self.assertAlmostEqual(tensor[1, 1], 44.0)
        self.assertAlmostEqual(tensor[1, 2], -55.0)
        self.assertAlmostEqual(tensor[2, 0], 33.0)
        self.assertAlmostEqual(tensor[2, 1], -55.0)
        self.assertAlmostEqual(tensor[2, 2], 66.0)

        self.assertAlmostEqual(tensor[3, 3], 30.0)
        self.assertAlmostEqual(tensor[3, 4], 0.0)
        self.assertAlmostEqual(tensor[3, 5], 0.0)
        self.assertAlmostEqual(tensor[4, 3], 0.0)
        self.assertAlmostEqual(tensor[4, 4], 30.0)
        self.assertAlmostEqual(tensor[4, 5], 0.0)
        self.assertAlmostEqual(tensor[5, 3], 0.0)
        self.assertAlmostEqual(tensor[5, 4], 0.0)
        self.assertAlmostEqual(tensor[5, 5], 30.0)

        for i in range(3):
            for j in range(3, 6):
                self.assertAlmostEqual(tensor[i, j], 0.0)
                self.assertAlmostEqual(tensor[j, i], 0.0)

    def test_callOperatorOnTwist(self):
        inertia = Inertia(10.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0)

        result = inertia(Twist([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]))

        self.assertTrue(isinstance(result, Wrench))

        self.assertAlmostEqual(result["e23"], 1.0)
        self.assertAlmostEqual(result["e13"], 2.0)
        self.assertAlmostEqual(result["e12"], 3.0)
        self.assertAlmostEqual(result["e01"], 40.0)
        self.assertAlmostEqual(result["e02"], 50.0)
        self.assertAlmostEqual(result["e03"], 60.0)

    def test_transform(self):
        inertia = Inertia(10.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0)

        translator = Translator(TranslatorGenerator([0.0, 0.0, 1.0]))
        rotor = Rotor(RotorGenerator([0.0, 0.0, 1.0]), math.pi / 2.0)
        motor = Motor(rotor, translator)

        result = inertia.transform(motor)

        self.assertTrue(isinstance(result, Inertia))

        tensor = result.getTensor()

        self.assertTrue(isinstance(tensor, np.ndarray))
        self.assertTrue(tensor.shape == (6, 6))

        self.assertAlmostEqual(tensor[0, 0], 14.0)
        self.assertAlmostEqual(tensor[0, 1], 2.0)
        self.assertAlmostEqual(tensor[0, 2], -5.0)
        self.assertAlmostEqual(tensor[1, 0], 2.0)
        self.assertAlmostEqual(tensor[1, 1], 11.0)
        self.assertAlmostEqual(tensor[1, 2], -3.0)
        self.assertAlmostEqual(tensor[2, 0], -5.0)
        self.assertAlmostEqual(tensor[2, 1], -3.0)
        self.assertAlmostEqual(tensor[2, 2], 6.0)

        self.assertAlmostEqual(tensor[0, 3], 0.0)
        self.assertAlmostEqual(tensor[0, 4], -10.0)
        self.assertAlmostEqual(tensor[0, 5], 0.0)
        self.assertAlmostEqual(tensor[1, 3], -10.0)
        self.assertAlmostEqual(tensor[1, 4], 0.0)
        self.assertAlmostEqual(tensor[1, 5], 0.0)
        self.assertAlmostEqual(tensor[2, 3], 0.0)
        self.assertAlmostEqual(tensor[2, 4], 0.0)
        self.assertAlmostEqual(tensor[2, 5], 0.0)

        self.assertAlmostEqual(tensor[3, 0], 0.0)
        self.assertAlmostEqual(tensor[3, 1], -10.0)
        self.assertAlmostEqual(tensor[3, 2], 0.0)
        self.assertAlmostEqual(tensor[4, 0], -10.0)
        self.assertAlmostEqual(tensor[4, 1], 0.0)
        self.assertAlmostEqual(tensor[4, 2], 0.0)
        self.assertAlmostEqual(tensor[5, 0], 0.0)
        self.assertAlmostEqual(tensor[5, 1], 0.0)
        self.assertAlmostEqual(tensor[5, 2], 0.0)

        self.assertAlmostEqual(tensor[3, 3], 10.0)
        self.assertAlmostEqual(tensor[3, 4], 0.0)
        self.assertAlmostEqual(tensor[3, 5], 0.0)
        self.assertAlmostEqual(tensor[4, 3], 0.0)
        self.assertAlmostEqual(tensor[4, 4], 10.0)
        self.assertAlmostEqual(tensor[4, 5], 0.0)
        self.assertAlmostEqual(tensor[5, 3], 0.0)
        self.assertAlmostEqual(tensor[5, 4], 0.0)
        self.assertAlmostEqual(tensor[5, 5], 10.0)

    def test_inverseTransform(self):
        inertia = Inertia(10.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0)

        translator = Translator(TranslatorGenerator([0.0, 0.0, 1.0]))
        rotor = Rotor(RotorGenerator([0.0, 0.0, 1.0]), math.pi / 2.0)
        motor = Motor(rotor, translator)

        result = inertia.inverseTransform(motor)

        self.assertTrue(isinstance(result, Inertia))

        tensor = result.getTensor()

        self.assertTrue(isinstance(tensor, np.ndarray))
        self.assertTrue(tensor.shape == (6, 6))

        self.assertAlmostEqual(tensor[0, 0], 14.0)
        self.assertAlmostEqual(tensor[0, 1], 2.0)
        self.assertAlmostEqual(tensor[0, 2], 5.0)
        self.assertAlmostEqual(tensor[1, 0], 2.0)
        self.assertAlmostEqual(tensor[1, 1], 11.0)
        self.assertAlmostEqual(tensor[1, 2], 3.0)
        self.assertAlmostEqual(tensor[2, 0], 5.0)
        self.assertAlmostEqual(tensor[2, 1], 3.0)
        self.assertAlmostEqual(tensor[2, 2], 6.0)

        self.assertAlmostEqual(tensor[0, 3], 0.0)
        self.assertAlmostEqual(tensor[0, 4], 10.0)
        self.assertAlmostEqual(tensor[0, 5], 0.0)
        self.assertAlmostEqual(tensor[1, 3], 10.0)
        self.assertAlmostEqual(tensor[1, 4], 0.0)
        self.assertAlmostEqual(tensor[1, 5], 0.0)
        self.assertAlmostEqual(tensor[2, 3], 0.0)
        self.assertAlmostEqual(tensor[2, 4], 0.0)
        self.assertAlmostEqual(tensor[2, 5], 0.0)

        self.assertAlmostEqual(tensor[3, 0], 0.0)
        self.assertAlmostEqual(tensor[3, 1], 10.0)
        self.assertAlmostEqual(tensor[3, 2], 0.0)
        self.assertAlmostEqual(tensor[4, 0], 10.0)
        self.assertAlmostEqual(tensor[4, 1], 0.0)
        self.assertAlmostEqual(tensor[4, 2], 0.0)
        self.assertAlmostEqual(tensor[5, 0], 0.0)
        self.assertAlmostEqual(tensor[5, 1], 0.0)
        self.assertAlmostEqual(tensor[5, 2], 0.0)

        self.assertAlmostEqual(tensor[3, 3], 10.0)
        self.assertAlmostEqual(tensor[3, 4], 0.0)
        self.assertAlmostEqual(tensor[3, 5], 0.0)
        self.assertAlmostEqual(tensor[4, 3], 0.0)
        self.assertAlmostEqual(tensor[4, 4], 10.0)
        self.assertAlmostEqual(tensor[4, 5], 0.0)
        self.assertAlmostEqual(tensor[5, 3], 0.0)
        self.assertAlmostEqual(tensor[5, 4], 0.0)
        self.assertAlmostEqual(tensor[5, 5], 10.0)


if __name__ == "__main__":
    unittest.main()
