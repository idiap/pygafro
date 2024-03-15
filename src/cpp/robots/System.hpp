/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#pragma once

#include <gafro/robot/System.hpp>
#include "FixedJoint.hpp"
#include "PrismaticJoint.hpp"
#include "RevoluteJoint.hpp"
#include "Link.hpp"

namespace pygafro
{

    template <class T>
    Joint<T>* createFixedJoint(gafro::System<T>* system, const std::string& name)
    {
        std::unique_ptr<gafro::FixedJoint<T>> joint = std::make_unique<gafro::FixedJoint<T>>();
        joint->setName(name);

        system->addJoint(std::move(joint));

        return new FixedJoint<T>(system, name);
    }

    template <class T>
    Joint<T>* createPrismaticJoint(gafro::System<T>* system, const std::string& name)
    {
        std::unique_ptr<gafro::PrismaticJoint<T>> joint = std::make_unique<gafro::PrismaticJoint<T>>();
        joint->setName(name);

        system->addJoint(std::move(joint));

        return new PrismaticJoint<T>(system, name);
    }

    template <class T>
    Joint<T>* createPrismaticJoint(gafro::System<T>* system, const std::string& name, const std::array<T, 6> &parameters, int axis)
    {
        std::unique_ptr<gafro::PrismaticJoint<T>> joint = std::make_unique<gafro::PrismaticJoint<T>>(parameters, axis);
        joint->setName(name);

        system->addJoint(std::move(joint));

        return new PrismaticJoint<T>(system, name);
    }

    template <class T>
    Joint<T>* createRevoluteJoint(gafro::System<T>* system, const std::string& name)
    {
        std::unique_ptr<gafro::RevoluteJoint<T>> joint = std::make_unique<gafro::RevoluteJoint<T>>();
        joint->setName(name);

        system->addJoint(std::move(joint));

        return new RevoluteJoint<T>(system, name);
    }

    template <class T>
    Joint<T>* createRevoluteJoint(gafro::System<T>* system, const std::string& name, const std::array<T, 3> &parameters)
    {
        std::unique_ptr<gafro::RevoluteJoint<T>> joint = std::make_unique<gafro::RevoluteJoint<T>>(parameters);
        joint->setName(name);

        system->addJoint(std::move(joint));

        return new RevoluteJoint<T>(system, name);
    }

    template <class T>
    Joint<T>* createRevoluteJoint(gafro::System<T>* system, const std::string& name, const std::array<T, 6> &parameters, int axis)
    {
        std::unique_ptr<gafro::RevoluteJoint<T>> joint = std::make_unique<gafro::RevoluteJoint<T>>(parameters, axis);
        joint->setName(name);

        system->addJoint(std::move(joint));

        return new RevoluteJoint<T>(system, name);
    }

    template <class T>
    Link<T>* createLink(gafro::System<T>* system, const std::string& name)
    {
        std::unique_ptr<gafro::Link<T>> link = std::make_unique<gafro::Link<T>>();
        link->setName(name);

        system->addLink(std::move(link));

        return new Link<T>(system, name);
    }

    template <class T>
    KinematicChain<T>* createKinematicChain(gafro::System<T>* system, const std::string& name)
    {
        std::unique_ptr<gafro::KinematicChain<T>> chain = std::make_unique<gafro::KinematicChain<T>>();

        system->addKinematicChain(name, std::move(chain));

        return new KinematicChain<T>(system, name);
    }

    template <class T>
    Joint<double>* getJoint(gafro::System<T>* system, const std::string& name)
    {
        gafro::Joint<T>* joint = system->getJoint(name);
        if (!joint)
            return nullptr;

        return new Joint<T>(system, joint);
    }

    template <class T>
    inline const std::vector<Joint<T> *> getJoints(gafro::System<T>* system)
    {
        const auto& joints = system->getJoints();

        std::vector<Joint<T> *> result;
        result.reserve(joints.size());

        for (auto iter = joints.cbegin(), iterEnd = joints.cend(); iter != iterEnd; ++iter)
        {
            switch ((*iter)->getType())
            {
                case gafro::Joint<T>::Type::FIXED:
                    result.emplace_back(new FixedJoint<T>(system, (*iter)->getName()));

                case gafro::Joint<T>::Type::PRISMATIC:
                    result.emplace_back(new PrismaticJoint<T>(system, (*iter)->getName()));

                case gafro::Joint<T>::Type::REVOLUTE:
                    result.emplace_back(new RevoluteJoint<T>(system, (*iter)->getName()));
            }
        }

        return result;
    }

    template <class T>
    Link<double>* getLink(gafro::System<T>* system, const std::string& name)
    {
        gafro::Link<T>* link = system->getLink(name);
        if (!link)
            return nullptr;

        return new Link<T>(system, link);
    }

    template <class T>
    Link<double>* getBaseLink(gafro::System<T>* system)
    {
        const auto& links = system->getLinks();
        if (links.empty())
            return nullptr;

        return new Link<T>(system, links.front().get());
    }

    template <class T>
    inline const std::vector<Link<T> *> getLinks(gafro::System<T>* system)
    {
        const auto& links = system->getLinks();

        std::vector<Link<T> *> result;
        result.reserve(links.size());

        for (auto iter = links.cbegin(), iterEnd = links.cend(); iter != iterEnd; ++iter)
            result.emplace_back(new Link<T>(system, iter->get()));

        return result;
    }

    template <class T>
    KinematicChain<T>* getKinematicChain(gafro::System<T>* system, const std::string& name)
    {
        gafro::KinematicChain<T>* chain = system->getKinematicChain(name);
        if (!chain)
            return nullptr;

        return new KinematicChain<T>(system, chain);
    }

    template <class T>
    gafro::Motor<T> computeKinematicChainMotor(gafro::System<T>* system, const std::string &name, const std::vector<T> &position)
    {
        return KinematicChain<T>(system, system->getKinematicChain(name)).computeFullMotor(position);
    }

    template <class T>
    std::vector<gafro::Motor<T>> computeKinematicChainAnalyticJacobian(gafro::System<T>* system,
                                                                       const std::string &name,
                                                                       const std::vector<T> &position)
    {
        return KinematicChain<T>(system, system->getKinematicChain(name)).computeAnalyticJacobian(position);
    }

    template <class T>
    std::vector<typename gafro::Motor<T>::Generator> computeKinematicChainGeometricJacobian(
        gafro::System<T>* system, const std::string &name, const std::vector<T> &position)
    {
        return KinematicChain<T>(system, system->getKinematicChain(name)).computeGeometricJacobian(position);
    }

    template <class T>
    std::vector<typename gafro::Motor<T>::Generator> computeKinematicChainGeometricJacobianBody(
        gafro::System<T>* system, const std::string &name, const std::vector<T> &position)
    {
        return KinematicChain<T>(system, system->getKinematicChain(name)).computeGeometricJacobianBody(position);
    }

    template <class T>
    std::vector<T> computeInverseDynamics(gafro::System<T>* system, const std::vector<T> &position, const std::vector<T> &velocity,
                                          const std::vector<T> &acceleration)
    {
        #define INVERSEDYNAMICS(DOF) \
            case DOF: \
                memcpy( \
                    result.data(), \
                    system->computeInverseDynamics(Eigen::Vector<T, DOF>(position.data()), Eigen::Vector<T, DOF>(velocity.data()), Eigen::Vector<T, DOF>(acceleration.data())).data(), \
                    position.size() * sizeof(T) \
                ); \
                break;

        std::vector<T> result(position.size());

        // Downsides: every possibility is compiled even if never used, up to a hard limit that can't be changed by the user
        switch (position.size())
        {
            INVERSEDYNAMICS(1);
            INVERSEDYNAMICS(2);
            INVERSEDYNAMICS(3);
            INVERSEDYNAMICS(4);
            INVERSEDYNAMICS(5);
            INVERSEDYNAMICS(6);
            INVERSEDYNAMICS(7);
            INVERSEDYNAMICS(8);
            INVERSEDYNAMICS(9);
            INVERSEDYNAMICS(10);
            INVERSEDYNAMICS(11);
            INVERSEDYNAMICS(12);

            default:
                throw std::runtime_error("can't compute so many dof!");
        }

        return result;

        #undef INVERSEDYNAMICS
    }

    template <class T>
    std::vector<T> computeForwardDynamics(gafro::System<T>* system, const std::vector<T> &position, const std::vector<T> &velocity,
                                          const std::vector<T> &torque)
    {
        #define FORWARDDYNAMICS(DOF) \
            case DOF: \
                memcpy( \
                    result.data(), \
                    system->computeForwardDynamics(Eigen::Vector<T, DOF>(position.data()), Eigen::Vector<T, DOF>(velocity.data()), Eigen::Vector<T, DOF>(torque.data())).data(), \
                    position.size() * sizeof(T) \
                ); \
                break;

        std::vector<T> result(position.size());

        // Downsides: every possibility is compiled even if never used, up to a hard limit that can't be changed by the user
        switch (position.size())
        {
            FORWARDDYNAMICS(1);
            FORWARDDYNAMICS(2);
            FORWARDDYNAMICS(3);
            FORWARDDYNAMICS(4);
            FORWARDDYNAMICS(5);
            FORWARDDYNAMICS(6);
            FORWARDDYNAMICS(7);
            FORWARDDYNAMICS(8);
            FORWARDDYNAMICS(9);
            FORWARDDYNAMICS(10);
            FORWARDDYNAMICS(11);
            FORWARDDYNAMICS(12);

            default:
                throw std::runtime_error("can't compute so many dof!");
        }

        return result;

        #undef FORWARDDYNAMICS
    }

}  // namespace pygafro
