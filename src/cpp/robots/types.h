/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#pragma once

#include <gafro/gafro.hpp>

#include "Link.hpp"
#include "Joint.hpp"
#include "RevoluteJoint.hpp"
#include "PrismaticJoint.hpp"
#include "FixedJoint.hpp"
#include "KinematicChain.hpp"
#include "Manipulator.hpp"
#include "FrankaEmikaRobot.hpp"
#include "UR5.hpp"

#include <gafro_robot_descriptions/AnymalC.hpp>
#include <gafro_robot_descriptions/Atlas.hpp>
#include <gafro_robot_descriptions/LeapHand.hpp>


typedef pygafro::Link<double> pyLink;
typedef gafro::Joint<double> Joint;
typedef pygafro::Joint<double> pyJoint;
typedef pygafro::RevoluteJoint<double> pyRevoluteJoint;
typedef pygafro::PrismaticJoint<double> pyPrismaticJoint;
typedef pygafro::FixedJoint<double> pyFixedJoint;
typedef pygafro::KinematicChain<double> pyKinematicChain;
typedef gafro::System<double> System;

typedef pygafro::FrankaEmikaRobot<double> FrankaEmikaRobot;
typedef pygafro::UR5<double> UR5;
typedef gafro::AnymalC<double> AnymalC;
typedef gafro::Atlas<double> Atlas;
typedef gafro::LeapHand<double> LeapHand;
