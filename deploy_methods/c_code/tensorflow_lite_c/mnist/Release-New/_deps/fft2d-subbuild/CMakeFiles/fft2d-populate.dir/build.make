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
CMAKE_SOURCE_DIR = /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild

# Utility rule file for fft2d-populate.

# Include any custom commands dependencies for this target.
include CMakeFiles/fft2d-populate.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/fft2d-populate.dir/progress.make

CMakeFiles/fft2d-populate: CMakeFiles/fft2d-populate-complete

CMakeFiles/fft2d-populate-complete: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-install
CMakeFiles/fft2d-populate-complete: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-mkdir
CMakeFiles/fft2d-populate-complete: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-download
CMakeFiles/fft2d-populate-complete: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-update
CMakeFiles/fft2d-populate-complete: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-patch
CMakeFiles/fft2d-populate-complete: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-configure
CMakeFiles/fft2d-populate-complete: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-build
CMakeFiles/fft2d-populate-complete: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-install
CMakeFiles/fft2d-populate-complete: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-test
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Completed 'fft2d-populate'"
	/usr/bin/cmake -E make_directory /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/CMakeFiles
	/usr/bin/cmake -E touch /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/CMakeFiles/fft2d-populate-complete
	/usr/bin/cmake -E touch /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-done

fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-build: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-configure
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "No build step for 'fft2d-populate'"
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-build && /usr/bin/cmake -E echo_append
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-build && /usr/bin/cmake -E touch /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-build

fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-configure: fft2d-populate-prefix/tmp/fft2d-populate-cfgcmd.txt
fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-configure: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-patch
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "No configure step for 'fft2d-populate'"
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-build && /usr/bin/cmake -E echo_append
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-build && /usr/bin/cmake -E touch /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-configure

fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-download: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-urlinfo.txt
fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-download: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-mkdir
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Performing download step (download, verify and extract) for 'fft2d-populate'"
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New && /usr/bin/cmake -P /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/fft2d-populate-prefix/src/fft2d-populate-stamp/download-fft2d-populate.cmake
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New && /usr/bin/cmake -P /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/fft2d-populate-prefix/src/fft2d-populate-stamp/verify-fft2d-populate.cmake
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New && /usr/bin/cmake -P /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/fft2d-populate-prefix/src/fft2d-populate-stamp/extract-fft2d-populate.cmake
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New && /usr/bin/cmake -E touch /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-download

fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-install: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-build
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "No install step for 'fft2d-populate'"
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-build && /usr/bin/cmake -E echo_append
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-build && /usr/bin/cmake -E touch /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-install

fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-mkdir:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "Creating directories for 'fft2d-populate'"
	/usr/bin/cmake -E make_directory /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/fft2d
	/usr/bin/cmake -E make_directory /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-build
	/usr/bin/cmake -E make_directory /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/fft2d-populate-prefix
	/usr/bin/cmake -E make_directory /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/fft2d-populate-prefix/tmp
	/usr/bin/cmake -E make_directory /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/fft2d-populate-prefix/src/fft2d-populate-stamp
	/usr/bin/cmake -E make_directory /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/fft2d-populate-prefix/src
	/usr/bin/cmake -E make_directory /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/fft2d-populate-prefix/src/fft2d-populate-stamp
	/usr/bin/cmake -E touch /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-mkdir

fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-patch: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-update
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/CMakeFiles --progress-num=$(CMAKE_PROGRESS_7) "No patch step for 'fft2d-populate'"
	/usr/bin/cmake -E echo_append
	/usr/bin/cmake -E touch /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-patch

fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-test: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-install
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/CMakeFiles --progress-num=$(CMAKE_PROGRESS_8) "No test step for 'fft2d-populate'"
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-build && /usr/bin/cmake -E echo_append
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-build && /usr/bin/cmake -E touch /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-test

fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-update: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-download
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/CMakeFiles --progress-num=$(CMAKE_PROGRESS_9) "No update step for 'fft2d-populate'"
	/usr/bin/cmake -E echo_append
	/usr/bin/cmake -E touch /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-update

fft2d-populate: CMakeFiles/fft2d-populate
fft2d-populate: CMakeFiles/fft2d-populate-complete
fft2d-populate: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-build
fft2d-populate: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-configure
fft2d-populate: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-download
fft2d-populate: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-install
fft2d-populate: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-mkdir
fft2d-populate: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-patch
fft2d-populate: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-test
fft2d-populate: fft2d-populate-prefix/src/fft2d-populate-stamp/fft2d-populate-update
fft2d-populate: CMakeFiles/fft2d-populate.dir/build.make
.PHONY : fft2d-populate

# Rule to build all files generated by this target.
CMakeFiles/fft2d-populate.dir/build: fft2d-populate
.PHONY : CMakeFiles/fft2d-populate.dir/build

CMakeFiles/fft2d-populate.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/fft2d-populate.dir/cmake_clean.cmake
.PHONY : CMakeFiles/fft2d-populate.dir/clean

CMakeFiles/fft2d-populate.dir/depend:
	cd /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild /home/lucaserf/tiniMLVM/deploy_methods/c_code/tensorflow_lite_c/mnist/Release-New/_deps/fft2d-subbuild/CMakeFiles/fft2d-populate.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/fft2d-populate.dir/depend

