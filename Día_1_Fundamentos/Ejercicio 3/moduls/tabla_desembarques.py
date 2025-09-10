import sys
import os

# Ruta raíz del proyecto (CURSO DASH)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_dir)

from dash import dash_table
import pandas as pd
import utils.functions_Python_BBDD as f