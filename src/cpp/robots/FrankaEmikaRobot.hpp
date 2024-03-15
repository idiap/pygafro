/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#pragma once

#include <gafro_robot_descriptions/FrankaEmikaRobot.hpp>
#include "robots/Manipulator.hpp"
#include "utils.h"

namespace pygafro
{
    template <class T>
    class FrankaEmikaRobot : public Manipulator<T, 7>
    {
      public:
        FrankaEmikaRobot()
        {
            this->manipulator = new gafro::FrankaEmikaRobot<T>(getAssetsPath());
        }
    };
}
