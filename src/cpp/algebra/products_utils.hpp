/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#pragma once

#include <gafro/gafro.hpp>


template<class MV>
std::tuple<std::array<bool, 32>, Eigen::Matrix<double, 32, 1>> toTuple(const MV& mv) {
    auto bits = mv.bits().bits;
    Eigen::Matrix<double, 32, 1> parameters = Eigen::Matrix<double, 32, 1>::Zero();
    const auto vector = mv.vector();
    const auto blades = mv.blades();

    for (int i = 0; i < mv.size; ++i)
        parameters(blades[i], 0) = vector[i];

    return std::make_tuple(bits, parameters);
}


template<class M1, class M2>
std::tuple<std::array<bool, 32>, Eigen::Matrix<double, 32, 1>>geometricProduct(const M1& a, const M2& b) {
    return toTuple((a * b).evaluate());
}


template<class M1, class M2>
std::tuple<std::array<bool, 32>, Eigen::Matrix<double, 32, 1>>innerProduct(const M1& a, const M2& b) {
    return toTuple((a | b).evaluate());
}


template<class M1, class M2>
std::tuple<std::array<bool, 32>, Eigen::Matrix<double, 32, 1>>outerProduct(const M1& a, const M2& b) {
    return toTuple((a ^ b).evaluate());
}
