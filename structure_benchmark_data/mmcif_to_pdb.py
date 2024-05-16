import os
from pymol import cmd
import argparse

def list_files_in_directory_and_subdirectories(directory):
    files_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            files_list.append(os.path.join(root, file))
    return files_list

# Function to convert mmCIF to PDB
def convert_mmcif_to_pdb(input_file, output_file):
    cmd.load(input_file)
    cmd.save(output_file)
    cmd.delete('all')  # Clear the session to avoid conflicts with next file

# Main function to process all mmCIF files in a directory
def batch_convert(input_dir):
    # List all files recursively in the input directory
    mmcif_files = list_files_in_directory_and_subdirectories(input_dir)
    mmcif_files = [f for f in mmcif_files if f.endswith('.cif')]

    for filename in mmcif_files:
        input_file = os.path.join(input_dir, filename)
        output_file = os.path.join(input_dir, os.path.splitext(filename)[0] + '.pdb')
        convert_mmcif_to_pdb(input_file, output_file)
        print(f"Converted {filename} to PDB format")

# Read input folder as a command line argument
parser = argparse.ArgumentParser()
parser.add_argument('input_dir', help='Input directory containing mmCIF files')
args = parser.parse_args()
input_dir = args.input_dir

# To run this script, add this to your .zshrc (on mac)
# alias pymol=/Applications/PyMOL.app/Contents/MacOS/PyMOL
# pymol -cg mmcif_to_pdb.py 

if __name__ == '__main__':
    # Launch PyMOL in headless mode and run the batch conversion
    cmd.reinitialize()
    batch_convert(input_dir)
    cmd.quit()

