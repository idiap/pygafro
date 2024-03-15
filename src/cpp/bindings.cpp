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
using namespace gafro;


void init_multivectors(py::module &);
void init_algebra(py::module &);
// void init_optimization(py::module &);
void init_physics(py::module &);
void init_robots(py::module &);
void init_geometric_products(py::module &);
void init_inner_products(py::module &);
void init_outer_products(py::module &);



PYBIND11_MODULE(_pygafro, m) {

    // blades-related constants
    py::module m_blades = m.def_submodule("blades");

    m_blades.attr("scalar") = blades::scalar;
    m_blades.attr("e1") = blades::e1;
    m_blades.attr("e2") = blades::e2;
    m_blades.attr("e3") = blades::e3;
    m_blades.attr("ei") = blades::ei;
    m_blades.attr("e0") = blades::e0;

    m_blades.attr("e23") = blades::e23;
    m_blades.attr("e13") = blades::e13;
    m_blades.attr("e12") = blades::e12;
    m_blades.attr("e1i") = blades::e1i;
    m_blades.attr("e2i") = blades::e2i;
    m_blades.attr("e3i") = blades::e3i;
    m_blades.attr("e01") = blades::e01;
    m_blades.attr("e02") = blades::e02;
    m_blades.attr("e03") = blades::e03;
    m_blades.attr("e0i") = blades::e0i;

    m_blades.attr("e123") = blades::e123;
    m_blades.attr("e12i") = blades::e12i;
    m_blades.attr("e13i") = blades::e13i;
    m_blades.attr("e23i") = blades::e23i;
    m_blades.attr("e012") = blades::e012;
    m_blades.attr("e013") = blades::e013;
    m_blades.attr("e023") = blades::e023;
    m_blades.attr("e01i") = blades::e01i;
    m_blades.attr("e02i") = blades::e02i;
    m_blades.attr("e03i") = blades::e03i;

    m_blades.attr("e123i") = blades::e123i;
    m_blades.attr("e0123") = blades::e0123;
    m_blades.attr("e012i") = blades::e012i;
    m_blades.attr("e023i") = blades::e023i;
    m_blades.attr("e013i") = blades::e013i;

    m_blades.attr("e0123i") = blades::e0123i;


    // Bindings of each sections
    init_multivectors(m);
    init_algebra(m);
    // init_optimization(m);
    init_physics(m);
    init_robots(m);


    // Internal functions
    py::module m_internals = m.def_submodule("internals");

    init_geometric_products(m_internals);
    init_inner_products(m_internals);
    init_outer_products(m_internals);
}
