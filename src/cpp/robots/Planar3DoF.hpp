/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

#pragma once

#include <gafro_robot_descriptions/Planar3DoF.hpp>
#include "robots/Manipulator.hpp"
#include "utils.h"

namespace pygafro
{
    template <class T>
    class Planar3DoF : public Manipulator<T, 3>
    {
      public:
        Planar3DoF()
        {
            this->manipulator = new gafro::Planar3DoF<T>(getAssetsPath());
        }
    };
}
