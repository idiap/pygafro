/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute
 * <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>

#include <gafro/gafro.hpp>

namespace py = pybind11;

#include "multivectors.h"
#include "similarity_transformation_utils.hpp"

void init_similarity_apply_methods(
    py::class_<gafro::SimilarityTransformation<double>,
               Multivector_scalare12e13e23e0ie1ie2ie012ie3ie013ie023ie123i> &);

void init_similarity(py::module &m) {
#include "algebra/types.h"

  py::class_<gafro::SimilarityTransformation<double>,
             Multivector_scalare12e13e23e0ie1ie2ie012ie3ie013ie023ie123i>
      similarity(m, "SimilarityTransformation");

  similarity.def(py::init<>())
      .def(py::init<const gafro::SimilarityTransformation<double> &>())
      .def(py::init<
           const gafro::SimilarityTransformation<double>::Generator &>())
      .def(py::init<
           const gafro::SimilarityTransformation<double>::Parameters &>())
      .def(py::init<
           const Multivector_scalare12e13e23e0ie1ie2ie012ie3ie013ie023ie123i
               &>())
      .def_static("Random", &gafro::SimilarityTransformation<double>::Random)
      .def("log", &gafro::SimilarityTransformation<double>::log)
      .def_static(
          "exp",
          static_cast<gafro::SimilarityTransformation<double> (*)(
              const gafro::SimilarityTransformation<double>::Generator &)>(
              &gafro::SimilarityTransformation<double>::exp))

      .def(
          "__imul__",
          [](gafro::SimilarityTransformation<double> &a,
             const gafro::SimilarityTransformation<double> &b) {
            a = a * b;
            return a;
          },
          py::is_operator())

      .def("apply", &similarity_apply<Circle>)
      .def("apply", &similarity_apply<DirectionVector>)
      .def("apply", &similarity_apply<Line>)
      .def("apply", &similarity_apply<Plane>)
      .def("apply", &similarity_apply<Point>)
      .def("apply", &similarity_apply<PointPair>)
      .def("apply", &similarity_apply<Sphere>)
      .def("apply", &similarity_apply<Vector>);

  init_similarity_apply_methods(similarity);
}
