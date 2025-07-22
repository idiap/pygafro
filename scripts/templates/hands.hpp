py::class_<Hand_FINGERSSUFFIX>(m, "Hand_FINGERSSUFFIX")
    .def(py::init<const gafro::System<double>&, const std::array<std::string, NB_FINGERS>&>())
    .def_property_readonly_static("nbFingers", [](py::object) { return NB_FINGERS; })
    .def_property_readonly_static("dof", [](py::object) { return DOF; })
    .def("getSystem", &Hand_FINGERSSUFFIX::getSystem, py::return_value_policy::reference)
    .def("getFingerMotor", &Hand_FINGERSSUFFIX::getFingerMotor)
    .def("getFingerAnalyticJacobian", &Hand_FINGERSSUFFIX::getFingerAnalyticJacobian)
    .def("getFingerGeometricJacobian", py::overload_cast<const unsigned&, const std::vector<double>&>(&Hand_FINGERSSUFFIX::getFingerGeometricJacobian, py::const_))
    .def("getFingerGeometricJacobian", py::overload_cast<const unsigned&, const std::vector<double>&, const Motor&>(&Hand_FINGERSSUFFIX::getFingerGeometricJacobian, py::const_))
    .def("getFingerMotors", &Hand_FINGERSSUFFIX::getFingerMotors)
    .def("getFingerPoints", &Hand_FINGERSSUFFIX::getFingerPoints)
    .def("getAnalyticJacobian", &Hand_FINGERSSUFFIX::getAnalyticJacobian)
    .def("getGeometricJacobian", py::overload_cast<const Eigen::Vector<double, DOF>&>(&Hand_FINGERSSUFFIX::getGeometricJacobian, py::const_))
    .def("getGeometricJacobian", py::overload_cast<const Eigen::Vector<double, DOF>&, const Motor&>(&Hand_FINGERSSUFFIX::getGeometricJacobian, py::const_))
    .def("getMeanMotor", &Hand_FINGERSSUFFIX::getMeanMotor)
    .def("getMeanMotorAnalyticJacobian", &Hand_FINGERSSUFFIX::getMeanMotorAnalyticJacobian)
    .def("getMeanMotorGeometricJacobian", &Hand_FINGERSSUFFIX::getMeanMotorGeometricJacobian)
BEGIN_3_FINGERS
    .def("getFingerCircle", &Hand_FINGERSSUFFIX::getFingerCircle)
    .def("getFingerCircleJacobian", &Hand_FINGERSSUFFIX::getFingerCircleJacobian)
END_3_FINGERS
BEGIN_4_FINGERS
    .def("getFingerSphere", &Hand_FINGERSSUFFIX::getFingerSphere)
    .def("getFingerSphereJacobian", &Hand_FINGERSSUFFIX::getFingerSphereJacobian)
END_4_FINGERS
    ;
