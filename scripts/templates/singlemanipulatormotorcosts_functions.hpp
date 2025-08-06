inline SingleManipulatorMotorCost_DOF create_SingleManipulatorMotorCost_DOF(
    const Manipulator_DOF* arm, const gafro::Motor<double>& target
)
{
    return SingleManipulatorMotorCost_DOF(arm->getManipulator(), target);
}


std::tuple<Eigen::Matrix<double, DOF, 1>, Eigen::Matrix<double, DOF, DOF>> SingleManipulatorMotorCost_DOF_getGradientAndHessian(
    const SingleManipulatorMotorCost_DOF& self, const Eigen::Matrix<double, DOF, 1>& x
)
{
    Eigen::Matrix<double, DOF, 1> gradient;
    Eigen::Matrix<double, DOF, DOF> hessian;

    self.getGradientAndHessian(x, gradient, hessian);

    return std::make_tuple(gradient, hessian);
}

