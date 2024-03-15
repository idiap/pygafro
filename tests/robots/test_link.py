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

from pygafro import Inertia
from pygafro import MotorGenerator
from pygafro import System
from pygafro import Translator
from pygafro import TranslatorGenerator


class TestDefaultLink(unittest.TestCase):

    def test_defaults(self):
        system = System()
        link = system.createLink("link1")

        self.assertAlmostEqual(link.getMass(), 0.0)

        centerOfMass = link.getCenterOfMass()

        self.assertTrue(isinstance(centerOfMass, Translator))

        self.assertAlmostEqual(centerOfMass["scalar"], 1.0)
        self.assertAlmostEqual(centerOfMass["e1i"], 0.0)
        self.assertAlmostEqual(centerOfMass["e2i"], 0.0)
        self.assertAlmostEqual(centerOfMass["e3i"], 0.0)

        inertia = link.getInertia()
        self.assertTrue(isinstance(inertia, Inertia))

        self.assertTrue(link.getName() == "link1")
        self.assertTrue(link.getParentJoint() is None)

        children = link.getChildJoints()

        self.assertTrue(isinstance(children, list))
        self.assertTrue(len(children) == 0)

        axis = link.getAxis()

        self.assertTrue(isinstance(axis, MotorGenerator))

        rotorGenerator = axis.getRotorGenerator()
        translatorGenerator = axis.getTranslatorGenerator()

        self.assertAlmostEqual(rotorGenerator.e23(), 0.0)
        self.assertAlmostEqual(rotorGenerator.e13(), 0.0)
        self.assertAlmostEqual(rotorGenerator.e12(), 0.0)

        self.assertAlmostEqual(translatorGenerator.x(), 0.0)
        self.assertAlmostEqual(translatorGenerator.y(), 0.0)
        self.assertAlmostEqual(translatorGenerator.z(), 0.0)

        # self.assertTrue(link.getVisual() is None)

    def test_mass(self):
        system = System()
        link = system.createLink("link1")

        link.setMass(10.0)

        self.assertAlmostEqual(link.getMass(), 10.0)

    def test_centerOfMass(self):
        system = System()
        link = system.createLink("link1")

        generator = TranslatorGenerator([1.0, 2.0, 3.0])
        translator = Translator(generator)

        link.setCenterOfMass(translator)

        centerOfMass = link.getCenterOfMass()

        self.assertTrue(isinstance(centerOfMass, Translator))

        self.assertAlmostEqual(centerOfMass["scalar"], translator["scalar"])
        self.assertAlmostEqual(centerOfMass["e1i"], translator["e1i"])
        self.assertAlmostEqual(centerOfMass["e2i"], translator["e2i"])
        self.assertAlmostEqual(centerOfMass["e3i"], translator["e3i"])

    def test_inertia(self):
        system = System()
        link = system.createLink("link1")

        inertia = Inertia(10.0, np.eye(3))

        link.setInertia(inertia)

        inertia2 = link.getInertia()
        self.assertTrue(isinstance(inertia2, Inertia))

        tensor = inertia2.getTensor()

        self.assertTrue(isinstance(tensor, np.ndarray))
        self.assertTrue(tensor.shape == (6, 6))

        self.assertAlmostEqual(tensor[0, 0], 1.0)
        self.assertAlmostEqual(tensor[0, 1], 0.0)
        self.assertAlmostEqual(tensor[0, 2], 0.0)
        self.assertAlmostEqual(tensor[1, 0], 0.0)
        self.assertAlmostEqual(tensor[1, 1], 1.0)
        self.assertAlmostEqual(tensor[1, 2], 0.0)
        self.assertAlmostEqual(tensor[2, 0], 0.0)
        self.assertAlmostEqual(tensor[2, 1], 0.0)
        self.assertAlmostEqual(tensor[2, 2], 1.0)

        self.assertAlmostEqual(tensor[3, 3], 10.0)
        self.assertAlmostEqual(tensor[3, 4], 0.0)
        self.assertAlmostEqual(tensor[3, 5], 0.0)
        self.assertAlmostEqual(tensor[4, 3], 0.0)
        self.assertAlmostEqual(tensor[4, 4], 10.0)
        self.assertAlmostEqual(tensor[4, 5], 0.0)
        self.assertAlmostEqual(tensor[5, 3], 0.0)
        self.assertAlmostEqual(tensor[5, 4], 0.0)
        self.assertAlmostEqual(tensor[5, 5], 10.0)

        for i in range(3):
            for j in range(3, 6):
                self.assertAlmostEqual(tensor[i, j], 0.0)
                self.assertAlmostEqual(tensor[j, i], 0.0)

    def test_parentJoint(self):
        system = System()
        link = system.createLink("link1")

        joint = system.createRevoluteJoint("joint1")

        link.setParentJoint(joint)
        self.assertTrue(link.getParentJoint() is not None)
        self.assertTrue(link.getParentJoint().getName() == "joint1")

    def test_childJoints(self):
        system = System()
        link = system.createLink("link1")

        joint1 = system.createRevoluteJoint("joint1")
        joint2 = system.createRevoluteJoint("joint2")

        link.addChildJoint(joint1)
        link.addChildJoint(joint2)

        children = link.getChildJoints()

        self.assertTrue(isinstance(children, list))
        self.assertTrue(len(children) == 2)

        self.assertTrue(children[0].getName() in ["joint1", "joint2"])
        self.assertTrue(children[1].getName() in ["joint1", "joint2"])
        self.assertTrue(children[0].getName() != children[1].getName())

    def test_axis(self):
        system = System()
        link = system.createLink("link1")

        generator = MotorGenerator([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        link.setAxis(generator)

        axis = link.getAxis()

        self.assertTrue(isinstance(axis, MotorGenerator))

        rotorGenerator1 = axis.getRotorGenerator()
        translatorGenerator1 = axis.getTranslatorGenerator()

        rotorGenerator2 = generator.getRotorGenerator()
        translatorGenerator2 = generator.getTranslatorGenerator()

        self.assertAlmostEqual(rotorGenerator2.e23(), rotorGenerator1.e23())
        self.assertAlmostEqual(rotorGenerator2.e13(), rotorGenerator1.e13())
        self.assertAlmostEqual(rotorGenerator2.e12(), rotorGenerator1.e12())

        self.assertAlmostEqual(translatorGenerator2.x(), translatorGenerator1.x())
        self.assertAlmostEqual(translatorGenerator2.y(), translatorGenerator1.y())
        self.assertAlmostEqual(translatorGenerator2.z(), translatorGenerator1.z())


if __name__ == "__main__":
    unittest.main()
