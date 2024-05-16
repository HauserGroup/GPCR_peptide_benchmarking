# Script to rename the models in the AF3 benchmark data to match the names in the structure benchmark data
import os
import argparse

def list_files_in_directory_and_subdirectories(directory):
    files_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            files_list.append(os.path.join(root, file))
    return files_list


def rename_af3_models(input_dir, output_dir):

    # List all the files in the directory
    files = list_files_in_directory_and_subdirectories(input_dir)
    files = [f for f in files if f.endswith('model_0.pdb')]

    # Rename the models
    for filename in files:
        # Get pdb code from the filename – between fold_ and _full
        fname = filename.split("/")[-1]
        pdb_code = fname.split('_')[1]
        pdb_code = pdb_code.upper()
        output_file = os.path.join(output_dir, pdb_code + '.pdb')
        os.rename(filename, output_file)

argparser = argparse.ArgumentParser()
argparser.add_argument('input_dir', help='Input directory containing AF3 models')
argparser.add_argument('--output_dir', help='Output directory for renamed models', required = False, default = "")
args = argparser.parse_args()

input_dir = args.input_dir
output_dir = args.output_dir
if output_dir == "":
    output_dir = input_dir

if __name__ == '__main__':
    rename_af3_models(input_dir, output_dir)