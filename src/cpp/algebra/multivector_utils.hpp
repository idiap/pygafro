/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#pragma once


// Wrapper for *::reverse() that forces the evaluation of the result
template<class Object>
Object evaluated_reverse(const Object& mv) {
    return mv.reverse().evaluate();
}


// Wrapper for *::inverse() that forces the evaluation of the result
template<class Object>
Object evaluated_inverse(const Object& mv) {
    return mv.inverse().evaluate();
}


// Wrapper for *::dual() that forces the evaluation of the result
template<class Object>
auto evaluated_dual(const Object& mv) {
    return mv.dual().evaluate();
}
