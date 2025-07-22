/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

#pragma once

#include <gafro_robot_descriptions/KukaIIWA14.hpp>
#include "robots/Manipulator.hpp"
#include "utils.h"

namespace pygafro
{
    template <class T>
    class KukaIIWA14 : public Manipulator<T, 7>
    {
      public:
        KukaIIWA14()
        {
            this->manipulator = new gafro::KukaIIWA14<T>(getAssetsPath());
        }
    };
}
