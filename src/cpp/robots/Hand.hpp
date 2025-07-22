/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

#pragma once

#include <gafro/robot/Quadruped.hpp>
#include "System.hpp"
#include "utils.hpp"

#include <stdexcept>


namespace pygafro
{
    // Allows to use quadrupeds from Python while avoiding any memory ownership problem and giving
    // access to the System methods (Manipulor inherits PRIVATELY from System)
    template <class T, int... fingers>
    class Hand
    {
        public:
            constexpr static int n_fingers = sizeof...(fingers);
            constexpr static int dof = (fingers + ...);
            constexpr static std::array<int, n_fingers> finger_dof = { fingers... };

        protected:
            Hand()
            : hand(nullptr)
            {
            }

        public:
            Hand(const gafro::System<T>& system, const std::array<std::string, n_fingers> &finger_tip_names)
            : hand(nullptr), finger_tip_names(finger_tip_names)
            {
                // Can't create a Quadruped from a System without giving up ownership, which Python can't do, so
                // we have to make a copy of everything...
                gafro::System<T> system2;
                copySystem<T>(system, system2);

                hand = new gafro::Hand<T, fingers...>(std::move(system2), finger_tip_names);
            }

            virtual ~Hand()
            {
                delete hand;
            }

            inline const gafro::Hand<T, fingers...> *getHand() const
            {
                return this->hand;
            }

            inline const gafro::System<T> *getSystem() const
            {
                return &hand->getSystem();
            }

            inline gafro::Motor<T> getFingerMotor(const unsigned &id, const std::vector<T> &position) const
            {
                if (id >= n_fingers)
                    throw std::length_error("Invalid finger id");

                if (position.size() != finger_dof[id])
                    throw std::length_error("Invalid number of DOF");

                switch (id)
                {
                    case 0: return this->template _getFingerMotor<0>(position);
                    case 1: return this->template _getFingerMotor<1>(position);
                    case 2: return this->template _getFingerMotor<2>(position);
                    case 3: return this->template _getFingerMotor<3>(position);
                    case 4: return this->template _getFingerMotor<4>(position);
                }
            }

            std::vector<gafro::Motor<T>> getFingerAnalyticJacobian(const unsigned &id, const std::vector<T> &position) const
            {
                if (id >= n_fingers)
                    throw std::length_error("Invalid finger id");

                if (position.size() != finger_dof[id])
                    throw std::length_error("Invalid number of DOF");

                return computeKinematicChainAnalyticJacobian<T>(&hand->getSystem(), finger_tip_names[id], position);
            }

            std::vector<gafro::MotorGenerator<T>> getFingerGeometricJacobian(const unsigned &id, const std::vector<T> &position) const
            {
                if (id >= n_fingers)
                    throw std::length_error("Invalid finger id");

                if (position.size() != finger_dof[id])
                    throw std::length_error("Invalid number of DOF");

                return computeKinematicChainGeometricJacobian<T>(&hand->getSystem(), finger_tip_names[id], position);
            }

            std::vector<gafro::MotorGenerator<T>> getFingerGeometricJacobian(
                const unsigned &id, const std::vector<T> &position, const gafro::Motor<T> &motor
            ) const
            {
                if (id >= n_fingers)
                    throw std::length_error("Invalid finger id");

                if (position.size() != finger_dof[id])
                    throw std::length_error("Invalid number of DOF");

                auto jacobian = computeKinematicChainGeometricJacobian<T>(&hand->getSystem(), finger_tip_names[id], position);

                std::vector<gafro::MotorGenerator<T>> result;
                gafro::Motor<T> reverse_motor = motor.reverse();
                for (auto iter = jacobian.cbegin(); iter != jacobian.cend(); ++iter)
                    result.emplace_back(reverse_motor.apply(*iter));

                return result;
            }

            std::vector<gafro::Motor<T>> getFingerMotors(const Eigen::Vector<T, dof> &position) const
            {
                gafro::MultivectorMatrix<T, gafro::Motor, 1, n_fingers> motors = hand->getFingerMotors(position);

                std::vector<gafro::Motor<T>> result;
                for (int i = 0; i < n_fingers; ++i)
                    result.emplace_back(motors.getCoefficient(0, i));

                return result;
            }

            std::vector<gafro::Point<T>> getFingerPoints(const Eigen::Vector<T, dof> &position) const
            {
                gafro::MultivectorMatrix<T, gafro::Point, 1, n_fingers> points = hand->getFingerPoints(position);

                std::vector<gafro::Point<T>> result;
                for (int i = 0; i < n_fingers; ++i)
                    result.emplace_back(points.getCoefficient(0, i));

                return result;
            }

            std::vector<gafro::Motor<T>> getAnalyticJacobian(const Eigen::Vector<T, dof> &position) const
            {
                gafro::MultivectorMatrix<T, gafro::Motor, 1, dof> jacobian = hand->getAnalyticJacobian(position);

                std::vector<gafro::Motor<T>> result(dof);
                for (int i = 0; i < dof; ++i)
                    result.emplace_back(jacobian.getCoefficient(0, i));

                return result;
            }

            std::vector<gafro::MotorGenerator<T>> getGeometricJacobian(const Eigen::Vector<T, dof> &position) const
            {
                gafro::MultivectorMatrix<T, gafro::MotorGenerator, 1, dof> jacobian = hand->getGeometricJacobian(position);

                std::vector<gafro::MotorGenerator<T>> result;
                for (int i = 0; i < dof; ++i)
                    result.emplace_back(jacobian.getCoefficient(0, i));

                return result;
            }

            std::vector<gafro::MotorGenerator<T>> getGeometricJacobian(
                const Eigen::Vector<T, dof> &position, const gafro::Motor<T> &motor
            ) const
            {
                gafro::MultivectorMatrix<T, gafro::MotorGenerator, 1, dof> jacobian = hand->getGeometricJacobian(position, motor);

                std::vector<gafro::MotorGenerator<T>> result;
                for (int i = 0; i < dof; ++i)
                    result.emplace_back(jacobian.getCoefficient(0, i));

                return result;
            }

            inline gafro::Motor<T> getMeanMotor(const Eigen::Vector<T, dof> &position) const
            {
                return hand->getMeanMotor(position);
            }

            std::vector<gafro::Motor<T>> getMeanMotorAnalyticJacobian(const Eigen::Vector<T, dof> &position) const
            {
                gafro::MultivectorMatrix<T, gafro::Motor, 1, dof> jacobian = hand->getMeanMotorAnalyticJacobian(position);

                std::vector<gafro::Motor<T>> result(dof);
                for (int i = 0; i < dof; ++i)
                    result.emplace_back(jacobian.getCoefficient(0, i));

                return result;
            }

            std::vector<gafro::MotorGenerator<T>> getMeanMotorGeometricJacobian(const Eigen::Vector<T, dof> &position) const
            {
                gafro::MultivectorMatrix<T, gafro::MotorGenerator, 1, dof> jacobian = hand->getMeanMotorGeometricJacobian(position);

                std::vector<gafro::MotorGenerator<T>> result;
                for (int i = 0; i < dof; ++i)
                    result.emplace_back(jacobian.getCoefficient(0, i));

                return result;
            }

            gafro::Circle<T> getFingerCircle(const Eigen::Vector<T, dof> &position) const
                requires(n_fingers == 3)
            {
                return hand->getFingerCircle(position);
            }

            std::vector<gafro::Circle<T>> getFingerCircleJacobian(const Eigen::Vector<T, dof> &position) const
                requires(n_fingers == 3)
            {
                gafro::MultivectorMatrix<T, gafro::Circle, 1, dof> circles = hand->getFingerCircleJacobian(position);

                std::vector<gafro::Circle<T>> result;
                for (int i = 0; i < dof; ++i)
                    result.emplace_back(circles.getCoefficient(0, i));

                return result;
            }

            gafro::Sphere<T> getFingerSphere(const Eigen::Vector<T, dof> &position) const
                requires(n_fingers == 4)
            {
                return hand->getFingerSphere(position);
            }

            std::vector<gafro::Sphere<T>> getFingerSphereJacobian(const Eigen::Vector<T, dof> &position) const
                requires(n_fingers == 4)
            {
                gafro::MultivectorMatrix<T, gafro::Sphere, 1, dof> spheres = hand->getFingerSphereJacobian(position);

                std::vector<gafro::Sphere<T>> result;
                for (int i = 0; i < dof; ++i)
                    result.emplace_back(spheres.getCoefficient(0, i));

                return result;
            }


        private:
            template<int id>
            requires(id < n_fingers)
            inline gafro::Motor<T> _getFingerMotor(const std::vector<T> &position) const
            {
                Eigen::Vector<T, finger_dof[id]> position2(position.data());
                return hand->template getFingerMotor<id>(position2);
            }

            template<int id>
            requires(id >= n_fingers)
            inline gafro::Motor<T> _getFingerMotor(const std::vector<T> &position) const
            {
                throw std::length_error("Invalid finger id");
            }


        protected:
            gafro::Hand<T, fingers...>* hand;
            std::array<std::string, n_fingers> finger_tip_names;
    };

}  // namespace pygafro
