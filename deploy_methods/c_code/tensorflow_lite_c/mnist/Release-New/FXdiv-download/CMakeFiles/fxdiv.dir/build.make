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
CMAKE_SOURCE_DIR = /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download

# Utility rule file for fxdiv.

# Include any custom commands dependencies for this target.
include CMakeFiles/fxdiv.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/fxdiv.dir/progress.make

CMakeFiles/fxdiv: CMakeFiles/fxdiv-complete

CMakeFiles/fxdiv-complete: fxdiv-prefix/src/fxdiv-stamp/fxdiv-install
CMakeFiles/fxdiv-complete: fxdiv-prefix/src/fxdiv-stamp/fxdiv-mkdir
CMakeFiles/fxdiv-complete: fxdiv-prefix/src/fxdiv-stamp/fxdiv-download
CMakeFiles/fxdiv-complete: fxdiv-prefix/src/fxdiv-stamp/fxdiv-update
CMakeFiles/fxdiv-complete: fxdiv-prefix/src/fxdiv-stamp/fxdiv-patch
CMakeFiles/fxdiv-complete: fxdiv-prefix/src/fxdiv-stamp/fxdiv-configure
CMakeFiles/fxdiv-complete: fxdiv-prefix/src/fxdiv-stamp/fxdiv-build
CMakeFiles/fxdiv-complete: fxdiv-prefix/src/fxdiv-stamp/fxdiv-install
CMakeFiles/fxdiv-complete: fxdiv-prefix/src/fxdiv-stamp/fxdiv-test
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Completed 'fxdiv'"
	/usr/bin/cmake -E make_directory /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/CMakeFiles
	/usr/bin/cmake -E touch /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/CMakeFiles/fxdiv-complete
	/usr/bin/cmake -E touch /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/fxdiv-prefix/src/fxdiv-stamp/fxdiv-done

fxdiv-prefix/src/fxdiv-stamp/fxdiv-build: fxdiv-prefix/src/fxdiv-stamp/fxdiv-configure
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "No build step for 'fxdiv'"
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv && /usr/bin/cmake -E echo_append
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv && /usr/bin/cmake -E touch /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/fxdiv-prefix/src/fxdiv-stamp/fxdiv-build

fxdiv-prefix/src/fxdiv-stamp/fxdiv-configure: fxdiv-prefix/tmp/fxdiv-cfgcmd.txt
fxdiv-prefix/src/fxdiv-stamp/fxdiv-configure: fxdiv-prefix/src/fxdiv-stamp/fxdiv-patch
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "No configure step for 'fxdiv'"
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv && /usr/bin/cmake -E echo_append
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv && /usr/bin/cmake -E touch /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/fxdiv-prefix/src/fxdiv-stamp/fxdiv-configure

fxdiv-prefix/src/fxdiv-stamp/fxdiv-download: fxdiv-prefix/src/fxdiv-stamp/fxdiv-gitinfo.txt
fxdiv-prefix/src/fxdiv-stamp/fxdiv-download: fxdiv-prefix/src/fxdiv-stamp/fxdiv-mkdir
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Performing download step (git clone) for 'fxdiv'"
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New && /usr/bin/cmake -P /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/fxdiv-prefix/tmp/fxdiv-gitclone.cmake
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New && /usr/bin/cmake -E touch /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/fxdiv-prefix/src/fxdiv-stamp/fxdiv-download

fxdiv-prefix/src/fxdiv-stamp/fxdiv-install: fxdiv-prefix/src/fxdiv-stamp/fxdiv-build
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "No install step for 'fxdiv'"
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv && /usr/bin/cmake -E echo_append
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv && /usr/bin/cmake -E touch /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/fxdiv-prefix/src/fxdiv-stamp/fxdiv-install

fxdiv-prefix/src/fxdiv-stamp/fxdiv-mkdir:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "Creating directories for 'fxdiv'"
	/usr/bin/cmake -E make_directory /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-source
	/usr/bin/cmake -E make_directory /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv
	/usr/bin/cmake -E make_directory /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/fxdiv-prefix
	/usr/bin/cmake -E make_directory /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/fxdiv-prefix/tmp
	/usr/bin/cmake -E make_directory /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/fxdiv-prefix/src/fxdiv-stamp
	/usr/bin/cmake -E make_directory /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/fxdiv-prefix/src
	/usr/bin/cmake -E make_directory /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/fxdiv-prefix/src/fxdiv-stamp
	/usr/bin/cmake -E touch /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/fxdiv-prefix/src/fxdiv-stamp/fxdiv-mkdir

fxdiv-prefix/src/fxdiv-stamp/fxdiv-patch: fxdiv-prefix/src/fxdiv-stamp/fxdiv-update
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/CMakeFiles --progress-num=$(CMAKE_PROGRESS_7) "No patch step for 'fxdiv'"
	/usr/bin/cmake -E echo_append
	/usr/bin/cmake -E touch /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/fxdiv-prefix/src/fxdiv-stamp/fxdiv-patch

fxdiv-prefix/src/fxdiv-stamp/fxdiv-test: fxdiv-prefix/src/fxdiv-stamp/fxdiv-install
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/CMakeFiles --progress-num=$(CMAKE_PROGRESS_8) "No test step for 'fxdiv'"
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv && /usr/bin/cmake -E echo_append
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv && /usr/bin/cmake -E touch /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/fxdiv-prefix/src/fxdiv-stamp/fxdiv-test

fxdiv-prefix/src/fxdiv-stamp/fxdiv-update: fxdiv-prefix/src/fxdiv-stamp/fxdiv-download
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/CMakeFiles --progress-num=$(CMAKE_PROGRESS_9) "Performing update step for 'fxdiv'"
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-source && /usr/bin/cmake -P /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/fxdiv-prefix/tmp/fxdiv-gitupdate.cmake

fxdiv: CMakeFiles/fxdiv
fxdiv: CMakeFiles/fxdiv-complete
fxdiv: fxdiv-prefix/src/fxdiv-stamp/fxdiv-build
fxdiv: fxdiv-prefix/src/fxdiv-stamp/fxdiv-configure
fxdiv: fxdiv-prefix/src/fxdiv-stamp/fxdiv-download
fxdiv: fxdiv-prefix/src/fxdiv-stamp/fxdiv-install
fxdiv: fxdiv-prefix/src/fxdiv-stamp/fxdiv-mkdir
fxdiv: fxdiv-prefix/src/fxdiv-stamp/fxdiv-patch
fxdiv: fxdiv-prefix/src/fxdiv-stamp/fxdiv-test
fxdiv: fxdiv-prefix/src/fxdiv-stamp/fxdiv-update
fxdiv: CMakeFiles/fxdiv.dir/build.make
.PHONY : fxdiv

# Rule to build all files generated by this target.
CMakeFiles/fxdiv.dir/build: fxdiv
.PHONY : CMakeFiles/fxdiv.dir/build

CMakeFiles/fxdiv.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/fxdiv.dir/cmake_clean.cmake
.PHONY : CMakeFiles/fxdiv.dir/clean

CMakeFiles/fxdiv.dir/depend:
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/FXdiv-download/CMakeFiles/fxdiv.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/fxdiv.dir/depend

