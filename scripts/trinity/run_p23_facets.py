# Runs p23_facets.py at delta = 3/5: the facets of P_23, enumerated in exact rationals.
import os, runpy, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
sys.argv = ['p23_facets.py', '3/5']
runpy.run_path(os.path.join(here, 'p23_facets.py'), run_name='__main__')
