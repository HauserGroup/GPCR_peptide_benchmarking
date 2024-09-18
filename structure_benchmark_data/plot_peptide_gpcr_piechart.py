import requests
import json
import pandas as pd


# Get all GPCRs that have at least one known endogenous peptide ligand
url = "https://gpcrdb.org/services/ligands/endogenousligands/"
response = requests.get(url)
data = response.json()
data = pd.DataFrame(data)
data = data[data["ligand_type"] == "peptide"]
data = data[data["receptor"].str.contains("_human")]
data = data.drop_duplicates(subset=["receptor", "ligand_type"], keep="first")
data = data.drop(columns=["ligand_type", "endogenous_status", "ligand_name", "potency_ranking"])
data = data.rename(columns={"receptor": "entry_name"})

# Get receptor list - used to merge above data with receptor family and class information
receptor_list_url = "https://gpcrdb.org/services/receptorlist/"
response = requests.get(receptor_list_url)
receptor_list = response.json()
receptor_list = pd.DataFrame(receptor_list)
receptor_list = receptor_list[receptor_list["species"] == "Homo sapiens"]
receptor_list = receptor_list[["entry_name", "receptor_family", "receptor_class", "ligand_type"]]

# Drop protein receptors
receptor_list = receptor_list[receptor_list["ligand_type"] != "Protein receptors"]
receptor_list = receptor_list.drop_duplicates()

# Merge data with receptor_list
data = pd.merge(data, receptor_list, on="entry_name", how="inner")
print(data["receptor_class"].value_counts())
