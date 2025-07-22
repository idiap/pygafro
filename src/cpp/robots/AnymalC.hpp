/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

#pragma once

#include <gafro_robot_descriptions/AnymalC.hpp>
#include "robots/Quadruped.hpp"
#include "utils.h"

namespace pygafro
{
    template <class T>
    class AnymalC : public Quadruped<T, 3>
    {
      public:
        AnymalC()
        {
            this->quadruped = new gafro::AnymalC<T>(getAssetsPath());
        }
    };
}
