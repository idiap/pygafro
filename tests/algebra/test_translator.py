#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

import unittest

from pygafro import Translator
from pygafro import TranslatorGenerator


class TestTranslator(unittest.TestCase):

    def test_defaultCreation(self):
        translator = Translator()

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], 0.0)
        self.assertAlmostEqual(translator["e2i"], 0.0)
        self.assertAlmostEqual(translator["e3i"], 0.0)

    def test_creationFromGenerator(self):
        generator = TranslatorGenerator([1.0, 2.0, 3.0])
        translator = Translator(generator)

        self.assertAlmostEqual(translator["scalar"], 1.0)
        self.assertAlmostEqual(translator["e1i"], -0.5)
        self.assertAlmostEqual(translator["e2i"], -1.0)
        self.assertAlmostEqual(translator["e3i"], -1.5)

    def test_log(self):
        generator = TranslatorGenerator([1.0, 2.0, 3.0])
        translator = Translator(generator)

        log = translator.log()

        self.assertTrue(isinstance(log, TranslatorGenerator))

        self.assertAlmostEqual(log.x(), 1.0)
        self.assertAlmostEqual(log.y(), 2.0)
        self.assertAlmostEqual(log.z(), 3.0)


if __name__ == "__main__":
    unittest.main()
