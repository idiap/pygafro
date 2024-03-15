#
# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-only
#

import numpy as np

from .innerproductcayleytable import table as innerproductcayleytable
from .utils import _getProductBlades


class SingleManipulatorDualTarget:

    def __init__(self, arm, tool, target):
        self.arm = arm
        self.tool = tool
        self.target = target

    def getValue(self, x):
        error = self.getError(x)
        return np.inner(error, error)

    def getGradient(self, x):
        jacobian = self.getJacobian(x)
        return jacobian.T @ self.getError(x)

    def getGradientAndHessian(self, x):
        jacobian = self.getJacobian(x)

        gradient = jacobian.T @ self.getError(x)
        hessian = jacobian.T @ jacobian

        return (gradient, hessian)

    def getError(self, x):
        try:
            x = x.tolist()
        except AttributeError:
            pass

        return (
            self.target.dual() | self.arm.getEEMotor(x).apply(self.tool).dual()
        ).vector()

    def getJacobian(self, x):
        try:
            x = x.tolist()
        except AttributeError:
            pass

        motor = self.arm.getEEMotor(x)
        jacobian_ee = self.arm.getEEAnalyticJacobian(x)

        blades = _getProductBlades(
            self.target.blades(), self.tool.blades(), innerproductcayleytable
        )

        jacobian = np.ndarray((len(blades), self.arm.dof))

        mv = self.target.dual() | (
            jacobian_ee[0] * self.tool.dual() * motor.reverse()
            + motor * self.tool.dual() * jacobian_ee[0].reverse()
        )

        mask = [b in blades for b in mv.blades()]

        jacobian[:, 0] = 2.0 * mv.vector()[mask]

        for i in range(1, self.arm.dof):
            jacobian[:, i] = (
                2.0
                * (
                    self.target.dual()
                    | (
                        jacobian_ee[i] * self.tool.dual() * motor.reverse()
                        + motor * self.tool.dual() * jacobian_ee[i].reverse()
                    )
                ).vector()[mask]
            )

        return jacobian
