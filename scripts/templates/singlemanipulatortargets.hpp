py::class_<SingleManipulatorTarget_DOF_TOOL_TARGET>(m, "SingleManipulatorTarget_DOF_TOOL_TARGET")
    .def(py::init(&create_SingleManipulatorTarget_DOF_TOOL_TARGET))
    .def("getValue", &SingleManipulatorTarget_DOF_TOOL_TARGET::getValue)
    .def("getGradient", &SingleManipulatorTarget_DOF_TOOL_TARGET::getGradient)
    .def("getJacobian", &SingleManipulatorTarget_DOF_TOOL_TARGET::getJacobian)
    .def("getGradientAndHessian", &SingleManipulatorTarget_DOF_TOOL_TARGET_getGradientAndHessian)
    .def("getError", &SingleManipulatorTarget_DOF_TOOL_TARGET::getError);
