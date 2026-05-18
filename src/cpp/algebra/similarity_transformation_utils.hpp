/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute
 * <contact@idiap.ch>
 *
 * SPDX-FileContributor: Tobias Löw <tobias.loew@idiap.ch>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

#pragma once

// Wrapper for SimilarityTransformation::apply() that forces the evaluation of
// the result
template <class Object>
Object
similarity_apply(const gafro::SimilarityTransformation<double> &similarity,
                 const Object &object) {
  return similarity.apply(object).evaluate();
}
