""" """

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns


# sns uses rgb values between 0 and 1
COLOR = {
    # compounds
    "Receptor": "#0b3d91",
    "Ligand": "#f9aa43",
    "Agonist": "#f9aa43",
    "Dissimilar decoy": "#99231b",
    "Similar decoy": "#c62d1f",
    # models (3D)
    "NeuralPLexer": "#5b616b",
    "ESMFold": "#478347",
    "RF-AA": "#A676D6",
    "RF-AA (no templates)": "#7352BF",
    "AF2": "#115185",
    "AF2 (no templates)": "#008FD7",
    "AF3": "#061f4a",
    # models (no structure)
    "Peptriever" : "#aeb0b5",
    "D-SCRIPT2" : "#aeb0b5",
    "AF2-LIS" : "#02bfe7",
    
    # classes
    "Class A (Rhodopsin)": "#115185",
    "Class B1 (Secretin)": "#478347",
    "Class F (Frizzled)": "#A676D6",
    "Other GPCRs": "#aeb0b5",
}


def get_good_bad_cmap():
    start_color = "#99231b"
    middle_color = "#f1f1f1"
    end_color = "#0b3d91"
    colors = [start_color, middle_color, end_color]
    cmap = LinearSegmentedColormap.from_list("good_bad_cmap", colors)
    return cmap


CMAP_GOOD_BAD = get_good_bad_cmap()

if __name__ == "__main__":
    # example
    plt.imshow(
        [[0, 0.5, 1]],
        cmap=CMAP_GOOD_BAD,
        aspect="auto",
        interpolation="nearest",
    )
    plt.colorbar()
    plt.show()
