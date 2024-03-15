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
#include "motor_utils.hpp"


void init_motor_apply_methods(py::class_<gafro::Motor<double>, Multivector_scalare23e13e12e1ie2ie3ie123i> &);


void init_motor(py::module &m)
{
    #include "algebra/types.h"

    py::class_<Motor, Multivector_scalare23e13e12e1ie2ie3ie123i> motor(m, "Motor");

    motor.def(py::init<>())
         .def(py::init<const Motor&>())
         .def(py::init<const Motor::Generator&>())
         .def(py::init<const Motor::Parameters&>())
         .def(py::init<const Multivector_scalare23e13e12e1ie2ie3ie123i&>())
         .def(py::init<const Translator&>())
         .def(py::init<const Translator&, const Rotor&>())
         .def(py::init<const Rotor&, const Translator&>())
         .def(py::init<const Rotor&>())
         .def("getRotor", &Motor::getRotor)
         .def("getTranslator", &Motor::getTranslator)
         .def("log", &Motor::log)
         .def("logJacobian", &Motor::logJacobian)
         .def_static("Unit", &Motor::Unit)
         .def_static("Random", &Motor::Random)
         .def_static("exp", &Motor::exp)

         .def("__imul__", [](Motor &a, const Motor &b) {
             return a *= b;
         }, py::is_operator())

         .def("apply", &motor_apply<Circle>)
         .def("apply", &motor_apply<DirectionVector>)
         .def("apply", &motor_apply<Line>)
         .def("apply", &motor_apply<Plane>)
         .def("apply", &motor_apply<Point>)
         .def("apply", &motor_apply<PointPair>)
         .def("apply", &motor_apply<Sphere>)
         .def("apply", &motor_apply<Vector>);

     init_motor_apply_methods(motor);
}
