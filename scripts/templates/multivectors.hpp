py::class_<MULTIVECTOR_CLASS_NAME>(m, "MULTIVECTOR_CLASS_NAME")
    .def(py::init<>())
    .def(py::init<const int&>())
    .def(py::init<const MULTIVECTOR_CLASS_NAME::Parameters&>())
    .def(py::init<const MULTIVECTOR_CLASS_NAME&>())

    .def("setParameters", py::overload_cast<const MULTIVECTOR_CLASS_NAME::Parameters&>(&MULTIVECTOR_CLASS_NAME::setParameters))
    .def("vector", py::overload_cast<>(&MULTIVECTOR_CLASS_NAME::vector, py::const_))

    .def("reverse", &evaluated_reverse<MULTIVECTOR_CLASS_NAME>)

BEGIN_DUAL_METHOD
    .def("dual", &evaluated_dual<MULTIVECTOR_CLASS_NAME>)
END_DUAL_METHOD

    .def_static("size", []() { return MULTIVECTOR_CLASS_NAME::size; })
    .def_static("blades", &MULTIVECTOR_CLASS_NAME::blades)
    .def_static("has", &MULTIVECTOR_CLASS_NAME::has)
    .def_static("Random", &MULTIVECTOR_CLASS_NAME::Random)

BEGIN_NORM_METHODS
    .def("inverse", &evaluated_inverse<MULTIVECTOR_CLASS_NAME>)

    .def("norm", &MULTIVECTOR_CLASS_NAME::norm)
    .def("squaredNorm", &MULTIVECTOR_CLASS_NAME::squaredNorm)
    .def("signedNorm", &MULTIVECTOR_CLASS_NAME::signedNorm)
    .def("normalize", &MULTIVECTOR_CLASS_NAME::normalize)
    .def("normalized", &MULTIVECTOR_CLASS_NAME::normalized)
END_NORM_METHODS

    MULTIVECTOR_SET_METHODS
    MULTIVECTOR_GET_METHODS

    .def("__imul__", [](MULTIVECTOR_CLASS_NAME &a, double b) {
        return a *= b;
    }, py::is_operator())

    .def("__itruediv__", [](MULTIVECTOR_CLASS_NAME &a, double b) {
        return a /= b;
    }, py::is_operator())

    .def("__iadd__", [](MULTIVECTOR_CLASS_NAME &a, const MULTIVECTOR_CLASS_NAME &b) {
        return a += b;
    }, py::is_operator())

    .def("__repr__", [](MULTIVECTOR_CLASS_NAME &mv) {
        std::ostringstream s;
        s << mv;
        return s.str();
    }, py::is_operator());
