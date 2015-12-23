__author__ = 'Cedric'
# Maltego transform for getting the robots.txt file from websites

from MaltegoTransform import *
import pastebin_python
import sys
import os
import requests

m = MaltegoTransform()
m.parseArguments(sys.argv)

uid = m.getVar('affiliation.uid')


