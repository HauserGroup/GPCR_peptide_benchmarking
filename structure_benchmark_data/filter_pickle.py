import pickle
import json
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='View contents of a pickle file')
parser.add_argument('pickle_file', type=str, help='Path to pickle file')
args = parser.parse_args()

if __name__ == "__main__":

    # Load pickle file
    with open(args.pickle_file, 'rb') as f:
        data = pickle.load(f)

    # Print contents
    for key in data.keys():
        print(key, " : ", data[key])