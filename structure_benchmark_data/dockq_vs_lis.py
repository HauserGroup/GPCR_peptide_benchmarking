# Script to visualize the correlation between DockQ and LIS scores for the benchmark dataset
#
# Usage: python dockq_vs_lis.py
#

import os 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import sys

# Get the top-level directory
top_level_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(top_level_dir)
from colors import *



if __name__ == "__main__":
    # Get the file directory
    file_dir = os.path.dirname(__file__)

    # Path to the DockQ results file
    dockq_path = f"{file_dir}/DockQ_results.csv"

    # Get only AF2, AF3 and RFAA models
    input_models = ["AF2", "AF2_no_templates", "AF3"]
    for model in input_models:
        
        identity_vs_dockq_plot(model, dockq_path, training_struct_df)