# Runs p23_gen.py with the parameter values used in the paper.
import os, runpy, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
sys.argv = ['p23_gen.py', '0.70', '0.705', '0.707', '0.7071', '0.7072', '0.71']
runpy.run_path(os.path.join(here, 'p23_gen.py'), run_name='__main__')
