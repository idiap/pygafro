/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

#pragma once

#include <gafro_robot_descriptions/UFactoryLite6.hpp>
#include "robots/Manipulator.hpp"
#include "utils.h"

namespace pygafro
{
    template <class T>
    class UFactoryLite6 : public Manipulator<T, 6>
    {
      public:
        UFactoryLite6()
        {
            this->manipulator = new gafro::UFactoryLite6<T>(getAssetsPath());
        }
    };
}
