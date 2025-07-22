#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2025 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: MPL-2.0
#

import unittest

import numpy as np

from pygafro import Planar3DoF


class TestPlanar3DoFRobot(unittest.TestCase):

    def testRandomConfiguration(self):
        robot = Planar3DoF()

        config = robot.getRandomConfiguration()

        self.assertTrue(isinstance(config, np.ndarray))
        self.assertEqual(config.shape, (3,))


if __name__ == "__main__":
    unittest.main()
