import pandas as pd
import numpy as np
import requests
import json
import os

BASE_URL = "https://www.genenetwork.nl/api/v1/gene/"
# Specify the root directory from which to start the iteration
root_dir = "/Users/jfaybishenko/Documents/School/CSE/CSE_182/project/amplicorrelation/out"
df = pd.DataFrame()
row_id = []
columns = {}
samples = 0
# Iterate over every subdirectory in the root directory
for dirpath, amplicons, filenames in os.walk(root_dir):
    # dirpath: the path to the current subdirectory
    # dirnames: a list of the subdirectories in dirpath
    # filenames: a list of the filenames in dirpath

    for cycles in amplicons:
        path = os.path.join(dirpath, cycles)
        for subdirpath, subdirnames, subfilenames in os.walk(path):
            for file in subfilenames:
                #row_id.append(amplicons + '_' + cycles)
                if 'genes' in file:
                    print(file)
                    full_path = os.path.join(path, file)
                    
                    
                    with open(full_path, "r") as f:
                        # Read all lines of the file into a list
                        lines = f.readlines()
                    genes = [line.strip() for line in lines]

                    for gene_id in genes: 
                        res = requests.get(f"{BASE_URL}{gene_id}")
                        data = res.json()
                        gene_id_dict = data["gene"]
                        cycle_genes = []
                        if gene_id_dict['biotype'] == 'ncRNA' or gene_id_dict['biotype'] == 'lncRNA':
                            if gene_id not in df.columns:
                                df[gene_id] = pd.Series(dtype=int)
                                cycle_genes.append(gene_id)
                        
                    new_row = {}
                    for column in df.columns:
                        if column in cycle_genes:
                            new_row[column] = 1
                        else:
                            new_row[column] = 0  

                    #df = df.append(new_row, ignore_index=True)
                    df.loc[amplicons + '_' + cycles] = new_row


output_file = "out_matrix.csv"

# Write the DataFrame to a CSV file
df.to_csv(output_file, index=True)


'''
# Iterate over every subdirectory in the root directory
for dirpath, dirnames, filenames in os.walk(root_dir):
    # dirpath: the path to the current subdirectory
    # dirnames: a list of the subdirectories in dirpath
    # filenames: a list of the filenames in dirpath

    # Process the current subdirectory as needed
    print("Subdirectory:", dirpath)

    # Iterate over the filenames in the current subdirectory
    for path in dirnames:
        for subdirpath, subdirnames, subfilenames in os.walk(dirnames):
        # Process each filename in the subdirectory as needed
            for file in subdirnames:
                print(file)
###################################################
BASE_URL = "https://www.genenetwork.nl/api/v1/gene/"

gene = "TMCC1"
res = requests.get(f"{BASE_URL}{gene}")
data = res.json()
# print(res.status_code)
# print(res.content)
# print(data["comment"])
#print(data.keys())
print(data["gene"])
'''