# @file    setup.py
# @brief   Python distutils code for libSBML Python module (including dependencies)
# @author  Michael Hucka
# @author  Ben Bornstein
# @author  Ben Kovitz
# @author  Frank Bergmann (fbergman@caltech.edu)
#
#
# This file is part of libSBML.  Please visit http://sbml.org for more
# information about SBML, and the latest version of libSBML.
#
# Copyright (C) 2013-2018 jointly by the following organizations:
#     1. California Institute of Technology, Pasadena, CA, USA
#     2. EMBL European Bioinformatics Institute (EMBL-EBI), Hinxton, UK
#     3. University of Heidelberg, Heidelberg, Germany
#
# Copyright 2005-2010 California Institute of Technology.
# Copyright 2002-2005 California Institute of Technology and
#                     Japan Science and Technology Corporation.
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation.  A copy of the license agreement is provided
# in the file named "LICENSE.txt" included with this software distribution
# and also available online as http://sbml.org/software/libsbml/license.html


import os
import platform
from distutils.core import Extension, setup
from distutils.sysconfig import get_config_var
from glob import glob
from os.path import dirname, join, realpath

current_dir = dirname(realpath(__file__))

# Remove the `-Wstrict-prototypes` compiler flag.
opt = get_config_var("OPT")
if opt:
    os.environ["OPT"] = " ".join(
        flag for flag in opt.split() if flag != "-Wstrict-prototypes"
    )

# Define macros based on the platform.
basepath = join(current_dir, "src", "base")
current_os = "LINUX"
definitions = []
packages = [
    ("USE_COMP", None),
    ("USE_QUAL", None),
    ("USE_FBC", None),
    ("USE_LAYOUT", None),
    ("USE_GROUPS", None),
    ("USE_MULTI", None),
    ("USE_RENDER", None),
    ("USE_L3V2EXTENDEDMATH", None),
]
if platform.system() == "Darwin":
    current_os = "DARWIN"
elif platform.system() == "Windows":
    current_os = "WIN32"
    definitions.extend([("LIBSBML_EXPORTS", None), ("LIBLAX_STATIC", None)])

definitions.extend(
    [("BZIP2_STATIC", None), ("HAVE_MEMMOVE", None), ("_LIB", None)]
)

# Add all source files.
cfiles = [join(basepath, "libsbml_wrap.cpp")]
cfiles.extend(glob(join(basepath, "*.c")))
for root, dirs, files in os.walk(join(basepath, "sbml")):
    for file in files:
        if file.endswith(".c") or file.endswith(".cpp"):
            cfiles.append(join(root, file))


setup(
    version="5.18.0",
    packages=["libsbml"],
    package_dir={"libsbml": "src/libsbml"},
    ext_package="libsbml",
    ext_modules=[
        Extension(
            "_libsbml",
            sources=cfiles,
            define_macros=definitions
            + [
                (current_os, None),
                ("USE_EXPAT", None),
                ("USE_ZLIB", None),
                ("USE_BZ2", None),
            ]
            + packages,
            include_dirs=[
                basepath,
            ],
        )
    ],
)
