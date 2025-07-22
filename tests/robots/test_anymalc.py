#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: MPL-2.0
#

import unittest

import numpy as np

from pygafro import AnymalC


class TestAnymalC(unittest.TestCase):

    def testRandomConfiguration(self):
        robot = AnymalC()

        config = robot.getSystem().getRandomConfiguration()

        self.assertTrue(isinstance(config, np.ndarray))
        self.assertEqual(config.shape, (12,))


if __name__ == "__main__":
    unittest.main()
