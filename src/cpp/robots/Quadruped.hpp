/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

#pragma once

#include <gafro/robot/Quadruped.hpp>
#include "utils.hpp"


namespace pygafro
{
    // Allows to use quadrupeds from Python while avoiding any memory ownership problem and giving
    // access to the System methods (Manipulor inherits PRIVATELY from System)
    template <class T, int dof>
    class Quadruped
    {
        protected:
            Quadruped()
            : quadruped(nullptr)
            {
            }

        public:
            Quadruped(const gafro::System<T>& system, const std::array<std::string, 4>& foot_tip_names)
            : quadruped(nullptr)
            {
                // Can't create a Quadruped from a System without giving up ownership, which Python can't do, so
                // we have to make a copy of everything...
                gafro::System<T> system2;
                copySystem<T>(system, system2);

                quadruped = new gafro::Quadruped<T, dof>(std::move(system2), foot_tip_names);
            }

            virtual ~Quadruped()
            {
                delete quadruped;
            }

            inline const gafro::Quadruped<T, dof> *getQuadruped() const
            {
                return this->quadruped;
            }

            inline const gafro::System<T> *getSystem() const
            {
                return &quadruped->getSystem();
            }

            inline gafro::Motor<T> getFootMotor(const unsigned &id, const Eigen::Vector<T, dof> &position) const
            {
                return quadruped->getFootMotor(id, position);
            }

            std::vector<gafro::Motor<T>> getFootMotors(const Eigen::Vector<T, 4 * dof> &position) const
            {
                gafro::MultivectorMatrix<T, gafro::Motor, 1, 4> motors = quadruped->getFootMotors(position);

                std::vector<gafro::Motor<T>> result(4);
                for (int i = 0; i < 4; ++i)
                    result[i] = motors.getCoefficient(0, i);

                return result;
            }

            std::vector<gafro::Point<T>> getFootPoints(const Eigen::Vector<T, 4 * dof> &position) const
            {
                gafro::MultivectorMatrix<T, gafro::Point, 1, 4> points = quadruped->getFootPoints(position);

                std::vector<gafro::Point<T>> result(4);
                for (int i = 0; i < 4; ++i)
                    result[i] = points.getCoefficient(0, i);

                return result;
            }

            inline gafro::Sphere<T> getFootSphere(const Eigen::Vector<T, 4 * dof> &position) const
            {
                return quadruped->getFootSphere(position);
            }

            // std::vector<gafro::Sphere<T>> getFootSphereJacobian(const Eigen::Vector<T, 4 * dof> &position) const requires(4 == 4)
            // {
            //     gafro::MultivectorMatrix<T, gafro::Sphere, 1, 4 * dof> spheres = quadruped->getFootSphereJacobian(position);
            //
            //     std::vector<gafro::Sphere<T>> result(4 * dof);
            //     for (int i = 0; i < 4 * dof; ++i)
            //         result[i] = spheres.getCoefficient(0, i);
            //
            //     return result;
            // }

            std::vector<gafro::Motor<T>> getFootAnalyticJacobian(const unsigned &id, const Eigen::Vector<T, dof> &position) const
            {
                gafro::MultivectorMatrix<T, gafro::Motor, 1, dof> jacobian = quadruped->getFootAnalyticJacobian(id, position);

                std::vector<gafro::Motor<T>> result(dof);
                for (int i = 0; i < dof; ++i)
                    result[i] = jacobian.getCoefficient(0, i);

                return result;
            }

            std::vector<gafro::MotorGenerator<T>> getFootGeometricJacobian(const unsigned &id, const Eigen::Vector<T, dof> &position) const
            {
                gafro::MultivectorMatrix<T, gafro::MotorGenerator, 1, dof> jacobian = quadruped->getFootGeometricJacobian(id, position);

                std::vector<gafro::MotorGenerator<T>> result(dof);
                for (int i = 0; i < dof; ++i)
                    result[i] = jacobian.getCoefficient(0, i);

                return result;
            }

            std::vector<gafro::MotorGenerator<T>> getFootGeometricJacobian(
                const unsigned &id, const Eigen::Vector<T, dof> &position, const gafro::Motor<T> &motor
            ) const
            {
                gafro::MultivectorMatrix<T, gafro::MotorGenerator, 1, dof> jacobian = quadruped->getFootGeometricJacobian(id, position, motor);

                std::vector<gafro::MotorGenerator<T>> result(dof);
                for (int i = 0; i < dof; ++i)
                    result[i] = jacobian.getCoefficient(0, i);

                return result;
            }

            std::vector<gafro::Motor<T>> getAnalyticJacobian(const Eigen::Vector<T, 4 * dof> &position) const
            {
                gafro::MultivectorMatrix<T, gafro::Motor, 1, 4 * dof> jacobian = quadruped->getAnalyticJacobian(position);

                std::vector<gafro::Motor<T>> result(4 * dof);
                for (int i = 0; i < 4 * dof; ++i)
                    result[i] = jacobian.getCoefficient(0, i);

                return result;
            }

            std::vector<gafro::MotorGenerator<T>> getGeometricJacobian(const Eigen::Vector<T, 4 * dof> &position) const
            {
                gafro::MultivectorMatrix<T, gafro::MotorGenerator, 1, 4 * dof> jacobian = quadruped->getGeometricJacobian(position);

                std::vector<gafro::MotorGenerator<T>> result(4 * dof);
                for (int i = 0; i < 4 * dof; ++i)
                    result[i] = jacobian.getCoefficient(0, i);

                return result;
            }

            std::vector<gafro::MotorGenerator<T>> getGeometricJacobian(
                const Eigen::Vector<T, 4 * dof> &position, const gafro::Motor<T> &motor
            ) const
            {
                gafro::MultivectorMatrix<T, gafro::MotorGenerator, 1, 4 * dof> jacobian = quadruped->getGeometricJacobian(position, motor);

                std::vector<gafro::MotorGenerator<T>> result(4 * dof);
                for (int i = 0; i < 4 * dof; ++i)
                    result[i] = jacobian.getCoefficient(0, i);

                return result;
            }

            inline gafro::Motor<T> getMeanMotor(const Eigen::Vector<T, 4 * dof> &position) const
            {
                return quadruped->getMeanMotor(position);
            }

            std::vector<gafro::Motor<T>> getMeanMotorAnalyticJacobian(const Eigen::Vector<T, 4 * dof> &position) const
            {
                gafro::MultivectorMatrix<T, gafro::Motor, 1, 4 * dof> jacobian = quadruped->getMeanMotorAnalyticJacobian(position);

                std::vector<gafro::Motor<T>> result(4 * dof);
                for (int i = 0; i < 4 * dof; ++i)
                    result[i] = jacobian.getCoefficient(0, i);

                // std::vector<gafro::Motor<T>> result;
                // for (int i = 0; i < 4 * dof; ++i)
                //     result.emplace_back(jacobian.getCoefficient(0, i));

                return result;
            }

            std::vector<gafro::MotorGenerator<T>> getMeanMotorGeometricJacobian(const Eigen::Vector<T, 4 * dof> &position) const
            {
                gafro::MultivectorMatrix<T, gafro::MotorGenerator, 1, 4 * dof> jacobian = quadruped->getMeanMotorGeometricJacobian(position);

                std::vector<gafro::MotorGenerator<T>> result(4 * dof);
                for (int i = 0; i < 4 * dof; ++i)
                    result[i] = jacobian.getCoefficient(0, i);

                return result;
            }


        protected:
            gafro::Quadruped<T, dof>* quadruped;
    };

}  // namespace pygafro
