#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

from ._pygafro import *  # noqa: we need to discover at runtime which Manipulator classes were compiled


def createManipulator(system, dof, ee_joint_name):
    class_name = f"Manipulator_{dof}"

    try:
        manipulator_class = globals()[class_name]
        return manipulator_class(system, ee_joint_name)
    except Exception:
        raise TypeError(f"Invalid number of DOF for Manipulator: {dof}")


def _getEEPrimitiveJacobian(manipulator, position, primitive):
    ee_motor = manipulator.getEEMotor(position)
    ee_jacobian = manipulator.getEEAnalyticJacobian(position)

    dof = len(ee_jacobian)
    Primitive = type(primitive)

    blades = Primitive.blades()

    jacobian = []

    for i in range(dof):
        mv = (
            ee_jacobian[i] * primitive * ee_motor.reverse()
            + ee_motor * primitive * ee_jacobian[i].reverse()
        )

        mv.blades = blades
        mv.mask = [b in blades for b in mv._mv.blades()]

        jacobian.append(mv)

    return jacobian


for name in [x for x in globals().keys() if x.startswith("Manipulator_")]:
    globals()[name].getEEPrimitiveJacobian = _getEEPrimitiveJacobian
