#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

import unittest

from pygafro import MotorGenerator
from pygafro import Multivector


class TestMotorGenerator(unittest.TestCase):

    def test_defaultCreation(self):
        generator = MotorGenerator()

        rotorGenerator = generator.getRotorGenerator()
        translatorGenerator = generator.getTranslatorGenerator()

        self.assertAlmostEqual(rotorGenerator.e23(), 0.0)
        self.assertAlmostEqual(rotorGenerator.e13(), 0.0)
        self.assertAlmostEqual(rotorGenerator.e12(), 0.0)

        self.assertAlmostEqual(translatorGenerator.x(), 0.0)
        self.assertAlmostEqual(translatorGenerator.y(), 0.0)
        self.assertAlmostEqual(translatorGenerator.z(), 0.0)

    def test_creationFromMultivector(self):
        mv = Multivector.create(
            ["e23", "e13", "e12", "e1i", "e2i", "e3i"], [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        )
        generator = MotorGenerator(mv)

        rotorGenerator = generator.getRotorGenerator()
        translatorGenerator = generator.getTranslatorGenerator()

        self.assertAlmostEqual(rotorGenerator.e23(), mv["e23"])
        self.assertAlmostEqual(rotorGenerator.e13(), mv["e13"])
        self.assertAlmostEqual(rotorGenerator.e12(), mv["e12"])

        self.assertAlmostEqual(translatorGenerator.x(), mv["e1i"])
        self.assertAlmostEqual(translatorGenerator.y(), mv["e2i"])
        self.assertAlmostEqual(translatorGenerator.z(), mv["e3i"])

    def test_creationFromGenerator(self):
        generator1 = MotorGenerator([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        generator2 = MotorGenerator(generator1)

        rotorGenerator1 = generator1.getRotorGenerator()
        translatorGenerator1 = generator1.getTranslatorGenerator()

        rotorGenerator2 = generator2.getRotorGenerator()
        translatorGenerator2 = generator2.getTranslatorGenerator()

        self.assertAlmostEqual(rotorGenerator2.e23(), rotorGenerator1.e23())
        self.assertAlmostEqual(rotorGenerator2.e13(), rotorGenerator1.e13())
        self.assertAlmostEqual(rotorGenerator2.e12(), rotorGenerator1.e12())

        self.assertAlmostEqual(translatorGenerator2.x(), translatorGenerator1.x())
        self.assertAlmostEqual(translatorGenerator2.y(), translatorGenerator1.y())
        self.assertAlmostEqual(translatorGenerator2.z(), translatorGenerator1.z())

    def test_creationFromParameters(self):
        generator = MotorGenerator([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])

        rotorGenerator = generator.getRotorGenerator()
        translatorGenerator = generator.getTranslatorGenerator()

        self.assertAlmostEqual(rotorGenerator.e23(), 1.0)
        self.assertAlmostEqual(rotorGenerator.e13(), 2.0)
        self.assertAlmostEqual(rotorGenerator.e12(), 3.0)

        self.assertAlmostEqual(translatorGenerator.x(), 4.0)
        self.assertAlmostEqual(translatorGenerator.y(), 5.0)
        self.assertAlmostEqual(translatorGenerator.z(), 6.0)

    def test_creationFromMatrices(self):
        generator = MotorGenerator([1.0, 2.0, 3.0], [4.0, 5.0, 6.0])

        rotorGenerator = generator.getRotorGenerator()
        translatorGenerator = generator.getTranslatorGenerator()

        self.assertAlmostEqual(rotorGenerator.e23(), 1.0)
        self.assertAlmostEqual(rotorGenerator.e13(), 2.0)
        self.assertAlmostEqual(rotorGenerator.e12(), 3.0)

        self.assertAlmostEqual(translatorGenerator.x(), 4.0)
        self.assertAlmostEqual(translatorGenerator.y(), 5.0)
        self.assertAlmostEqual(translatorGenerator.z(), 6.0)


if __name__ == "__main__":
    unittest.main()
