<!--
 SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>

 SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>

 SPDX-License-Identifier: MPL-2.0
-->


# Geometric Algebra For RObotics in Python

This library provides a geometric algebra tools targeted towards robotics applications.
It includes various computations for the kinematics and dynamics of serial manipulators
as well as optimal control.

It is based on *gafro*, a C++ library relying on templates to efficiently implement the
geometric algebra operations.

**Note that only the Conformal Geometric Algebra part of *gafro* is available in *pygafro***.

Please visit https://gitlab.com/gafro in order to find the entire *gafro* software stack.

## Installation using pip (pre-compiled binaries)

	pip install pygafro

Wheels for Linux (x64_86 & arm64) and MacOS (arm64) are available (for Python 3.8 to 3.13).

For other platforms, *pygafro* is compiled from sources.

Should you want to have access to mesh and texture files for the robots, you can install the
optional package *pygafro-assets* by running either one of those commands:

	pip install pygafro-assets
	pip install pygafro[assets]

Note that *pygafro* doesn't provide any rendering functions, it only indicates which mesh file
to use for each link.

## Installation using pip (compilation from sources)

Due to the template-based nature of *gafro* (see **Differences between *gafro* and *pygafro***
below), the compilation of pygafro can take a long time. Additionally, **using ```clang```
instead of ```gcc```** is highly recommended: ```gcc``` requires more memory resources when
compiling *pygafro*, which can become problematic on lower-end computers.

### Using the default compiler of your computer

	pip install pygafro

### Forcing the usage of *clang*

(assuming that ```clang``` is installed at ```/usr/bin/clang```)

	export CC=/usr/bin/clang
	export CXX=/usr/bin/clang++
	pip install pygafro

## Installation with ROS2

Add PyGafro in your colcon workspace and build it with:

	CC=clang CXX=clang++ USE_COLCON=1 colcon build

## Installation from source

(works either in a **conda** or **virtual environment**)

Requirements:

* ```numpy```

Due to the template-based nature of *gafro* (see **Differences between *gafro* and *pygafro***
below), the compilation of pygafro can take a long time. Additionally, **using ```clang```
instead of ```gcc```** is highly recommended: ```gcc``` requires more memory resources when
compiling *pygafro*, which can become problematic on lower-end computers.

### Using the default compiler of your computer

	git clone
	cd pygafro
	mkdir build && cd build
	cmake ..
	make # or for example "make -j4" if you have enough resources
	make install

### Forcing the usage of *clang*

(assuming that ```clang``` is installed at ```/usr/bin/clang```)

	git clone
	cd pygafro
	mkdir build && cd build
	cmake -DCMAKE_CXX_COMPILER=/usr/bin/clang++ -DCMAKE_C_COMPILER=/usr/bin/clang ..
	make # or for example "make -j4" if you have enough resources
	make install

## Usage

### Multivectors

	from pygafro import Multivector
	from pygafro import Point
	from pygafro import Motor

	# create a multivector that corresponds to a Euclidean vector
	vector = Multivector.create(['e1', 'e2', 'e3'], [1.0, 2.0, 3.0])

	# create a point (a specialized multivector subclass)
	point = Point(1.0, 2.0, 3.0)

	# create a random motor
	motor = Motor.Random()

	# apply the motor to our multivectors
	vector2 = motor.apply(vector)
	point2 = motor.apply(point)

	# geometric product
	result = vector * point

	# inner product
	result = vector | point

	# outer product
	result = vector ^ point

### Robots

	from pygafro import FrankaEmikaRobot

	panda = FrankaEmikaRobot()

	position = panda.getRandomConfiguration()

	# forward kinematics: compute the motor at the end-effector
	ee_motor = panda.getEEMotor(position)

## Differences between *gafro* and *pygafro*

*gafro* being based on C++ templates, only the classes and operations you are effectively
using are compiled into your software.

This versatility cannot be achieved in a Python library: we cannot instantiate the
templates at runtime, nor can we realistically instantiate all the possible combinations
at compile time.

A compromise was choosen: a subset of multivectors (using sensible blades combinations)
are instantiated and compiled, and other blades combinations are supported through a
Python class that internally use a C++ multivector with more blades and transparently
use a mask to only expose the blades requested by the user.

Thus, creating a multivector is done using the following helper function:

	# using values
	vector = Multivector.create(['e1', 'e2', 'e3'], [1.0, 2.0, 3.0])

	# using only the list of blades
	vector = Multivector.create(['e1', 'e2', 'e3', 'ei', 'e123i'])

## Background

You can find the accompanying article [here](http://arxiv.org/abs/2212.07237) and more information on our [website](https://geometric-algebra.tobiloew.ch/).

## How to cite

If you use *gafro* in your research, please cite:

	@article{loewGeometricAlgebraOptimal2023,
	  title = {Geometric {{Algebra}} for {{Optimal Control}} with {{Applications}} in {{Manipulation Tasks}}},
	  author = {L\"ow, Tobias and Calinon, Sylvain},
	  date = {2023},
	  journal = {IEEE Transactions on Robotics},
	  doi = {10.1109/TRO.2023.3277282}
	}
