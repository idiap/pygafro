/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#pragma once

#include <gafro/robot/Manipulator.hpp>
#include <gafro/robot/Link.hpp>
#include <gafro/robot/Joint.hpp>
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
                system2.setName(system.getName());

                const std::vector<std::unique_ptr<gafro::Joint<T>>>& joints = system.getJoints();
                for (auto iter = joints.begin(), iterEnd = joints.end(); iter != iterEnd; ++iter)
                {
                    if ((*iter)->getType() == gafro::Joint<T>::Type::FIXED)
                    {
                        std::unique_ptr<gafro::FixedJoint<T>> joint = std::make_unique<gafro::FixedJoint<T>>();
                        joint->setFrame((*iter)->getFrame());
                        joint->setLimits((*iter)->getLimits());
                        joint->setName((*iter)->getName());
                        system2.addJoint(std::move(joint));
                    }
                    else if ((*iter)->getType() == gafro::Joint<T>::Type::PRISMATIC)
                    {
                        std::unique_ptr<gafro::PrismaticJoint<T>> joint = std::make_unique<gafro::PrismaticJoint<T>>();
                        joint->setFrame((*iter)->getFrame());
                        joint->setLimits((*iter)->getLimits());
                        joint->setName((*iter)->getName());
                        joint->setAxis(static_cast<gafro::PrismaticJoint<T>*>((*iter).get())->getAxis());
                        system2.addJoint(std::move(joint));
                    }
                    else if ((*iter)->getType() == gafro::Joint<T>::Type::REVOLUTE)
                    {
                        std::unique_ptr<gafro::RevoluteJoint<T>> joint = std::make_unique<gafro::RevoluteJoint<T>>();
                        joint->setFrame((*iter)->getFrame());
                        joint->setLimits((*iter)->getLimits());
                        joint->setName((*iter)->getName());
                        joint->setAxis(static_cast<gafro::RevoluteJoint<T>*>((*iter).get())->getAxis());
                        system2.addJoint(std::move(joint));
                    }
                }

                const std::vector<std::unique_ptr<gafro::Link<T>>>& links = system.getLinks();
                for (auto iter = links.begin(), iterEnd = links.end(); iter != iterEnd; ++iter)
                {
                    std::unique_ptr<gafro::Link<T>> link = std::make_unique<gafro::Link<T>>();
                    link->setMass((*iter)->getMass());
                    link->setCenterOfMass((*iter)->getCenterOfMass());
                    link->setInertia((*iter)->getInertia());
                    link->setName((*iter)->getName());
                    link->setAxis((*iter)->getAxis());

                    const gafro::Joint<T>* parentJoint = (*iter)->getParentJoint();
                    if (parentJoint)
                        link->setParentJoint(system2.getJoint(parentJoint->getName()));

                    const std::vector<const gafro::Joint<T> *>& childJoints = (*iter)->getChildJoints();
                    for (auto iter2 = childJoints.begin(), iterEnd2 = childJoints.end(); iter2 != iterEnd2; ++iter2)
                        link->addChildJoint(system2.getJoint((*iter2)->getName()));

                    system2.addLink(std::move(link));
                }

                for (auto iter = joints.begin(), iterEnd = joints.end(); iter != iterEnd; ++iter)
                {
                    gafro::Joint<T>* joint = system2.getJoint((*iter)->getName());
                    joint->setParentLink(system2.getLink((*iter)->getParentLink()->getName()));
                    joint->setChildLink(system2.getLink((*iter)->getChildLink()->getName()));
                }

                manipulator = new gafro::Manipulator<T, dof>(std::move(system2), ee_joint_name);
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

        protected:
            gafro::Manipulator<T, dof>* manipulator;
    };

}  // namespace pygafro
