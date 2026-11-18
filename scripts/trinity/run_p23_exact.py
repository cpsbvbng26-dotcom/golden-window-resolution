# Runs p23_exact.py with the parameter values used in the paper.
import os, runpy, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
sys.argv = ['p23_exact.py', '51/100', '11/20', '3/5', '5/8', '13/20', '2/3', '69/100', '7/10', '707/1000']
runpy.run_path(os.path.join(here, 'p23_exact.py'), run_name='__main__')
