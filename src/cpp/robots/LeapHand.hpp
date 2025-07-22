/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

#pragma once

#include <gafro_robot_descriptions/LeapHand.hpp>
#include "robots/Hand.hpp"
#include "utils.h"

namespace pygafro
{
    template <class T>
    class LeapHand : public Hand<T, 4, 4, 4, 4>
    {
      public:
        LeapHand()
        {
            this->hand = new gafro::LeapHand<T>(getAssetsPath());
        }
    };
}
