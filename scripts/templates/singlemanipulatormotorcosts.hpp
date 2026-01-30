py::class_<SingleManipulatorMotorCost_DOF>(m, "SingleManipulatorMotorCost_DOF")
    .def(py::init(&create_SingleManipulatorMotorCost_DOF))
    .def("getGradientAndHessian", &SingleManipulatorMotorCost_DOF_getGradientAndHessian)
    .def("getJacobian", &SingleManipulatorMotorCost_DOF::getJacobian)
    .def("getError", &SingleManipulatorMotorCost_DOF::getError);
