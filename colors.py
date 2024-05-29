""" """

import pandas as pd


def hex_to_rgb(hex: str) -> tuple:
    """
    Convert hex to rgb
    """
    hex = hex.lstrip("#")
    lv = len(hex)
    return tuple(int(hex[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


# sns uses rgb values between 0 and 1
COLOR = {
    # compounds
    "receptor": "#0b3d91",
    "ligand": "#f9aa43",
    "agonist": "#f9aa43",
    "dissimilar_decoy": "#99231b",
    "similar_decoy": "#c62d1f",
    # models
    "RF-AA": "#0b3d91",
    "AlphaFold2": "#f9aa43",
    "AlphaFold3": "#f9aa43",
    # classes
    "Class A (Rhodopsin)": "#0b3d91",
    "Class B1 (Secretin)": "#2e8540",
    "Class F (Frizzled)": "#4c2c92",
    "Other GPCRs": "#aeb0b5",
}
