/*
 * SPDX-FileCopyrightText: Copyright © 2025 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

#include <gafro/robot/System.hpp>
#include <gafro/robot/Link.hpp>
#include <gafro/robot/Joint.hpp>

#pragma once


namespace pygafro
{
    template<class T>
    void copySystem(const gafro::System<T>& system, gafro::System<T>& system2)
    {
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
    }
}
