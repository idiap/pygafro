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
    class RevoluteJoint : public Joint<T>
    {
      public:
        RevoluteJoint(gafro::System<T>* system, const std::string& name)
        : Joint<T>(system, name)
        {}

        RevoluteJoint(gafro::System<T>* system, gafro::RevoluteJoint<T>* joint)
        : Joint<T>(system, joint)
        {}

        virtual ~RevoluteJoint() {}

        inline void setAxis(const typename gafro::RevoluteJoint<T>::Axis &axis)
        {
            static_cast<gafro::RevoluteJoint<T>*>(Joint<T>::joint)->setAxis(axis);
        }

        const typename gafro::RevoluteJoint<T>::Axis &getAxis() const
        {
            return static_cast<gafro::RevoluteJoint<T>*>(Joint<T>::joint)->getAxis();
        }

        gafro::Rotor<T> getRotor(const T &angle) const
        {
            return static_cast<gafro::RevoluteJoint<T>*>(Joint<T>::joint)->getRotor(angle);
        }

    };

}  // namespace pygafro
