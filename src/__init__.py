#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: MPL-2.0
#

from ._pygafro import *  # noqa: we want to import all exported symbols from the shared library
from .manipulator import createManipulator  # noqa
from .multivector import Multivector  # noqa
from .singlemanipulatordualtarget import SingleManipulatorDualTarget  # noqa
from .singlemanipulatormotorcost import SingleManipulatorMotorCost  # noqa
from .singlemanipulatortarget import SingleManipulatorTarget  # noqa

Scalar = lambda value: Multivector_scalar([value])  # noqa
E1 = lambda value: Multivector_e1([value])  # noqa
E2 = lambda value: Multivector_e2([value])  # noqa
E3 = lambda value: Multivector_e3([value])  # noqa
Ei = lambda value: Multivector_ei([value])  # noqa
E0 = lambda value: Multivector_e0([value])  # noqa
E23 = lambda value: Multivector_e23([value])  # noqa
E13 = lambda value: Multivector_e13([value])  # noqa
E12 = lambda value: Multivector_e12([value])  # noqa
E1i = lambda value: Multivector_e1i([value])  # noqa
E2i = lambda value: Multivector_e2i([value])  # noqa
E3i = lambda value: Multivector_e3i([value])  # noqa
E01 = lambda value: Multivector_e01([value])  # noqa
E02 = lambda value: Multivector_e02([value])  # noqa
E03 = lambda value: Multivector_e03([value])  # noqa
E123 = lambda value: Multivector_e123([value])  # noqa
E12i = lambda value: Multivector_e12i([value])  # noqa
E13i = lambda value: Multivector_e13i([value])  # noqa
E23i = lambda value: Multivector_e23i([value])  # noqa
E012 = lambda value: Multivector_e012([value])  # noqa
E013 = lambda value: Multivector_e013([value])  # noqa
E023 = lambda value: Multivector_e023([value])  # noqa
E01i = lambda value: Multivector_e01i([value])  # noqa
E02i = lambda value: Multivector_e02i([value])  # noqa
E03i = lambda value: Multivector_e03i([value])  # noqa
E123i = lambda value: Multivector_e123i([value])  # noqa
E0123 = lambda value: Multivector_e0123([value])  # noqa
E012i = lambda value: Multivector_e012i([value])  # noqa
E023i = lambda value: Multivector_e023i([value])  # noqa
E013i = lambda value: Multivector_e013i([value])  # noqa
E0123i = lambda value: Multivector_e0123i([value])  # noqa
