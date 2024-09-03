# Script to get statistics on the number of peptides that target GPCRs

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import requests

url = "https://gpcrdb.org/services/ligands/endogenousligands/"

# Get the data
response = requests.get(url)
data = response.json()
data = pd.DataFrame(data)

# Filter out small-molecule ligands
data = data[data['ligand_type'] == 'peptide']
data = data[data['receptor'].str.contains("_human")]

# Drop duplicate rows based on receptor and ligand_name
data = data.drop_duplicates(subset=['receptor', 'ligand_name'], keep='first')
data = data.reset_index(drop=True)

# Get the number of unique GPCR-peptide pairs
print("Number of unique GPCR-peptide pairs: ", len(data))

# Print number of unique receptors
print("Number of unique receptors: ", len(data['receptor'].unique()))

# Get the number of unique peptides
print("Number of unique peptides: ", len(data['ligand_name'].unique()))
print("Number of unique peptide sequences: ", len(data['sequence'].unique()))

print(data)

pdb_url = "https://gpcrdb.org/services/structure/"

# Get the data
response = requests.get(pdb_url)
pdb_data = response.json()
pdb_data = pd.DataFrame(pdb_data)

def get_peptide_ligands(input_dict):
    
    peptide_ligands = []
    for ligand in input_dict:
        if ligand['type'] == 'peptide':
            peptide_ligands.append(ligand['name'])

    if len(peptide_ligands) == 0:
        return None    
    
    return " | ".join(peptide_ligands)

# Get only rows where ligands contain "peptide"
pdb_data['peptide_ligands'] = pdb_data['ligands'].apply(get_peptide_ligands)

# Filter out rows where peptide_ligands is None
pdb_data = pdb_data.dropna(subset=['peptide_ligands'])

print(pdb_data)

print("Number of unique GPCR-peptide pairs in PDB: ", len(pdb_data["pdb_code"].unique()))

# Get counts by class
class_counts = pdb_data['class'].value_counts()
print("Class counts: ", class_counts)
# Get percentage by class
class_percentages = pdb_data['class'].value_counts(normalize=True)
print("Class percentages: ", class_percentages)

print(pdb_data["type"].value_counts())
# percentage by type
type_percentages = pdb_data['type'].value_counts(normalize=True)
print("Type percentages: ", type_percentages)