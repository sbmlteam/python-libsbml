Standalone libSBML Python module
================================

This is used to create a standalone module for Python.  The module consists of [libSBML](http://sbml.org/Software/libSBML) and libSBML extensions for accepted/released [SBML Level 3 packages](http://sbml.org/Documents/Specifications#SBML_Level_3_Packages).

[![License](http://img.shields.io/:license-LGPL-blue.svg)](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html)  [![Latest stable release](https://img.shields.io/badge/Latest_stable_release-5.19.0-brightgreen.svg)](http://shields.io)

----
*Main Authors*: [Frank T. Bergmann](http://www.cos.uni-heidelberg.de/index.php/f.bergmann?l=_e), [Sarah Keating](http://www.ebi.ac.uk/about/people/sarah-keating), [Ben Bornstein](http://www.bbornstein.org), [Lucian P. Smith](http://www.washington.edu/home/peopledir/?method=name&term=smith), [Akiya Jouraku](https://www.researchgate.net/profile/Akiya_Jouraku), and [Michael Hucka](http://www.cds.caltech.edu/~mhucka).

*Repository*:   [https://github.com/sbmlteam/python-libsbml](https://github.com/sbmlteam/python-libsbml)

*Developers' discussion group*: [https://groups.google.com/forum/#!forum/libsbml-development](https://groups.google.com/forum/#!forum/libsbml-development)

*License*: For full license information, please refer to the file [../LICENSE.txt](https://raw.githubusercontent.com/sbmlteam/python-libsbml/master/LICENSE.txt) for details.


♥️ Please cite the libSBML paper and the version you use
---------------------------------------------------------

Article citations are **critical** for us to be able to continue support for libSBML.  If you use libSBML and you publish papers about your software, we ask that you **please cite the libSBML paper**:

<dl>
<dd>
Benjamin J. Bornstein, Sarah M. Keating, Akira Jouraku, and Michael Hucka (2008) <a href="https://academic.oup.com/bioinformatics/article/24/6/880/194657/LibSBML-an-API-Library-for-SBML">LibSBML: An API Library for SBML.</a> <i>Bioinformatics</i>, 24(6):880–881, doi:10.1093/bioinformatics/btn051.
</dd>
</dl>


☀ Background and introduction
-----------------------------

[libSBML](http://sbml.org/Software/libSBML) is a free, open-source programming library to help you read, write, manipulate, translate, and validate [SBML](http://sbml.org) files and data streams. It's not an application itself, but rather a library you embed in your own applications. The library supports all Levels and Versions of SBML, up to Level&nbsp;3 Version&nbsp;1 Core.

This repository contains code to generate a standalone Python module wrapping [libSBML](http://sbml.org/Software/libSBML) with a Python API.  The API is the standard Python API implemented with the help of [SWIG](http://swig.org) and provided in the libSBML distribution.

Preparing the package build
------------
First you will have a compiler compatible with your python version installed, as well as a recent version of: 

* cmake
* swig

In order to to build the python package, you will have to check out the repository, including its submodules, from there on all dependencies, libsbml and the python bindings will be built: 

	git clone https://github.com/sbmlteam/python-libsbml
	cd python-libsbml
	git submodule update --init


Building the package
------------
Once those steps are done, the library can be build using the `setup.py` script.

	python setup.py build

to build the experimental package, all that needs to be done is to set the environment variable `LIBSBML_EXPERIMENTAL=1` prior to building

⁇ Getting Help
------------

The [libSBML](http://sbml.org/Software/libSBML) library, and associated utilities such as this Python module, under active development by a distributed team.  If you have any questions, please feel free to post or email on the  ([https://groups.google.com/forum/#!forum/libsbml-development](https://groups.google.com/forum/#!forum/libsbml-development)) forum, or contact the [libSBML Team](mailto:libsbml-team@googlegroups.com) directly.


☮ Copyright and license
---------------------

Please see the file [../LICENSE.txt](https://raw.githubusercontent.com/sbmlteam/python-libsbml/master/LICENSE.txt) for copyright and license details.


More information
----------------

Please visit [SBML.org](http://sbml.org) for more information about SBML (the Systems Biology Markup Language), as well as many resources for working with SBML.

