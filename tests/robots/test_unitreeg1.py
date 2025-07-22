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

from pygafro import UnitreeG1


class TestUnitreeG1(unittest.TestCase):

    def testRandomConfiguration(self):
        robot = UnitreeG1()

        config = robot.getRandomConfiguration()

        self.assertTrue(isinstance(config, np.ndarray))
        self.assertEqual(config.shape, (43,))


if __name__ == "__main__":
    unittest.main()
