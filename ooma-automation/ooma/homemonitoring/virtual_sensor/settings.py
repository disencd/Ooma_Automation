import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

print "PROJECT_ROOT %s" , PROJECT_ROOT
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'homemonitoring'))

