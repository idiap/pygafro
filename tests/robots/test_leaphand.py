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

from pygafro import LeapHand


class TestLeapHand(unittest.TestCase):

    def testRandomConfiguration(self):
        robot = LeapHand()

        self.assertEqual(robot.nbFingers, 4)
        self.assertEqual(robot.dof, 16)


if __name__ == "__main__":
    unittest.main()
