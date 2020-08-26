try:
    import nose
    have_nose = True
except: 
    have_nose = False
    pass

import libsbml


def test_libsbml():
    if have_nose: 
      nose.tools.assert_equal(libsbml.__version__, libsbml.getLibSBMLDottedVersion())
    
    print (libsbml.__version__)
    print (libsbml.getLibSBMLDottedVersion())

