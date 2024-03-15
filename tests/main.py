#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

import os
import sys
import unittest

# Load all the tests (using automatic discovery)
start_dir = os.path.dirname(os.path.realpath(__file__))
suite = unittest.defaultTestLoader.discover(start_dir, pattern="test_*.py")

sys.path.append(start_dir)

# Run the tests
runner = unittest.TextTestRunner()
result = runner.run(suite)

if not result.wasSuccessful():
    sys.exit(1)
