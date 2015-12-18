#!/usr/bin/env python

"""
This software is used to test the KneadData pipeline.
Dependencies: KneadData (and all KneadData dependencies)
"""

import os
import sys
import unittest

# Try to load the kneaddata package to check the installation
try:
    from kneaddata import utilities
    from kneaddata import config
except ImportError:
    sys.exit("CRITICAL ERROR: Unable to find the kneaddata python package." +
        " Please check your install.") 

# check for the required python version
required_python_version_major = 2
required_python_version_minor = 7
    
try:
    if (sys.version_info[0] != required_python_version_major or
        sys.version_info[1] < required_python_version_minor):
        sys.exit("CRITICAL ERROR: The python version found (version "+
            str(sys.version_info[0])+"."+str(sys.version_info[1])+") "+
            "does not match the version required (version "+
            str(required_python_version_major)+"."+
            str(required_python_version_minor)+"+)")
except (AttributeError,IndexError):
    sys.exit("CRITICAL ERROR: The python version found (version 1) " +
        "does not match the version required (version "+
        str(required_python_version_major)+"."+
        str(required_python_version_minor)+"+)")  

def check_dependency(exe,bypass_permissions_check=None):
    """ Check the dependency can be found """
    if not utilities.find_exe_in_path(exe, bypass_permissions_check):
        sys.exit("ERROR: Unable to find "+exe+". Please install.")

def main():
    # Check for dependencies
    check_dependency(config.trimmomatic_jar,bypass_permissions_check=True)
    check_dependency(config.bowtie2_exe)
    check_dependency(config.bmtagger_exe)
    
    # Get the unittests
    directory_of_tests=os.path.dirname(os.path.abspath(__file__))
    
    functional_suite = unittest.TestLoader().discover(directory_of_tests,pattern='functional_tests*.py')
    basic_suite = unittest.TestLoader().discover(directory_of_tests,pattern='basic_tests*.py')

    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([basic_suite,functional_suite]))

if __name__ == '__main__':
    main()