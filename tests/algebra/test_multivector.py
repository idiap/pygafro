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

from pygafro import E1
from pygafro import Multivector
from pygafro import Multivector_
from pygafro import Multivector_e1e2e3eie0
from pygafro import Multivector_e1ie2ie3i
from pygafro import Multivector_e23e13e12
from pygafro import Multivector_e123i
from pygafro import Multivector_e123ie0123e012ie023ie013i
from pygafro import Multivector_scalar
from pygafro import blades


class TestMultivector(unittest.TestCase):

    def test_size(self):
        self.assertEqual(Multivector_e1ie2ie3i.size(), 3)
        self.assertEqual(Multivector_e1e2e3eie0.size(), 5)

    def test_blades(self):
        blades1 = Multivector_e1ie2ie3i.blades()

        self.assertTrue(isinstance(blades1, list))
        self.assertEqual(len(blades1), 3)

        self.assertEqual(blades1[0], blades.e1i)
        self.assertEqual(blades1[1], blades.e2i)
        self.assertEqual(blades1[2], blades.e3i)

    def test_hasBlade(self):
        self.assertTrue(Multivector_e1ie2ie3i.has(blades.e1i))
        self.assertTrue(Multivector_e1ie2ie3i.has(blades.e2i))
        self.assertTrue(Multivector_e1ie2ie3i.has(blades.e3i))
        self.assertFalse(Multivector_e1ie2ie3i.has(blades.e0))

    def test_creation(self):
        mv = Multivector_e1e2e3eie0()

        self.assertAlmostEqual(mv["e1"], 0.0)
        self.assertAlmostEqual(mv["e2"], 0.0)
        self.assertAlmostEqual(mv["e3"], 0.0)
        self.assertAlmostEqual(mv["ei"], 0.0)
        self.assertAlmostEqual(mv["e0"], 0.0)

    def test_creationWithValue(self):
        mv = Multivector_e1e2e3eie0(10)

        self.assertAlmostEqual(mv["e1"], 10.0)
        self.assertAlmostEqual(mv["e2"], 10.0)
        self.assertAlmostEqual(mv["e3"], 10.0)
        self.assertAlmostEqual(mv["ei"], 10.0)
        self.assertAlmostEqual(mv["e0"], 10.0)

    def test_creationFromParameters(self):
        mv = Multivector_e1e2e3eie0([1.0, 2.0, 3.0, 4.0, 5.0])

        self.assertAlmostEqual(mv["e1"], 1.0)
        self.assertAlmostEqual(mv["e2"], 2.0)
        self.assertAlmostEqual(mv["e3"], 3.0)
        self.assertAlmostEqual(mv["ei"], 4.0)
        self.assertAlmostEqual(mv["e0"], 5.0)

    def test_creationFromNumpyParameters(self):
        mv = Multivector_e1e2e3eie0(np.array([1.0, 2.0, 3.0, 4.0, 5.0]))

        self.assertAlmostEqual(mv["e1"], 1.0)
        self.assertAlmostEqual(mv["e2"], 2.0)
        self.assertAlmostEqual(mv["e3"], 3.0)
        self.assertAlmostEqual(mv["ei"], 4.0)
        self.assertAlmostEqual(mv["e0"], 5.0)

    def test_creationFromIncorrectNumberOfParameters(self):
        with self.assertRaises(TypeError):
            mv = Multivector_e1e2e3eie0([1.0, 2.0, 3.0, 4.0])  # noqa

    def test_creationFromMultivector(self):
        mv = Multivector_e1e2e3eie0([1.0, 2.0, 3.0, 4.0, 5.0])
        mv2 = Multivector_e1e2e3eie0(mv)

        self.assertAlmostEqual(mv2["e1"], 1.0)
        self.assertAlmostEqual(mv2["e2"], 2.0)
        self.assertAlmostEqual(mv2["e3"], 3.0)
        self.assertAlmostEqual(mv2["ei"], 4.0)
        self.assertAlmostEqual(mv2["e0"], 5.0)

    def test_creationUsingHelper(self):
        mv = Multivector.create(["e1", "e2", "e3", "ei", "e0"])

        self.assertAlmostEqual(mv["e1"], 0.0)
        self.assertAlmostEqual(mv["e2"], 0.0)
        self.assertAlmostEqual(mv["e3"], 0.0)
        self.assertAlmostEqual(mv["ei"], 0.0)
        self.assertAlmostEqual(mv["e0"], 0.0)

    def test_creationUsingHelperWithValue(self):
        mv = Multivector.create(["e1", "e2", "e3", "ei", "e0"], 10)

        self.assertAlmostEqual(mv["e1"], 10.0)
        self.assertAlmostEqual(mv["e2"], 10.0)
        self.assertAlmostEqual(mv["e3"], 10.0)
        self.assertAlmostEqual(mv["ei"], 10.0)
        self.assertAlmostEqual(mv["e0"], 10.0)

    def test_creationUsingHelperFromParameters(self):
        mv = Multivector.create(
            ["e1", "e2", "e3", "ei", "e0"], [1.0, 2.0, 3.0, 4.0, 5.0]
        )

        self.assertAlmostEqual(mv["e1"], 1.0)
        self.assertAlmostEqual(mv["e2"], 2.0)
        self.assertAlmostEqual(mv["e3"], 3.0)
        self.assertAlmostEqual(mv["ei"], 4.0)
        self.assertAlmostEqual(mv["e0"], 5.0)

    def test_creationUsingHelperFromNumpyParameters(self):
        mv = Multivector.create(
            ["e1", "e2", "e3", "ei", "e0"], np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        )

        self.assertAlmostEqual(mv["e1"], 1.0)
        self.assertAlmostEqual(mv["e2"], 2.0)
        self.assertAlmostEqual(mv["e3"], 3.0)
        self.assertAlmostEqual(mv["ei"], 4.0)
        self.assertAlmostEqual(mv["e0"], 5.0)

    def test_creationUsingHelperFromIncorrectNumberOfParameters(self):
        with self.assertRaises(TypeError):
            mv = Multivector.create(  # noqa
                ["e1", "e2", "e3", "ei", "e0"], [1.0, 2.0, 3.0, 4.0]
            )

    def test_creationUsingHelperOutOfOrder(self):
        mv = Multivector.create(
            ["e1", "e2", "ei", "e0", "e3"], [1.0, 2.0, 4.0, 5.0, 3.0]
        )

        self.assertAlmostEqual(mv["e1"], 1.0)
        self.assertAlmostEqual(mv["e2"], 2.0)
        self.assertAlmostEqual(mv["e3"], 3.0)
        self.assertAlmostEqual(mv["ei"], 4.0)
        self.assertAlmostEqual(mv["e0"], 5.0)

    def test_creationUsingHelperWithNumericalBlades(self):
        mv = Multivector.create([1, 2, 4, 5, 3], [1.0, 2.0, 4.0, 5.0, 3.0])

        self.assertAlmostEqual(mv["e1"], 1.0)
        self.assertAlmostEqual(mv["e2"], 2.0)
        self.assertAlmostEqual(mv["e3"], 3.0)
        self.assertAlmostEqual(mv["ei"], 4.0)
        self.assertAlmostEqual(mv["e0"], 5.0)

    def test_creationUsingSingleBladeHelper(self):
        mv = E1(10)
        self.assertAlmostEqual(mv["e1"], 10.0)

    def test_multiplicationOfCppMultivectorByScalar(self):
        mv = Multivector_e1e2e3eie0([1.0, 2.0, 3.0, 4.0, 5.0])

        mv *= 2.0

        self.assertAlmostEqual(mv["e1"], 2.0)
        self.assertAlmostEqual(mv["e2"], 4.0)
        self.assertAlmostEqual(mv["e3"], 6.0)
        self.assertAlmostEqual(mv["ei"], 8.0)
        self.assertAlmostEqual(mv["e0"], 10.0)

    def test_multiplicationOfPythonMultivectorByScalar(self):
        mv = Multivector(["e1", "e2", "e3", "ei", "e0"], [1.0, 2.0, 3.0, 4.0, 5.0])

        mv *= 2.0

        self.assertAlmostEqual(mv["e1"], 2.0)
        self.assertAlmostEqual(mv["e2"], 4.0)
        self.assertAlmostEqual(mv["e3"], 6.0)
        self.assertAlmostEqual(mv["ei"], 8.0)
        self.assertAlmostEqual(mv["e0"], 10.0)

    def test_multiplicationOfCppMultivectors(self):
        mv = Multivector_e1e2e3eie0([1.0, 2.0, 3.0, 4.0, 5.0])
        mv2 = Multivector_e123i([6.0])

        v = mv * mv2

        self.assertEqual(v.size(), 5)
        self.assertAlmostEqual(v["e123"], 30.0)
        self.assertAlmostEqual(v["e12i"], 18.0)
        self.assertAlmostEqual(v["e13i"], -12.0)
        self.assertAlmostEqual(v["e23i"], 6.0)
        self.assertAlmostEqual(v["e0123i"], 30.0)

        v = mv2 * mv

        self.assertEqual(v.size(), 5)
        self.assertAlmostEqual(v["e123"], -30.0)
        self.assertAlmostEqual(v["e12i"], -18.0)
        self.assertAlmostEqual(v["e13i"], 12.0)
        self.assertAlmostEqual(v["e23i"], -6.0)
        self.assertAlmostEqual(v["e0123i"], 30.0)

    def test_multiplicationOfPythonMultivectors(self):
        mv = Multivector(["e1", "e2", "e3", "ei", "e0"], [1.0, 2.0, 3.0, 4.0, 5.0])
        mv2 = Multivector(["e123i"], [6.0])

        v = mv * mv2

        self.assertEqual(v.size(), 5)
        self.assertAlmostEqual(v["e123"], 30.0)
        self.assertAlmostEqual(v["e12i"], 18.0)
        self.assertAlmostEqual(v["e13i"], -12.0)
        self.assertAlmostEqual(v["e23i"], 6.0)
        self.assertAlmostEqual(v["e0123i"], 30.0)

        v = mv2 * mv

        self.assertEqual(v.size(), 5)
        self.assertAlmostEqual(v["e123"], -30.0)
        self.assertAlmostEqual(v["e12i"], -18.0)
        self.assertAlmostEqual(v["e13i"], 12.0)
        self.assertAlmostEqual(v["e23i"], -6.0)
        self.assertAlmostEqual(v["e0123i"], 30.0)

    def test_multiplicationOfPythonMultivectorsUsingHelpers(self):
        mv = Multivector.create(
            ["e1", "e2", "e3", "ei", "e0"], [1.0, 2.0, 3.0, 4.0, 5.0]
        )
        mv2 = Multivector.create(["e123i"], [6.0])

        v = mv * mv2

        self.assertEqual(v.size(), 5)
        self.assertAlmostEqual(v["e123"], 30.0)
        self.assertAlmostEqual(v["e12i"], 18.0)
        self.assertAlmostEqual(v["e13i"], -12.0)
        self.assertAlmostEqual(v["e23i"], 6.0)
        self.assertAlmostEqual(v["e0123i"], 30.0)

        v = mv2 * mv

        self.assertEqual(v.size(), 5)
        self.assertAlmostEqual(v["e123"], -30.0)
        self.assertAlmostEqual(v["e12i"], -18.0)
        self.assertAlmostEqual(v["e13i"], 12.0)
        self.assertAlmostEqual(v["e23i"], -6.0)
        self.assertAlmostEqual(v["e0123i"], 30.0)

    def test_innerProductOfCppMultivectors(self):
        mv = Multivector_e1e2e3eie0([1.0, 2.0, 3.0, 4.0, 5.0])
        mv2 = Multivector_e123i([6.0])

        v = mv | mv2

        self.assertEqual(v.size(), 4)
        self.assertAlmostEqual(v["e123"], 30.0)
        self.assertAlmostEqual(v["e12i"], 18.0)
        self.assertAlmostEqual(v["e13i"], -12.0)
        self.assertAlmostEqual(v["e23i"], 6.0)

        v = mv2 | mv

        self.assertEqual(v.size(), 4)
        self.assertAlmostEqual(v["e123"], -30.0)
        self.assertAlmostEqual(v["e12i"], -18.0)
        self.assertAlmostEqual(v["e13i"], 12.0)
        self.assertAlmostEqual(v["e23i"], -6.0)

    def test_innerProductOfPythonMultivectors(self):
        mv = Multivector(["e1", "e2", "e3", "ei", "e0"], [1.0, 2.0, 3.0, 4.0, 5.0])
        mv2 = Multivector(["e123i"], [6.0])

        v = mv | mv2

        self.assertEqual(v.size(), 4)
        self.assertAlmostEqual(v["e123"], 30.0)
        self.assertAlmostEqual(v["e12i"], 18.0)
        self.assertAlmostEqual(v["e13i"], -12.0)
        self.assertAlmostEqual(v["e23i"], 6.0)

        v = mv2 | mv

        self.assertEqual(v.size(), 4)
        self.assertAlmostEqual(v["e123"], -30.0)
        self.assertAlmostEqual(v["e12i"], -18.0)
        self.assertAlmostEqual(v["e13i"], 12.0)
        self.assertAlmostEqual(v["e23i"], -6.0)

    def test_innerProductOfPythonMultivectorsUsingHelpers(self):
        mv = Multivector.create(
            ["e1", "e2", "e3", "ei", "e0"], [1.0, 2.0, 3.0, 4.0, 5.0]
        )
        mv2 = Multivector.create(["e123i"], [6.0])

        v = mv | mv2

        self.assertEqual(v.size(), 4)
        self.assertAlmostEqual(v["e123"], 30.0)
        self.assertAlmostEqual(v["e12i"], 18.0)
        self.assertAlmostEqual(v["e13i"], -12.0)
        self.assertAlmostEqual(v["e23i"], 6.0)

        v = mv2 | mv

        self.assertEqual(v.size(), 4)
        self.assertAlmostEqual(v["e123"], -30.0)
        self.assertAlmostEqual(v["e12i"], -18.0)
        self.assertAlmostEqual(v["e13i"], 12.0)
        self.assertAlmostEqual(v["e23i"], -6.0)

    def test_outerProductOfCppMultivectors(self):
        mv = Multivector_e1e2e3eie0([1.0, 2.0, 3.0, 4.0, 5.0])
        mv2 = Multivector_e123i([6.0])

        v = mv ^ mv2

        self.assertEqual(v.size(), 1)
        self.assertAlmostEqual(v["e0123i"], 30.0)

        v = mv2 ^ mv

        self.assertEqual(v.size(), 1)
        self.assertAlmostEqual(v["e0123i"], 30.0)

    def test_outerProductOfPythonMultivectors(self):
        mv = Multivector(["e1", "e2", "e3", "ei", "e0"], [1.0, 2.0, 3.0, 4.0, 5.0])
        mv2 = Multivector(["e123i"], [6.0])

        v = mv ^ mv2

        self.assertEqual(v.size(), 1)
        self.assertAlmostEqual(v["e0123i"], 30.0)

        v = mv2 ^ mv

        self.assertEqual(v.size(), 1)
        self.assertAlmostEqual(v["e0123i"], 30.0)

    def test_outerProductOfPythonMultivectorsUsingHelpers(self):
        mv = Multivector.create(
            ["e1", "e2", "e3", "ei", "e0"], [1.0, 2.0, 3.0, 4.0, 5.0]
        )
        mv2 = Multivector.create(["e123i"], [6.0])

        v = mv ^ mv2

        self.assertEqual(v.size(), 1)
        self.assertAlmostEqual(v["e0123i"], 30.0)

        v = mv2 ^ mv

        self.assertEqual(v.size(), 1)
        self.assertAlmostEqual(v["e0123i"], 30.0)

    def test_divisionByScalar(self):
        mv = Multivector_e1e2e3eie0([1.0, 2.0, 3.0, 4.0, 5.0])

        mv /= 2.0

        self.assertAlmostEqual(mv["e1"], 0.5)
        self.assertAlmostEqual(mv["e2"], 1.0)
        self.assertAlmostEqual(mv["e3"], 1.5)
        self.assertAlmostEqual(mv["ei"], 2.0)
        self.assertAlmostEqual(mv["e0"], 2.5)

    def test_addition(self):
        mv = Multivector_e1e2e3eie0([1.0, 2.0, 3.0, 4.0, 5.0])
        mv2 = Multivector_e1e2e3eie0([10.0, 20.0, 30.0, 40.0, 50.0])

        mv += mv2

        self.assertAlmostEqual(mv["e1"], 11.0)
        self.assertAlmostEqual(mv["e2"], 22.0)
        self.assertAlmostEqual(mv["e3"], 33.0)
        self.assertAlmostEqual(mv["ei"], 44.0)
        self.assertAlmostEqual(mv["e0"], 55.0)

    def test_addition2(self):
        mv = Multivector_e1e2e3eie0([1.0, 2.0, 3.0, 4.0, 5.0])
        mv2 = Multivector_e123i([6.0])

        v = mv + mv2

        self.assertAlmostEqual(v["e1"], 1.0)
        self.assertAlmostEqual(v["e2"], 2.0)
        self.assertAlmostEqual(v["e3"], 3.0)
        self.assertAlmostEqual(v["ei"], 4.0)
        self.assertAlmostEqual(v["e0"], 5.0)
        self.assertAlmostEqual(v["e123i"], 6.0)

    def test_additionOfPythonMultivectors(self):
        mv = Multivector(["e1", "e2", "e3", "ei", "e0"], [1.0, 2.0, 3.0, 4.0, 5.0])
        mv2 = Multivector(
            ["e1", "e2", "e3", "ei", "e0"], [10.0, 20.0, 30.0, 40.0, 50.0]
        )

        mv += mv2

        self.assertAlmostEqual(mv["e1"], 11.0)
        self.assertAlmostEqual(mv["e2"], 22.0)
        self.assertAlmostEqual(mv["e3"], 33.0)
        self.assertAlmostEqual(mv["ei"], 44.0)
        self.assertAlmostEqual(mv["e0"], 55.0)

    def test_substraction(self):
        mv = Multivector_e1e2e3eie0([1.0, 2.0, 3.0, 4.0, 5.0])
        mv2 = Multivector_e123i([6.0])

        v = mv - mv2

        self.assertAlmostEqual(v["e1"], 1.0)
        self.assertAlmostEqual(v["e2"], 2.0)
        self.assertAlmostEqual(v["e3"], 3.0)
        self.assertAlmostEqual(v["ei"], 4.0)
        self.assertAlmostEqual(v["e0"], 5.0)
        self.assertAlmostEqual(v["e123i"], -6.0)

    def test_setParameters(self):
        mv = Multivector_e1e2e3eie0()

        mv.setParameters([1.0, 2.0, 3.0, 4.0, 5.0])

        self.assertAlmostEqual(mv["e1"], 1.0)
        self.assertAlmostEqual(mv["e2"], 2.0)
        self.assertAlmostEqual(mv["e3"], 3.0)
        self.assertAlmostEqual(mv["ei"], 4.0)
        self.assertAlmostEqual(mv["e0"], 5.0)

    def test_getVector(self):
        mv = Multivector_e1e2e3eie0([1.0, 2.0, 3.0, 4.0, 5.0])

        vector = mv.vector()

        self.assertTrue(isinstance(vector, np.ndarray))
        self.assertEqual(vector.shape, (5,))

        self.assertAlmostEqual(vector[0], 1.0)
        self.assertAlmostEqual(vector[1], 2.0)
        self.assertAlmostEqual(vector[2], 3.0)
        self.assertAlmostEqual(vector[3], 4.0)
        self.assertAlmostEqual(vector[4], 5.0)

    def test_getReverse(self):
        mv = Multivector_e23e13e12([1.0, 2.0, 3.0])

        reverse = mv.reverse()

        self.assertTrue(isinstance(reverse, type(mv)))

        self.assertAlmostEqual(reverse["e23"], -1.0)
        self.assertAlmostEqual(reverse["e13"], -2.0)
        self.assertAlmostEqual(reverse["e12"], -3.0)

    def test_getInverse(self):
        mv = Multivector_e23e13e12([1.0, 2.0, 3.0])

        inverse = mv.inverse()

        self.assertTrue(isinstance(inverse, type(mv)))

        self.assertAlmostEqual(inverse["e23"], -0.07142857)
        self.assertAlmostEqual(inverse["e13"], -0.14285714)
        self.assertAlmostEqual(inverse["e12"], -0.21428571)

    def test_getDual(self):
        mv = Multivector_e1e2e3eie0([1.0, 2.0, 3.0, 4.0, 5.0])

        dual = mv.dual()

        self.assertTrue(isinstance(dual, Multivector_e123ie0123e012ie023ie013i))

        self.assertAlmostEqual(dual["e123i"], -4.0)
        self.assertAlmostEqual(dual["e0123"], -5.0)
        self.assertAlmostEqual(dual["e012i"], -3.0)
        self.assertAlmostEqual(dual["e023i"], -1.0)
        self.assertAlmostEqual(dual["e013i"], 2.0)

    def test_setBlade(self):
        mv = Multivector_e1e2e3eie0()

        mv.set_e2(1.0)

        self.assertAlmostEqual(mv["e1"], 0.0)
        self.assertAlmostEqual(mv["e2"], 1.0)
        self.assertAlmostEqual(mv["e3"], 0.0)
        self.assertAlmostEqual(mv["ei"], 0.0)
        self.assertAlmostEqual(mv["e0"], 0.0)

    def test_getNorm(self):
        mv = Multivector_e1e2e3eie0([1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertAlmostEqual(mv.norm(), 5.0990195136)

    def test_getSquaredNorm(self):
        mv = Multivector_e1e2e3eie0([1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertAlmostEqual(mv.squaredNorm(), -26.0)

    def test_getSignedNorm(self):
        mv = Multivector_e1e2e3eie0([1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertAlmostEqual(mv.signedNorm(), -5.0990195136)

    def test_normalize(self):
        mv = Multivector_e1e2e3eie0([1.0, 2.0, 3.0, 4.0, 5.0])

        mv.normalize()

        self.assertAlmostEqual(mv["e1"], 0.1961161351)
        self.assertAlmostEqual(mv["e2"], 0.3922322703)
        self.assertAlmostEqual(mv["e3"], 0.5883484054)
        self.assertAlmostEqual(mv["ei"], 0.7844645406)
        self.assertAlmostEqual(mv["e0"], 0.9805806757)

    def test_getNormalizedCopy(self):
        mv = Multivector_e1e2e3eie0([1.0, 2.0, 3.0, 4.0, 5.0])

        mv2 = mv.normalized()

        self.assertAlmostEqual(mv2["e1"], 0.1961161351)
        self.assertAlmostEqual(mv2["e2"], 0.3922322703)
        self.assertAlmostEqual(mv2["e3"], 0.5883484054)
        self.assertAlmostEqual(mv2["ei"], 0.7844645406)
        self.assertAlmostEqual(mv2["e0"], 0.9805806757)

        self.assertAlmostEqual(mv["e1"], 1.0)
        self.assertAlmostEqual(mv["e2"], 2.0)
        self.assertAlmostEqual(mv["e3"], 3.0)
        self.assertAlmostEqual(mv["ei"], 4.0)
        self.assertAlmostEqual(mv["e0"], 5.0)

    def test_randomCreation(self):
        # We can only check that it compiles and doesn't throw any exception
        mv = Multivector_e1e2e3eie0.Random()
        v = mv["e1"]  # noqa


class TestMultivectorWrapper(unittest.TestCase):

    def test_unknownBladesCombination(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"])
        self.assertTrue(isinstance(mv, Multivector))

    def test_size(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"])
        self.assertEqual(mv.size(), 4)

    def test_blades(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"])
        blades1 = mv.blades()

        self.assertTrue(isinstance(blades1, list))
        self.assertEqual(len(blades1), 4)

        self.assertEqual(blades1[0], blades.e1)
        self.assertEqual(blades1[1], blades.e2)
        self.assertEqual(blades1[2], blades.e3)
        self.assertEqual(blades1[3], blades.e123)

    def test_hasBlade(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"])

        self.assertTrue(mv.has(blades.e1))
        self.assertTrue(mv.has(blades.e2))
        self.assertTrue(mv.has(blades.e3))
        self.assertTrue(mv.has(blades.e123))
        self.assertFalse(mv.has(blades.e0))

    def test_creation(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"])

        self.assertEqual(mv.size(), 4)
        self.assertAlmostEqual(mv["e1"], 0.0)
        self.assertAlmostEqual(mv["e2"], 0.0)
        self.assertAlmostEqual(mv["e3"], 0.0)
        self.assertAlmostEqual(mv["e123"], 0.0)

    def test_creationWithValue(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], 10)

        self.assertEqual(mv.size(), 4)
        self.assertAlmostEqual(mv["e1"], 10.0)
        self.assertAlmostEqual(mv["e2"], 10.0)
        self.assertAlmostEqual(mv["e3"], 10.0)
        self.assertAlmostEqual(mv["e123"], 10.0)

        self.assertAlmostEqual(mv._mv["scalar"], 0.0)

    def test_creationFromParameters(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])

        self.assertEqual(mv.size(), 4)
        self.assertAlmostEqual(mv["e1"], 1.0)
        self.assertAlmostEqual(mv["e2"], 2.0)
        self.assertAlmostEqual(mv["e3"], 3.0)
        self.assertAlmostEqual(mv["e123"], 4.0)

    def test_creationFromNumpyParameters(self):
        mv = Multivector.create(
            ["e1", "e2", "e3", "e123"], np.array([1.0, 2.0, 3.0, 4.0])
        )

        self.assertEqual(mv.size(), 4)
        self.assertAlmostEqual(mv["e1"], 1.0)
        self.assertAlmostEqual(mv["e2"], 2.0)
        self.assertAlmostEqual(mv["e3"], 3.0)
        self.assertAlmostEqual(mv["e123"], 4.0)

    def test_creationFromIncorrectNumberOfParameters(self):
        with self.assertRaises(TypeError):
            mv = Multivector.create(  # noqa
                ["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0, 5.0]
            )

    def test_creationFromMultivector(self):
        mv = Multivector.create(
            ["e1", "e2", "e3", "e123"], np.array([1.0, 2.0, 3.0, 4.0])
        )
        mv2 = Multivector.clone(mv)

        self.assertEqual(mv2.size(), 4)
        self.assertAlmostEqual(mv2["e1"], 1.0)
        self.assertAlmostEqual(mv2["e2"], 2.0)
        self.assertAlmostEqual(mv2["e3"], 3.0)
        self.assertAlmostEqual(mv2["e123"], 4.0)

    def test_creationWithOutOfOrderBlades(self):
        mv = Multivector.create(["e1", "e2", "e123", "e3"], [1.0, 2.0, 4.0, 3.0])

        self.assertEqual(mv.size(), 4)
        self.assertAlmostEqual(mv["e1"], 1.0)
        self.assertAlmostEqual(mv["e2"], 2.0)
        self.assertAlmostEqual(mv["e3"], 3.0)
        self.assertAlmostEqual(mv["e123"], 4.0)

    def test_creationWithNumericalBlades(self):
        mv = Multivector.create([1, 2, 16, 3], [1.0, 2.0, 4.0, 3.0])

        self.assertEqual(mv.size(), 4)
        self.assertAlmostEqual(mv["e1"], 1.0)
        self.assertAlmostEqual(mv["e2"], 2.0)
        self.assertAlmostEqual(mv["e3"], 3.0)
        self.assertAlmostEqual(mv["e123"], 4.0)

    def test_multiplicationByScalar(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])

        mv *= 2.0

        self.assertEqual(mv.size(), 4)
        self.assertAlmostEqual(mv["e1"], 2.0)
        self.assertAlmostEqual(mv["e2"], 4.0)
        self.assertAlmostEqual(mv["e3"], 6.0)
        self.assertAlmostEqual(mv["e123"], 8.0)

    def test_multiplication(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])
        mv2 = Multivector_e123i([6.0])

        v = mv * mv2

        self.assertTrue(isinstance(v, Multivector))
        self.assertEqual(v.size(), 4)
        self.assertAlmostEqual(v["ei"], -24.0)
        self.assertAlmostEqual(v["e12i"], 18.0)
        self.assertAlmostEqual(v["e13i"], -12.0)
        self.assertAlmostEqual(v["e23i"], 6.0)

        v = mv2 * mv

        self.assertTrue(isinstance(v, Multivector))
        self.assertEqual(v.size(), 4)
        self.assertAlmostEqual(v["ei"], 24.0)
        self.assertAlmostEqual(v["e12i"], -18.0)
        self.assertAlmostEqual(v["e13i"], 12.0)
        self.assertAlmostEqual(v["e23i"], -6.0)

    def test_multiplicationWithEmptyMultivector(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])
        mv2 = Multivector_()

        v = mv * mv2

        self.assertTrue(isinstance(v, Multivector_))

        v = mv2 * mv

        self.assertTrue(isinstance(v, Multivector_))

    def test_innerProduct(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])
        mv2 = Multivector_e123i([6.0])

        v = mv | mv2

        self.assertTrue(isinstance(v, Multivector))
        self.assertEqual(v.size(), 4)
        self.assertAlmostEqual(v["ei"], -24.0)
        self.assertAlmostEqual(v["e12i"], 18.0)
        self.assertAlmostEqual(v["e13i"], -12.0)
        self.assertAlmostEqual(v["e23i"], 6.0)

        v = mv2 | mv

        self.assertTrue(isinstance(v, Multivector))
        self.assertEqual(v.size(), 4)
        self.assertAlmostEqual(v["ei"], 24.0)
        self.assertAlmostEqual(v["e12i"], -18.0)
        self.assertAlmostEqual(v["e13i"], 12.0)
        self.assertAlmostEqual(v["e23i"], -6.0)

    def test_innerProductWithEmptyMultivector(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])
        mv2 = Multivector_()

        v = mv | mv2

        self.assertTrue(isinstance(v, Multivector_))

        v = mv2 | mv

        self.assertTrue(isinstance(v, Multivector_))

    def test_outerProduct(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])
        mv2 = Multivector_scalar([6.0])

        v = mv ^ mv2

        self.assertTrue(isinstance(v, Multivector))
        self.assertEqual(v.size(), 4)
        self.assertAlmostEqual(v["e1"], 6.0)
        self.assertAlmostEqual(v["e2"], 12.0)
        self.assertAlmostEqual(v["e3"], 18.0)
        self.assertAlmostEqual(v["e123"], 24.0)

        v = mv2 ^ mv

        self.assertTrue(isinstance(v, Multivector))
        self.assertEqual(v.size(), 4)
        self.assertAlmostEqual(v["e1"], 6.0)
        self.assertAlmostEqual(v["e2"], 12.0)
        self.assertAlmostEqual(v["e3"], 18.0)
        self.assertAlmostEqual(v["e123"], 24.0)

    def test_outerProduct2(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])
        mv2 = Multivector_e123i([6.0])

        v = mv ^ mv2

        self.assertTrue(isinstance(v, Multivector_))
        self.assertEqual(v.size(), 0)

        v = mv2 ^ mv

        self.assertTrue(isinstance(v, Multivector_))
        self.assertEqual(v.size(), 0)

    def test_outerProductWithEmptyMultivector(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])
        mv2 = Multivector_()

        v = mv ^ mv2

        self.assertTrue(isinstance(v, Multivector_))
        self.assertEqual(v.size(), 0)

        v = mv2 ^ mv

        self.assertTrue(isinstance(v, Multivector_))
        self.assertEqual(v.size(), 0)

    def test_divisionByScalar(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])

        mv /= 2.0

        self.assertEqual(mv.size(), 4)
        self.assertAlmostEqual(mv["e1"], 0.5)
        self.assertAlmostEqual(mv["e2"], 1.0)
        self.assertAlmostEqual(mv["e3"], 1.5)
        self.assertAlmostEqual(mv["e123"], 2.0)

    def test_addition(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])
        mv2 = Multivector.create(["e1", "e2", "e3", "e123"], [10.0, 20.0, 30.0, 40.0])

        mv += mv2

        self.assertEqual(mv.size(), 4)
        self.assertAlmostEqual(mv["e1"], 11.0)
        self.assertAlmostEqual(mv["e2"], 22.0)
        self.assertAlmostEqual(mv["e3"], 33.0)
        self.assertAlmostEqual(mv["e123"], 44.0)

    def test_addition2(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])
        mv2 = Multivector_e123i([6.0])

        v = mv + mv2

        self.assertEqual(v.size(), 5)
        self.assertAlmostEqual(v["e1"], 1.0)
        self.assertAlmostEqual(v["e2"], 2.0)
        self.assertAlmostEqual(v["e3"], 3.0)
        self.assertAlmostEqual(v["e123"], 4.0)
        self.assertAlmostEqual(v["e123i"], 6.0)

    def test_substraction(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])
        mv2 = Multivector_e123i([6.0])

        v = mv - mv2

        self.assertEqual(v.size(), 5)
        self.assertAlmostEqual(v["e1"], 1.0)
        self.assertAlmostEqual(v["e2"], 2.0)
        self.assertAlmostEqual(v["e3"], 3.0)
        self.assertAlmostEqual(v["e123"], 4.0)
        self.assertAlmostEqual(v["e123i"], -6.0)

    def test_setParameters(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"])

        mv.setParameters([1.0, 2.0, 3.0, 4.0])

        self.assertAlmostEqual(mv["e1"], 1.0)
        self.assertAlmostEqual(mv["e2"], 2.0)
        self.assertAlmostEqual(mv["e3"], 3.0)
        self.assertAlmostEqual(mv["e123"], 4.0)

    def test_getVector(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])

        vector = mv.vector()

        self.assertTrue(isinstance(vector, np.ndarray))
        self.assertEqual(vector.shape, (4,))

        self.assertAlmostEqual(vector[0], 1.0)
        self.assertAlmostEqual(vector[1], 2.0)
        self.assertAlmostEqual(vector[2], 3.0)
        self.assertAlmostEqual(vector[3], 4.0)

    def test_getReverse(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])

        reverse = mv.reverse()

        self.assertTrue(isinstance(reverse, Multivector))

        self.assertEqual(reverse.size(), 4)
        self.assertAlmostEqual(reverse["e1"], 1.0)
        self.assertAlmostEqual(reverse["e2"], 2.0)
        self.assertAlmostEqual(reverse["e3"], 3.0)
        self.assertAlmostEqual(reverse["e123"], -4.0)

    def test_getInverse(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])

        inverse = mv.inverse()

        self.assertTrue(isinstance(inverse, Multivector))

        self.assertEqual(inverse.size(), 4)
        self.assertAlmostEqual(inverse["e1"], 0.033333, places=5)
        self.assertAlmostEqual(inverse["e2"], 0.066667, places=5)
        self.assertAlmostEqual(inverse["e3"], 0.1)
        self.assertAlmostEqual(inverse["e123"], -0.133333, places=5)

    def test_getDual(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])

        dual = mv.dual()

        self.assertTrue(isinstance(dual, Multivector))

        self.assertEqual(dual.size(), 4)
        self.assertAlmostEqual(dual["e0i"], 4.0)
        self.assertAlmostEqual(dual["e012i"], -3.0)
        self.assertAlmostEqual(dual["e023i"], -1.0)
        self.assertAlmostEqual(dual["e013i"], 2.0)

    def test_setBlade(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"])

        mv["e2"] = 1.0
        mv[blades.e3] = 2.0

        self.assertAlmostEqual(mv["e1"], 0.0)
        self.assertAlmostEqual(mv["e2"], 1.0)
        self.assertAlmostEqual(mv["e3"], 2.0)
        self.assertAlmostEqual(mv["ei"], 0.0)
        self.assertAlmostEqual(mv["e0"], 0.0)

    def test_getNorm(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])
        self.assertAlmostEqual(mv.norm(), 5.477225575051661)

    def test_getSquaredNorm(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])
        self.assertAlmostEqual(mv.squaredNorm(), 30.0)

    def test_getSignedNorm(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])
        self.assertAlmostEqual(mv.signedNorm(), 5.477225575051661)

    def test_normalize(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])

        mv.normalize()

        self.assertAlmostEqual(mv["e1"], 0.182574, places=6)
        self.assertAlmostEqual(mv["e2"], 0.365148, places=6)
        self.assertAlmostEqual(mv["e3"], 0.547723, places=6)
        self.assertAlmostEqual(mv["e123"], 0.730297, places=6)

    def test_getNormalizedCopy(self):
        mv = Multivector.create(["e1", "e2", "e3", "e123"], [1.0, 2.0, 3.0, 4.0])

        mv2 = mv.normalized()

        self.assertAlmostEqual(mv2["e1"], 0.182574, places=6)
        self.assertAlmostEqual(mv2["e2"], 0.365148, places=6)
        self.assertAlmostEqual(mv2["e3"], 0.547723, places=6)
        self.assertAlmostEqual(mv2["e123"], 0.730297, places=6)

        self.assertAlmostEqual(mv["e1"], 1.0)
        self.assertAlmostEqual(mv["e2"], 2.0)
        self.assertAlmostEqual(mv["e3"], 3.0)
        self.assertAlmostEqual(mv["e123"], 4.0)

    def test_randomCreation(self):
        # We can only check that it compiles and doesn't throw any exception
        mv = Multivector.create(["e1", "e2", "e3", "e123"])
        v = mv["e1"]  # noqa


if __name__ == "__main__":
    unittest.main()
