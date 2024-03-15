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
from pygafro import Wrench


class TestWrenchCreation(unittest.TestCase):

    def test_default(self):
        wrench = Wrench()

        self.assertAlmostEqual(wrench["e23"], 0.0)
        self.assertAlmostEqual(wrench["e13"], 0.0)
        self.assertAlmostEqual(wrench["e12"], 0.0)
        self.assertAlmostEqual(wrench["e01"], 0.0)
        self.assertAlmostEqual(wrench["e02"], 0.0)
        self.assertAlmostEqual(wrench["e03"], 0.0)

        mv = wrench.multivector()

        self.assertTrue(mv.size() == wrench.size())

        self.assertAlmostEqual(mv["e23"], 0.0)
        self.assertAlmostEqual(mv["e13"], 0.0)
        self.assertAlmostEqual(mv["e12"], 0.0)
        self.assertAlmostEqual(mv["e01"], 0.0)
        self.assertAlmostEqual(mv["e02"], 0.0)
        self.assertAlmostEqual(mv["e03"], 0.0)

    def test_fromParameters(self):
        wrench = Wrench([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])

        self.assertAlmostEqual(wrench["e23"], 1.0)
        self.assertAlmostEqual(wrench["e13"], 2.0)
        self.assertAlmostEqual(wrench["e12"], 3.0)
        self.assertAlmostEqual(wrench["e01"], 4.0)
        self.assertAlmostEqual(wrench["e02"], 5.0)
        self.assertAlmostEqual(wrench["e03"], 6.0)

        mv = wrench.multivector()

        self.assertTrue(mv.size() == wrench.size())

        self.assertAlmostEqual(mv["e23"], 1.0)
        self.assertAlmostEqual(mv["e13"], 2.0)
        self.assertAlmostEqual(mv["e12"], 3.0)
        self.assertAlmostEqual(mv["e01"], 4.0)
        self.assertAlmostEqual(mv["e02"], 5.0)
        self.assertAlmostEqual(mv["e03"], 6.0)

    def test_fromWrench(self):
        wrench1 = Wrench([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        wrench2 = Wrench(wrench1)

        self.assertAlmostEqual(wrench2["e23"], 1.0)
        self.assertAlmostEqual(wrench2["e13"], 2.0)
        self.assertAlmostEqual(wrench2["e12"], 3.0)
        self.assertAlmostEqual(wrench2["e01"], 4.0)
        self.assertAlmostEqual(wrench2["e02"], 5.0)
        self.assertAlmostEqual(wrench2["e03"], 6.0)

    def test_fromMultivector(self):
        mv = Multivector.create(
            ["e23", "e13", "e12", "e01", "e02", "e03"], [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        )
        wrench = Wrench(mv)

        self.assertAlmostEqual(wrench["e23"], 1.0)
        self.assertAlmostEqual(wrench["e13"], 2.0)
        self.assertAlmostEqual(wrench["e12"], 3.0)
        self.assertAlmostEqual(wrench["e01"], 4.0)
        self.assertAlmostEqual(wrench["e02"], 5.0)
        self.assertAlmostEqual(wrench["e03"], 6.0)


class TestWrenchTransformByMotor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.wrench = Wrench([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])

    def test_default(self):
        motor = Motor()

        wrench = self.wrench.transform(motor)

        self.assertTrue(isinstance(wrench, Wrench))

        self.assertAlmostEqual(wrench["e23"], 1.0)
        self.assertAlmostEqual(wrench["e13"], 2.0)
        self.assertAlmostEqual(wrench["e12"], 3.0)
        self.assertAlmostEqual(wrench["e01"], 4.0)
        self.assertAlmostEqual(wrench["e02"], 5.0)
        self.assertAlmostEqual(wrench["e03"], 6.0)

    def test_withTranslation(self):
        translator = Translator(TranslatorGenerator([0.0, 0.0, 1.0]))
        motor = Motor(translator)

        wrench = self.wrench.transform(motor)

        self.assertTrue(isinstance(wrench, Wrench))

        self.assertAlmostEqual(wrench["e23"], -4.0)
        self.assertAlmostEqual(wrench["e13"], -2.0)
        self.assertAlmostEqual(wrench["e12"], 3.0)
        self.assertAlmostEqual(wrench["e01"], 4.0)
        self.assertAlmostEqual(wrench["e02"], 5.0)
        self.assertAlmostEqual(wrench["e03"], 6.0)

    def test_withRotation(self):
        rotor = Rotor(RotorGenerator([0.0, 0.0, 1.0]), math.pi / 2.0)
        motor = Motor(rotor)

        wrench = self.wrench.transform(motor)

        self.assertTrue(isinstance(wrench, Wrench))

        self.assertAlmostEqual(wrench["e23"], 2.0)
        self.assertAlmostEqual(wrench["e13"], -1.0)
        self.assertAlmostEqual(wrench["e12"], 3.0)
        self.assertAlmostEqual(wrench["e01"], -5.0)
        self.assertAlmostEqual(wrench["e02"], 4.0)
        self.assertAlmostEqual(wrench["e03"], 6.0)

    def test_withTranslationAndRotation(self):
        translator = Translator(TranslatorGenerator([0.0, 0.0, 1.0]))
        rotor = Rotor(RotorGenerator([0.0, 0.0, 1.0]), math.pi / 2.0)
        motor = Motor(translator, rotor)

        wrench = self.wrench.transform(motor)

        self.assertTrue(isinstance(wrench, Wrench))

        self.assertAlmostEqual(wrench["e23"], -2.0)
        self.assertAlmostEqual(wrench["e13"], 4.0)
        self.assertAlmostEqual(wrench["e12"], 3.0)
        self.assertAlmostEqual(wrench["e01"], -5.0)
        self.assertAlmostEqual(wrench["e02"], 4.0)
        self.assertAlmostEqual(wrench["e03"], 6.0)


class TestWrenchOperations(unittest.TestCase):

    def test_addition(self):
        wrench = Wrench([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        wrench2 = Wrench([10.0, 20.0, 30.0, 40.0, 50.0, 60.0])

        wrench += wrench2

        self.assertAlmostEqual(wrench["e23"], 11.0)
        self.assertAlmostEqual(wrench["e13"], 22.0)
        self.assertAlmostEqual(wrench["e12"], 33.0)
        self.assertAlmostEqual(wrench["e01"], 44.0)
        self.assertAlmostEqual(wrench["e02"], 55.0)
        self.assertAlmostEqual(wrench["e03"], 66.0)

    def test_isubstration(self):
        wrench = Wrench([10.0, 20.0, 30.0, 40.0, 50.0, 60.0])
        wrench2 = Wrench([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])

        wrench -= wrench2

        self.assertAlmostEqual(wrench["e23"], 9.0)
        self.assertAlmostEqual(wrench["e13"], 18.0)
        self.assertAlmostEqual(wrench["e12"], 27.0)
        self.assertAlmostEqual(wrench["e01"], 36.0)
        self.assertAlmostEqual(wrench["e02"], 45.0)
        self.assertAlmostEqual(wrench["e03"], 54.0)

    def test_substration(self):
        wrench1 = Wrench([10.0, 20.0, 30.0, 40.0, 50.0, 60.0])
        wrench2 = Wrench([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])

        wrench = wrench1 - wrench2

        self.assertAlmostEqual(wrench["e23"], 9.0)
        self.assertAlmostEqual(wrench["e13"], 18.0)
        self.assertAlmostEqual(wrench["e12"], 27.0)
        self.assertAlmostEqual(wrench["e01"], 36.0)
        self.assertAlmostEqual(wrench["e02"], 45.0)
        self.assertAlmostEqual(wrench["e03"], 54.0)


if __name__ == "__main__":
    unittest.main()
