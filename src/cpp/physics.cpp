/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>

#include <gafro/gafro.hpp>


namespace py = pybind11;


void init_physics(py::module &m)
{
    #include "multivectors.h"
    #include "physics_types.h"


    // Inertia class
    py::class_<Inertia>(m, "Inertia")
        .def(py::init<>())
        .def(py::init<const double&, const double&, const double&, const double&, const double&, const double&, const double&>())
        .def(py::init<const double&, const Eigen::Matrix<double, 3, 3>&>())
        .def(py::init<const std::array<gafro::InertiaElement<double>, 6>&>())
        .def("transform", &Inertia::transform)
        .def("inverseTransform", &Inertia::inverseTransform)
        .def("getElement23", &Inertia::getElement23)
        .def("getElement13", &Inertia::getElement13)
        .def("getElement12", &Inertia::getElement12)
        .def("getElement01", &Inertia::getElement01)
        .def("getElement02", &Inertia::getElement02)
        .def("getElement03", &Inertia::getElement03)
        .def("getTensor", py::overload_cast<>(&Inertia::getTensor, py::const_))
        .def_static("Zero", &Inertia::Zero)
        .def("__iadd__", &Inertia::operator+=, py::is_operator())
        .def("__add__", &Inertia::operator+, py::is_operator())
        .def("__call__", &Inertia::operator(), py::is_operator());


    // Twist class
    py::class_<Twist, Multivector_e23e13e12e1ie2ie3i>(m, "Twist")
        .def(py::init<>())
        .def(py::init<const Multivector_e23e13e12e1ie2ie3i&>())
        .def(py::init<const Multivector_e23e13e12e1ie2ie3i::Parameters&>())
        .def("multivector", [](Twist &self) {
            return Multivector_e23e13e12e1ie2ie3i(self.multivector());
        })
        .def("getAngular", &Twist::getAngular)
        .def("getLinear", &Twist::getLinear)
        .def("transform", &Twist::transform)
        .def("commute", &Twist::commute)
        .def("__iadd__", [](Twist &a, const Twist &b) {
            return a += b;
        }, py::is_operator());


    // Wrench class
    py::class_<Wrench, Multivector_e23e13e12e01e02e03>(m, "Wrench")
        .def(py::init<>())
        .def(py::init<const Multivector_e23e13e12e01e02e03&>())
        .def(py::init<const Multivector_e23e13e12e01e02e03::Parameters&>())
        .def("multivector", [](Wrench &self) {
            return Multivector_e23e13e12e01e02e03(self.multivector());
        })
        .def("transform", &Wrench::transform)
        // .def("commute", &Twist::commute)
        .def("__iadd__", [](Wrench &a, const Wrench &b) {
            return a += b;
        }, py::is_operator())
        .def("__isub__", [](Wrench &a, const Wrench &b) {
            return a -= b;
        }, py::is_operator())
        .def("__sub__", [](const Wrench &a, const Wrench &b) {
            return a - b;
        }, py::is_operator());

}
