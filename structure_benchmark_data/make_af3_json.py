import pandas as pd
import json
import os 

def make_template_dict(name, sequences_dict_list):
    template_dict = {
        "name": name,
        "modelSeeds": [],
        "sequences": sequences_dict_list
    }
    return template_dict

def make_protein_chain_dict(sequence, count):
    sequences_dict = {
        "proteinChain": {
            "sequence": sequence,
            "count": count
        }
    }
    return sequences_dict

def make_af3_json(csv_file, json_dir):
    # Read in the data
    df = pd.read_csv(csv_file)
    os.makedirs(json_dir, exist_ok=True)

    # Loop over dataframe
    json_list = []
    batch_no = 1
    batch_size = 20
    for i, row in df.iterrows():

        # Get name, receptor and ligand sequences
        name = row['pdb']
        receptor_sequence = row['receptor_pdb_seq']
        ligand_sequence = row['ligand_pdb_seq']
        count = 1

        # Make template dictionary and add it to the json_list
        receptor_dict = make_protein_chain_dict(receptor_sequence, count)
        ligand_dict = make_protein_chain_dict(ligand_sequence, count)
        template_dict = make_template_dict(name, [receptor_dict, ligand_dict])
        json_list.append(template_dict)

        # Save json file if batch size is reached or at the end of the dataframe
        if len(json_list) == batch_size or i == len(df) - 1:
            with open(f'{json_dir}/batch_{batch_no}.json', 'w') as f:
                json.dump(json_list, f, indent=4)
            json_list = []
            batch_no += 1
    
    print(f"Created {batch_no - 1} json files in {json_dir}")
    return

if __name__ == '__main__':
    make_af3_json("3f_known_structures_benchmark_2021-09-30.csv", "fastas/af3_jsons")