inline SingleManipulatorTarget_DOF_TOOL_TARGET create_SingleManipulatorTarget_DOF_TOOL_TARGET(
    const Manipulator_DOF* arm, const gafro::TOOL<double>& tool, const gafro::TARGET<double>& target
)
{
    return SingleManipulatorTarget_DOF_TOOL_TARGET(arm->getManipulator(), tool, target);
}


std::tuple<Eigen::Matrix<double, DOF, 1>, Eigen::Matrix<double, DOF, DOF>> SingleManipulatorTarget_DOF_TOOL_TARGET_getGradientAndHessian(
    const SingleManipulatorTarget_DOF_TOOL_TARGET& self, const Eigen::Matrix<double, DOF, 1>& x
)
{
    Eigen::Matrix<double, DOF, 1> gradient;
    Eigen::Matrix<double, DOF, DOF> hessian;

    self.getGradientAndHessian(x, gradient, hessian);

    return std::make_tuple(gradient, hessian);
}

