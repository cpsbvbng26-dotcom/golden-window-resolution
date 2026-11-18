# Runs aps_face1.py with the parameter values used in the paper.
import os, runpy, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
sys.argv = ['aps_face1.py', '0.74', '0.76']
runpy.run_path(os.path.join(here, 'aps_face1.py'), run_name='__main__')
