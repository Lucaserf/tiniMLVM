# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New

# Include any dependencies generated for this target.
include _deps/xnnpack-build/CMakeFiles/packing.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include _deps/xnnpack-build/CMakeFiles/packing.dir/compiler_depend.make

# Include the progress variables for this target.
include _deps/xnnpack-build/CMakeFiles/packing.dir/progress.make

# Include the compile flags for this target's objects.
include _deps/xnnpack-build/CMakeFiles/packing.dir/flags.make

_deps/xnnpack-build/CMakeFiles/packing.dir/src/packing.c.o: _deps/xnnpack-build/CMakeFiles/packing.dir/flags.make
_deps/xnnpack-build/CMakeFiles/packing.dir/src/packing.c.o: xnnpack/src/packing.c
_deps/xnnpack-build/CMakeFiles/packing.dir/src/packing.c.o: _deps/xnnpack-build/CMakeFiles/packing.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object _deps/xnnpack-build/CMakeFiles/packing.dir/src/packing.c.o"
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/xnnpack-build && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT _deps/xnnpack-build/CMakeFiles/packing.dir/src/packing.c.o -MF CMakeFiles/packing.dir/src/packing.c.o.d -o CMakeFiles/packing.dir/src/packing.c.o -c /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/xnnpack/src/packing.c

_deps/xnnpack-build/CMakeFiles/packing.dir/src/packing.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/packing.dir/src/packing.c.i"
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/xnnpack-build && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/xnnpack/src/packing.c > CMakeFiles/packing.dir/src/packing.c.i

_deps/xnnpack-build/CMakeFiles/packing.dir/src/packing.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/packing.dir/src/packing.c.s"
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/xnnpack-build && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/xnnpack/src/packing.c -o CMakeFiles/packing.dir/src/packing.c.s

packing: _deps/xnnpack-build/CMakeFiles/packing.dir/src/packing.c.o
packing: _deps/xnnpack-build/CMakeFiles/packing.dir/build.make
.PHONY : packing

# Rule to build all files generated by this target.
_deps/xnnpack-build/CMakeFiles/packing.dir/build: packing
.PHONY : _deps/xnnpack-build/CMakeFiles/packing.dir/build

_deps/xnnpack-build/CMakeFiles/packing.dir/clean:
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/xnnpack-build && $(CMAKE_COMMAND) -P CMakeFiles/packing.dir/cmake_clean.cmake
.PHONY : _deps/xnnpack-build/CMakeFiles/packing.dir/clean

_deps/xnnpack-build/CMakeFiles/packing.dir/depend:
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/xnnpack /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/xnnpack-build /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/xnnpack-build/CMakeFiles/packing.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : _deps/xnnpack-build/CMakeFiles/packing.dir/depend

