# Runs p23_scan.py with the parameter values used in the paper.
import os, runpy, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
sys.argv = ['p23_scan.py', '0.505', '0.55', '0.62', '0.66', '0.69', '0.71', '0.72', '0.75']
runpy.run_path(os.path.join(here, 'p23_scan.py'), run_name='__main__')
