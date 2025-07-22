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

from pygafro import KukaIIWA14


class TestKukaIIWA14Robot(unittest.TestCase):

    def testRandomConfiguration(self):
        robot = KukaIIWA14()

        config = robot.getRandomConfiguration()

        self.assertTrue(isinstance(config, np.ndarray))
        self.assertEqual(config.shape, (7,))


if __name__ == "__main__":
    unittest.main()
