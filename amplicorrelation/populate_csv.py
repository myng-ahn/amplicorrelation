import pandas as pd
import numpy as np
import requests
import json
import os

BASE_URL = "https://www.genenetwork.nl/api/v1/gene/"
# Specify the root directory from which to start the iteration
# root_dir = "/Users/myahn725/Code/CSE_182/project/amplicorrelation/out"
root_dir = "/Users/jfaybishenko/Documents/School/CSE/CSE_182/project/amplicorrelation/out"
output_file = "out_matrix.csv"
df = pd.DataFrame(columns=["sample"])

row_id = []
columns = {}
samples = 0
# Iterate over every subdirectory in the root directory
for dirpath, dirnames, filenames in os.walk(root_dir):
    # dirpath: the path to the current subdirectory
    # dirnames: a list of the subdirectories in dirpath
    # filenames: a list of the filenames in dirpath

    for amplicons in dirnames:
        old_path = os.path.join(dirpath, amplicons)
        df.to_csv(output_file, index=True)
        for subdirpath, subdirnames, _ in os.walk(old_path):
            for cycles in subdirnames:
                path = os.path.join(old_path, cycles)
                
                for subsubdirpath, subsubdirnames, subfilenames in os.walk(path):
                    for file in subfilenames:
                        # row_id.append(amplicons + '_' + cycles)
                        
                        if "genes" in file:
                            # print(file)
                            full_path = os.path.join(path, file)

                            
                            with open(full_path, "r") as f:
                                # Read all lines of the file into a list
                                lines = f.readlines()
                            genes = [line.strip() for line in lines]
                            cycle_genes = []
                            for gene_id in genes:
                                try:
                                    res = requests.get(f"{BASE_URL}{gene_id}")
                                    data = res.json()
                                except:
                                    print("Gene Broke:")
                                    print(gene_id, cycles, amplicons)
                                    continue
                                if res.status_code != 200:
                                    continue
                                gene_id_dict = data["gene"]
                                
                                if (
                                    gene_id_dict["biotype"] != "protein_coding"
                                ):
                                    #print(amplicons, cycles, gene_id)
                                    if gene_id not in df.columns:
                                        df[gene_id] = pd.Series(dtype=int)
                                        cycle_genes.append(gene_id)
                            identity = str(amplicons) + "_" + str(cycles)
                            new_row = {"sample": identity}
                            
                            for column in df.columns:
                                if column in cycle_genes:
                                    new_row[column] = 1
                                else:
                                    new_row[column] = 0

                            #df = df.append(new_row, ignore_index=True)
                            df.loc[identity] = new_row


# Write the DataFrame to a CSV file
df.to_csv(output_file, index=True)


"""
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
"""
