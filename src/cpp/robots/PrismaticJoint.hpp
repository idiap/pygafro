/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#pragma once

#include "Joint.hpp"

namespace pygafro
{

    // Allows to access and manipulate joints from Python while avoiding any memory
    // ownership problem (Joints are managed in System using std::unique_ptr)
    template <class T>
    class PrismaticJoint : public Joint<T>
    {
      public:
        PrismaticJoint(gafro::System<T>* system, const std::string& name)
        : Joint<T>(system, name)
        {}

        PrismaticJoint(gafro::System<T>* system, gafro::PrismaticJoint<T>* joint)
        : Joint<T>(system, joint)
        {}

        virtual ~PrismaticJoint() {}

        inline void setAxis(const typename gafro::PrismaticJoint<T>::Axis &axis)
        {
            static_cast<gafro::PrismaticJoint<T>*>(Joint<T>::joint)->setAxis(axis);
        }

        const typename gafro::PrismaticJoint<T>::Axis &getAxis() const
        {
            return static_cast<gafro::PrismaticJoint<T>*>(Joint<T>::joint)->getAxis();
        }

        gafro::Translator<T> getTranslator(const T &displacement) const
        {
            return static_cast<gafro::PrismaticJoint<T>*>(Joint<T>::joint)->getTranslator(displacement);
        }
    };

}  // namespace pygafro
