Standalone libSBML Python module
================================

This is used to create a standalone module for Python consisting of libSBML and libSBML extensions for accepted/released [SBML Level 3 packages](http://sbml.org/Documents/Specifications#SBML_Level_3_Packages).

[![License](http://img.shields.io/:license-LGPL-blue.svg)](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html)  [![Latest stable release](https://img.shields.io/badge/Latest_stable_release-5.12.1-brightgreen.svg)](http://shields.io)

----
*Main Authors*: [Sarah Keating](http://www.ebi.ac.uk/about/people/sarah-keating), [Michael Hucka](http://www.cds.caltech.edu/~mhucka), [Lucian P. Smith](http://www.washington.edu/home/peopledir/?method=name&term=smith), [Frank T. Bergmann](http://www.cos.uni-heidelberg.de/index.php/f.bergmann?l=_e), [Bruce Shapiro](http://www.bruce-shapiro.com), Thomas W. Evans, [Colin S. Gillespie](http://www.ncl.ac.uk/maths/about/staff/profile/colingillespie.html#background), [Darren J. Wilkinson](https://www.staff.ncl.ac.uk/d.j.wilkinson/), [Brett Olivier](http://www.bgoli.net), [Andrew Finney](https://www.linkedin.com/in/andrewmartinfinney).

*Repository*:   [https://github.com/sbmlteam/python-libsbml](https://github.com/sbmlteam/python-libsbml)

*Developers' discussion group*: [https://groups.google.com/forum/#!forum/libsbml-development](https://groups.google.com/forum/#!forum/libsbml-development)

*License*: For full license information, please refer to the file [../LICENSE.txt](https://raw.githubusercontent.com/sbmlteam/moccasin/master/LICENSE.txt) for details.  Briefly, the test case distributions of the SBML Test Suite are distributed under the terms of the [LGPL v2.1](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html); the overall SBML Test Suite (including the software components) are distributed under the LGPL but include components from other sources licensed under other open-source terms.  (However, none of the terms are more restrictive than the LGPL.)


♥️ Please cite the libSBML paper and the version you use
---------------------------------------------------------

Article citations are **critical** for us to be able to continue support for libSBML.  If you use libSBML and you publish papers about your software, we ask that you **please cite the libSBML paper**:

<dl>
<dd>
Benjamin J. Bornstein, Sarah M. Keating, Akira Jouraku, and Michael Hucka (2008) <a href="https://academic.oup.com/bioinformatics/article/24/6/880/194657/LibSBML-an-API-Library-for-SBML">LibSBML: An API Library for SBML.</a> <i>Bioinformatics</i>, 24(6):880–881, doi:10.1093/bioinformatics/btn051.

Harold F. Gómez, Michael Hucka, Sarah M. Keating, German Nudelman, Dagmar Iber and Stuart C. Sealfon.  <a href="http://bioinformatics.oxfordjournals.org/content/32/12/1905">MOCCASIN: converting MATLAB ODE models to SBML</a>. <i>Bioinformatics</i> (2016), 32(12): 1905-1906.
</dd>
</dl>


☀ Background and introduction
-----------------------------

LibSBML is a free, open-source programming library to help you read, write, manipulate, translate, and validate [SBML](http://sbml.org) files and data streams. It's not an application itself, but rather a library you embed in your own applications. The library supports all Levels and Versions of SBML, up to Level&nbsp;3 Version&nbsp;1 Core.

This repository contains code to generate a standalone Python module wrapping libSBML with a Python API.  The API is the standard Python API implemented with the help of [SWIG](http://swig.org) and provided in the libSBML distribution.


⁇ Getting Help
------------

The libSBML library, and associated utilities such as this Python module, under active development by a distributed team.  If you have any questions, please feel free to post or email on the  ([https://groups.google.com/forum/#!forum/libsbml-development](https://groups.google.com/forum/#!forum/libsbml-development)) forum, or contact the [libSBML Team](mailto:libsbml-team@googlegroups.com) directly.


☮ Copyright and license
---------------------

Please see the file [../LICENSE.txt](https://raw.githubusercontent.com/sbmlteam/sbml-test-suite/develop/src/misc/graphics-originals/Official-sbml-supported-70.jpg) for copyright and license details.


More information
----------------

Please visit [SBML.org](http://sbml.org) for more information about SBML (the Systems Biology Markup Language), as well as many resources for working with SBML.

