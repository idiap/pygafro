#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

import unittest

from pygafro import Multivector
from pygafro import TranslatorGenerator


class TestTranslatorGenerator(unittest.TestCase):

    def test_defaultCreation(self):
        generator = TranslatorGenerator()

        self.assertAlmostEqual(generator.x(), 0.0)
        self.assertAlmostEqual(generator.y(), 0.0)
        self.assertAlmostEqual(generator.z(), 0.0)

    def test_creationFromMultivector(self):
        mv = Multivector.create(["e1i", "e2i", "e3i"], [1.0, 2.0, 3.0])
        generator = TranslatorGenerator(mv)

        self.assertAlmostEqual(generator.x(), mv["e1i"])
        self.assertAlmostEqual(generator.y(), mv["e2i"])
        self.assertAlmostEqual(generator.z(), mv["e3i"])

    def test_creationFromGenerator(self):
        generator1 = TranslatorGenerator([1.0, 2.0, 3.0])
        generator2 = TranslatorGenerator(generator1)

        self.assertAlmostEqual(generator2.x(), generator1.x())
        self.assertAlmostEqual(generator2.y(), generator1.y())
        self.assertAlmostEqual(generator2.z(), generator1.z())

    def test_creationFromParameters(self):
        generator = TranslatorGenerator([1.0, 2.0, 3.0])

        self.assertAlmostEqual(generator.x(), 1.0)
        self.assertAlmostEqual(generator.y(), 2.0)
        self.assertAlmostEqual(generator.z(), 3.0)

        self.assertAlmostEqual(generator.x(), generator["e1i"])
        self.assertAlmostEqual(generator.y(), generator["e2i"])
        self.assertAlmostEqual(generator.z(), generator["e3i"])


if __name__ == "__main__":
    unittest.main()
