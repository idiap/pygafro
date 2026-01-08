/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

#pragma once

#include <gafro/robot/Manipulator.hpp>
#include <gafro_robot_descriptions/serialization/FilePath.hpp>
#include <gafro_robot_descriptions/serialization/SystemSerialization.hpp>
#include "utils.hpp"
#include "KinematicChain.hpp"


namespace pygafro
{
    // Allows to use manipulators from Python while avoiding any memory ownership problem and giving
    // access to the System methods (Manipulor inherits PRIVATELY from System)
    template <class T, int dof>
    class Manipulator
    {
        protected:
            Manipulator()
            : manipulator(nullptr)
            {
            }

        public:
            Manipulator(const gafro::System<T>& system, const std::string &ee_joint_name = "endeffector")
            : manipulator(nullptr)
            {
                // Can't create a Manipulator from a System without giving up ownership, which Python can't do, so
                // we have to make a copy of everything...
                gafro::System<T> system2;
                copySystem<T>(system, system2);

                manipulator = new gafro::Manipulator<T, dof>(std::move(system2), ee_joint_name);
            }

            Manipulator(const std::string &yaml_file_path, const std::string &ee_joint_name = "endeffector")
            : manipulator(nullptr)
            {
                manipulator = new gafro::Manipulator<T, dof>(
                    std::move(gafro::SystemSerialization(gafro::FilePath(yaml_file_path)).load().cast<T>()), ee_joint_name
                );
            }

            virtual ~Manipulator()
            {
                delete manipulator;
            }

            inline const gafro::Manipulator<T, dof> *getManipulator() const
            {
                return this->manipulator;
            }

            inline const gafro::System<T> *getSystem() const
            {
                return &manipulator->getSystem();
            }

            inline const Link<T> *getLink(const std::string &name) const
            {
                gafro::Link<T>* link = manipulator->getLink(name);
                if (!link)
                    return nullptr;

                return new Link<T>(&manipulator->getSystem(), link);
            }

            inline const Joint<T> *getJoint(const std::string &name) const
            {
                gafro::Joint<T>* joint = manipulator->getJoint(name);
                if (!joint)
                    return nullptr;

                return new Joint<T>(&manipulator->getSystem(), joint);
            }

            inline typename gafro::Manipulator<T, dof>::Vector getRandomConfiguration() const
            {
                return manipulator->getRandomConfiguration();
            }

            inline typename gafro::Manipulator<T, dof>::Vector getJointLimitsMin() const
            {
                return manipulator->getJointLimitsMin();
            }

            inline typename gafro::Manipulator<T, dof>::Vector getJointLimitsMax() const
            {
                return manipulator->getJointLimitsMax();
            }

            inline const KinematicChain<T>* getEEKinematicChain() const
            {
                return new KinematicChain<T>(&manipulator->getSystem(), manipulator->getEEKinematicChain());
            }

            inline gafro::Motor<T> getEEMotor(const std::vector<T> &position) const
            {
                return manipulator->getEEMotor(typename gafro::Manipulator<T, dof>::Vector(position.data()));
            }

            std::vector<gafro::Motor<T>> getEEAnalyticJacobian(const std::vector<T> &position) const
            {
                gafro::MultivectorMatrix<T, gafro::Motor, 1, dof> jacobian = manipulator->getEEAnalyticJacobian(
                    typename gafro::Manipulator<T, dof>::Vector(position.data())
                );

                std::vector<gafro::Motor<T>> result(dof);
                for (int i = 0; i < dof; ++i)
                    result[i] = jacobian.getCoefficient(0, i);

                return result;
            }

            std::vector<typename gafro::Motor<T>::Generator> getEEGeometricJacobian(const std::vector<T> &position) const
            {
                gafro::MultivectorMatrix<T, gafro::MotorGenerator, 1, dof> jacobian = manipulator->getEEGeometricJacobian(
                    typename gafro::Manipulator<T, dof>::Vector(position.data())
                );

                std::vector<typename gafro::Motor<T>::Generator> result(dof);
                for (int i = 0; i < dof; ++i)
                    result[i] = jacobian.getCoefficient(0, i);

                return result;
            }

            std::vector<typename gafro::Motor<T>::Generator> getGeometricJacobian(
                const std::vector<T> &position, const gafro::Motor<T> &reference
            ) const
            {
                gafro::MultivectorMatrix<T, gafro::MotorGenerator, 1, dof> jacobian = manipulator->getGeometricJacobian(
                    typename gafro::Manipulator<T, dof>::Vector(position.data()), reference
                );

                std::vector<typename gafro::Motor<T>::Generator> result(dof);
                for (int i = 0; i < dof; ++i)
                    result[i] = jacobian.getCoefficient(0, i);

                return result;
            }

            std::vector<typename gafro::Motor<T>::Generator> getGeometricJacobianTimeDerivative(
                const std::vector<T> &position, const std::vector<T> &velocity, const gafro::Motor<T> &reference
            ) const
            {
                gafro::MultivectorMatrix<T, gafro::MotorGenerator, 1, dof> jacobian = manipulator->getGeometricJacobianTimeDerivative(
                    typename gafro::Manipulator<T, dof>::Vector(position.data()),
                    typename gafro::Manipulator<T, dof>::Vector(velocity.data()),
                    reference
                );

                std::vector<typename gafro::Motor<T>::Generator> result(dof);
                for (int i = 0; i < dof; ++i)
                    result[i] = jacobian.getCoefficient(0, i);

                return result;
            }

            std::vector<typename gafro::Motor<T>::Generator> getEEFrameJacobian(const std::vector<T> &position) const
            {
                gafro::MultivectorMatrix<T, gafro::MotorGenerator, 1, dof> jacobian = manipulator->getEEFrameJacobian(
                    typename gafro::Manipulator<T, dof>::Vector(position.data())
                );

                std::vector<typename gafro::Motor<T>::Generator> result(dof);
                for (int i = 0; i < dof; ++i)
                    result[i] = jacobian.getCoefficient(0, i);

                return result;
            }

            Eigen::Matrix<T, 6, 6> getEEVelocityManipulability(const std::vector<T> &position) const
            {
                return manipulator->getEEVelocityManipulability(
                    typename gafro::Manipulator<T, dof>::Vector(position.data())
                );
            }

            Eigen::Matrix<T, 6, 6> getEEForceManipulability(const std::vector<T> &position) const
            {
                return manipulator->getEEForceManipulability(
                    typename gafro::Manipulator<T, dof>::Vector(position.data())
                );
            }

            Eigen::Matrix<T, 6, 6> getEEDynamicManipulability(const std::vector<T> &position) const
            {
                return manipulator->getEEDynamicManipulability(
                    typename gafro::Manipulator<T, dof>::Vector(position.data())
                );
            }

            Eigen::Matrix<T, dof, dof> getEEKinematicNullspaceProjector(const std::vector<T> &position) const
            {
                return manipulator->getEEKinematicNullspaceProjector(
                    typename gafro::Manipulator<T, dof>::Vector(position.data())
                );
            }

            inline typename gafro::Manipulator<T, dof>::Vector getJointTorques(
                const typename gafro::Manipulator<T, dof>::Vector &position,
                const typename gafro::Manipulator<T, dof>::Vector &velocity,
                const typename gafro::Manipulator<T, dof>::Vector &acceleration,
                const T &gravity = 9.81,
                const gafro::Wrench<T> ee_wrench = gafro::Wrench<T>::Zero()) const
            {
                return manipulator->getJointTorques(position, velocity, acceleration, gravity, ee_wrench);
            }

            inline typename gafro::Manipulator<T, dof>::Vector getJointAccelerations(
                const typename gafro::Manipulator<T, dof>::Vector &position,
                const typename gafro::Manipulator<T, dof>::Vector &velocity,
                const typename gafro::Manipulator<T, dof>::Vector &torque) const
            {
                return manipulator->getJointAccelerations(position, velocity, torque);
            }

            Eigen::Matrix<T, dof, dof> getMassMatrix(const std::vector<T> &position) const
            {
                return manipulator->getMassMatrix(
                    typename gafro::Manipulator<T, dof>::Vector(position.data())
                );
            }

        protected:
            gafro::Manipulator<T, dof>* manipulator;
    };

}  // namespace pygafro
