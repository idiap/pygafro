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

from pygafro import Inertia
from pygafro import Joint
from pygafro import Motor
from pygafro import MotorGenerator
from pygafro import System
from pygafro import RotorGenerator
from pygafro import Translator
from pygafro import TranslatorGenerator
from pygafro import Quadruped_2


def addLeg(name, system):
    # Create some links
    com = Translator(TranslatorGenerator([0.0, 0.0, 0.0]))

    link1 = system.createLink(name + "_link1")
    link1.setMass(0.1)
    link1.setCenterOfMass(com)
    link1.setInertia(Inertia(0.1, np.eye(3)))
    link1.setAxis(MotorGenerator([1.0, 0.0, 0.0, 0.0, 0.0, 0.0]))

    link2 = system.createLink(name + "_link2")
    link2.setMass(0.1)
    link2.setCenterOfMass(com)
    link2.setInertia(Inertia(0.1, np.eye(3)))
    link2.setAxis(MotorGenerator([1.0, 0.0, 0.0, 0.0, 0.0, 0.0]))

    # Create some joints
    t = Translator(TranslatorGenerator([0.0, 1.0, 0.0]))

    joint1 = system.createRevoluteJoint(name + "_joint1")
    joint1.setAxis(RotorGenerator([1.0, 0.0, 0.0]))
    joint1.setFrame(Motor(t))

    limits = Joint.Limits()
    limits.positionLower = -0.5
    limits.positionUpper = 0.5
    limits.velocity = 1.0
    limits.torque = 1.0

    joint1.setLimits(limits)

    joint2 = system.createRevoluteJoint(name + "_joint2")
    joint2.setAxis(RotorGenerator([1.0, 0.0, 0.0]))
    joint2.setFrame(Motor(t))

    limits = Joint.Limits()
    limits.positionLower = -0.8
    limits.positionUpper = 0.8
    limits.velocity = 1.0
    limits.torque = 1.0

    joint2.setLimits(limits)

    # Setup the hierarchy
    body = system.getLink("body")

    joint1.setParentLink(body)
    body.addChildJoint(joint1)

    joint1.setChildLink(link1)
    link1.setParentJoint(joint1)

    joint2.setParentLink(link1)
    link1.addChildJoint(joint2)

    joint2.setChildLink(link2)
    link2.setParentJoint(joint2)


class TestQuadruped(unittest.TestCase):

    def testAllMethodsRun(self):
        # Create the system
        system = System()

        com = Translator(TranslatorGenerator([0.0, 0.0, 0.0]))

        body = system.createLink("body")
        body.setMass(0.1)
        body.setCenterOfMass(com)
        body.setInertia(Inertia(0.1, np.eye(3)))
        body.setAxis(MotorGenerator([1.0, 0.0, 0.0, 0.0, 0.0, 0.0]))

        addLeg("leg1", system)
        addLeg("leg2", system)
        addLeg("leg3", system)
        addLeg("leg4", system)

        system.finalize()

        # Create the hand
        quadruped = Quadruped_2(system, ["leg1_joint2", "leg2_joint2", "leg3_joint2", "leg4_joint2"])

        position2 = [0] * 2
        position8 = [0] * 8
        motor = Motor()

        # Test that some methods at least run, without testing the results
        result = quadruped.getFootMotor(0, position2)
        result = quadruped.getFootMotors(position8)
        result = quadruped.getFootPoints(position8)
        result = quadruped.getFootSphere(position8)
        # # result = quadruped.getFootSphereJacobian(position8)
        result = quadruped.getFootAnalyticJacobian(0, position2)
        result = quadruped.getFootGeometricJacobian(0, position2)
        result = quadruped.getFootGeometricJacobian(0, position2, motor)
        result = quadruped.getAnalyticJacobian(position8)
        result = quadruped.getGeometricJacobian(position8)
        result = quadruped.getGeometricJacobian(position8, motor)
        result = quadruped.getMeanMotor(position8)
        result = quadruped.getMeanMotorAnalyticJacobian(position8)
        result = quadruped.getMeanMotorGeometricJacobian(position8)


if __name__ == "__main__":
    unittest.main()
