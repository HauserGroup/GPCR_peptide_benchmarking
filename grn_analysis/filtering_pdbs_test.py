"""
Script to filter out PDB templates that are too similar to the input sequence.
Queries RCSB PDB API using the input sequence and filters out sequences with identity and e-value higher than a given threshold.

Example:
python3 ./filtering_pdbs_test.py pdb_hits.sto vipr2_human.fasta filtered_pdb_hits.sto --identity_threshold 0.9 --e_value 0.1

Author: Teemu Rönkkö
Date: 2023-11-29
"""

import argparse
import requests
import os
import Bio.AlignIO as AlignIO

# The posterior probability is encoded as 11 possible characters 0-9*+: 
# 0.0  ≤ p < 0.05 is coded as 0
# 0.05 ≤ p < 0.15 is coded as 1 (... and so on...), 0.85 ≤ p < 0.95 is coded as 9
# 0.95 ≤ p ≤ 1.0  is coded as ’*’
# Gap characters appear in the PP line where no residue has been assigned.


def read_fasta_sequence(file_path):
    """
    Helper function to read a single FASTA file and return the sequence as a string.
    file_path   : path to the FASTA file
    """
    try:
        with open(file_path, 'r') as f:
            # Skip the header line starting with '>'
            next(f)
            # Read the sequence and remove any whitespace characters
            sequence = ''.join(line.strip() for line in f)
        return sequence
    
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None

def get_pdb_entries_by_seq(seq, identity = 0.9, e_value = 0.1):
    '''
    Function to get a list of PDB entries for a given sequence with at most a given identity and e-value
    seq         : sequence to search for
    identity    : maximum identity between the input sequence and the sequences in PDB (0.0-1.0)
    e_value     : maximum e-value between the input sequence and the sequences in PDB (0.0-1.0)

    returns     : list of PDB entries (empty list if no entries found)
    '''

    # Define the RCSB PDB API endpoint for UniProt search
    api_url = "https://search.rcsb.org/rcsbsearch/v2/query"
    
    # Define the query parameters – in this case, we want to search for entries that contain a given UniProt ID
    query = {
        "query": {
            "type": "terminal",
            "service": "sequence",
            "parameters": {
            "evalue_cutoff": e_value,
            "identity_cutoff": identity,
            "sequence_type": "protein",
            "value": seq,
            }
        },
        "return_type": "polymer_entity",
        "request_options": {
            "results_content_type": [
            "experimental"
            ]
        }
    }

    # Make the API request
    response = requests.post(api_url, json=query)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:

        # Parse the JSON response
        result = response.json()
        
        # Extract PDB entries from the result, save PDB identifier only, and 
        # remove duplicates
        pdb_entries = [hit['identifier'] for hit in result['result_set']]
        pdb_entries = [x.lower() for x in pdb_entries]
        pdb_entries = [x.split('_')[0] for x in pdb_entries]
        pdb_entries = list(set(pdb_entries))
        return pdb_entries
    else:
        # Print an error message if the request was not successful
        print(f"Querying PDB using sequence {seq} failed.")
        print(f"Error code: {response.status_code}")
        return []


def read_PDB_hits_sto_BioPython(input_path):
    """ Read a pdb_hits.sto (Stockholm) file with Bio.AlignIO.
    input_path: pathlib.Path
                path to the pdb_hits.sto file (made through HMMbuild and HMMsearch)
    """
    with open(input_path, "r") as input_file:
        alignment = AlignIO.read(input_file, "stockholm")
    return alignment


def filter_PDB_hits_sto_BioPython(alignment, input_sequence, identity_threshold, e_value):
 
    # create empty MultipleSeqAlignment
    filtered_alignment = AlignIO.MultipleSeqAlignment([])

    # lower IDs_to_keep
    IDs_to_remove = get_pdb_entries_by_seq(input_sequence, identity_threshold, e_value)

    # Add the sequences with the specified IDs to the MultipleSeqAlignment
    for record in alignment:
        trimmed_id = record.id.split("_")[0].lower()
        print(record.letter_annotations["posterior_probability"], "\n")
        if trimmed_id not in IDs_to_remove:
            filtered_alignment.append(record)

    return filtered_alignment


def write_PDB_hits_sto_BioPython(alignment, output_path):
    """ Write a pdb_hits.sto (Stockholm) file with Bio.AlignIO.
    alignment: Bio.AlignIO.MultipleSeqAlignment
    output_path: pathlib.Path
                path to the output file, a new pdb_hits.sto file but with only the specified IDs
    """
    with open(output_path, "w") as output_file:
        AlignIO.write(alignment, output_file, "stockholm")


def create_empty_stockholm_file(output_path):
    """ Create an empty stockholm file with pyhmmer.
    output_path: pathlib.Path
    """
    with open(output_path, "w") as output_file:
        output_file.write("# STOCKHOLM 1.0\n")
        output_file.write("#=GF SQ 0")
        output_file.write("//\n")


def filter_stockholm_file(input_path, fasta_file, output_path, identity_threshold, e_value):

    # Read the input FASTA sequence
    input_sequence = read_fasta_sequence(fasta_file)

    # Read alignment
    alignment = read_PDB_hits_sto_BioPython(input_path)

    # Filter alignment using identity and e-value thresholds (compared to input sequence)
    filtered_alignment = filter_PDB_hits_sto_BioPython(alignment, input_sequence, identity_threshold, e_value)
    print(f"filter_templates.py: Filtered {len(alignment)} sequences to {len(filtered_alignment)} sequences")
    
    # Create a new MSA with the filtered sequences
    number_of_sequences = len(filtered_alignment)
    if number_of_sequences > 0:
        write_PDB_hits_sto_BioPython(filtered_alignment, output_path)
    else:
        # create empty file
        create_empty_stockholm_file(output_path)
    

# Read arguments from the command line
parser = argparse.ArgumentParser(description='Filter out PDB templates that are too similar to the input sequence.')
parser.add_argument('stockholm_file', help='Path to the Stockholm file')
parser.add_argument('fasta_file', help='Path to the FASTA file containing the input sequence')
parser.add_argument('output_path', help='Path to the output Stockholm file')
parser.add_argument('--identity_threshold', help='Maximum identity between the input sequence and the sequences in the Stockholm file (0.0-1.0)', type=float, default=0.9)
parser.add_argument('--e_value', help='Maximum e-value between the input sequence and the sequences in the Stockholm file (0.0-1.0)', type=float, default=0.1)
args = parser.parse_args()

if __name__ == "__main__":

    # Make sure all arguments are given and correct
    if not args.stockholm_file.endswith('.sto'):
        raise ValueError("The input file must be a Stockholm file (.sto)")
    
    if not args.fasta_file.endswith('.fasta'):
        raise ValueError("The input file must be a FASTA file (.fasta)")
    
    if not args.output_path.endswith('.sto'):
        raise ValueError("The output file must be a Stockholm file (.sto)")
    
    if args.identity_threshold < 0 or args.identity_threshold > 1:
        raise ValueError("The identity threshold must be between 0 and 1.")
    
    if args.e_value < 0 or args.e_value > 1:
        raise ValueError("The e-value must be between 0 and 1.")

    # Filter out sequences from the Stockholm file
    filter_stockholm_file(args.stockholm_file, args.fasta_file, args.output_path, args.identity_threshold, args.e_value)