#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

import numpy as np

from ._pygafro import *  # noqa: we need to discover at runtime which Multivector classes were compiled
from ._pygafro import internals
from .geometricproductcayleytable import table as geometricproductcayleytable
from .innerproductcayleytable import table as innerproductcayleytable
from .mv_combinations import combinations as mv_combinations
from .outerproductcayleytable import table as outerproductcayleytable
from .utils import _fillParameters
from .utils import _getProductBlades

all_blades = [
    "scalar",
    "e1",
    "e2",
    "e3",
    "ei",
    "e0",
    "e23",
    "e13",
    "e12",
    "e1i",
    "e2i",
    "e3i",
    "e01",
    "e02",
    "e03",
    "e0i",
    "e123",
    "e12i",
    "e13i",
    "e23i",
    "e012",
    "e013",
    "e023",
    "e01i",
    "e02i",
    "e03i",
    "e123i",
    "e0123",
    "e012i",
    "e023i",
    "e013i",
    "e0123i",
]


# gafro being based on C++ templates, only the classes and operations you are effectively
# using are compiled into your software.
#
# This versatility cannot be achieved in a Python library: we cannot instantiate the
# templates at runtime, nor can we realistically instantiate all the possible combinations
# at compile time.
#
# A compromise was choosen: a subset of multivectors (using sensible blades combinations)
# are instantiated and compiled, and other blades combinations are supported through this
# Python class that internally use a C++ multivector with more blades and transparently
# use a mask to only expose the blades requested by the user.
#
# It is expected that multivectors are created through the Multivector.create()
# method, which will either return a C++ multivector (if the required combination of blades
# was compiled) or an instance of this class.
class Multivector:

    def __init__(self, blades, parameters=None, mv=None):
        if (len(blades) > 0) and isinstance(blades[0], str):
            blades = [all_blades.index(b) for b in blades]

        self._blades = sorted(list(set(blades)))
        self._mv = (
            _createTemplatedMultivector(blades, parameters=parameters)
            if mv is None
            else mv
        )
        self._mask = [b in blades for b in self._mv.blades()]

    def size(self):
        return len(self._blades)

    def blades(self):
        return self._blades

    def has(self, blade):
        return blade in self._blades

    def setParameters(self, parameters):
        full_parameters = np.zeros((len(self._mask),))
        full_parameters[self._mask] = parameters
        self._mv.setParameters(full_parameters)

    def vector(self):
        return self._mv.vector()[self._mask]

    def reverse(self):
        result = self._mv.reverse()
        parameters = result.vector()[self._mask]
        return Multivector(self._blades, parameters=parameters)

    def dual(self):
        result = self._mv.dual()
        blades = _getProductBlades(
            self._blades, [all_blades.index("e0123i")], geometricproductcayleytable
        )
        return Multivector(blades, mv=result)

    def inverse(self):
        result = self._mv.inverse()
        parameters = result.vector()[self._mask]
        return Multivector(self._blades, parameters=parameters)

    def norm(self):
        return self._mv.norm()

    def squaredNorm(self):
        return self._mv.squaredNorm()

    def signedNorm(self):
        return self._mv.signedNorm()

    def normalize(self):
        self._mv.normalize()

    def normalized(self):
        result = self._mv.normalized()
        return Multivector(self._blades, mv=result)

    def __getitem__(self, blade):
        if isinstance(blade, str):
            blade_name = blade
            blade = all_blades.index(blade)
        else:
            blade_name = all_blades[blade]

        if blade in self._blades:
            return getattr(self._mv, f"get_{blade_name}")()

        return 0.0

    def __setitem__(self, blade, value):
        if isinstance(blade, str):
            blade_name = blade
            blade = all_blades.index(blade)
        else:
            blade_name = all_blades[blade]

        if blade in self._blades:
            getattr(self._mv, f"set_{blade_name}")(value)

    def __imul__(self, v):
        self._mv *= v
        return self

    def __itruediv__(self, v):
        self._mv /= v
        return self

    def __iadd__(self, v):
        self._mv += v
        return self

    def __repr__(self):
        first = True
        s = ""

        vector = self.vector()

        for b, v in zip(self._blades, vector):
            if abs(v) < 1e-10:
                continue

            if not first:
                s += " + " if v >= 0.0 else " - "
                s += f"{abs(v):06f}"
            else:
                s += f"{v:06f}"
                first = False

            if b > 0:
                s += "*" + all_blades[b]

        if first:
            s = "0"

        return s

    @staticmethod
    def Random(blades):
        return Multivector(blades, parameters=np.random.random((len(blades),)))

    @staticmethod
    def create(blades, parameters=None, mvclass=None):
        if not (isinstance(blades, list)):
            raise TypeError("A list of blades must be provided")

        if not all([isinstance(x, int) for x in blades]) and not all(
            [isinstance(x, str) for x in blades]
        ):
            raise TypeError("All blades must be of the same type (int or str)")

        mv = _createTemplatedMultivector(blades, parameters=parameters)

        if (len(blades) > 0) and isinstance(blades[0], str):
            blades = [all_blades.index(b) for b in blades]

        if mv.blades() != blades:
            return Multivector(blades, mv=mv)
        elif mvclass is not None:
            return mvclass(mv)

        return mv

    @staticmethod
    def clone(mv):
        if isinstance(mv, Multivector):
            return Multivector(mv.blades(), mv=type(mv._mv)(mv._mv))

        return type(mv)(mv)


def _createTemplatedMultivector(blades, parameters=None):
    if not (isinstance(blades, list)):
        raise TypeError("A list of blades must be provided")

    if not all([isinstance(x, int) for x in blades]) and not all(
        [isinstance(x, str) for x in blades]
    ):
        raise TypeError("All blades must be of the same type (int or str)")

    global_blades = globals()["blades"]

    if (len(blades) > 0) and isinstance(blades[0], int):
        blades_dict = {
            getattr(global_blades, x): x
            for x in all_blades
            if getattr(global_blades, x) in blades
        }
        blades = [blades_dict[x] for x in blades]

    indexed_blades = [(getattr(global_blades, x), x) for x in blades]

    sorted_blades = [x[1] for x in sorted(list(set(indexed_blades)))]

    if parameters is not None:
        if isinstance(parameters, float):
            parameters = [int(parameters)] * len(sorted_blades)

        elif isinstance(parameters, int):
            parameters = [parameters] * len(sorted_blades)

        else:
            try:
                nb = len(parameters)
            except TypeError:
                raise TypeError(f"Invalid parameters type: {parameters}")

            if nb != len(sorted_blades):
                raise TypeError(
                    f"Invalid number of parameters: {nb} instead of {len(sorted_blades)}"
                )

            unsorted_blades = [x[1] for x in indexed_blades]
            parameters = [parameters[unsorted_blades.index(x)] for x in sorted_blades]

    class_name = "Multivector_" + "".join([x for x in sorted_blades])

    try:
        multivector_class = globals()[class_name]
        if parameters is not None:
            return multivector_class(parameters)
        else:
            return multivector_class()
    except KeyError:
        pass

    for mv_blades in mv_combinations:
        if not all([b in mv_blades for b in sorted_blades]):
            continue

        class_name = "Multivector_" + "".join([x for x in mv_blades])

        multivector_class = globals()[class_name]
        if parameters is not None:
            full_parameters = []
            for i in range(len(mv_blades)):
                if mv_blades[i] in blades:
                    full_parameters.append(
                        parameters[sorted_blades.index(mv_blades[i])]
                    )
                else:
                    full_parameters.append(0.0)

            return multivector_class(full_parameters)
        else:
            return multivector_class()


def _addMultivectors(a, b):
    blades1 = a.blades()
    blades2 = b.blades()

    blades = blades1.copy()
    blades.extend(blades2)

    blades = sorted(list(set(blades)))

    vector1 = _fillParameters(a.vector(), blades1, blades)
    vector2 = _fillParameters(b.vector(), blades2, blades)

    parameters = vector1 + vector2

    mvclass = None
    if (
        (blades1 == blades2)
        and not (isinstance(a, Multivector))
        and not (a.__class__.__name__.startswith("Multivector_"))
    ):
        mvclass = a.__class__

    return Multivector.create(blades, parameters=parameters, mvclass=mvclass)


def _subMultivectors(a, b):
    blades1 = a.blades()
    blades2 = b.blades()

    blades = blades1.copy()
    blades.extend(blades2)

    blades = sorted(list(set(blades)))

    vector1 = _fillParameters(a.vector(), blades1, blades)
    vector2 = _fillParameters(b.vector(), blades2, blades)

    parameters = vector1 - vector2

    mvclass = None
    if (
        (blades1 == blades2)
        and not (isinstance(a, Multivector))
        and not (a.__class__.__name__.startswith("Multivector_"))
    ):
        mvclass = a.__class__

    return Multivector.create(blades, parameters=parameters, mvclass=mvclass)


def _getClassName(mv):
    if isinstance(mv, Multivector):
        return mv._mv.__class__.__name__
    else:
        return (
            mv.__class__.__name__
            if mv.__class__.__name__.startswith("Multivector_")
            else mv.__class__.__bases__[0].__name__
        )


def _product(a, b, prefix, table):
    class1 = _getClassName(a)
    class2 = _getClassName(b)

    blades1 = class1.replace("Multivector_", "")
    blades2 = class2.replace("Multivector_", "")

    function_name = f"{prefix}_{blades1}_{blades2}"
    if hasattr(internals, function_name):
        func = getattr(internals, function_name)
        bits, params = func(
            a._mv if isinstance(a, Multivector) else a,
            b._mv if isinstance(b, Multivector) else b,
        )
    else:
        blades = "".join(all_blades)
        function_name = f"{prefix}_{blades}_{blades}"

        mv1 = _fillParameters(a.vector(), a.blades(), list(range(len(all_blades))))
        mv2 = _fillParameters(b.vector(), b.blades(), list(range(len(all_blades))))

        func = getattr(internals, function_name)
        _, params = func(
            Multivector.create(all_blades, mv1), Multivector.create(all_blades, mv2)
        )

        result_blades = _getProductBlades(a.blades(), b.blades(), table)
        bits = [x in result_blades for x in range(len(params))]

    blades = [idx for idx, v in enumerate(bits) if v]
    parameters = [params[idx] for idx, v in enumerate(bits) if v]

    return Multivector.create(blades, parameters)


def _geometricProduct(a, b):
    return _product(a, b, "geometricProduct", geometricproductcayleytable)


def _innerProduct(a, b):
    return _product(a, b, "innerProduct", innerproductcayleytable)


def _outerProduct(a, b):
    return _product(a, b, "outerProduct", outerproductcayleytable)


def _getitem(mv, blade):
    if isinstance(blade, str):
        blade_name = blade
        blade = all_blades.index(blade)
    else:
        blade_name = all_blades[blade]

    if blade in mv.blades():
        return getattr(mv, f"get_{blade_name}")()

    return 0.0


def _setitem(mv, blade, value):
    if isinstance(blade, str):
        blade_name = blade
        blade = all_blades.index(blade)
    else:
        blade_name = all_blades[blade]

    if blade in mv.blades():
        getattr(mv, f"set_{blade_name}")(value)


# Add additional methods to the C++-based multivector classes
for name in [x for x in globals().keys() if x.startswith("Multivector_")]:
    globals()[name].__add__ = _addMultivectors
    globals()[name].__sub__ = _subMultivectors
    globals()[name].__mul__ = _geometricProduct
    globals()[name].__or__ = _innerProduct
    globals()[name].__xor__ = _outerProduct
    globals()[name].__getitem__ = _getitem
    globals()[name].__setitem__ = _setitem

# Add additional methods to the Python-based multivector class
Multivector.__add__ = _addMultivectors
Multivector.__sub__ = _subMultivectors
Multivector.__mul__ = _geometricProduct
Multivector.__or__ = _innerProduct
Multivector.__xor__ = _outerProduct
