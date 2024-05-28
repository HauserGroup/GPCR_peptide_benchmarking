import requests
import json

def get_pdb_codes_since(date):
    query = {
        "query": {
            "type": "terminal",
            "label": "text",
            "service": "text",
            "parameters": {
                "attribute": "rcsb_accession_info.initial_release_date",
                "operator": "greater",
                "value": date,
                "negation": False
            }
        },
        "request_options": {
            "return_all_hits": True
        },
        "return_type": "entry"
    }
    query = json.dumps(query)
    url = f"https://search.rcsb.org/rcsbsearch/v2/query?json={query}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def list_pdb_codes(results):
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
        for line in lines:
            if line.startswith(">"):
                pdb_code = line.split("_")[0][1:].upper().strip()
                if pdb_code not in pdb_codes:
                    f.write(line)
                    print(f"{pdb_code} not in pdb_codes, writing...")
                    write = True
                else:
                    write = False
            elif write:
                f.write(line)

# Example usage
date = "2021-09-30"  # Specify the date here
results = get_pdb_codes_since(date)
pdb_codes = list_pdb_codes(results)


filter_pdb_seqres("pdb_seqres.txt", pdb_codes, "seqres_filtered.txt")


