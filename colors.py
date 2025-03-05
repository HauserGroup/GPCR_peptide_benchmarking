"""
This script contains the colors used in the project.
It also contains functions to convert between different color formats. 
These colors are used in the project to maintain consistency in the color scheme.
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

def rgba_to_hex(rgba: tuple) -> str:
    """Convert rgba to hex.
    rgba is tuple of 4 floats between 0 and 1.
    """
    hex_color = "#{:02x}{:02x}{:02x}".format(
        int(rgba[0] * 255), int(rgba[1] * 255), int(rgba[2] * 255)
    )
    return hex_color

def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex to rgb.
    hex_color is a string of 6 characters.
    """
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return r, g, b

COLOR = {
    # compounds
    "Receptor": "#0b3d91",
    "Ligand": "#f9aa43",
    "Agonist": "#f9aa43",
    "Principal Agonist": "#f9aa43",
    # Decoys
    "Dissimilar decoy": "#99231b",
    "Similar decoy": "#0b3d91",
    "Dissimilar4": "#99231b",
    "Dissimilar3": "#aa4b44",
    "Dissimilar2": "#bc7570",
    "Dissimilar1": "#cd9d9a",
    "Dissimilar0": "#dfc7c6",
    "Similar0": "#c3cddd",
    "Similar1": "#94a8ca",
    "Similar2": "#6785b7",
    "Similar3": "#3860a3",
    "Similar4": "#0b3d91",
    # models (3D)
    "NeuralPLexer": "#5b616b",
    'Neuralplexer': "#5b616b",
    "ESMFold": "#478347",
    "RF-AA": "#A676D6",
    "RF-AA (no templates)": "#7352BF",
    "AF2": "#115185",
    "AF2 (no templates)": "#008FD7",
    "AF3": "#061F4A",
    "AF3 (no templates)": "#0b1321",
    "AF3 (server)": "#080e17",
    "Chai-1": "#855e40",
    "Chai-1 (no MSAs)": "#b89881",
    "ColabFold (no MSAs)": "#5b616b",

    # models (no structure)
    "Peptriever": "#9E005D",
    "D-SCRIPT2": "#aeb0b5",
    "D-SCRIPT": "#aeb0b5",
    # models (subanalysis)
    "AF2 LIS (no templates)": "#9E005D",
    "AF2 LIS": "#9E005D",
    "AF2 APPRAISE": "#98ECF9",
    # classes
    "Class A (Rhodopsin)": "#115185",
    "Class B1 (Secretin)": "#478347",
    "Class F (Frizzled)": "#A676D6",
    "Other GPCRs": "#aeb0b5",
    # pocket subtype
    "AF2 LIS (no templates)+pocket": "#aeb0b5",
    "RF-AA (no templates)+pocket": "#aeb0b5",
    "AF2+pocket": "#aeb0b5",
    "AF2 (no templates)+pocket": "#aeb0b5",
    # general
    False: "#0b3d91",
    True: "#f9aa43",

    # rescoring
    "RF-AA APPRAISE": "#A676D6",
    "RF-AA RIA energy": "#A676D6",
    "RF-AA RIA sc": "#A676D6",    
    "AF2 APPRAISE (no templates)": "#008FD7",
    "AF2 LIS (no templates)": "#008FD7",
    'AF2 LIS (no templates) 1m' :  "#008FD7",
    "AF2 RIA energy (no templates)": "#008FD7",
    "ColabFold (no MSAs)": "#5b616b",
    "ColabFold (no MSAs) LIS": "#5b616b",
    'AF2 RIA energy': "#008FD7",
    "AF2 RIA sc (no templates)": "#008FD7",
    'AF2 RIA sc': "#008FD7",
    "Peptriever": "#9E005D",

}

def get_good_bad_cmap():
    start_color = "#99231b"
    middle_color = "#f1f1f1"
    end_color = "#0b3d91"
    colors = [start_color, middle_color, end_color]
    cmap = LinearSegmentedColormap.from_list("good_bad_cmap", colors)
    return cmap

# Define the colormap for the good and bad decoys
CMAP_GOOD_BAD = get_good_bad_cmap()

def run_main():
    # Print decoy colors by splitting CMAP_GOOD_BAD in 11 and skipping the middle color
    colors_to_show = []
    for i in range(0, 11, 1):
        if i == 5:
            continue
        # Print hex color
        rgba = CMAP_GOOD_BAD(i / 10)
        hex_color = rgba_to_hex(rgba)
        print(rgba, hex_color)
        colors_to_show.append(hex_color)

    fig, ax = plt.subplots(1, 10, figsize=(10, 1))
    for i, color in enumerate(colors_to_show):
        plt.sca(ax[i])
        plt.axis("off")
        plt.fill_between([0, 1], 0, 1, color=color)
    plt.show()

if __name__ == "__main__":
    run_main()
