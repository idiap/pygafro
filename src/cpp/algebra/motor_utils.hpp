/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

#pragma once

// Wrapper for Motor::apply() that forces the evaluation of the result
template<class Object>
Object motor_apply(const gafro::Motor<double>& motor, const Object &object) {
    return motor.apply(object).evaluate();
}
