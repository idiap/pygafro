#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: MPL-2.0
#

import numpy as np

from ._pygafro import Motor
from ._pygafro import MotorLogarithm
from ._pygafro import internals


class _SingleManipulatorMotorCost:

    def __init__(self, arm, target):
        self.arm = arm
        self.target = target

    def getError(self, x):
        try:
            x = x.tolist()
        except AttributeError:
            pass

        return (
            Motor(self.target.reverse() * self.arm.getEEMotor(x))
            .log()
            .evaluate()
            .vector()
        )

    def getGradientAndHessian(self, x):
        try:
            x = x.tolist()
        except AttributeError:
            pass

        error = self.getError(x)

        jacobian = self.getJacobian(x);
        gradient = jacobian.T @ error
        hessian = jacobian.T @ jacobian

        return (gradient, hessian)

    def getJacobian(self, x):
        try:
            x = x.tolist()
        except AttributeError:
            pass

        jacobian_log = MotorLogarithm.jacobian(Motor(
            self.target.reverse() * self.arm.getEEMotor(x)
        ))
        jacobian_ee = self.arm.getEEAnalyticJacobian(x)

        embedded = np.ndarray((jacobian_log.shape[1], self.arm.dof))

        for i in range(0, self.arm.dof):
            embedded[:, i] = (self.target.reverse() * jacobian_ee[i]).vector()

        return jacobian_log @ embedded



def SingleManipulatorMotorCost(arm, target):
    name = 'SingleManipulatorMotorCost_' + str(arm.dof)

    if hasattr(internals, name):
        return getattr(internals, name)(arm, target)

    return _SingleManipulatorMotorCost(arm, target)
