/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#pragma once

#include <gafro/robot/System.hpp>

namespace pygafro
{

    template <class T>
    class Link;


    // Allows to access and manipulate joints from Python while avoiding any memory
    // ownership problem (Joints are managed in System using std::unique_ptr)
    template <class T>
    class Joint
    {
      public:
        Joint(gafro::System<T>* system, const std::string& name)
        : system(system), joint(system->getJoint(name))
        {}

        Joint(gafro::System<T>* system, gafro::Joint<T>* joint)
        : system(system), joint(joint)
        {}

        virtual ~Joint() {}

        // setter functions
        inline void setFrame(const gafro::Motor<T> &frame)
        {
            joint->setFrame(frame);
        }

        inline void setLimits(const typename gafro::Joint<T>::Limits &limits)
        {
            joint->setLimits(limits);
        }

        inline void setParentLink(const Link<T> *parent_link)
        {
            joint->setParentLink(parent_link->getPtr());
        }

        inline void setChildLink(const Link<T> *child_link)
        {
            joint->setChildLink(child_link->getPtr());
        }

        // getter functions
        inline const std::string &getName() const
        {
            return joint->getName();
        }

        inline const gafro::Motor<T> &getFrame() const
        {
            return joint->getFrame();
        }

        inline const typename gafro::Joint<T>::Type &getType() const
        {
            return joint->getType();
        }

        inline const typename gafro::Joint<T>::Limits &getLimits() const
        {
            return joint->getLimits();
        }

        inline Link<T> *getParentLink()
        {
            const gafro::Link<T>* link = joint->getParentLink();
            if (!link)
                return nullptr;

            return new Link<T>(system, link->getName());
        }

        inline Link<T> *getChildLink()
        {
            const gafro::Link<T>* link = joint->getChildLink();
            if (!link)
                return nullptr;

            return new Link<T>(system, link->getName());
        }

        inline const gafro::Joint<T>* getPtr() const
        {
            return joint;
        }

        inline gafro::System<T>* getSystem() const
        {
            return system;
        }

        //

        inline bool isActuated() const
        {
            return joint->isActuated();
        }

        // virtual functions
        inline gafro::Motor<T> getMotor(const T &angle) const
        {
            return joint->getMotor(angle);
        }

        inline gafro::Motor<T> getMotorDerivative(const T &angle) const
        {
            return joint->getMotorDerivative(angle);
        }

        inline typename gafro::Motor<T>::Generator getCurrentAxis(const gafro::Motor<T> &motor) const
        {
            return joint->getCurrentAxis(motor);
        }

      protected:
        gafro::System<T>* system;
        gafro::Joint<T>* joint;
    };

}  // namespace pygafro
