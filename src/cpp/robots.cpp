/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>

#include <gafro/gafro.hpp>

#include "robots/FixedJoint.hpp"
#include "robots/Joint.hpp"
#include "robots/KinematicChain.hpp"
#include "robots/Link.hpp"
#include "robots/Manipulator.hpp"
#include "robots/Quadruped.hpp"
#include "robots/PrismaticJoint.hpp"
#include "robots/RevoluteJoint.hpp"
#include "robots/System.hpp"
#include "utils.h"


namespace py = pybind11;


std::unique_ptr<Atlas> createAtlas()
{
    return std::make_unique<gafro::Atlas<double>>(getAssetsPath());
}

std::unique_ptr<UnitreeG1> createUnitreeG1()
{
    return std::make_unique<gafro::UnitreeG1<double>>(getAssetsPath());
}


void init_robots(py::module &m)
{
    #include "multivectors.h"
    #include "physics_types.h"
    #include "robots/types.h"


    // Link class
    py::class_<pyLink>(m, "Link")
        .def("setMass", &pyLink::setMass)
        .def("setCenterOfMass", &pyLink::setCenterOfMass)
        .def("setInertia", &pyLink::setInertia)
        .def("setParentJoint", &pyLink::setParentJoint)
        .def("addChildJoint", &pyLink::addChildJoint)
        .def("setAxis", &pyLink::setAxis)
        // .def("setVisual", &pyLink::setVisual)
        .def("getMass", &pyLink::getMass)
        .def("getCenterOfMass", &pyLink::getCenterOfMass)
        .def("getInertia", &pyLink::getInertia)
        .def("getName", &pyLink::getName)
        .def("getParentJoint", &pyLink::getParentJoint)
        .def("getChildJoints", &pyLink::getChildJoints)
        .def("getAxis", &pyLink::getAxis)
        .def("hasVisual", &pyLink::hasVisual)
        .def("getVisual", &pyLink::getVisual);


    // Joint class
    py::class_<pyJoint> joint(m, "Joint");
    joint.def("setFrame", &pyJoint::setFrame)
         .def("setLimits", &pyJoint::setLimits)
         .def("setParentLink", &pyJoint::setParentLink)
         .def("setChildLink", &pyJoint::setChildLink)
         .def("getName", &pyJoint::getName)
         .def("getFrame", &pyJoint::getFrame)
         .def("getType", &pyJoint::getType)
         .def("getLimits", &pyJoint::getLimits)
         .def("getParentLink", &pyJoint::getParentLink)
         .def("getChildLink", &pyJoint::getChildLink)
         .def("isActuated", &pyJoint::isActuated)
         .def("getMotor", &pyJoint::getMotor)
         .def("getMotorDerivative", &pyJoint::getMotorDerivative)
         .def("getCurrentAxis", &pyJoint::getCurrentAxis);


    // Joint types
    py::enum_<Joint::Type>(joint, "Type")
        .value("FIXED", Joint::Type::FIXED)
        .value("REVOLUTE", Joint::Type::REVOLUTE)
        .value("PRISMATIC", Joint::Type::PRISMATIC)
        .export_values();


    // Joint limits
    py::class_<Joint::Limits>(joint, "Limits")
        .def(py::init<>())
        .def_readwrite("positionLower", &Joint::Limits::position_lower)
        .def_readwrite("positionUpper", &Joint::Limits::position_upper)
        .def_readwrite("velocity", &Joint::Limits::velocity)
        .def_readwrite("torque", &Joint::Limits::torque);


    // RevoluteJoint class
    py::class_<pyRevoluteJoint, pyJoint>(m, "RevoluteJoint")
        .def("setAxis", &pyRevoluteJoint::setAxis)
        .def("getAxis", &pyRevoluteJoint::getAxis)
        .def("getRotor", &pyRevoluteJoint::getRotor);


    // PrismaticJoint class
    py::class_<pyPrismaticJoint, pyJoint>(m, "PrismaticJoint")
        .def("setAxis", &pyPrismaticJoint::setAxis)
        .def("getAxis", &pyPrismaticJoint::getAxis)
        .def("getTranslator", &pyPrismaticJoint::getTranslator);


    // FixedJoint class
    py::class_<pyFixedJoint, pyJoint>(m, "FixedJoint");


    // KinematicChain class
    py::class_<pyKinematicChain>(m, "KinematicChain")
        .def("getDoF", &pyKinematicChain::getDoF)
        .def("addActuatedJoint", &pyKinematicChain::addActuatedJoint)
        .def("addFixedMotor", &pyKinematicChain::addFixedMotor)
        .def("setFixedMotors", &pyKinematicChain::setFixedMotors)
        .def("getFixedMotors", &pyKinematicChain::getFixedMotors)
        .def("getActuatedJoints", &pyKinematicChain::getActuatedJoints)
        .def("computeMotor", &pyKinematicChain::computeFullMotor)
        .def("computeMotor", &pyKinematicChain::computeMotor)
        .def("computeMotorDerivative", &pyKinematicChain::computeMotorDerivative)
        .def("computeAnalyticJacobian", &pyKinematicChain::computeAnalyticJacobian)
        .def("computeGeometricJacobian", &pyKinematicChain::computeGeometricJacobian)
        .def("computeGeometricJacobianBody", &pyKinematicChain::computeGeometricJacobianBody)
        .def("computeKinematicChainGeometricJacobianTimeDerivative", &pyKinematicChain::computeKinematicChainGeometricJacobianTimeDerivative)
        .def("computeMassMatrix", &pyKinematicChain::computeMassMatrix)
        .def("finalize", &pyKinematicChain::finalize);


    // System class
    py::class_<System>(m, "System")
        .def(py::init<>())
        .def("createFixedJoint", &pygafro::createFixedJoint<double>)
        .def("createPrismaticJoint", py::overload_cast<System*, const std::string&>(&pygafro::createPrismaticJoint<double>))
        .def("createPrismaticJoint", py::overload_cast<System*, const std::string&, const std::array<double, 6>&, int>(&pygafro::createPrismaticJoint<double>))
        .def("createRevoluteJoint", py::overload_cast<System*, const std::string&>(&pygafro::createRevoluteJoint<double>))
        .def("createRevoluteJoint", py::overload_cast<System*, const std::string&, const std::array<double, 3>&>(&pygafro::createRevoluteJoint<double>))
        .def("createRevoluteJoint", py::overload_cast<System*, const std::string&, const std::array<double, 6>&, int>(&pygafro::createRevoluteJoint<double>))
        .def("createLink", &pygafro::createLink<double>)
        .def("createKinematicChain", &pygafro::createKinematicChain<double>)
        .def("setName", &System::setName)
        .def("getName", &System::getName)
        .def("getBaseLink", &pygafro::getBaseLink<double>)
        .def("getLink", &pygafro::getLink<double>)
        .def("getLinks", &pygafro::getLinks<double>)
        .def("getJoint", &pygafro::getJoint<double>)
        .def("getJoints", &pygafro::getJoints<double>)
        .def("setJointLimits", &System::setJointLimits)
        .def("getJointLimitsMin", &System::getJointLimitsMin)
        .def("getJointLimitsMax", &System::getJointLimitsMax)
        .def("isJointPositionFeasible", &System::isJointPositionFeasible)
        .def("getRandomConfiguration", &System::getRandomConfiguration)
        .def("hasKinematicChain", &System::hasKinematicChain)
        .def("getKinematicChain", &pygafro::getKinematicChain<double>)
        .def("computeKinematicChainMotor", &pygafro::computeKinematicChainMotor<double>)
        .def("computeKinematicChainAnalyticJacobian", &pygafro::computeKinematicChainAnalyticJacobian<double>)
        .def("computeKinematicChainGeometricJacobian", &pygafro::computeKinematicChainGeometricJacobian<double>)
        .def("computeKinematicChainGeometricJacobianBody", &pygafro::computeKinematicChainGeometricJacobianBody<double>)
        .def("computeInverseDynamics", &pygafro::computeInverseDynamics<double>)
        .def("computeForwardDynamics", &pygafro::computeForwardDynamics<double>)
        .def("finalize", &System::finalize);


    // Manipulator class
    #include "manipulators.h"
    #include "manipulators.hpp"


    // Quadruped class
    #include "quadrupeds.h"
    #include "quadrupeds.hpp"


    // Hand class
    #include "hands.h"
    #include "hands.hpp"


    // AnymalC class
    py::class_<AnymalC, Quadruped_3>(m, "AnymalC")
        .def(py::init());


    // Atlas class
    py::class_<Atlas, System>(m, "Atlas")
        .def(py::init(&createAtlas));


    // FrankaEmikaRobot class
    py::class_<FrankaEmikaRobot, Manipulator_7>(m, "FrankaEmikaRobot")
        .def(py::init());


    // KukaIIWA7 class
    py::class_<KukaIIWA7, Manipulator_7>(m, "KukaIIWA7")
        .def(py::init());


    // KukaIIWA14 class
    py::class_<KukaIIWA14, Manipulator_7>(m, "KukaIIWA14")
        .def(py::init());


    // LeapHand class
    py::class_<LeapHand, Hand_4_4_4_4>(m, "LeapHand")
        .def(py::init());


    // Planar3DoF class
    py::class_<Planar3DoF, Manipulator_3>(m, "Planar3DoF")
        .def(py::init());


    // UFactoryLite6 class
    py::class_<UFactoryLite6, Manipulator_6>(m, "UFactoryLite6")
        .def(py::init());


    // UnitreeG1 class
    py::class_<UnitreeG1, System>(m, "UnitreeG1")
        .def(py::init(&createUnitreeG1));


    // UR5 class
    py::class_<UR5, Manipulator_6>(m, "UR5")
        .def(py::init());


    // Visual module
    py::module m_visual = m.def_submodule("visual");

    py::class_<Visual> visual(m_visual, "Visual");
    visual.def("getType", &Visual::getType)
          .def("getTransform", &Visual::getTransform);

    py::enum_<Visual::Type>(m_visual, "Type")
        .value("SPHERE", Visual::Type::SPHERE)
        .value("MESH", Visual::Type::MESH)
        .value("CYLINDER", Visual::Type::CYLINDER)
        .value("BOX", Visual::Type::BOX)
        .export_values();

    py::class_<VisualSphere, Visual>(m_visual, "Sphere")
        .def("getRadius", &VisualSphere::getRadius);

    py::class_<VisualMesh, Visual>(m_visual, "Mesh")
        .def("getFilename", &VisualMesh::getFilename)
        .def("getScaleX", &VisualMesh::getScaleX)
        .def("getScaleY", &VisualMesh::getScaleY)
        .def("getScaleZ", &VisualMesh::getScaleZ);

    py::class_<VisualCylinder, Visual>(m_visual, "Cylinder")
        .def("getLength", &VisualCylinder::getLength)
        .def("getRadius", &VisualCylinder::getRadius);

    py::class_<VisualBox, Visual>(m_visual, "Box")
        .def("getDimX", &VisualBox::getDimX)
        .def("getDimY", &VisualBox::getDimY)
        .def("getDimZ", &VisualBox::getDimZ);
}
