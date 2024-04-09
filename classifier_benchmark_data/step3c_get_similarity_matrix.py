""" Get similarity matrix for all GPCRs in the interactions dataset.
    These similarity values are later used to select the decoys.
"""
# standard library
import requests
import json
import pathlib
import random 
import os
import time 
from collections import Counter
import argparse

# external libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.spatial import distance
from scipy.cluster import hierarchy


def get_generic_residue_numbers_from_string(input_str):
    """ input_str: string with all the generic residue numbers separated by a newline

    example:
    1x28 [GPCRdb(A)] (Residue) 
    1x29 [GPCRdb(A)] (Residue) 
    1x27 [GPCRdb(A)] (Residue) 
    ...

    returns:
    list of strings with the generic residue numbers
    for example: ["1x28", "1x29", "1x27", ...]
    """
    lines = input_str.split("\n")
    lines = [line.strip() for line in lines if len(line.strip()) > 0]
    # only keep the 6x58 part
    lines = [split_part[0] for split_part in [line.split(" ") for line in lines]]
    # remove duplicates
    lines = list(set(lines))
    return lines


def get_class_A_ligand_binding_pocket_generic_residue_numbers():
    """ https://gpcrdb.org/similaritysearch/segmentselection -> ligand binding pocket -> Class A
    """
    out_str = """
    1x28 [GPCRdb(A)] (Residue) 
    1x29 [GPCRdb(A)] (Residue) 
    1x27 [GPCRdb(A)] (Residue) 
    1x32 [GPCRdb(A)] (Residue) 
    1x30 [GPCRdb(A)] (Residue) 
    1x31 [GPCRdb(A)] (Residue) 
    1x33 [GPCRdb(A)] (Residue) 
    1x34 [GPCRdb(A)] (Residue) 
    1x25 [GPCRdb(A)] (Residue) 
    1x35 [GPCRdb(A)] (Residue) 
    1x24 [GPCRdb(A)] (Residue) 
    1x36 [GPCRdb(A)] (Residue) 
    1x38 [GPCRdb(A)] (Residue) 
    1x39 [GPCRdb(A)] (Residue) 
    1x41 [GPCRdb(A)] (Residue) 
    1x42 [GPCRdb(A)] (Residue) 
    1x43 [GPCRdb(A)] (Residue) 
    1x46 [GPCRdb(A)] (Residue) 
    1x47 [GPCRdb(A)] (Residue) 
    4x46 [GPCRdb(A)] (Residue) 
    45x50 [GPCRdb(A)] (Residue) 
    45x51 [GPCRdb(A)] (Residue) 
    45x52 [GPCRdb(A)] (Residue) 
    6x62 [GPCRdb(A)] (Residue) 
    5x33 [GPCRdb(A)] (Residue) 
    5x35 [GPCRdb(A)] (Residue) 
    3x35 [GPCRdb(A)] (Residue) 
    3x44 [GPCRdb(A)] (Residue) 
    4x48 [GPCRdb(A)] (Residue) 
    5x65 [GPCRdb(A)] (Residue) 
    7x32 [GPCRdb(A)] (Residue) 
    7x36 [GPCRdb(A)] (Residue) 
    7x43 [GPCRdb(A)] (Residue) 
    7x45 [GPCRdb(A)] (Residue) 
    5x28 [GPCRdb(A)] (Residue) 
    2x43 [GPCRdb(A)] (Residue) 
    4x45 [GPCRdb(A)] (Residue) 
    5x62 [GPCRdb(A)] (Residue) 
    7x34 [GPCRdb(A)] (Residue) 
    8x47 [GPCRdb(A)] (Residue) 
    23x47 [GPCRdb(A)] (Residue) 
    23x501 [GPCRdb(A)] (Residue) 
    4x50 [GPCRdb(A)] (Residue) 
    4x52 [GPCRdb(A)] (Residue) 
    5x461 [GPCRdb(A)] (Residue) 
    7x39 [GPCRdb(A)] (Residue) 
    8x48 [GPCRdb(A)] (Residue) 
    8x49 [GPCRdb(A)] (Residue) 
    12x49 [GPCRdb(A)] (Residue) 
    2x50 [GPCRdb(A)] (Residue) 
    2x63 [GPCRdb(A)] (Residue) 
    6x34 [GPCRdb(A)] (Residue) 
    6x40 [GPCRdb(A)] (Residue) 
    2x56 [GPCRdb(A)] (Residue) 
    5x61 [GPCRdb(A)] (Residue) 
    7x31 [GPCRdb(A)] (Residue) 
    4x56 [GPCRdb(A)] (Residue) 
    5x50 [GPCRdb(A)] (Residue) 
    12x51 [GPCRdb(A)] (Residue) 
    2x42 [GPCRdb(A)] (Residue) 
    2x53 [GPCRdb(A)] (Residue) 
    3x22 [GPCRdb(A)] (Residue) 
    3x26 [GPCRdb(A)] (Residue) 
    4x41 [GPCRdb(A)] (Residue) 
    4x49 [GPCRdb(A)] (Residue) 
    6x57 [GPCRdb(A)] (Residue) 
    7x55 [GPCRdb(A)] (Residue) 
    3x18 [GPCRdb(A)] (Residue) 
    3x50 [GPCRdb(A)] (Residue) 
    5x38 [GPCRdb(A)] (Residue) 
    6x56 [GPCRdb(A)] (Residue) 
    6x64 [GPCRdb(A)] (Residue) 
    3x24 [GPCRdb(A)] (Residue) 
    3x40 [GPCRdb(A)] (Residue) 
    4x68 [GPCRdb(A)] (Residue) 
    6x54 [GPCRdb(A)] (Residue) 
    7x46 [GPCRdb(A)] (Residue) 
    1x57 [GPCRdb(A)] (Residue) 
    3x39 [GPCRdb(A)] (Residue) 
    5x48 [GPCRdb(A)] (Residue) 
    7x35 [GPCRdb(A)] (Residue) 
    23x49 [GPCRdb(A)] (Residue) 
    23x50 [GPCRdb(A)] (Residue) 
    4x57 [GPCRdb(A)] (Residue) 
    4x58 [GPCRdb(A)] (Residue) 
    5x59 [GPCRdb(A)] (Residue) 
    6x59 [GPCRdb(A)] (Residue) 
    8x53 [GPCRdb(A)] (Residue) 
    12x50 [GPCRdb(A)] (Residue) 
    2x57 [GPCRdb(A)] (Residue) 
    3x25 [GPCRdb(A)] (Residue) 
    3x46 [GPCRdb(A)] (Residue) 
    3x48 [GPCRdb(A)] (Residue) 
    5x44 [GPCRdb(A)] (Residue) 
    3x28 [GPCRdb(A)] (Residue) 
    4x51 [GPCRdb(A)] (Residue) 
    5x36 [GPCRdb(A)] (Residue) 
    5x51 [GPCRdb(A)] (Residue) 
    2x37 [GPCRdb(A)] (Residue) 
    2x62 [GPCRdb(A)] (Residue) 
    3x30 [GPCRdb(A)] (Residue) 
    34x56 [GPCRdb(A)] (Residue) 
    5x57 [GPCRdb(A)] (Residue) 
    6x45 [GPCRdb(A)] (Residue) 
    6x49 [GPCRdb(A)] (Residue) 
    7x30 [GPCRdb(A)] (Residue) 
    7x33 [GPCRdb(A)] (Residue) 
    2x61 [GPCRdb(A)] (Residue) 
    3x37 [GPCRdb(A)] (Residue) 
    7x47 [GPCRdb(A)] (Residue) 
    3x41 [GPCRdb(A)] (Residue) 
    34x53 [GPCRdb(A)] (Residue) 
    6x33 [GPCRdb(A)] (Residue) 
    7x38 [GPCRdb(A)] (Residue) 
    2x52 [GPCRdb(A)] (Residue) 
    2x59 [GPCRdb(A)] (Residue) 
    2x66 [GPCRdb(A)] (Residue) 
    7x48 [GPCRdb(A)] (Residue) 
    3x34 [GPCRdb(A)] (Residue) 
    3x47 [GPCRdb(A)] (Residue) 
    3x49 [GPCRdb(A)] (Residue) 
    4x43 [GPCRdb(A)] (Residue) 
    4x60 [GPCRdb(A)] (Residue) 
    6x44 [GPCRdb(A)] (Residue) 
    6x48 [GPCRdb(A)] (Residue) 
    5x32 [GPCRdb(A)] (Residue) 
    1x53 [GPCRdb(A)] (Residue) 
    2x551 [GPCRdb(A)] (Residue) 
    5x37 [GPCRdb(A)] (Residue) 
    5x47 [GPCRdb(A)] (Residue) 
    7x40 [GPCRdb(A)] (Residue) 
    2x65 [GPCRdb(A)] (Residue) 
    2x68 [GPCRdb(A)] (Residue) 
    3x21 [GPCRdb(A)] (Residue) 
    6x61 [GPCRdb(A)] (Residue) 
    3x32 [GPCRdb(A)] (Residue) 
    3x51 [GPCRdb(A)] (Residue) 
    5x55 [GPCRdb(A)] (Residue) 
    5x58 [GPCRdb(A)] (Residue) 
    5x66 [GPCRdb(A)] (Residue) 
    6x30 [GPCRdb(A)] (Residue) 
    6x37 [GPCRdb(A)] (Residue) 
    7x41 [GPCRdb(A)] (Residue) 
    5x29 [GPCRdb(A)] (Residue) 
    2x39 [GPCRdb(A)] (Residue) 
    2x40 [GPCRdb(A)] (Residue) 
    2x64 [GPCRdb(A)] (Residue) 
    3x27 [GPCRdb(A)] (Residue) 
    3x54 [GPCRdb(A)] (Residue) 
    6x60 [GPCRdb(A)] (Residue) 
    7x37 [GPCRdb(A)] (Residue) 
    2x49 [GPCRdb(A)] (Residue) 
    3x45 [GPCRdb(A)] (Residue) 
    3x52 [GPCRdb(A)] (Residue) 
    6x51 [GPCRdb(A)] (Residue) 
    1x56 [GPCRdb(A)] (Residue) 
    4x62 [GPCRdb(A)] (Residue) 
    6x55 [GPCRdb(A)] (Residue) 
    7x27 [GPCRdb(A)] (Residue) 
    7x28 [GPCRdb(A)] (Residue) 
    7x29 [GPCRdb(A)] (Residue) 
    8x50 [GPCRdb(A)] (Residue) 
    7x24 [GPCRdb(A)] (Residue) 
    2x58 [GPCRdb(A)] (Residue) 
    23x52 [GPCRdb(A)] (Residue) 
    3x36 [GPCRdb(A)] (Residue) 
    4x54 [GPCRdb(A)] (Residue) 
    4x65 [GPCRdb(A)] (Residue) 
    5x39 [GPCRdb(A)] (Residue) 
    5x46 [GPCRdb(A)] (Residue) 
    6x47 [GPCRdb(A)] (Residue) 
    7x42 [GPCRdb(A)] (Residue) 
    6x63 [GPCRdb(A)] (Residue) 
    7x23 [GPCRdb(A)] (Residue) 
    2x38 [GPCRdb(A)] (Residue) 
    3x31 [GPCRdb(A)] (Residue) 
    3x33 [GPCRdb(A)] (Residue) 
    3x38 [GPCRdb(A)] (Residue) 
    34x57 [GPCRdb(A)] (Residue) 
    5x53 [GPCRdb(A)] (Residue) 
    5x54 [GPCRdb(A)] (Residue) 
    6x38 [GPCRdb(A)] (Residue) 
    2x55 [GPCRdb(A)] (Residue) 
    4x53 [GPCRdb(A)] (Residue) 
    5x42 [GPCRdb(A)] (Residue) 
    6x41 [GPCRdb(A)] (Residue) 
    6x52 [GPCRdb(A)] (Residue) 
    2x54 [GPCRdb(A)] (Residue) 
    2x67 [GPCRdb(A)] (Residue) 
    4x61 [GPCRdb(A)] (Residue) 
    4x63 [GPCRdb(A)] (Residue) 
    4x64 [GPCRdb(A)] (Residue) 
    7x53 [GPCRdb(A)] (Residue) 
    2x60 [GPCRdb(A)] (Residue) 
    3x29 [GPCRdb(A)] (Residue) 
    4x42 [GPCRdb(A)] (Residue) 
    5x40 [GPCRdb(A)] (Residue) 
    5x41 [GPCRdb(A)] (Residue) 
    5x43 [GPCRdb(A)] (Residue) 
    5x49 [GPCRdb(A)] (Residue) 
    6x35 [GPCRdb(A)] (Residue) 
    6x36 [GPCRdb(A)] (Residue) 
    6x58 [GPCRdb(A)] (Residue)
    """
    return get_generic_residue_numbers_from_string(out_str)


def get_class_B1_ligand_binding_pocket_generic_residue_numbers():
    out_str = """
    2x79 [GPCRdb(B)] (Residue) 
    2x81 [GPCRdb(B)] (Residue) 
    1x29 [GPCRdb(B)] (Residue) 
    1x30 [GPCRdb(B)] (Residue) 
    1x32 [GPCRdb(B)] (Residue) 
    1x33 [GPCRdb(B)] (Residue) 
    1x34 [GPCRdb(B)] (Residue) 
    1x35 [GPCRdb(B)] (Residue) 
    1x36 [GPCRdb(B)] (Residue) 
    1x37 [GPCRdb(B)] (Residue) 
    1x38 [GPCRdb(B)] (Residue) 
    1x39 [GPCRdb(B)] (Residue) 
    1x40 [GPCRdb(B)] (Residue) 
    1x41 [GPCRdb(B)] (Residue) 
    1x42 [GPCRdb(B)] (Residue) 
    1x43 [GPCRdb(B)] (Residue) 
    1x44 [GPCRdb(B)] (Residue) 
    1x45 [GPCRdb(B)] (Residue) 
    2x60 [GPCRdb(B)] (Residue) 
    3x40 [GPCRdb(B)] (Residue) 
    3x41 [GPCRdb(B)] (Residue) 
    3x43 [GPCRdb(B)] (Residue) 
    3x44 [GPCRdb(B)] (Residue) 
    3x54 [GPCRdb(B)] (Residue) 
    4x60 [GPCRdb(B)] (Residue) 
    4x62 [GPCRdb(B)] (Residue) 
    4x64 [GPCRdb(B)] (Residue) 
    4x66 [GPCRdb(B)] (Residue) 
    6x54 [GPCRdb(B)] (Residue) 
    6x55 [GPCRdb(B)] (Residue) 
    6x56 [GPCRdb(B)] (Residue) 
    6x57 [GPCRdb(B)] (Residue) 
    6x58 [GPCRdb(B)] (Residue) 
    7x32 [GPCRdb(B)] (Residue) 
    7x38 [GPCRdb(B)] (Residue) 
    7x39 [GPCRdb(B)] (Residue) 
    1x25 [GPCRdb(B)] (Residue) 
    3x36 [GPCRdb(B)] (Residue) 
    1x26 [GPCRdb(B)] (Residue) 
    1x27 [GPCRdb(B)] (Residue) 
    1x47 [GPCRdb(B)] (Residue) 
    1x48 [GPCRdb(B)] (Residue) 
    1x49 [GPCRdb(B)] (Residue) 
    2x64 [GPCRdb(B)] (Residue) 
    2x65 [GPCRdb(B)] (Residue) 
    2x66 [GPCRdb(B)] (Residue) 
    2x67 [GPCRdb(B)] (Residue) 
    2x68 [GPCRdb(B)] (Residue) 
    2x69 [GPCRdb(B)] (Residue) 
    2x70 [GPCRdb(B)] (Residue) 
    3x29 [GPCRdb(B)] (Residue) 
    3x32 [GPCRdb(B)] (Residue) 
    7x49 [GPCRdb(B)] (Residue) 
    7x51 [GPCRdb(B)] (Residue) 
    7x52 [GPCRdb(B)] (Residue) 
    8x49 [GPCRdb(B)] (Residue) 
    2x73 [GPCRdb(B)] (Residue) 
    2x74 [GPCRdb(B)] (Residue) 
    7x56 [GPCRdb(B)] (Residue) 
    2x71 [GPCRdb(B)] (Residue) 
    7x47 [GPCRdb(B)] (Residue) 
    2x57 [GPCRdb(B)] (Residue) 
    2x72 [GPCRdb(B)] (Residue) 
    2x75 [GPCRdb(B)] (Residue) 
    6x41 [GPCRdb(B)] (Residue) 
    6x42 [GPCRdb(B)] (Residue) 
    6x43 [GPCRdb(B)] (Residue) 
    6x44 [GPCRdb(B)] (Residue) 
    3x33 [GPCRdb(B)] (Residue) 
    7x37 [GPCRdb(B)] (Residue) 
    7x45 [GPCRdb(B)] (Residue) 
    7x46 [GPCRdb(B)] (Residue) 
    3x37 [GPCRdb(B)] (Residue) 
    6x40 [GPCRdb(B)] (Residue) 
    2x76 [GPCRdb(B)] (Residue) 
    5x65 [GPCRdb(B)] (Residue) 
    6x36 [GPCRdb(B)] (Residue) 
    6x37 [GPCRdb(B)] (Residue) 
    6x60 [GPCRdb(B)] (Residue) 
    7x41 [GPCRdb(B)] (Residue) 
    7x42 [GPCRdb(B)] (Residue) 
    7x44 [GPCRdb(B)] (Residue) 
    6x46 [GPCRdb(B)] (Residue) 
    6x47 [GPCRdb(B)] (Residue) 
    6x49 [GPCRdb(B)] (Residue) 
    6x50 [GPCRdb(B)] (Residue) 
    6x52 [GPCRdb(B)] (Residue) 
    6x53 [GPCRdb(B)] (Residue) 
    6x59 [GPCRdb(B)] (Residue) 
    3x47 [GPCRdb(B)] (Residue) 
    45x50 [GPCRdb(B)] (Residue) 
    45x51 [GPCRdb(B)] (Residue) 
    45x52 [GPCRdb(B)] (Residue) 
    5x37 [GPCRdb(B)] (Residue) 
    5x38 [GPCRdb(B)] (Residue) 
    5x39 [GPCRdb(B)] (Residue) 
    5x47 [GPCRdb(B)] (Residue) 
    5x50 [GPCRdb(B)] (Residue) 
    5x51 [GPCRdb(B)] (Residue) 
    5x61 [GPCRdb(B)] (Residue) 
    5x62 [GPCRdb(B)] (Residue) 
    6x38 [GPCRdb(B)] (Residue) 
    6x39 [GPCRdb(B)] (Residue) 
    7x60 [GPCRdb(B)] (Residue) 
    5x40 [GPCRdb(B)] (Residue) 
    5x43 [GPCRdb(B)] (Residue) 
    5x44 [GPCRdb(B)] (Residue) 
    7x34 [GPCRdb(B)] (Residue) 
    7x35 [GPCRdb(B)] (Residue) 
    5x54 [GPCRdb(B)] (Residue) 
    5x58 [GPCRdb(B)] (Residue) 
    8x47 [GPCRdb(B)] (Residue) 
    8x48 [GPCRdb(B)] (Residue)
    """
    return get_generic_residue_numbers_from_string(out_str)


def get_class_F_ligand_binding_pocket_generic_residue_numbers():
    out_str = """
    2x51 [GPCRdb(F)] (Residue) 
    3x36 [GPCRdb(F)] (Residue) 
    5x47 [GPCRdb(F)] (Residue) 
    5x51 [GPCRdb(F)] (Residue) 
    6x31 [GPCRdb(F)] (Residue) 
    7x35 [GPCRdb(F)] (Residue) 
    7x38 [GPCRdb(F)] (Residue) 
    7x41 [GPCRdb(F)] (Residue) 
    7x42 [GPCRdb(F)] (Residue) 
    5x70 [GPCRdb(F)] (Residue) 
    6x35 [GPCRdb(F)] (Residue) 
    6x38 [GPCRdb(F)] (Residue) 
    6x44 [GPCRdb(F)] (Residue) 
    6x47 [GPCRdb(F)] (Residue) 
    6x51 [GPCRdb(F)] (Residue) 
    6x54 [GPCRdb(F)] (Residue) 
    6x58 [GPCRdb(F)] (Residue) 
    6x61 [GPCRdb(F)] (Residue) 
    6x62 [GPCRdb(F)] (Residue) 
    1x32 [GPCRdb(F)] (Residue) 
    1x36 [GPCRdb(F)] (Residue) 
    45x51 [GPCRdb(F)] (Residue) 
    5x44 [GPCRdb(F)] (Residue) 
    3x40 [GPCRdb(F)] (Residue) 
    3x43 [GPCRdb(F)] (Residue) 
    3x50 [GPCRdb(F)] (Residue) 
    2x58 [GPCRdb(F)] (Residue) 
    5x62 [GPCRdb(F)] (Residue) 
    6x65 [GPCRdb(F)] (Residue) 
    5x66 [GPCRdb(F)] (Residue) 
    7x44 [GPCRdb(F)] (Residue) 
    7x45 [GPCRdb(F)] (Residue) 
    7x48 [GPCRdb(F)] (Residue
    """
    return get_generic_residue_numbers_from_string(out_str)


def get_GPCR_similarity_data(query_protein, comparison_proteins, segments):
    """ Get similarity between two GPCRs using a 7TM alignments (only the 
    transmembrane / conserved regions, not the loops)
    /services/alignment/protein/{proteins}/{segments}/

    query_protein: str, GPCRdb ID of the query protein
    comparison_proteins: list of str, GPCRdb IDs of the comparison proteins
    segments: list of str, segments to compare (e.g. 'TM1', 'TM2', 'TM3', 'TM4', 'TM5', 'TM6', 'TM7')
              full list of segments: https://gpcrdb.org/similaritymatrix/segmentselection -> sequence segments

    returns: dict (keys are the protein identifier, 
                   values are nested dicts.
                     keys of nested dict are 'similarity', 'identity', 'AA')
    """
    # proteins
    all_proteins = [query_protein] + comparison_proteins
    # proteins shouldn't be command separated, they should also start and end with comma
    proteins = ','.join(all_proteins)
    segments = ','.join(segments)

    base = "https://gpcrdb.org/services/alignment/similarity/"
    request_url = f"{base}{proteins}/{segments}/"

    response = requests.get(request_url)
    if response.status_code == 200:
        # load json and return
        json_data = json.loads(response.text)
        return json_data
    else:
        print(f"ERROR: {response.status_code}\n")
        return None
 

def get_GPCR_similarity_values_TM(query_protein, compared_proteins, mode):
    """ Get the GPCR similarity values by aligning the transmembrane regions (TM1-TM7)
    """
    segments = ["TM1", "TM2", "TM3", "TM4", "TM5", "TM6", "TM7"]
    data = get_GPCR_similarity_data(query_protein=query_protein, comparison_proteins=compared_proteins, segments=segments)
    out_dict = dict()

    for compared_protein in compared_proteins:
        # get similarity value
        similarity = data[compared_protein][mode]
        out_dict[compared_protein] = float(similarity)

    return out_dict


def get_GPCR_similarity_values_generic_residue_map(query_protein, compared_proteins, mode):
    """ Get the GPCR similarity values by aligning on the generic residue numbers of the
        binding pockets (shared between class A and class B1 receptors)
    """
    # 7x34, 7x38, 3x32, 3x33, 45x52 or 45x51 
    segments = ["7x34", "7x38", "3x32", "3x33", "45x52", "45x51"]
    data = get_GPCR_similarity_data(query_protein=query_protein, 
                                    comparison_proteins=compared_proteins, 
                                    segments=segments)
    out_dict = dict()
    for compared_protein in compared_proteins:
        # get similarity value
        similarity = data[compared_protein][mode]
        out_dict[compared_protein] = float(similarity)

    return out_dict


def get_residue_data_for_GPCR(gpcrdb_id):
    base = "https://gpcrdb.org/services/residues/extended"
    request_url = f"{base}/{gpcrdb_id}/"
    response = requests.get(request_url)
    if response.status_code == 200:
        # load json and return
        json_data = json.loads(response.text)
        return json_data
    else:
        print(f"ERROR: {response.status_code}\n")
        return None
    

def get_generic_residues_for_GPCR(gpcrdb_id):
    """ Get the generic residue numbers for a GPCR
    """
    data = get_residue_data_for_GPCR(gpcrdb_id)
    generic_residues = [residue["display_generic_number"] for residue in data if residue["display_generic_number"] is not None]
    return generic_residues


def get_GPCR_similarity_values_binding_pocket(query_protein, compared_proteins, list_of_GPCRdb_ids, mode):
    """ Get the GPCR similarity values by aligning on the generic residue numbers of the
        binding pockets (shared between class A and class B1 receptors)
    """
    # get generic residue numbers for the binding pocket (first for A)
    segments_A = get_class_A_ligand_binding_pocket_generic_residue_numbers()
    segments_B = get_class_B1_ligand_binding_pocket_generic_residue_numbers()
    segments_F = get_class_F_ligand_binding_pocket_generic_residue_numbers()
    segments_A = set(segments_A)
    segments_B = set(segments_B)
    segments_F = set(segments_F)
    # add all sets together
    segments = segments_A.intersection(segments_B).intersection(segments_F)
    data = get_GPCR_similarity_data(query_protein=query_protein, 
                                    comparison_proteins=compared_proteins, 
                                    segments=segments)
    if data is None:
        print("No data for this query protein, returning empty dict", query_protein)
        return dict()
        
    out_dict = dict()
    for compared_protein in compared_proteins:
        # get similarity value
        similarity = data[compared_protein][mode]
      
        out_dict[compared_protein] = float(similarity)

    return out_dict


def save_similarity_matrix_seaborn(sim_df, save_path, title):
    """
    """
    # the first column are the GPCRdb IDs (not numeric), adjust
    sim_df = sim_df.set_index(sim_df.columns[0])

    # make df numeric (in case it is not)
    sim_df = sim_df.apply(pd.to_numeric)

    # plot the similarity matrix
    sns.set_theme(style="white")

    # do hierarchical clustering
    correlations = sim_df.corr()
    correlations_array = np.asarray(sim_df.corr())
    row_linkage = hierarchy.linkage(distance.pdist(correlations_array), method='average')
    col_linkage = hierarchy.linkage(distance.pdist(correlations_array.T), method='average')
    clusters = sns.clustermap(correlations, row_linkage=row_linkage, col_linkage=col_linkage, method="average")
    plt.close()
    # apply this clustering to the similarity matrix
    sim_df = sim_df.iloc[clusters.dendrogram_row.reordered_ind, 
                         clusters.dendrogram_col.reordered_ind]
    
    # assert the similarity columns and rows are the same
    assert list(sim_df.columns) == list(sim_df.index), "Columns and rows are not symmetrical"

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(sim_df, dtype=bool))

    # add values >25 to the mask
    # mask = mask | (sim_df > 25)

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(20, 20))

    # calculate usable font size for the xlabels and ylabels
    size = len(sim_df) / 20
    if size < 1:
        size = 1
    ax.set_title(title, fontsize=size+25)

    cmap = sns.diverging_palette(230, 20, as_cmap=True, center="light")
    
    # set font xlabels
    for item in ax.get_xticklabels() + ax.get_yticklabels():
        item.set_fontsize(size)

    # set padding of labels to 0
    ax.tick_params(axis='both', which='major', pad=0)
    
    # draw the heatmap with the mask and correct aspect ratio, also make sure the labels are readable
    sns.heatmap(sim_df, mask=mask, cmap=cmap, vmax=100, center=50,                
                square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=False)

    # add a black outline to the heatmap values that are 100% similar
    # update the colorbar
    cbar_size = size + 10
    cbar = ax.collections[0].colorbar
    cbar.set_ticks([0, 25, 50, 75, 100])
    cbar.set_ticklabels([0, 25, 50, 75, 100])
    cbar.ax.tick_params(labelsize=cbar_size)
    cbar.ax.set_ylabel("Similarity metric (%)",
                       rotation=270, 
                       fontsize=cbar_size,
                       labelpad=20)
    # give the colorbar a minimum value of 0 TO 100
    #  cbar.mappable.set_clim(vmin=0, vmax=100)
    # set colorbar minimum to min and max
    cbar.mappable.set_clim(vmin=sim_df[mask].min().min(), vmax=sim_df[mask].max().max())

    # add GPCR count to the top right corner
    test_to_add = f"Unique GPCRs:\n n={len(sim_df)}"
    ax.text(0.99, 0.99, test_to_add, horizontalalignment='right', verticalalignment='top', 
            transform=ax.transAxes, fontsize=size+10)

    # move the colorbar position
    pos = ax.get_position()
    cbar.ax.set_position([pos.x1 - 0.075, pos.y1 - 0.35, 0.25, pos.height / 2])

    # subtitle
    ax.text(0.5, 0.975, "Average linkage hierarchical clustering", horizontalalignment='center', verticalalignment='top', 
            transform=ax.transAxes, fontsize=size+15)

    # get most similar GPCR values (ignoring self similarity)
    most_sim_df = sim_df.copy()
    # self similarity is 100, so set this to None
    for gpcr in list(most_sim_df.index):
        most_sim_df[gpcr][gpcr] = None
    most_sim_df = most_sim_df.idxmax(axis=1)
    # color the ylabels based on the most similar GPCR (color is based on the similarity score and the cmap)
    for item in ax.get_yticklabels() + ax.get_xticklabels():
        item.set_fontsize(size)
        gpcr_id = item.get_text()
        most_sim = most_sim_df[gpcr_id]
        # get color from cmap
        color = cmap(sim_df.loc[gpcr_id, most_sim] / 100)
        item.set_bbox(dict(facecolor=color, alpha=0.5, boxstyle='square,pad=0.1'))

    # add a title to the ylabels
    ax.set_ylabel("GPCRdb ID, colored based on most similar GPCR", fontsize=size+3)
    ax.set_xlabel("GPCRdb ID, colored based on most similar GPCR", fontsize=size+3)

    # save the figure
    plt.savefig(save_path, dpi=300, bbox_inches='tight')


def create_similarity_matrix(interactions_df_path, output_path, get_similarity_function, mode):
    """
    get_similarity_function: use get_GPCR_similarity_values_TM or get_GPCR_similarity_values_binding_pocket
                             TM = all transmembrane regions,
                            binding pocket = only the generic residue numbers of the binding pocket present for both class A and class B1
    """
    assert mode in ['similarity', 'identity'], "Mode should be either 'similarity' or 'identity"
    # read the interactions between GPCRs and ligands
    df_inter = pd.read_csv(interactions_df_path)
    all_gpcrs = list(df_inter["Target GPCRdb ID"].unique())
    count = 0 

    # create empty df matrix of all GPCRs vs all GPCRs
    out_df = pd.DataFrame(index=all_gpcrs, columns=all_gpcrs)

    # create seq similarity matrix
    print(f"Getting pairwise similarity matrix for {len(all_gpcrs)} GPCRs")

    for target_index, target in enumerate(all_gpcrs):
        print(f"{target_index+1}/{len(all_gpcrs)} : {target}")#, end="\r")
        query_protein = target
        compared_proteins = all_gpcrs

        # get dict with format {compared_protein: similarity}
        if get_similarity_function == get_GPCR_similarity_values_TM:
            similarity_dict = get_similarity_function(query_protein, compared_proteins, mode)
        elif get_similarity_function == get_GPCR_similarity_values_binding_pocket:
            similarity_dict = get_similarity_function(query_protein, compared_proteins, all_gpcrs, mode)
        elif get_similarity_function == get_GPCR_similarity_values_generic_residue_map:
            similarity_dict = get_similarity_function(query_protein, compared_proteins, mode)
        else:
            raise ValueError(f"Unknown similarity function: {get_similarity_function}")

        # add to larger output df
        for compared_protein, similarity in similarity_dict.items():
            out_df.loc[target, compared_protein] = similarity
    
    # save df
    out_df.to_csv(output_path)


def report_similarity_matrix(df):
    """
    """
    # report on GPCRs with different target IDs but 100% similarity
    df = df.set_index(df.columns[0])
    # set self similarity to None
    for gpcr in list(df.index):
        df[gpcr][gpcr] = None

    # get column and row index pairs with 100% similarity
    similar_gpcrs = set()
    for gpcr in list(df.index):
        for compared_gpcr in list(df.columns):
            if df[gpcr][compared_gpcr] == 100:
                similar_gpcrs.add(tuple(sorted([gpcr, compared_gpcr])))
    
    # report
    print(f"Found {len(similar_gpcrs)} GPCR pairs with different target IDs but 100% similarity")
    for gpcr, compared_gpcr in similar_gpcrs:
        print(f"\t{gpcr} {compared_gpcr}", df[gpcr][compared_gpcr])


def plot_similarity_distribution(inter_df, sim_df, save_path,
                                 rec_col="Target GPCRdb ID", lig_col="Ligand ID"):
    """
    inter_df: pd.DataFrame, interactions between GPCRs and ligands
    sim_df: pd.DataFrame, similarity matrix
    save_path: pathlib.Path, path to save the figure
    """
    # get edges (receptor and ligand pairs) from inter_df
    receptors = list(inter_df[rec_col].unique())
    ligands = list(inter_df[lig_col].unique())
    edge_list = inter_df[[rec_col, lig_col]].values.tolist()

    # count the number of edges per receptor
    edges_to_receptor = {lig:rec for rec, lig in edge_list}
    edges_to_receptor = Counter(edges_to_receptor.values())

    # count the number of edges per ligand
    edges_to_ligand = {rec:lig for rec, lig in edge_list}
    edges_to_ligand = Counter(edges_to_ligand.values())

    # count the number of ligands that target 2+ receptors
    ligands_with_multiple_receptors = [lig for lig, count in edges_to_ligand.items() if count > 1]
    print(f"Found {len(ligands_with_multiple_receptors)} ligands that target 2+ receptors")

    # get the similarity values for the ligands that target 2+ receptors
    positive_similarities = []
    negative_similarities = []
    for lig in ligands_with_multiple_receptors:
        receptors_targeted = [rec for rec, ligand in edge_list if ligand == lig]
        receptors_not_targeted = [rec for rec in receptors if rec not in receptors_targeted]
        print(f"{lig}\t{len(receptors_targeted)} receptors targeted: {receptors_targeted}")

        # get similarities for negative binding: shape = (receptors targeted, receptors not targeted)
        sim_df_neg = sim_df.loc[receptors_targeted, receptors_not_targeted]

        # get similarities for positive binding: shape = (receptors targeted, receptors targeted)
        sim_df_pos = sim_df.loc[receptors_targeted, receptors_targeted]
        # only keep the upper triangle (diagonal included)
        sim_df_pos = sim_df_pos.where(np.triu(np.ones(sim_df_pos.shape)).astype(np.bool_))
        # remove diagonal (self similarity)
        for rec in receptors_targeted:
            sim_df_pos[rec][rec] = None

        # extend the list of similarities (filtering out NaN)
        positive_similarities.extend([sim for sim in sim_df_pos.values.flatten() if not np.isnan(sim)])
        negative_similarities.extend([sim for sim in sim_df_neg.values.flatten() if not np.isnan(sim)])
    
    # plot the distribution of similarities
    sns.set_theme(style="white")
    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)

    sns.histplot(positive_similarities, alpha=0.6, bins=20, binrange=(0, 100),
                 label="Positive binding", stat="probability", color="blue")
    sns.histplot(negative_similarities, alpha=0.6, bins=20, binrange=(0, 100),
                 label="Negative binding", stat="probability", color="red")
    plt.tight_layout()
    ax.set_xlim(0, 100)
    ax.set_xticks(np.arange(0, 100, 5))
    # make space for title
    plt.subplots_adjust(top=0.9)
    # set ticks for each bin
    ax.set_xlabel("Similarity (%)")
    ax.set_ylabel("Probability")
    ax.set_title("GPCR similarity between receptors targeted by the same ligand (positive binding)\nand receptors not targeted by that same ligand (negative binding)")
    
    # add value percentages to the top of the bars
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f'{height*100:.2f}%', (p.get_x()+p.get_width()/2., height), ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=6)

    # add counts for neg and pos
    ax.text(0.05, 0.90, f"Positive binding: n={len(positive_similarities)}\nNegative binding: n={len(negative_similarities)}",
            horizontalalignment='left', verticalalignment='top', 
            transform=ax.transAxes, fontsize=10)
    plt.legend()
    plt.savefig(save_path)


def temp_receptors_with_less_than_25(sim_out, save_path):
    # plot how many receptors have <= 25% similarity
    sim_df = pd.read_csv(sim_out)
    sim_df = sim_df.set_index(sim_df.columns[0])
    # set self similarity to None
    for gpcr in list(sim_df.index):
        sim_df[gpcr][gpcr] = None
    # get number of receptors with <= 25% similarity
    receptor_to_low_similarity = dict()
    for gpcr in list(sim_df.index):
        receptor_to_low_similarity[gpcr] = len(sim_df[gpcr][sim_df[gpcr] <= 30])
    # plot
    sns.set_theme(style="white")
    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)

    x = list(receptor_to_low_similarity.keys())
    y = list(receptor_to_low_similarity.values())

    sort_y = sorted(y)
    sort_x = [x for _,x in sorted(zip(y,x))]

    sns.barplot(x=sort_x, y=sort_y, ax=ax)
    # rotate labels 90 degrees
    plt.xticks(rotation=90)
    # lower font size
    plt.xticks(fontsize=6)
    # add y ticks every 5 receptors
    plt.yticks(np.arange(0, max(y)+5+1, 5))
    # add lines for y ticks
    for y_tick in np.arange(0, max(y)+5+1, 5):
        plt.axhline(y=y_tick, color='black', linestyle='-', alpha=0.1)
    
    plt.tight_layout()
    plt.savefig(save_path)


def create_similarity_matrix_and_plots(interactions_df_path, 
                                       similarity_matrix_path,
                                       mode,
                                       get_similarity_function):
    if similarity_matrix_path.exists():
        print(f"Similarity matrix already exists at {similarity_matrix_path}, skipping")
    else:
        create_similarity_matrix(interactions_df_path=interactions_df_path,
                                 output_path=similarity_matrix_path,
                                 get_similarity_function=get_similarity_function,
                                 mode=mode)
    
    sim_matrix_df = pd.read_csv(similarity_matrix_path)
    report_similarity_matrix(sim_matrix_df)

    save_similarity_matrix_seaborn(sim_matrix_df,
                                   similarity_matrix_path.parent / f"{similarity_matrix_path.stem}_{mode}_heatmap.png",
                                   title=f"GPCR binding pocket {mode} matrix")
    
    plot_similarity_distribution(pd.read_csv(interactions_df_path),
                                 pd.read_csv(similarity_matrix_path, index_col=0),
                                 similarity_matrix_path.parent / f"{similarity_matrix_path.name.split('.')[0]}_{mode}_distribution.png")


if __name__ == "__main__":
    # args
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--metric", type=str, choices=["similarity", "identity"], required=True,
                        help="similarity or identity")
    PARSER.add_argument("--mode", type=str, choices=["TM", "binding_pocket"], required=True,
                        help="TM or binding_pocket")
    PARSER.add_argument("--interactions_path", type=pathlib.Path, required=True,
                        help="Path to the interactions df")
    PARSER.add_argument("--out_matrix_path", type=pathlib.Path, required=True,
                        help="Path to the similarity matrix (.csv)")
    ARGS = PARSER.parse_args()

    # create
    if ARGS.mode == "TM":
        FUNC = get_GPCR_similarity_values_TM
    elif ARGS.mode == "binding_pocket":
        FUNC = get_GPCR_similarity_values_binding_pocket
    else:
        raise ValueError(f"Unknown mode: {ARGS.mode}")
    
    create_similarity_matrix_and_plots(interactions_df_path=ARGS.interactions_path,
                                        similarity_matrix_path=ARGS.out_matrix_path,
                                        mode=ARGS.metric,
                                        get_similarity_function=FUNC)
