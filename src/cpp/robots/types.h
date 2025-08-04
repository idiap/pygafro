/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

#pragma once

#include <gafro/gafro.hpp>

#include "Link.hpp"
#include "Joint.hpp"
#include "RevoluteJoint.hpp"
#include "PrismaticJoint.hpp"
#include "FixedJoint.hpp"
#include "Hand.hpp"
#include "KinematicChain.hpp"
#include "Manipulator.hpp"
#include "Quadruped.hpp"
#include "AnymalC.hpp"
#include "FrankaEmikaRobot.hpp"
#include "KukaIIWA7.hpp"
#include "KukaIIWA14.hpp"
#include "LeapHand.hpp"
#include "Planar3DoF.hpp"
#include "UFactoryLite6.hpp"
#include "UR5.hpp"

#include <gafro_robot_descriptions/Atlas.hpp>
#include <gafro_robot_descriptions/UnitreeG1.hpp>
#include <gafro_robot_descriptions/serialization/Visual.hpp>


typedef pygafro::Link<double> pyLink;
typedef gafro::Joint<double> Joint;
typedef pygafro::Joint<double> pyJoint;
typedef pygafro::RevoluteJoint<double> pyRevoluteJoint;
typedef pygafro::PrismaticJoint<double> pyPrismaticJoint;
typedef pygafro::FixedJoint<double> pyFixedJoint;
typedef pygafro::KinematicChain<double> pyKinematicChain;
typedef gafro::System<double> System;
typedef gafro::visual::Visual Visual;
typedef gafro::visual::Sphere VisualSphere;
typedef gafro::visual::Mesh VisualMesh;
typedef gafro::visual::Cylinder VisualCylinder;
typedef gafro::visual::Box VisualBox;

typedef pygafro::AnymalC<double> AnymalC;
typedef gafro::Atlas<double> Atlas;
typedef pygafro::FrankaEmikaRobot<double> FrankaEmikaRobot;
typedef pygafro::KukaIIWA7<double> KukaIIWA7;
typedef pygafro::KukaIIWA14<double> KukaIIWA14;
typedef pygafro::LeapHand<double> LeapHand;
typedef pygafro::Planar3DoF<double> Planar3DoF;
typedef pygafro::UFactoryLite6<double> UFactoryLite6;
typedef gafro::UnitreeG1<double> UnitreeG1;
typedef pygafro::UR5<double> UR5;
