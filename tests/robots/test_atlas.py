#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

import unittest

import numpy as np

from pygafro import Atlas


class TestAtlas(unittest.TestCase):

    def testRandomConfiguration(self):
        robot = Atlas()

        config = robot.getRandomConfiguration()

        self.assertTrue(isinstance(config, np.ndarray))
        self.assertAlmostEqual(config.shape, (30,))


if __name__ == "__main__":
    unittest.main()
