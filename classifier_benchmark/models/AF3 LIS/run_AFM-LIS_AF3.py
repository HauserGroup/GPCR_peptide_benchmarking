import os
import re
import json
import warnings
import numpy as np
import pandas as pd
from Bio.PDB import MMCIFParser, MMCIFIO
from collections import Counter
from scipy.spatial.distance import pdist, squareform
import pathlib

warnings.filterwarnings('ignore')
np.seterr(divide='ignore', invalid='ignore')

def transform_pae_matrix(pae_matrix, pae_cutoff):
    # Initialize the transformed matrix with zeros
    transformed_pae = np.zeros_like(pae_matrix)
    print("a)transformed_pae", transformed_pae.shape)

    # Apply transformation: pae = 0 -> score = 1, pae = cutoff -> score = 0, above cutoff -> score = 0
    # Linearly scale values between 0 and cutoff to fall between 1 and 0
    within_cutoff = pae_matrix < pae_cutoff
    transformed_pae[within_cutoff] = 1 - (pae_matrix[within_cutoff] / pae_cutoff)
    
    return transformed_pae

def calculate_mean_lis(transformed_pae, subunit_number):
    # Calculate the cumulative sum of protein lengths to get the end indices of the submatrices
    cum_lengths = np.cumsum(subunit_number)
    
    # Add a zero at the beginning of the cumulative lengths to get the start indices
    start_indices = np.concatenate(([0], cum_lengths[:-1]))
    
    # Initialize an empty matrix to store the mean LIS
    mean_lis_matrix = np.zeros((len(subunit_number), len(subunit_number)))
    
    # Iterate over the start and end indices
    for i in range(len(subunit_number)):
        for j in range(len(subunit_number)):
            # Get the start and end indices of the interaction submatrix
            start_i, end_i = start_indices[i], cum_lengths[i]
            start_j, end_j = start_indices[j], cum_lengths[j]
            
            # Get the interaction submatrix
            submatrix = transformed_pae[start_i:end_i, start_j:end_j]
            
            # Calculate the mean LIS, considering only non-zero values
            mean_lis = submatrix[submatrix > 0].mean()
            
            # Store the mean LIS in the matrix
            mean_lis_matrix[i, j] = mean_lis
    
    return mean_lis_matrix

def calculate_contact_map(cif_file, distance_threshold=8):
    def read_cif_lines(cif_path):
        with open(cif_path, 'r') as file:
            lines = file.readlines()

        residue_lines = []
        for line in lines:
            if line.startswith('ATOM') and ('CB' in line or 'GLY' in line and 'CA' in line):
                residue_lines.append(line.strip())  # Store the line if it meets the criteria for ATOM

            if line.startswith('ATOM') and 'P   ' in line:
                residue_lines.append(line.strip()) # Store the line if it meets the criteria for ATOM

            elif line.startswith('HETATM'):
                residue_lines.append(line.strip())  # Store all HETATM lines

        return residue_lines

    def lines_to_dataframe(residue_lines):
        # Split lines and create a list of dictionaries for each atom
        data = []
        for line in residue_lines:
            parts = line.split()
            # Correctly convert numerical values
            for i in range(len(parts)):
                try:
                    parts[i] = float(parts[i])
                except ValueError:
                    pass
            data.append(parts)

        df = pd.DataFrame(data)

        # Add line number column
        df.insert(0, 'residue', range(1, 1 + len(df)))

        return df

    # Read lines from CIF file
    residue_lines = read_cif_lines(cif_file)

    # Convert lines to DataFrame
    df = lines_to_dataframe(residue_lines)

    # Assuming the columns for x, y, z coordinates are at indices 11, 12, 13 after insertion
    coordinates = df.iloc[:, 11:14].to_numpy()

    distances = squareform(pdist(coordinates))

    # Assuming the column for atom names is at index 3 after insertion
    has_phosphorus = df.iloc[:, 3].apply(lambda x: 'P' in str(x)).to_numpy()

    # Adjust the threshold for phosphorus-containing residues
    adjusted_distances = np.where(has_phosphorus[:, np.newaxis] | has_phosphorus[np.newaxis, :], 
                                  distances - 4, distances)

    contact_map = np.where(adjusted_distances < distance_threshold, 1, 0)
    return contact_map


def afm3_plot(af3_json, pae_cutoff=12, distance_cutoff=8.0):
    model_number = re.search(r'full_data_(\d+)', af3_json).group(1)
    json_data = json.load(open(af3_json,'rb'))
    token_chain_ids = json_data['token_chain_ids']
    chain_residue_counts = Counter(token_chain_ids)
    subunit_number = list(chain_residue_counts.values())    
    pae_matrix = np.array(json_data['pae'])
    pae_matrix = np.nan_to_num(pae_matrix)
    subunit_sizes = subunit_number
    boundaries = np.cumsum(subunit_sizes)[:-1]

    # Extract the base name of the JSON file (without extension)
    json_basename = os.path.splitext(os.path.basename(af3_json))[0]
    pdb_basename = json_basename.replace('_full_data_', '_model_')

    # Construct CIF file path based on JSON file path
    base_path = os.path.dirname(af3_json)
    cif_file = os.path.join(base_path, f'{pdb_basename}.cif')

    # Create a figure with 1 row and 5 columns
    fig, axs = plt.subplots(1, 6, figsize=(30, 6))

    # Plotting the PAE matrix
    cax1 = axs[0].matshow(pae_matrix, cmap='bwr')
    for boundary in boundaries:
        axs[0].axvline(x=boundary, color='black', lw=1, linestyle='-')
        axs[0].axhline(y=boundary, color='black', lw=1, linestyle='-')

    fig.colorbar(cax1, ax=axs[0], label='Predicted Aligned Error (PAE)', shrink=0.5)
    axs[0].set_title(f'Model {model_number} Predicted Aligned Error Map')
    axs[0].xaxis.tick_bottom()

    # Transform the PAE matrix
    transformed_pae_matrix = transform_pae_matrix(pae_matrix, pae_cutoff)
    transformed_pae_matrix = np.nan_to_num(transformed_pae_matrix)

    # Plotting the transformed PAE matrix
    cax2 = axs[1].matshow(transformed_pae_matrix, cmap='Blues', vmin=0, vmax=1)
    for boundary in boundaries:
        axs[1].axvline(x=boundary, color='black', lw=1, linestyle='-')
        axs[1].axhline(y=boundary, color='black', lw=1, linestyle='-')

    fig.colorbar(cax2, ax=axs[1], label='Local Interaction Score (LIS)', shrink=0.5)
    axs[1].set_title(f'Model {model_number} Local Interaction Area Map')
    axs[1].xaxis.tick_bottom()

    # Calculate the mean LIS matrix
    mean_lis_matrix = calculate_mean_lis(transformed_pae_matrix, subunit_sizes)
    mean_lis_matrix = np.nan_to_num(mean_lis_matrix)

    # Plot the mean LIS matrix as a heatmap
    cax3 = axs[2].imshow(mean_lis_matrix, cmap='magma_r', interpolation='nearest', vmin=0, vmax=1)
    fig.colorbar(cax3, ax=axs[2], label='Local Interaction Score (LIS)', shrink=0.5)
    axs[2].set_title(f'Model {model_number} Local Interaction Score Heatmap')
    subunit_labels = [i for i in range(1, len(subunit_sizes)+1)]
    axs[2].set_xticks(np.arange(len(subunit_sizes)))
    axs[2].set_yticks(np.arange(len(subunit_sizes)))
    axs[2].set_xticklabels(subunit_labels)
    axs[2].set_yticklabels(subunit_labels)

    for i in range(len(subunit_sizes)):
        for j in range(len(subunit_sizes)):
            value = mean_lis_matrix[i, j]
            text_color = 'w' if value > 0.5 else 'k'  
            axs[2].text(j, i, format(mean_lis_matrix[i, j], '.3f'), ha='center', va='center', color=text_color)
    
    # Calculate contact map
    contact_map = calculate_contact_map(cif_file, distance_cutoff)
    
    # Create a new map that combines the inverse PAE map with the contact map
    combined_map = np.where((transformed_pae_matrix > 0) & (contact_map == 1), transformed_pae_matrix, 0)

    # Plotting the transformed PAE matrix
    cax4 = axs[3].matshow(combined_map, cmap='Reds', vmin=0, vmax=1)
    for boundary in boundaries:
        axs[3].axvline(x=boundary, color='black', lw=1, linestyle='-')
        axs[3].axhline(y=boundary, color='black', lw=1, linestyle='-')

    fig.colorbar(cax4, ax=axs[3], label='Contact Local Interaction Score (cLIS)', shrink=0.5)
    axs[3].xaxis.tick_bottom()
    axs[3].set_title(f'Model {model_number} Contact Local Interaction Area Map')

    # Calculate the mean LIS matrix
    mean_clis_matrix = calculate_mean_lis(combined_map, subunit_sizes)
    mean_clis_matrix = np.nan_to_num(mean_clis_matrix)

    # Plot the mean cLIS matrix as a heatmap
    cax5 = axs[4].imshow(mean_clis_matrix, cmap='magma_r', interpolation='nearest', vmin=0, vmax=1)
    fig.colorbar(cax5, ax=axs[4], label='Contact Local Interaction Score (cLIS)', shrink=0.5)
    axs[4].set_title(f'Model {model_number} Contact Local Interaction Score Heatmap')
    subunit_labels = [i for i in range(1, len(subunit_sizes)+1)]
    axs[4].set_xticks(np.arange(len(subunit_sizes)))
    axs[4].set_yticks(np.arange(len(subunit_sizes)))
    axs[4].set_xticklabels(subunit_labels)
    axs[4].set_yticklabels(subunit_labels)

    for i in range(len(subunit_sizes)):
        for j in range(len(subunit_sizes)):
            value = mean_clis_matrix[i, j]
            text_color = 'w' if value > 0.5 else 'k'  
            axs[4].text(j, i, format(mean_clis_matrix[i, j], '.3f'), ha='center', va='center', color=text_color)
    
    json_confidence = af3_json.replace('full_data', 'summary_confidences')
    with open(json_confidence, 'r') as file:
        confidence_data = json.load(file)

    iptm_matrix = confidence_data['chain_pair_iptm']

    iptm_matrix = np.array(iptm_matrix, dtype=float)  # Converts None to np.nan automatically
    iptm_matrix = np.nan_to_num(iptm_matrix)
    cax6 = axs[5].imshow(iptm_matrix, cmap='Greens', vmin = 0, vmax = 1, interpolation='nearest')
    fig.colorbar(cax6, ax=axs[5], label='ipTM', shrink=0.5)
    axs[5].set_title(f'Model {model_number} ipTM Heatmap')

    # Set the ticks to start from 1 and be integers
    ticks = np.arange(1, iptm_matrix.shape[0] + 1)
    axs[5].set_xticks(ticks - 1)
    axs[5].set_yticks(ticks - 1)
    axs[5].set_xticklabels(ticks)
    axs[5].set_yticklabels(ticks)

    # Display the values of the IPTM matrix on the heatmap
    for i in range(iptm_matrix.shape[0]):
        for j in range(iptm_matrix.shape[1]):
            value = iptm_matrix[i, j]
            if np.isnan(value):
                continue  # Skip NaN values
            text_color = 'w' if value > 0.7 else 'k'

            axs[5].text(j, i, format(value, '.3f'), ha='center', va='center', color=text_color)

    plt.tight_layout()
    plt.show()

def load_and_plot_heatmap(json_file):
    # Step 1: Load JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Step 2: Extract IPTM matrix
    iptm_matrix = data['chain_pair_iptm']
    
    # Step 3: Convert None to np.nan (or any other value you prefer)
    iptm_matrix = np.array(iptm_matrix, dtype=float)  # Converts None to np.nan automatically
    
    # Step 4: Create heatmap
    plt.figure(figsize=(10, 8))
    plt.imshow(iptm_matrix, cmap='viridis', vmin = 0, vmax = 1, interpolation='nearest')
    plt.colorbar(label='ipTM')
    plt.title('Heatmap of IPTM')
    # plt.xlabel('Chain Index')
    # plt.ylabel('Chain Index')
    plt.show()


def generate_json_paths(base_path, number_of_models=5):
    """
    Generates a list of JSON file paths for a given number of models within a specified base path.

    Parameters:
    - base_path (str): The base directory where the model JSON files are stored.
    - number_of_models (int): The number of model JSON files to generate paths for.

    Returns:
    - list: A list of fully qualified paths to the JSON files.
    """
    model_identifier = os.path.basename(base_path)
    json_files = [f"{base_path}/{model_identifier}_full_data_{model}.json" for model in range(number_of_models)]
    return json_files

def afm3_plot_average(af3_jsons, pae_cutoff=12, distance_cutoff=8):
    # Initialize the sum of PAE matrices, transformed PAE matrices, mean LIS matrices, and contact maps
    sum_pae_matrix = None
    sum_transformed_pae_matrix = None
    sum_mean_lis_matrix = None
    sum_contact_lia_map = None
    sum_iptm_matrix = None
    
    for af3_json in af3_jsons:
        json_data = json.load(open(af3_json,'rb'))
        json_confidence = af3_json.replace('full_data', 'summary_confidences')
        confidence_data = json.load(open(json_confidence, 'rb'))
        token_chain_ids = json_data['token_chain_ids']
        chain_residue_counts = Counter(token_chain_ids)
        subunit_number = list(chain_residue_counts.values())    
        pae_matrix = np.array(json_data['pae'])
        subunit_sizes = subunit_number

        cif_file = af3_json.replace('_full_data_', '_model_').replace('.json', '.cif')
        
        # Transform the PAE matrix
        transformed_pae_matrix = transform_pae_matrix(pae_matrix, pae_cutoff)
        transformed_pae_matrix = np.nan_to_num(transformed_pae_matrix)

        # Calculate the mean LIS matrix
        mean_lis_matrix = calculate_mean_lis(transformed_pae_matrix, subunit_sizes)
        mean_lis_matrix = np.nan_to_num(mean_lis_matrix)

        contact_map = calculate_contact_map(cif_file, distance_cutoff)
        combined_map = np.where((transformed_pae_matrix > 0) & (contact_map == 1), transformed_pae_matrix, 0)
        
        iptm_matrix = confidence_data['chain_pair_iptm']
        iptm_matrix = np.array(iptm_matrix, dtype=float)  # Converts None to np.nan automatically
        iptm_matrix = np.nan_to_num(iptm_matrix)

        # Add the matrices to the sum
        if sum_pae_matrix is None:
            sum_pae_matrix = pae_matrix
            sum_transformed_pae_matrix = transformed_pae_matrix
            sum_mean_lis_matrix = mean_lis_matrix
            sum_contact_lia_map = combined_map
            sum_iptm_matrix = iptm_matrix
        else:
            sum_pae_matrix += pae_matrix
            sum_transformed_pae_matrix += transformed_pae_matrix
            sum_mean_lis_matrix += mean_lis_matrix
            sum_contact_lia_map += combined_map
            sum_iptm_matrix += iptm_matrix

    # Calculate the average matrices
    avg_pae_matrix = sum_pae_matrix / len(af3_jsons)
    avg_transformed_pae_matrix = sum_transformed_pae_matrix / len(af3_jsons)
    avg_mean_lis_matrix = sum_mean_lis_matrix / len(af3_jsons)
    sum_contact_lia_map = sum_contact_lia_map / len(af3_jsons)
    avg_iptm_matrix = sum_iptm_matrix / len(af3_jsons)    

    # Replace nan with 0 
    avg_pae_matrix = np.nan_to_num(avg_pae_matrix)
    avg_transformed_pae_matrix = np.nan_to_num(avg_transformed_pae_matrix)
    avg_mean_lis_matrix = np.nan_to_num(avg_mean_lis_matrix)
    avg_iptm_matrix = np.nan_to_num(avg_iptm_matrix)

    # Create a figure with 1 row and 5 columns
    fig, axs = plt.subplots(1, 6, figsize=(30, 5))

    # Calculate the cumulative sum of subunit sizes to get the boundaries
    boundaries = np.cumsum(subunit_sizes)[:-1]

    # Plotting the average PAE matrix
    cax1 = axs[0].matshow(avg_pae_matrix, cmap='bwr')
    fig.colorbar(cax1, ax=axs[0], label='Average Predicted Aligned Error (PAE)', shrink=0.5)
    axs[0].set_title('Average Predicted Aligned Error Map')
    axs[0].xaxis.tick_bottom()

    # Add vertical and horizontal lines at the boundaries
    for boundary in boundaries:
        axs[0].axvline(x=boundary, color='black', lw=1, linestyle='-')
        axs[0].axhline(y=boundary, color='black', lw=1, linestyle='-')

    # Plotting the average transformed PAE matrix
    cax2 = axs[1].matshow(avg_transformed_pae_matrix, cmap='Blues', vmin=0, vmax=1)
    fig.colorbar(cax2, ax=axs[1], label='Average Local Interaction Score (LIS)', shrink=0.5)
    axs[1].set_title('Average Local Interaction Area Map')
    axs[1].xaxis.tick_bottom()

    # Add vertical and horizontal lines at the boundaries
    for boundary in boundaries:
        axs[1].axvline(x=boundary, color='black', lw=1, linestyle='-')
        axs[1].axhline(y=boundary, color='black', lw=1, linestyle='-')

    # Plot the average mean LIS matrix as a heatmap
    cax3 = axs[2].imshow(avg_mean_lis_matrix, cmap='magma_r', interpolation='nearest', vmin=0, vmax=1)
    fig.colorbar(cax3, ax=axs[2], label='Average Local Interaction Score (LIS)', shrink=0.5)
    axs[2].set_title('Average Local Interaction Score Heatmap')
    subunit_labels = [i for i in range(1, len(subunit_sizes)+1)]
    axs[2].set_xticks(np.arange(len(subunit_sizes)))
    axs[2].set_yticks(np.arange(len(subunit_sizes)))
    axs[2].set_xticklabels(subunit_labels)
    axs[2].set_yticklabels(subunit_labels)

    for i in range(len(subunit_sizes)):
        for j in range(len(subunit_sizes)):
            value = avg_mean_lis_matrix[i, j]
            text_color = 'w' if value > 0.5 else 'k'  
            axs[2].text(j, i, format(value, '.3f'), ha='center', va='center', color=text_color)


    # Plotting the average mean contact LIS PAE matrix
    cax4 = axs[3].matshow(sum_contact_lia_map, cmap='Reds', vmin=0, vmax=1)
    for boundary in boundaries:
        axs[3].axvline(x=boundary, color='black', lw=1, linestyle='-')
        axs[3].axhline(y=boundary, color='black', lw=1, linestyle='-')

    fig.colorbar(cax4, ax=axs[3], label='Average Contact Local Interaction Score (cLIS)', shrink=0.5)
    axs[3].xaxis.tick_bottom()
    axs[3].set_title(f'Average Contact Local Interaction Area Map')

    # Calculate the mean LIS matrix
    mean_clis_matrix = calculate_mean_lis(sum_contact_lia_map, subunit_sizes)
    mean_clis_matrix = np.nan_to_num(mean_clis_matrix)

    # Plot the mean cLIS matrix as a heatmap
    cax5 = axs[4].imshow(mean_clis_matrix, cmap='magma_r', interpolation='nearest', vmin=0, vmax=1)
    fig.colorbar(cax5, ax=axs[4], label='Average Contact Local Interaction Score (cLIS)', shrink=0.5)
    axs[4].set_title(f'Average Contact Local Interaction Score Heatmap')
    subunit_labels = [i for i in range(1, len(subunit_sizes)+1)]
    axs[4].set_xticks(np.arange(len(subunit_sizes)))
    axs[4].set_yticks(np.arange(len(subunit_sizes)))
    axs[4].set_xticklabels(subunit_labels)
    axs[4].set_yticklabels(subunit_labels)

    for i in range(len(subunit_sizes)):
        for j in range(len(subunit_sizes)):
            value = mean_clis_matrix[i, j]
            text_color = 'w' if value > 0.5 else 'k'  
            axs[4].text(j, i, format(mean_clis_matrix[i, j], '.3f'), ha='center', va='center', color=text_color)


    cax6 = axs[5].imshow(avg_iptm_matrix, cmap='Greens', vmin = 0, vmax = 1, interpolation='nearest')
    fig.colorbar(cax6, ax=axs[5], label='ipTM', shrink=0.5)
    axs[5].set_title(f'Average ipTM Heatmap')

    # Set the ticks to start from 1 and be integers
    ticks = np.arange(1, avg_iptm_matrix.shape[0] + 1)
    axs[5].set_xticks(ticks - 1)
    axs[5].set_yticks(ticks - 1)
    axs[5].set_xticklabels(ticks)
    axs[5].set_yticklabels(ticks)

    # Display the values of the IPTM matrix on the heatmap
    for i in range(avg_iptm_matrix.shape[0]):
        for j in range(avg_iptm_matrix.shape[1]):
            value = avg_iptm_matrix[i, j]
            if np.isnan(value):
                continue  # Skip NaN values
            text_color = 'w' if value > 0.7 else 'k'
            axs[5].text(j, i, format(value, '.3f'), ha='center', va='center', color=text_color)
   
    plt.tight_layout()
    plt.show()


def get_nan_residues_per_chain_from_cif_file(cif_file_p):
    """
    Parses a CIF file and finds unknown residues ('X') per chain.
    Args:
        cif_file_p (str): Path to the CIF file.
    Returns:
        dict: A dictionary where keys are chain IDs and values tuples with
            (absolute amino acid index, residue number inside chain)
    """
    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure("structure", cif_file_p)
    
    unknown_residues = {}
    
    for model in structure:
        # calculate amino acid index (start at 0)
        amino_acid_index = -1
        for chain in model:
            chain_id = chain.id
            unknown_residues[chain_id] = []
            
            for residue in chain:
                amino_acid_index+=1
                resname = residue.get_resname().strip()
                res_id = residue.id[1]
                # if this residues is unknown/unidentified
                if resname == "X" or resname == "UNK":
                    unknown_residues[chain_id].append((amino_acid_index, res_id))
    
     # Remove empty chains
    return {k: v for k, v in unknown_residues.items() if v} 


def create_cif_file_without_unknown_residues(input_cif_p, output_cif_p):
    """
    Parses a CIF file and creates a new CIF file without unknown residues ('UNK').

    Args:
        input_cif_p (str): Path to the input CIF file.
        output_cif_p (str): Path to the output CIF file without 'UNK' residues.
    """
    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure("structure", input_cif_p)

    for model in structure:
        for chain in model:
            residues_to_remove = [res for res in chain if res.get_resname().strip() == "UNK"]
            if len(residues_to_remove) > 0:
                print("WARNING: REMOVING THESE RESIDUES from .cif file", residues_to_remove)
                for res in residues_to_remove:
                    chain.detach_child(res.id)

    io = MMCIFIO()
    io.set_structure(structure)
    io.save(output_cif_p)


def afm3_plot_average_to_df(af3_jsons, pae_cutoff=12, distance_cutoff=8, result_save = "True"):
    sum_pae_matrix = None
    sum_transformed_pae_matrix = None
    sum_mean_lis_matrix = None
    sum_contact_lia_map = None
    sum_iptm_matrix = None
    all_interactions = []

    for af3_json in af3_jsons:
        json_data = json.load(open(af3_json, 'rb'))
        json_confidence = af3_json.replace('full_data', 'summary_confidences')
        confidence_data = json.load(open(json_confidence, 'rb'))
        cif_file = af3_json.replace('_full_data_', '_model_').replace('.json', '.cif')

        # FIXED: shape mismatch problem: cif_file contains nans, confidence data does not... ====================================
        # approach 1: trim cif_file.
        x_residues = get_nan_residues_per_chain_from_cif_file(cif_file)
        # {'B': [1]}
        if len(x_residues) > 0:
            print("WARNING: CIF FILE HAS UNK RESIDUES WHICH COULD CAUSE ERRORS.")
            print(x_residues)
            # get residue indexes to drop
            residue_indexes_to_drop = set()
            for chain_with_x in x_residues.keys():
                for x_absolute_index, x_residue_number in x_residues[chain_with_x]:
                    residue_indexes_to_drop.add(x_absolute_index)
            print("WARNING: Dropping these residues", residue_indexes_to_drop)

            # for k, v in json_data.items():
            #     print(k, np.array(v).shape)
            # # atom_chain_ids (2620,)
            # # atom_plddts (2620,)
            # # contact_probs (349, 349)
            # # pae (349, 349)
            # # token_chain_ids (349,)
            # # token_res_ids (349,)
            
            # Drop residues from relevant arrays
            json_data['contact_probs'] = np.delete(json_data['contact_probs'], list(residue_indexes_to_drop), axis=0)
            json_data['contact_probs'] = np.delete(json_data['contact_probs'], list(residue_indexes_to_drop), axis=1)
            json_data['pae'] = np.delete(json_data['pae'], list(residue_indexes_to_drop), axis=0)
            json_data['pae'] = np.delete(json_data['pae'], list(residue_indexes_to_drop), axis=1)
            json_data['token_chain_ids'] = np.delete(json_data['token_chain_ids'], list(residue_indexes_to_drop), axis=0)
            json_data['token_res_ids'] = np.delete(json_data['token_res_ids'], list(residue_indexes_to_drop), axis=0)

            # from now on, calculate a cif file with dropped residues
            new_cif_file = pathlib.Path(cif_file)
            new_cif_file = new_cif_file.with_suffix(".removed_unk.cif")
            create_cif_file_without_unknown_residues(str(cif_file), str(new_cif_file))
            cif_file = str(new_cif_file)
        else:
            print("INFO: No UNK residues identified.")
        # end of changes =========================================================================================================

        token_chain_ids = json_data['token_chain_ids']
        chain_residue_counts = Counter(token_chain_ids)
        subunit_number = list(chain_residue_counts.values())
        pae_matrix = np.array(json_data['pae'])
        subunit_sizes = subunit_number

        
        transformed_pae_matrix = transform_pae_matrix(pae_matrix, pae_cutoff)
        print("transformed_pae_matrix", transformed_pae_matrix.shape)
        transformed_pae_matrix = np.nan_to_num(transformed_pae_matrix)
        print("transformed_pae_matrix", transformed_pae_matrix.shape)
        lia_map = np.where(transformed_pae_matrix > 0, 1, 0)
        print("lia_map", lia_map.shape)

        mean_lis_matrix = calculate_mean_lis(transformed_pae_matrix, subunit_sizes)
        print("mean_lis_matrix", mean_lis_matrix.shape)
        mean_lis_matrix = np.nan_to_num(mean_lis_matrix)
        print("mean_lis_matrix", mean_lis_matrix.shape)

        contact_map = calculate_contact_map(cif_file, distance_cutoff)
        print("contact_map", contact_map.shape)
        combined_map = np.where((transformed_pae_matrix > 0) & (contact_map == 1), transformed_pae_matrix, 0)
        print("combined_map", combined_map.shape)

        mean_clis_matrix = calculate_mean_lis(combined_map, subunit_sizes)
        print("mean_clis_matrix", mean_clis_matrix.shape)
        mean_clis_matrix = np.nan_to_num(mean_clis_matrix)
        print("mean_clis_matrix", mean_clis_matrix.shape)

        lia_matrix = np.zeros((len(subunit_sizes), len(subunit_sizes)))
        lir_matrix = np.zeros((len(subunit_sizes), len(subunit_sizes)))
        clia_matrix = np.zeros((len(subunit_sizes), len(subunit_sizes)))
        clir_matrix = np.zeros((len(subunit_sizes), len(subunit_sizes)))

        for i in range(len(subunit_sizes)):
            for j in range(len(subunit_sizes)):
                start_i, end_i = sum(subunit_sizes[:i]), sum(subunit_sizes[:i+1])
                start_j, end_j = sum(subunit_sizes[:j]), sum(subunit_sizes[:j+1])
                interaction_submatrix = lia_map[start_i:end_i, start_j:end_j]

                lia_matrix[i, j] = int(np.count_nonzero(interaction_submatrix))
                residues_i = np.unique(np.where(interaction_submatrix > 0)[0]) + start_i
                residues_j = np.unique(np.where(interaction_submatrix > 0)[1]) + start_j
                lir_matrix[i, j] = int(len(residues_i) + len(residues_j))

                combined_submatrix = combined_map[start_i:end_i, start_j:end_j]
                clia_matrix[i, j] = int(np.count_nonzero(combined_submatrix))

                residues_i = np.unique(np.where(combined_submatrix > 0)[0]) + start_i
                residues_j = np.unique(np.where(combined_submatrix > 0)[1]) + start_j
                clir_matrix[i, j] = int(len(residues_i) + len(residues_j))

        iptm_matrix = confidence_data['chain_pair_iptm']
        iptm_matrix = np.array(iptm_matrix, dtype=float)
        iptm_matrix = np.nan_to_num(iptm_matrix)

        if sum_pae_matrix is None:
            sum_pae_matrix = pae_matrix
            sum_transformed_pae_matrix = transformed_pae_matrix
            sum_mean_lis_matrix = mean_lis_matrix
            sum_contact_lia_map = combined_map
            sum_iptm_matrix = iptm_matrix
        else:
            sum_pae_matrix += pae_matrix
            sum_transformed_pae_matrix += transformed_pae_matrix
            sum_mean_lis_matrix += mean_lis_matrix
            sum_contact_lia_map += combined_map
            sum_iptm_matrix += iptm_matrix

        model_number = re.search(r'full_data_(\d+)', af3_json).group(1)
        folder_name = os.path.basename(os.path.dirname(af3_json))
        for i in range(len(subunit_sizes)):
            for j in range(len(subunit_sizes)):
                interaction = {
                    'folder_name': folder_name,
                    'model_number': model_number,
                    'protein_1': i + 1,
                    'protein_2': j + 1,
                    'LIS': mean_lis_matrix[i, j],
                    'LIA': lia_matrix[i, j],
                    'LIR': lir_matrix[i, j],
                    'cLIS': mean_clis_matrix[i, j],
                    'cLIA': clia_matrix[i, j],
                    'cLIR': clir_matrix[i, j],
                    'iptm': iptm_matrix[i, j],
                }
                all_interactions.append(interaction)

    avg_pae_matrix = sum_pae_matrix / len(af3_jsons)
    avg_transformed_pae_matrix = sum_transformed_pae_matrix / len(af3_jsons)
    avg_mean_lis_matrix = sum_mean_lis_matrix / len(af3_jsons)
    avg_contact_lia_map = sum_contact_lia_map / len(af3_jsons)
    avg_iptm_matrix = sum_iptm_matrix / len(af3_jsons)

    avg_pae_matrix = np.nan_to_num(avg_pae_matrix)
    avg_transformed_pae_matrix = np.nan_to_num(avg_transformed_pae_matrix)
    avg_mean_lis_matrix = np.nan_to_num(avg_mean_lis_matrix)
    avg_iptm_matrix = np.nan_to_num(avg_iptm_matrix)

    df_interactions = pd.DataFrame(all_interactions)
    df_interactions['interaction'] = df_interactions.apply(lambda row: tuple(sorted((row['protein_1'], row['protein_2']))), axis=1)
    df_merged = df_interactions.groupby(['folder_name', 'model_number', 'interaction']).mean().reset_index()
    df_merged[['protein_1', 'protein_2']] = pd.DataFrame(df_merged['interaction'].tolist(), index=df_merged.index)
    df_merged = df_merged.drop(columns=['interaction'])

    # Calculate average values for each protein pair and add as new rows
    avg_rows = []
    interaction_pairs = df_merged.groupby(['protein_1', 'protein_2'])

    for (protein_1, protein_2), group in interaction_pairs:
        avg_row = {
            'folder_name': folder_name,
            'model_number': 'average',
            'protein_1': protein_1,
            'protein_2': protein_2,
            'LIS': group['LIS'].mean(),
            'LIA': group['LIA'].mean(),
            'LIR': group['LIR'].mean(),
            'cLIS': group['cLIS'].mean(),
            'cLIA': group['cLIA'].mean(),
            'cLIR': group['cLIR'].mean(),
            'iptm': group['iptm'].mean(),
        }
        avg_rows.append(avg_row)

    df_avg = pd.DataFrame(avg_rows)
    df_merged = pd.concat([df_merged, df_avg], ignore_index=True)

    df_merged['LIA'] = df_merged['LIA'].astype(int)
    df_merged['LIR'] = df_merged['LIR'].astype(int)
    df_merged['cLIA'] = df_merged['cLIA'].astype(int)
    df_merged['cLIR'] = df_merged['cLIR'].astype(int)

    # Save DataFrame to CSV
    output_folder = os.path.dirname(af3_jsons[0])
    output_path = os.path.join(output_folder, f"{folder_name}_lis_analysis.csv")
    if result_save == "True":
        df_merged.to_csv(output_path, index=False)
        print("Results saved to: ", output_path)
        print(f"{folder_name}_lis_analysis.csv")

    return df_merged


def run_AFM_LIS_for_single_AF3_directory(d):
    """
    Processes a single AF3 directory containing multiple model predictions and calculates LIS metrics.
    """
    if not d.exists() or not d.is_dir():
        raise ValueError(f"Directory {d} does not exist or is not a directory.")
    
    # Identify JSON files containing full model data and summary confidences
    af3_jsons = sorted(d.glob("*_full_data_*.json"))
    af3_jsons = [j for j in af3_jsons if not "cleaned" in str(j)]
    confidence_jsons = sorted(d.glob("*_summary_confidences_*.json"))
    if not af3_jsons or not confidence_jsons:
        raise ValueError(f"No AF3 full data or summary confidence JSON files found in {d}.")

    af3_jsons = [str(j.resolve()) for j in af3_jsons]
    print(af3_jsons)
    df_results = afm3_plot_average_to_df(af3_jsons, pae_cutoff=12, distance_cutoff=8, result_save="True")


if __name__ == "__main__":
    # run_AFM_LIS_for_single_AF3_directory(pathlib.Path("/projects/ilfgrid/data/Luuk/Carlo_raw_data/input/ackr1_human___573"))
    # run_AFM_LIS_for_single_AF3_directory(pathlib.Path("/projects/ilfgrid/data/Luuk/Carlo_raw_data/input/ackr1_human___1579"))

    base_dir = pathlib.Path("/projects/ilfgrid/data/Luuk/Carlo_raw_data/input")
    for d in base_dir.iterdir():
        if d.is_dir():
            run_AFM_LIS_for_single_AF3_directory(d)
    