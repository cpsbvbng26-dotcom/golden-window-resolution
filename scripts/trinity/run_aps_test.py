# Runs aps_test.py with the parameter values used in the paper.
import os, runpy, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
sys.argv = ['aps_test.py', '0.55', '0.6', '0.7', '0.9', '0.74', '0.76', '0.89', '0.91']
runpy.run_path(os.path.join(here, 'aps_test.py'), run_name='__main__')
