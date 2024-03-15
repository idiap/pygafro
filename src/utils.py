#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

import numpy as np


def _fillParameters(parameters, src_blades, dst_blades):
    result = np.zeros((len(dst_blades),))

    for idx, blade in enumerate(src_blades):
        dst = dst_blades.index(blade)
        result[dst] = parameters[idx]

    return result


def _selectParameters(parameters, src_blades, dst_blades):
    result = np.zeros((len(dst_blades),))

    for idx, blade in enumerate(dst_blades):
        dst = src_blades.index(blade)
        result[dst] = parameters[idx]

    return result


def _getProductBlades(blades1, blades2, table):
    result_blades = []

    for b1 in blades1:
        for b2 in blades2:
            result_blades.extend(table[(b1, b2)])

    return sorted(list(set(result_blades)))
