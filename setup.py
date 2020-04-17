## @file    setup.py
## @brief   Python distutils code for libSBML Python module (including dependencies)
## @author  Michael Hucka
## @author  Ben Bornstein
## @author  Ben Kovitz
## @author  Frank Bergmann (fbergman@caltech.edu)
##
##<!---------------------------------------------------------------------------
## This file is part of libSBML.  Please visit http://sbml.org for more
## information about SBML, and the latest version of libSBML.
##
## Copyright (C) 2013-2018 jointly by the following organizations:
##     1. California Institute of Technology, Pasadena, CA, USA
##     2. EMBL European Bioinformatics Institute (EMBL-EBI), Hinxton, UK
##     3. University of Heidelberg, Heidelberg, Germany
##
## Copyright 2005-2010 California Institute of Technology.
## Copyright 2002-2005 California Institute of Technology and
##                     Japan Science and Technology Corporation.
##
## This library is free software; you can redistribute it and/or modify it
## under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation.  A copy of the license agreement is provided
## in the file named "LICENSE.txt" included with this software distribution
## and also available online as http://sbml.org/software/libsbml/license.html
##----------------------------------------------------------------------- -->*/

import errno
import os
import sys
import shutil
import platform
from os.path import abspath, exists, join, split

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


def makedirs(folder, *args, **kwargs):
  try:
    return os.makedirs(folder, exist_ok=True, *args, **kwargs)
  except TypeError: 
    # Unexpected arguments encountered 
    pass

  try:
    # Should work is TypeError was caused by exist_ok, eg., Py2
    return os.makedirs(folder, *args, **kwargs)
  except OSError as e:
    if e.errno != errno.EEXIST:
      raise

    if os.path.isfile(folder):
      # folder is a file, raise OSError just like os.makedirs() in Py3
      raise

def get_dir_if_exists(variable, default):
  value = os.getenv(variable, default)
  value = abspath(value)
  if not exists(value):
    return None
  return value

global SRC_DIR
SRC_DIR = get_dir_if_exists('LIBSBML_SRC_DIR', './libsbml_source')
global DEP_DIR
DEP_DIR = get_dir_if_exists('LIBSBML_DEP_DIR', '../libsbml_dependencies/')
DEP_DIR32 = get_dir_if_exists('LIBSBML_DEP_DIR_32', '../win_libsbml_dependencies_32/')
DEP_DIR64 = get_dir_if_exists('LIBSBML_DEP_DIR_64', '../win_libsbml_dependencies_64/')


if not SRC_DIR:
  src_defined = os.getenv('LIBSBML_SRC_DIR')
  if src_defined:
    raise ValueError("LibSBML Source defined as: {0}, but coun't be found".format(src_defined))
  else:
    raise ValueError("LibSBML Source not specified or not present, define LIBSBML_SRC_DIR.")

print ("Using libSBML from: {0}".format(SRC_DIR))

version_file_name = join(SRC_DIR, 'VERSION.txt')
print ("Using VERSION.txt: {0}".format(version_file_name))

if not exists(version_file_name):
  print(os.listdir(SRC_DIR))
  raise ValueError("Invalid libSBML Source directory, no VERSION.txt file")

with open(version_file_name, 'r') as version_file:
  VERSION = version_file.readline().strip()

print ("Version is: {0}".format(VERSION))
print ("building for python: {0}".format(sys.version))

if not exists('libsbml'):
  makedirs('libsbml')


class CMakeExtension(Extension):
    """Override the default setuptools extension building."""

    def __init__(self, name, sources=(), **kwargs):
        """Initialize by passing on arguments."""
        # Don't invoke the original `build_ext` for this special extension.
        try: 
          super(CMakeExtension, self).__init__(name=name, sources=list(sources), **kwargs)
        except:
          Extension.__init__(self, name, list(sources), **kwargs)


class CMakeBuild(build_ext):
    """Override `build_ext` to then register it in the command classes."""

    def run(self):
        """
        Call Cmake and build every extension.

        Overrides parent's method.

        """
        for ext in self.extensions:
            self.build_cmake(ext)
        super(CMakeBuild, self).run()

    def build_cmake(self, extension):
        """Configure `extension` with CMake and build modules."""
        cwd = os.getcwd()
        build_temp = self.build_temp
        ext_dir = self.get_ext_fullpath(extension.name)
        makedirs(build_temp)
        target_lib_path = abspath(ext_dir)
        target_dir_path, name = split(target_lib_path)
        makedirs(target_dir_path)
        makedirs(join(cwd, 'libsbml'))

        print ('name: {0}'.format(name))
        print ('build temp: {0}'.format(build_temp))
        print ('extension name: {0}'.format(extension.name))
        print ('extension dir: {0}'.format(ext_dir))
        print ('target_dir_path: {0}'.format(target_dir_path))
        print ('target_lib_path: {0}'.format(target_lib_path))
        print ('cwd: {0}'.format(cwd))

        # example of cmake args
        config = 'Debug' if self.debug else 'Release'
        print ('name: {0}, tmp: {1}'.format(name, build_temp))
        is_osx = platform.system() == 'Darwin'
        is_win = platform.system() == 'Windows'
        is_win_32 = is_win and ('win32' in name or 'win32' in build_temp)

        cmake_args = [
            '-DCMAKE_BUILD_TYPE=' + config, 
            '-DCMAKE_BUILD_PARALLEL_LEVEL=4',
        ]

        # example of build args
        build_args = [
            '--config', config,
            '--'
        ]

        global DEP_DIR
        if not DEP_DIR and not self.dry_run:
            print("compiling dependencies")
            makedirs('./build_dependencies')
            os.chdir('./build_dependencies')
            self.spawn(['cmake', '../libsbml_dependencies/'] + cmake_args
                       + [
                           '-DCMAKE_INSTALL_PREFIX=../install_dependencies',
                           '-DWITH_BZIP2=ON',
                           '-DWITH_CHECK=OFF',
                           '-DWITH_EXPAT=ON',
                           '-DWITH_XERCES=OFF',
                           '-DWITH_ICONV=OFF',
                           '-DWITH_LIBXML=OFF',
                       ]
                       )
            self.spawn(['cmake', '--build', '.', '--target', 'install'] + build_args)
            os.chdir('..')
            DEP_DIR = abspath('./install_dependencies')

        libsbml_args = [
            '-DENABLE_COMP=ON',
            '-DENABLE_FBC=ON',
            '-DENABLE_LAYOUT=ON',
            '-DENABLE_QUAL=ON',
            '-DENABLE_GROUPS=ON',
            '-DENABLE_MULTI=ON',
            '-DENABLE_RENDER=ON',

            '-DWITH_EXPAT=ON',
            '-DWITH_LIBXML=OFF',
            '-DWITH_SWIG=ON',
            '-DWITH_ZLIB=ON',
            '-DWITH_PYTHON=ON',
            '-DWITH_STATIC_RUNTIME=ON',
            '-DPYTHON_EXECUTABLE=' + sys.executable
        ]

        cmake_args = cmake_args + libsbml_args
        
        if DEP_DIR:
          cmake_args.append('-DLIBSBML_DEPENDENCY_DIR=' + DEP_DIR)
          cmake_args.append('-DLIBEXPAT_INCLUDE_DIR=' + join(DEP_DIR, 'include'))

        if is_win_32:
          cmake_args.append('-A')
          cmake_args.append('win32')
          if DEP_DIR32:
            cmake_args.append('-DLIBSBML_DEPENDENCY_DIR=' + DEP_DIR32)
            cmake_args.append('-DLIBEXPAT_INCLUDE_DIR=' + join(DEP_DIR32, 'include'))
        elif is_win:
          if DEP_DIR64:
            cmake_args.append('-DLIBSBML_DEPENDENCY_DIR=' + DEP_DIR64)
            cmake_args.append('-DLIBEXPAT_INCLUDE_DIR=' + join(DEP_DIR64, 'include'))
        elif is_osx: 
          cmake_args.append('-DCLANG_USE_LIBCPP=ON')
          cmake_args.append('-DCMAKE_OSX_DEPLOYMENT_TARGET=10.9')

        os.chdir(build_temp)
        self.spawn(['cmake', SRC_DIR] + cmake_args)
        if not self.dry_run:
            self.spawn(['cmake', '--build', '.', '--target', 'binding_python_lib'] + build_args)
        
            # at this point the build should be complete, and we have all the files 
            # neeed in the temp build_folder
            
            init_py2 = None
            init_py3 = None
            dst_file = join(target_dir_path, '__init__.py')
            
            for root, dirs, files in os.walk(".", topdown=False):
              for name in files:
                # 1. find pyd and copy to target_lib_path
                if name.endswith('.pyd') or name == '_libsbml.so' or name == '_libsbml.dylib':
                  pyd_file = join(root, name)
                  print('copying pyd file to output file')
                  shutil.copyfile(pyd_file, target_lib_path)
                # 2. get scripts and copy to target_lib_path.parent.__init__.py corresponding to version 
                if name == 'libsbml.py':
                  src_file = join(root, name)
                  shutil.copyfile(src_file, dst_file)
                if name == 'libsbml2.py':
                  init_py2 = join(root, name)
                if name == 'libsbml3.py':
                  init_py3 = join(root, name)

            if init_py2 and exists(init_py2) and sys.version_info.major == 2:
                  shutil.copyfile(init_py2, dst_file)
            
            if init_py3 and exists(init_py3) and sys.version_info.major == 3:
                  shutil.copyfile(init_py3, dst_file)
        
        os.chdir(cwd)


setup(name             = "python-libsbml",
      version          = VERSION,
      description      = "LibSBML Python API",
      long_description = ("LibSBML is a library for reading, writing and "+
                          "manipulating the Systems Biology Markup Language "+
                          "(SBML).  It is written in ISO C and C++, supports "+
                          "SBML Levels 1, 2 and 3, and runs on Linux, Microsoft "+
                          "Windows, and Apple MacOS X.  For more information "+
                          "about SBML, please see http://sbml.org."),
      license          = "LGPL",
      author           = "SBML Team",
      author_email     = "libsbml-team@googlegroups.com",
      url              = "http://sbml.org",
      packages         = ["libsbml"],
      package_dir      = {'libsbml': 'libsbml'},
      ext_package      = "libsbml",
      ext_modules=[CMakeExtension('_libsbml')],
      cmdclass={
        'build_ext': CMakeBuild,
      }
)