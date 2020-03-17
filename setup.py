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
import os
import sys
import shutil
import platform

try:
  import pathlib
except:
  pass

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as build_ext_orig

def get_dir_if_exists(variable, default):
  value = os.getenv(variable, default)
  value = os.path.abspath(value)
  if not os.path.exists(value):
    return None
  return value


SRC_DIR=get_dir_if_exists('LIBSBML_SRC_DIR', '../libsbml')
DEP_DIR=get_dir_if_exists('LIBSBML_DEP_DIR', '../libsbml_dependencies/')
DEP_DIR32=get_dir_if_exists('LIBSBML_DEP_DIR_32', '../win_libsbml_dependencies_32/')
DEP_DIR64=get_dir_if_exists('LIBSBML_DEP_DIR_64', '../win_libsbml_dependencies_64/')


if not SRC_DIR:
  raise ValueError("SRC_DIR not specified or not present, define LIBSBML_SRC_DIR.")

print ("Using libSBML from: {0}".format(SRC_DIR))

with open(os.path.join(SRC_DIR, 'VERSION.TXT'), 'r') as version_file: 
  VERSION = version_file.readline().strip()

print ("Version is: {0}".format(VERSION))

if not os.path.exists('libsbml'):
  os.makedirs('libsbml')

class CMakeExtension(Extension):

    def __init__(self, name):
        # don't invoke the original build_ext for this special extension
        try:
          super().__init__(name, sources=[])
        except:
          Extension.__init__(self, name, sources=[])
        


class build_ext(build_ext_orig):

    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)
        try:
          super().run()
        except:
          build_ext_orig.run(self)

    def build_cmake(self, ext):
        try:
          cwd = pathlib.Path().absolute()
          # these dirs will be created in build_py, so if you don't have
          # any python sources to bundle, the dirs will be missing
          
          build_temp = pathlib.Path(self.build_temp)
          build_temp.mkdir(parents=True, exist_ok=True)
          extdir = pathlib.Path(self.get_ext_fullpath(ext.name))
          extdir.parent.mkdir(parents=True, exist_ok=True)
          
          target_dir_path = str(extdir.parent.absolute())
          target_lib_path = str(extdir.absolute())
          name = str(extdir.name)
        except:
          cwd = os.path.abspath('.')
          build_temp = self.build_temp
          extdir = self.get_ext_fullpath(ext.name)
          if not os.path.exists(build_temp):
            os.makedirs(build_temp)
          target_lib_path = os.path.abspath(extdir)
          name = os.path.split(target_lib_path)[1]
          target_dir_path = os.path.split(target_lib_path)[0]
          if not os.path.exists(target_dir_path):
            os.makedirs(target_dir_path)

        if not os.path.exists(os.path.join(cwd, 'libsbml')):
            os.makedirs(os.path.join(cwd, 'libsbml'))

        # example of cmake args
        config = 'Debug' if self.debug else 'Release'
        print ('name: {0}, tmp: {1}'.format(name, build_temp))
        is_osx = platform.system() == 'Darwin'
        is_win = platform.system() == 'Windows'
        is_win_32 = is_win and ('win32' in name or 'win32' in str(build_temp))

        cmake_args = [
            '-DCMAKE_BUILD_TYPE=' + config, 
            '-DCMAKE_BUILD_PARALLEL_LEVEL=4',
            
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
        
        
        if DEP_DIR:
          cmake_args.append('-DLIBSBML_DEPENDENCY_DIR=' + DEP_DIR)
          cmake_args.append('-DLIBEXPAT_INCLUDE_DIR=' + os.path.join(DEP_DIR, 'include'))

        if is_win_32:
          cmake_args.append('-A')
          cmake_args.append('win32')
          if DEP_DIR32:
            cmake_args.append('-DLIBSBML_DEPENDENCY_DIR=' + DEP_DIR32)
            cmake_args.append('-DLIBEXPAT_INCLUDE_DIR=' + os.path.join(DEP_DIR32, 'include'))
        elif is_win:
          if DEP_DIR64:
            cmake_args.append('-DLIBSBML_DEPENDENCY_DIR=' + DEP_DIR64)
            cmake_args.append('-DLIBEXPAT_INCLUDE_DIR=' + os.path.join(DEP_DIR64, 'include'))
        elif is_osx: 
          cmake_args.append('-DCLANG_USE_LIBCPP=ON')
          cmake_args.append('-DCMAKE_OSX_DEPLOYMENT_TARGET=10.9')

        # example of build args
        build_args = [
            '--config', config,
            '--'
        ]

        os.chdir(str(build_temp))
        self.spawn(['cmake', str(SRC_DIR)] + cmake_args)
        if not self.dry_run:
            self.spawn(['cmake', '--build', '.', '--target', 'binding_python_lib'] + build_args)
        
            # at this point the build should be complete, and we have all the files 
            # neeed in the temp build_folder
            
            init_py2 = None
            init_py3 = None
            dst_file = os.path.join(target_dir_path, '__init__.py')
            
            for root, dirs, files in os.walk(".", topdown=False):
              for name in files:
                # 1. find pyd and copy to target_lib_path
                if name.endswith('.pyd') or name == '_libsbml.so' or name == '_libsbml.dylib':
                  pyd_file = os.path.join(root, name)
                  print('copying pyd file to output file')
                  shutil.copyfile(pyd_file, target_lib_path)
                # 2. get scripts and copy to target_lib_path.parent.__init__.py corresponding to version 
                if name == 'libsbml.py':
                  src_file = os.path.join(root, name)
                  shutil.copyfile(src_file, dst_file)
                if name == 'libsbml2.py':
                  init_py2 = os.path.join(root, name)
                if name == 'libsbml3.py':
                  init_py3 = os.path.join(root, name)

            if os.path.exists(init_py2) and sys.version_info.major == 2: 
                  shutil.copyfile(init_py2, dst_file)
            
            if os.path.exists(init_py3) and sys.version_info.major == 3:
                  shutil.copyfile(init_py3, dst_file)
        
        os.chdir(str(cwd))


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
        'build_ext': build_ext,
      }
)