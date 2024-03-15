/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>

#include <gafro/gafro.hpp>


namespace py = pybind11;

#include "multivectors.h"
#include "rotor_utils.hpp"


void init_rotor_apply_methods(py::class_<gafro::Rotor<double>, Multivector_scalare23e13e12> &);


void init_rotor(py::module &m)
{
    #include "algebra/types.h"

    py::class_<Rotor, Multivector_scalare23e13e12> rotor(m, "Rotor");

    rotor.def(py::init<>())
         .def(py::init<const Rotor::Parameters&>())
         .def(py::init<const Multivector_scalare23e13e12&>())
         .def(py::init<const Rotor::Generator&, const double&>())

         .def_static("fromQuaternion", [](const Eigen::Vector<double, 4>& q) {
             return Rotor::fromQuaternion(Eigen::Quaterniond(q[0], q[1], q[2], q[3]));
         })

         .def("angle", &Rotor::angle)
         .def("log", &Rotor::log)

         .def("quaternion", [](Rotor& self) {
             auto q = self.quaternion();
             return Eigen::Vector<double, 4>(q.w(), q.x(), q.y(), q.z());
         })

         .def("toRotationMatrix", &Rotor::toRotationMatrix)
         .def("scalar", &Rotor::scalar)
         .def("e23", &Rotor::e23)
         .def("e13", &Rotor::e13)
         .def("e12", &Rotor::e12)

         .def_static("exp", [](const Rotor::Generator &generator) {
             return Rotor::exp(generator).evaluate();
         })

         .def("apply", &rotor_apply<Circle>)
         .def("apply", &rotor_apply<DirectionVector>)
         .def("apply", &rotor_apply<Line>)
         .def("apply", &rotor_apply<Plane>)
         .def("apply", &rotor_apply<Point>)
         .def("apply", &rotor_apply<PointPair>)
         .def("apply", &rotor_apply<Sphere>)
         .def("apply", &rotor_apply<Vector>);

     init_rotor_apply_methods(rotor);
}
