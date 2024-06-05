"""For each GPCR,
1. Get the binding pocket residues (based on the GPCR class)
2. Get the extracellular residues (based on individual GPCRs)
3. See if any of the PTMs are considered 'in pocket' or 'extracellular'


"""

import requests
import json


def get_residues_extened(entry_name: str):
    "/services/residues/extended/{entry_name}/"
    url = f"https://gpcrdb.org/services/residues/extended/{entry_name}/"

    response = requests.get(url)
    data = response.json()
    return data


def run_main():
    gpcr = "oprm_human"
    data = get_residues_extened(gpcr)
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    run_main()
