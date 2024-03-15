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
    class FixedJoint : public Joint<T>
    {
      public:
        FixedJoint(gafro::System<T>* system, const std::string& name)
        : Joint<T>(system, name)
        {}

        FixedJoint(gafro::System<T>* system, gafro::FixedJoint<T>* joint)
        : Joint<T>(system, joint)
        {}

        virtual ~FixedJoint() {}
    };

}  // namespace pygafro
