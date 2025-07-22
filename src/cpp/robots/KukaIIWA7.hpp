/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#pragma once

#include <gafro_robot_descriptions/KukaIIWA7.hpp>
#include "robots/Manipulator.hpp"
#include "utils.h"

namespace pygafro
{
    template <class T>
    class KukaIIWA7 : public Manipulator<T, 7>
    {
      public:
        KukaIIWA7()
        {
            this->manipulator = new gafro::KukaIIWA7<T>(getAssetsPath());
        }
    };
}
