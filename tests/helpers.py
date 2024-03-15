#! /usr/bin/env python3

#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

import numpy as np

from pygafro import Inertia
from pygafro import Joint
from pygafro import Motor
from pygafro import MotorGenerator
from pygafro import RotorGenerator
from pygafro import System
from pygafro import Translator
from pygafro import TranslatorGenerator
from pygafro import createManipulator


def createManipulatorWith3Joints():
    return createManipulator(createSystemWith3Joints(), 3, "joint3")


def createSystemWith3Joints():
    # Create the system
    system = System()

    # Create some links
    com = Translator(TranslatorGenerator([0.0, 0.0, 0.0]))

    link1 = system.createLink("link1")
    link1.setMass(0.1)
    link1.setCenterOfMass(com)
    link1.setInertia(Inertia(0.1, np.eye(3)))
    link1.setAxis(MotorGenerator([0.0, 0.0, 1.0, 0.0, 0.0, 0.0]))

    link2 = system.createLink("link2")
    link2.setMass(0.1)
    link2.setCenterOfMass(com)
    link2.setInertia(Inertia(0.1, np.eye(3)))
    link2.setAxis(MotorGenerator([0.0, 0.0, 1.0, 0.0, 0.0, 0.0]))

    link3 = system.createLink("link3")
    link3.setMass(0.1)
    link3.setCenterOfMass(com)
    link3.setInertia(Inertia(0.1, np.eye(3)))
    link3.setAxis(MotorGenerator([0.0, 0.0, 1.0, 0.0, 0.0, 0.0]))

    link4 = system.createLink("link4")
    link4.setMass(0.1)
    link4.setCenterOfMass(com)
    link4.setInertia(Inertia(0.1, np.eye(3)))
    link4.setAxis(MotorGenerator([0.0, 0.0, 1.0, 0.0, 0.0, 0.0]))

    # Create some joints
    t = Translator(TranslatorGenerator([0.0, 1.0, 0.0]))

    joint1 = system.createRevoluteJoint("joint1")
    joint1.setAxis(RotorGenerator([0.0, 0.0, 1.0]))
    joint1.setFrame(Motor(t))

    limits = Joint.Limits()
    limits.positionLower = -0.5
    limits.positionUpper = 0.5
    limits.velocity = 1.0
    limits.torque = 1.0

    joint1.setLimits(limits)

    joint2 = system.createRevoluteJoint("joint2")
    joint2.setAxis(RotorGenerator([0.0, 0.0, 1.0]))
    joint2.setFrame(Motor(t))

    limits = Joint.Limits()
    limits.positionLower = -0.8
    limits.positionUpper = 0.8
    limits.velocity = 1.0
    limits.torque = 1.0

    joint2.setLimits(limits)

    joint3 = system.createRevoluteJoint("joint3")
    joint3.setAxis(RotorGenerator([0.0, 0.0, 1.0]))
    joint3.setFrame(Motor(t))

    limits = Joint.Limits()
    limits.positionLower = -0.8
    limits.positionUpper = 0.8
    limits.velocity = 1.0
    limits.torque = 1.0

    joint3.setLimits(limits)

    joint1.setParentLink(link1)
    link1.addChildJoint(joint1)

    joint1.setChildLink(link2)
    link2.setParentJoint(joint1)

    joint2.setParentLink(link2)
    link2.addChildJoint(joint2)

    joint2.setChildLink(link3)
    link3.setParentJoint(joint2)

    joint3.setParentLink(link3)
    link3.addChildJoint(joint3)

    joint3.setChildLink(link4)
    link4.setParentJoint(joint3)

    return system
