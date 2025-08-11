/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>

#include <gafro/gafro.hpp>


namespace py = pybind11;



template<class T>
const std::string __repr__(T &obj) {
    std::ostringstream s;
    s << obj;
    return s.str();
}


// Helper macros related to expressions
#define DECLARE_EXPRESSION(DERIVED, RESULT)                                             \
    py::class_<gafro::Expression<DERIVED, RESULT>>(m, "Expression_" #DERIVED "_" #RESULT)      \
        .def(py::init<>())                                                              \
        .def("evaluate", &gafro::Expression<DERIVED, RESULT>::evaluate)                        \
        .def("__repr__", &__repr__<gafro::Expression<DERIVED, RESULT>>, py::is_operator());

#define DECLARE_UNARY_EXPRESSION(DERIVED, OPERAND, RESULT)                                                      \
    typedef gafro::UnaryExpression<DERIVED, OPERAND, RESULT> UnaryExpression_##DERIVED;                                \
                                                                                                                \
    typedef gafro::Expression<UnaryExpression_##DERIVED,  RESULT> Expression_UnaryExpression_##DERIVED;                \
                                                                                                                \
    DECLARE_EXPRESSION(UnaryExpression_##DERIVED,  RESULT);                                                     \
                                                                                                                \
    py::class_<UnaryExpression_##DERIVED, Expression_UnaryExpression_##DERIVED>(m, "UnaryExpression_" #DERIVED) \
        .def(py::init<const OPERAND&>());

#define DECLARE_UNARY_EXPRESSION_WITH_NAMES(DERIVED, OPERAND, RESULT, DERIVED_NAME, RESULT_NAME)    \
    typedef DERIVED DERIVED_NAME;                                                                   \
    typedef RESULT RESULT_NAME;                                                                     \
    DECLARE_UNARY_EXPRESSION(DERIVED_NAME, OPERAND, RESULT_NAME)



void init_motor(py::module &m);
void init_rotor(py::module &m);



void init_algebra(py::module &m)
{
    #include "multivectors.h"
    #include "algebra/types.h"


    // Point class
    py::class_<Point, Multivector_e0e1e2e3ei>(m, "Point")
        .def(py::init<>())
        .def(py::init<const Multivector_e0e1e2e3ei&>())
        .def(py::init<const Point::Parameters&>())
        .def(py::init<const double&, const double&, const double&>())
        .def("getEmbeddingJacobian", &Point::getEmbeddingJacobian)
        .def("getEuclideanPoint", &Point::getEuclideanPoint)
        .def_static("X", static_cast<Point (*)(const double&)>(&Point::X))
        .def_static("Y", static_cast<Point (*)(const double&)>(&Point::Y))
        .def_static("Z", static_cast<Point (*)(const double&)>(&Point::Z))
        .def_static("Random", static_cast<Point (*)()>(&Point::Random));


    // Line class
    py::class_<Line, Multivector_e01ie02ie12ie03ie13ie23i>(m, "Line")
        .def(py::init<const Multivector_e01ie02ie12ie03ie13ie23i&>())
        .def(py::init<const Point&, const Point&>())
        .def("getMotor", &Line::getMotor)
        .def_static("X", static_cast<Line (*)()>(&Line::X))
        .def_static("Y", static_cast<Line (*)()>(&Line::Y))
        .def_static("Z", static_cast<Line (*)()>(&Line::Z))
        .def_static("Random", static_cast<Line (*)()>(&Line::Random));


    // PointPair class
    py::class_<PointPair, Multivector_e01e02e12e03e13e23e0ie1ie2ie3i>(m, "PointPair")
        .def(py::init<>())
        .def(py::init<const Multivector_e01e02e12e03e13e23e0ie1ie2ie3i&>())
        .def(py::init<const Point&, const Point&>())
        .def("getPoint1", &PointPair::getPoint1)
        .def("getPoint2", &PointPair::getPoint2);


    // Plane class
    py::class_<Plane, Multivector_e012ie013ie023ie123i>(m, "Plane")
        .def(py::init<const Multivector_e012ie013ie023ie123i&>())
        .def(py::init<const Point&, const Point&, const Point&>())
        .def("getNormal", &Plane::getNormal)
        .def("getMotor", &Plane::getMotor)
        .def_static("XY", static_cast<Plane (*)(const double&)>(&Plane::XY))
        .def_static("XZ", static_cast<Plane (*)(const double&)>(&Plane::XZ))
        .def_static("YZ", static_cast<Plane (*)(const double&)>(&Plane::YZ))
        .def_static("Random", static_cast<Plane (*)()>(&Plane::Random));


    // Circle class
    py::class_<Circle, Multivector_e012e013e023e123e01ie02ie12ie03ie13ie23i>(m, "Circle")
        .def(py::init<const Multivector_e012e013e023e123e01ie02ie12ie03ie13ie23i&>())
        .def(py::init<const Point&, const Point&, const Point&>())
        .def("getCenter", &Circle::getCenter)
        .def("getPlane", &Circle::getPlane)
        .def("getRadius", &Circle::getRadius)
        .def("getMotor", &Circle::getMotor)
        .def_static("Random", static_cast<Circle (*)()>(&Circle::Random))
        .def_static("Unit", static_cast<Circle (*)(const Motor&, const double&)>(&Circle::Unit));


    // Sphere class
    py::class_<Sphere, Multivector_e0123e012ie013ie023ie123i>(m, "Sphere")
        .def(py::init<const Multivector_e0123e012ie013ie023ie123i&>())
        .def(py::init<const Point&, const Point&, const Point&, const Point&>())
        .def(py::init<const Point&, const double&>())
        .def("getRadius", &Sphere::getRadius)
        .def("getCenter", &Sphere::getCenter)
        .def_static("Random", static_cast<Sphere (*)()>(&Sphere::Random));


    // Vector class
    py::class_<Vector, Multivector_e1e2e3>(m, "Vector")
        .def(py::init<>())
        .def(py::init<const Multivector_e1e2e3&>())
        .def(py::init<const Vector::Parameters&>())
        .def(py::init<const double&, const double&, const double&>());


    // DirectionVector class
    py::class_<DirectionVector, Multivector_e1ie2ie3i>(m, "DirectionVector")
        .def(py::init<>())
        .def(py::init<const Multivector_e1ie2ie3i&>())
        .def(py::init<const DirectionVector::Parameters&>())
        .def(py::init<const double&, const double&, const double&>());


    // Translator::Generator class
    py::class_<Translator::Generator, Multivector_e1ie2ie3i>(m, "TranslatorGenerator")
        .def(py::init<>())
        .def(py::init<const Multivector_e1ie2ie3i&>())
        .def(py::init<const Translator::Generator::Parameters&>())
        .def("x", &Translator::Generator::x)
        .def("y", &Translator::Generator::y)
        .def("z", &Translator::Generator::z);


    // Translator class
    py::class_<Translator, Multivector_scalare1ie2ie3i>(m, "Translator")
        .def(py::init<>())
        .def(py::init<const Translator::Generator&>())
        .def("log", &Translator::log)
        .def("toTranslationVector", &Translator::toTranslationVector)
        .def("toSkewSymmetricMatrix", &Translator::toSkewSymmetricMatrix)
        .def_static("exp", static_cast<Translator (*)(const Translator::Generator&)>(&Translator::exp));


    // Rotor::Generator class
    py::class_<Rotor::Generator, Multivector_e12e13e23>(m, "RotorGenerator")
        .def(py::init<>())
        .def(py::init<const Multivector_e12e13e23&>())
        .def(py::init<const Rotor::Generator::Parameters&>())
        .def("e23", &Rotor::Generator::e23)
        .def("e13", &Rotor::Generator::e13)
        .def("e12", &Rotor::Generator::e12);


    // Rotor class
    init_rotor(m);


    // Rotor::Exponential class
    DECLARE_UNARY_EXPRESSION_WITH_NAMES(Rotor::Exponential, Rotor::Generator, Rotor, Rotor_Exponential, Rotor)

    py::class_<Rotor_Exponential, Expression_UnaryExpression_Rotor_Exponential>(m, "RotorExponential")
        .def(py::init<const Rotor::Generator&>())
        .def("get_scalar", &Rotor::Exponential::get<gafro::blades::scalar>)
        .def("get_e23", &Rotor::Exponential::get<gafro::blades::e23>)
        .def("get_e13", &Rotor::Exponential::get<gafro::blades::e13>)
        .def("get_e12", &Rotor::Exponential::get<gafro::blades::e12>);


    // Motor::Generator
    py::class_<Motor::Generator, Multivector_e12e13e23e1ie2ie3i>(m, "MotorGenerator")
        .def(py::init<>())
        .def(py::init<const Multivector_e12e13e23e1ie2ie3i&>())
        .def(py::init<const Motor::Generator::Parameters&>())
        .def(py::init<const Eigen::Matrix<double, 3, 1>&, const Eigen::Matrix<double, 3, 1>&>())
        .def("getRotorGenerator", &Motor::Generator::getRotorGenerator)
        .def("getTranslatorGenerator", &Motor::Generator::getTranslatorGenerator);


    // Motor class
    init_motor(m);


    // Motor::Logarithm
    DECLARE_UNARY_EXPRESSION_WITH_NAMES(Motor::Logarithm, Motor, Motor::Generator, Motor_Logarithm, Motor_Generator)

    py::class_<Motor_Logarithm, Expression_UnaryExpression_Motor_Logarithm>(m, "MotorLogarithm")
        .def(py::init<const Motor&>())
        .def("get_e23", &Motor::Logarithm::get<gafro::blades::e23>)
        .def("get_e13", &Motor::Logarithm::get<gafro::blades::e13>)
        .def("get_e12", &Motor::Logarithm::get<gafro::blades::e12>)
        .def("get_e1i", &Motor::Logarithm::get<gafro::blades::e1i>)
        .def("get_e2i", &Motor::Logarithm::get<gafro::blades::e2i>)
        .def("get_e3i", &Motor::Logarithm::get<gafro::blades::e3i>)
        .def_static("jacobian", static_cast<Eigen::Matrix<double, 6, 8> (*)(const Motor&)>(&Motor::Logarithm::getJacobian));


    // Motor::Exponential
    DECLARE_UNARY_EXPRESSION_WITH_NAMES(Motor::Exponential, Motor::Generator, Motor, Motor_Exponential, Motor)

    py::class_<Motor_Exponential, Expression_UnaryExpression_Motor_Exponential>(m, "MotorExponential")
        .def(py::init<const Motor::Generator&>())
        .def("get_scalar", &Motor::Exponential::get<gafro::blades::scalar>)
        .def("get_e23", &Motor::Exponential::get<gafro::blades::e23>)
        .def("get_e13", &Motor::Exponential::get<gafro::blades::e13>)
        .def("get_e12", &Motor::Exponential::get<gafro::blades::e12>)
        .def("get_e1i", &Motor::Exponential::get<gafro::blades::e1i>)
        .def("get_e2i", &Motor::Exponential::get<gafro::blades::e2i>)
        .def("get_e3i", &Motor::Exponential::get<gafro::blades::e3i>)
        .def("get_e123i", &Motor::Exponential::get<gafro::blades::e123i>)
        .def_static("jacobian", static_cast<Eigen::Matrix<double, 8, 6> (*)(const Motor::Generator&)>(&Motor::Exponential::getJacobian));
}
