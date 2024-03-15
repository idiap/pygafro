/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#pragma once

#include <gafro/robot/System.hpp>
#include "PrismaticJoint.hpp"
#include "RevoluteJoint.hpp"
#include "FixedJoint.hpp"
#include "Link.hpp"

namespace pygafro
{

    template <class T>
    class Joint;


    // Allows to access and manipulate links from Python while avoiding any memory
    // ownership problem (Links are managed in System using std::unique_ptr)
    template <class T>
    class Link
    {
      public:
        Link(gafro::System<T>* system, const std::string& name)
        : system(system), link(system->getLink(name))
        {}

        Link(gafro::System<T>* system, gafro::Link<T>* link)
        : system(system), link(link)
        {}

        ~Link() {}

        inline void setMass(const T &mass)
        {
            link->setMass(mass);
        }

        inline void setCenterOfMass(const gafro::Translator<T> &center_of_mass)
        {
            link->setCenterOfMass(center_of_mass);
        }

        inline void setInertia(const gafro::Inertia<T> &inertia)
        {
            link->setInertia(inertia);
        }

        inline void setParentJoint(const Joint<T> *parent_joint)
        {
            link->setParentJoint(parent_joint->getPtr());
        }

        inline void addChildJoint(const Joint<T> *child_joint)
        {
            link->addChildJoint(child_joint->getPtr());
        }

        inline void setAxis(const typename gafro::Motor<T>::Generator &axis)
        {
            link->setAxis(axis);
        }

        inline const T &getMass() const
        {
            return link->getMass();
        }

        inline const gafro::Translator<T> &getCenterOfMass() const
        {
            return link->getCenterOfMass();
        }

        inline const gafro::Inertia<T> &getInertia() const
        {
            return link->getInertia();
        }

        inline const std::string &getName() const
        {
            return link->getName();
        }

        inline Joint<T> *getParentJoint() const
        {
            const gafro::Joint<T>* joint = link->getParentJoint();
            if (!joint)
                return nullptr;

            switch (joint->getType())
            {
                case gafro::Joint<T>::Type::FIXED:
                    return new pygafro::FixedJoint<T>(system, joint->getName());

                case gafro::Joint<T>::Type::PRISMATIC:
                    return new pygafro::PrismaticJoint<T>(system, joint->getName());

                case gafro::Joint<T>::Type::REVOLUTE:
                    return new pygafro::RevoluteJoint<T>(system, joint->getName());
            }

            return nullptr;
        }

        inline const std::vector<Joint<T> *> getChildJoints() const
        {
            const auto& joints = link->getChildJoints();

            std::vector<Joint<T> *> result;
            result.reserve(joints.size());

            for (auto iter = joints.cbegin(), iterEnd = joints.cend(); iter != iterEnd; ++iter)
            {
                switch ((*iter)->getType())
                {
                    case gafro::Joint<T>::Type::FIXED:
                        result.emplace_back(new pygafro::FixedJoint<T>(system, (*iter)->getName()));

                    case gafro::Joint<T>::Type::PRISMATIC:
                        result.emplace_back(new pygafro::PrismaticJoint<T>(system, (*iter)->getName()));

                    case gafro::Joint<T>::Type::REVOLUTE:
                        result.emplace_back(new pygafro::RevoluteJoint<T>(system, (*iter)->getName()));
                }
            }

            return result;
        }

        inline const typename gafro::Motor<T>::Generator &getAxis() const
        {
            return link->getAxis();
        }

        inline const gafro::Link<T>* getPtr() const
        {
            return link;
        }

      private:
        gafro::System<T>* system;
        gafro::Link<T>* link;
    };
}  // namespace pygafro
