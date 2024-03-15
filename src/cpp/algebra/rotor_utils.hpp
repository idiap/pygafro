/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#pragma once

// Wrapper for Rotor::apply() that forces the evaluation of the result
template<class Object>
Object rotor_apply(const gafro::Rotor<double>& rotor, const Object &object) {
    return rotor.apply(object).evaluate();
}
