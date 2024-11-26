import requests
import json

# Script to find PDB codes for structures used to train RoseTTAFold and AlphaFold 2 + 3.
# Assumes that the file "pdb_seqres.txt" is in the same directory as this script. 
# This file contains the sequence records for all PDB structures. The script will filter
# uses model specific date and resolution to filter the PDB codes according to the models' training
# criteria. The filtered sequences are written to "rfaa_training_seqres.txt" and "alphafold_training_seqres.txt".
# These two files were used to search for the closest training structures using MMseqs2.

def get_pdb_codes(date, resolution):
    query =  {
        "query": {
            "type": "group",
            "logical_operator": "and",
            "nodes": [
            {
                "type": "terminal",
                "service": "text",
                "parameters": {
                "attribute": "rcsb_entry_info.resolution_combined",
                "operator": "less_or_equal",
                "negation": False,
                "value": resolution
                }
            },
            {
                "type": "terminal",
                "service": "text",
                "parameters": {
                "attribute": "rcsb_accession_info.initial_release_date",
                "operator": "less_or_equal",
                "negation": False,
                "value": date,
                }
            }
            ],
            "label": "text"
        },
        "return_type": "entry",
        "request_options": {
            "results_content_type": [
            "experimental"
            ],
            "return_all_hits": True
        }
    }

    query = json.dumps(query)
    url = f"https://search.rcsb.org/rcsbsearch/v2/query?json={query}"
    response = requests.get(url)
    response.raise_for_status()
    results =  response.json()
    entries = results.get("result_set", [])
    if not entries:
        return []
    pdb_codes = [entry["identifier"] for entry in entries]
    pdb_codes = [pdb_code.upper() for pdb_code in pdb_codes]
    pdb_codes = [pdb_code.strip() for pdb_code in pdb_codes]
    return pdb_codes

def filter_pdb_seqres(seqres_path, pdb_codes, output_path):
    with open(seqres_path, "r") as f:
        lines = f.readlines()
    with open(output_path, "w") as f:
        c = 0
        end_n = len(lines)
        for line in lines:
            c += 1
            if line.startswith(">") and "mol:protein" in line:
                pdb_code = line.split("_")[0][1:].upper().strip()
                if pdb_code in pdb_codes:
                    f.write(line)
                    write = True
                else:
                    write = False
            elif write:
                f.write(line)
            
            if c % 1000 == 0:
                print(f"{c}/{end_n} processed.")

# RoseTTAFold
date = "2020-04-30"
pdb_codes = get_pdb_codes(date, 4.5)
filter_pdb_seqres("pdb_seqres.txt", pdb_codes, "rfaa_training_seqres.txt")

# AlphaFold 2 + 3
date = "2021-09-30"
pdb_codes = get_pdb_codes(date, 9.0)
filter_pdb_seqres("pdb_seqres.txt", pdb_codes, "alphafold_training_seqres.txt")