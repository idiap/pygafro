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
from pygafro import Hand_3_3_3
from pygafro import Hand_3_3_3_3


def addFinger(name, system):
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

    link3 = system.createLink(name + "_link3")
    link3.setMass(0.1)
    link3.setCenterOfMass(com)
    link3.setInertia(Inertia(0.1, np.eye(3)))
    link3.setAxis(MotorGenerator([1.0, 0.0, 0.0, 0.0, 0.0, 0.0]))

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

    joint3 = system.createRevoluteJoint(name + "_joint3")
    joint3.setAxis(RotorGenerator([1.0, 0.0, 0.0]))
    joint3.setFrame(Motor(t))
    joint3.setLimits(limits)

    # Setup the hierarchy
    palm = system.getLink("palm")

    joint1.setParentLink(palm)
    palm.addChildJoint(joint1)

    joint1.setChildLink(link1)
    link1.setParentJoint(joint1)

    joint2.setParentLink(link1)
    link1.addChildJoint(joint2)

    joint2.setChildLink(link2)
    link2.setParentJoint(joint2)

    joint3.setParentLink(link2)
    link2.addChildJoint(joint3)

    joint3.setChildLink(link3)
    link3.setParentJoint(joint3)



class TestHandWith4Fingers(unittest.TestCase):

    def testAllMethodsRun(self):
        # Create the system
        system = System()

        com = Translator(TranslatorGenerator([0.0, 0.0, 0.0]))

        palm = system.createLink("palm")
        palm.setMass(0.1)
        palm.setCenterOfMass(com)
        palm.setInertia(Inertia(0.1, np.eye(3)))
        palm.setAxis(MotorGenerator([1.0, 0.0, 0.0, 0.0, 0.0, 0.0]))

        addFinger("finger1", system)
        addFinger("finger2", system)
        addFinger("finger3", system)
        addFinger("finger4", system)

        system.finalize()

        # Create the hand
        hand = Hand_3_3_3_3(system, ["finger1_joint3", "finger2_joint3", "finger3_joint3", "finger4_joint3"])

        position3 = [0] * 3
        position12 = [0] * 12
        motor = Motor()

        # Test that some methods at least run, without testing the results
        result = hand.getFingerMotor(0, position3)
        result = hand.getFingerAnalyticJacobian(0, position3)
        result = hand.getFingerGeometricJacobian(0, position3)
        result = hand.getFingerGeometricJacobian(0, position3, motor)
        result = hand.getFingerMotors(position12)
        result = hand.getFingerPoints(position12)
        result = hand.getAnalyticJacobian(position12)
        result = hand.getGeometricJacobian(position12)
        result = hand.getGeometricJacobian(position12, motor)
        result = hand.getMeanMotor(position12)
        result = hand.getMeanMotorAnalyticJacobian(position12)
        result = hand.getMeanMotorGeometricJacobian(position12)
        result = hand.getFingerSphere(position12)
        result = hand.getFingerSphereJacobian(position12)



class TestHandWith3Fingers(unittest.TestCase):

    def testAllMethodsRun(self):
        # Create the system
        system = System()

        com = Translator(TranslatorGenerator([0.0, 0.0, 0.0]))

        palm = system.createLink("palm")
        palm.setMass(0.1)
        palm.setCenterOfMass(com)
        palm.setInertia(Inertia(0.1, np.eye(3)))
        palm.setAxis(MotorGenerator([1.0, 0.0, 0.0, 0.0, 0.0, 0.0]))

        addFinger("finger1", system)
        addFinger("finger2", system)
        addFinger("finger3", system)

        system.finalize()

        # Create the hand
        hand = Hand_3_3_3(system, ["finger1_joint3", "finger2_joint3", "finger3_joint3"])

        position3 = [0] * 3
        position9 = [0] * 9
        motor = Motor()

        # Test that some methods at least run, without testing the results
        result = hand.getFingerMotor(0, position3)
        result = hand.getFingerAnalyticJacobian(0, position3)
        result = hand.getFingerGeometricJacobian(0, position3)
        result = hand.getFingerGeometricJacobian(0, position3, motor)
        result = hand.getFingerMotors(position9)
        result = hand.getFingerPoints(position9)
        result = hand.getAnalyticJacobian(position9)
        result = hand.getGeometricJacobian(position9)
        result = hand.getGeometricJacobian(position9, motor)
        result = hand.getMeanMotor(position9)
        result = hand.getMeanMotorAnalyticJacobian(position9)
        result = hand.getMeanMotorGeometricJacobian(position9)
        result = hand.getFingerCircle(position9)
        result = hand.getFingerCircleJacobian(position9)



if __name__ == "__main__":
    unittest.main()
