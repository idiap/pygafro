py::class_<SingleManipulatorDualTarget_DOF_TOOL_TARGET>(m, "SingleManipulatorDualTarget_DOF_TOOL_TARGET")
    .def(py::init(&create_SingleManipulatorDualTarget_DOF_TOOL_TARGET))
    .def("getValue", &SingleManipulatorDualTarget_DOF_TOOL_TARGET::getValue)
    .def("getGradient", &SingleManipulatorDualTarget_DOF_TOOL_TARGET::getGradient)
    .def("getJacobian", &SingleManipulatorDualTarget_DOF_TOOL_TARGET::getJacobian)
    .def("getGradientAndHessian", &SingleManipulatorDualTarget_DOF_TOOL_TARGET_getGradientAndHessian)
    .def("getError", &SingleManipulatorDualTarget_DOF_TOOL_TARGET::getError);
