# Runs diff_check.py with the parameter values used in the paper.
import os, runpy, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
sys.argv = ['diff_check.py', '0.52', '0.6', '0.75', '0.8', '0.9', '0.95']
runpy.run_path(os.path.join(here, 'diff_check.py'), run_name='__main__')
