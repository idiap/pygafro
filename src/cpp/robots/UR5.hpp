/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#pragma once

#include <gafro_robot_descriptions/UR5.hpp>
#include "robots/Manipulator.hpp"
#include "utils.h"

namespace pygafro
{
    template <class T>
    class UR5 : public Manipulator<T, 6>
    {
      public:
        UR5()
        {
            this->manipulator = new gafro::UR5<T>(getAssetsPath());
        }
    };
}
