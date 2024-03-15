/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#pragma once

#include <gafro/robot/KinematicChain.hpp>
#include "PrismaticJoint.hpp"
#include "RevoluteJoint.hpp"

namespace pygafro
{

    // Allows to access and manipulate kinematic chains from Python while avoiding any memory
    // ownership problem (Kinematic chains are managed in System using std::unique_ptr)
    template <class T>
    class KinematicChain
    {
      public:
        KinematicChain(gafro::System<T>* system, const std::string& name)
        : system(system), chain(system->getKinematicChain(name))
        {}

        KinematicChain(gafro::System<T>* system, gafro::KinematicChain<T>* chain)
        : system(system), chain(chain)
        {}

        inline int getDoF() const
        {
            return chain->getDoF();
        }

        inline void addActuatedJoint(const Joint<T>* joint)
        {
            chain->addActuatedJoint(joint->getPtr());

            if (system == nullptr)
                system = joint->getSystem();
        }

        inline void addFixedMotor(const gafro::Motor<T> &motor)
        {
            chain->addFixedMotor(motor);
        }

        inline void setFixedMotors(const std::map<int, gafro::Motor<T>> &fixed_motors)
        {
            chain->setFixedMotors(fixed_motors);
        }

        inline const std::map<int, gafro::Motor<T>> &getFixedMotors() const
        {
            return chain->getFixedMotors();
        }

        const std::vector<const Joint<T>*> getActuatedJoints() const
        {
            const auto& joints = chain->getActuatedJoints();

            std::vector<const Joint<T>*> result;
            result.reserve(joints.size());

            for (auto iter = joints.cbegin(), iterEnd = joints.cend(); iter != iterEnd; ++iter)
            {
                switch ((*iter)->getType())
                {
                    case gafro::Joint<T>::Type::PRISMATIC:
                        result.emplace_back(new PrismaticJoint<T>(system, (*iter)->getName()));

                    case gafro::Joint<T>::Type::REVOLUTE:
                        result.emplace_back(new RevoluteJoint<T>(system, (*iter)->getName()));

                    default:
                        break;
                }
            }

            return result;
        }

        gafro::Motor<T> computeFullMotor(const std::vector<T> &position) const
        {
            if (position.size() != chain->getActuatedJoints().size())
                throw std::runtime_error("kinematic chain has not enough dof!");

            gafro::Motor<T> motor;

            for (size_t i = 0; i < position.size(); ++i)
                motor = motor * chain->computeMotor(i, position[i]);

            return motor;
        }

        inline gafro::Motor<T> computeMotor(const int &index, const T &position) const
        {
            return chain->computeMotor(index, position);
        }

        inline gafro::Motor<T> computeMotorDerivative(const int &index, const T &position) const
        {
            return chain->computeMotorDerivative(index, position);
        }

        std::vector<gafro::Motor<T>> computeAnalyticJacobian(const std::vector<T> &position) const
        {
            std::vector<gafro::Motor<T>> jacobian(position.size(), gafro::Motor<T>());

            for (unsigned int i = 0; i < position.size(); ++i)
            {
                gafro::Motor<T> motor = chain->computeMotor(i, position[i]);

                for (unsigned int j = 0; j < position.size(); ++j)
                {
                    if (j == i)
                        jacobian[j] *= chain->computeMotorDerivative(j, position[j]);
                    else
                        jacobian[j] *= motor;
                }
            }

            return jacobian;
        }

        std::vector<typename gafro::Motor<T>::Generator> computeGeometricJacobian(const std::vector<T> &position) const
        {
            std::vector<typename gafro::Motor<T>::Generator> jacobian(position.size(), typename gafro::Motor<T>::Generator());

            gafro::Motor<T> joint_motor;
            const auto& actuated_joints = chain->getActuatedJoints();

            for (unsigned int i = 0; i < position.size(); ++i)
            {
                gafro::Motor<T> motor = joint_motor * actuated_joints[i]->getFrame();

                jacobian[i] = actuated_joints[i]->getCurrentAxis(motor);

                joint_motor *= chain->computeMotor(i, position[i]);
            }

            return jacobian;
        }

        std::vector<typename gafro::Motor<T>::Generator> computeGeometricJacobianBody(const std::vector<T> &position) const
        {
            std::vector<typename gafro::Motor<T>::Generator> jacobian(position.size(), typename gafro::Motor<T>::Generator());

            const auto& actuated_joints = chain->getActuatedJoints();
            const auto& fixed_motors = chain->getFixedMotors();

            gafro::Motor<T> joint_motor = fixed_motors.at(position.size() - 1);

            for (int i = position.size() - 1; i > -1; --i)
            {
                jacobian[i] = actuated_joints[i]->getCurrentAxis(joint_motor.reverse());

                joint_motor = actuated_joints[i]->getMotor(position[i]) * joint_motor;
            }

            return jacobian;
        }

        void finalize()
        {
            chain->finalize();
        }

        inline gafro::KinematicChain<T>* getPtr() const
        {
            return chain;
        }

    private:
      gafro::System<T>* system;
      gafro::KinematicChain<T>* chain;
    };

}  // namespace pygafro
