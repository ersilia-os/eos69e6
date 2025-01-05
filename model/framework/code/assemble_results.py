import os
import sys
import csv
import random

root = os.path.dirname(os.path.abspath(__file__))

input_file = sys.argv[1]
n_samplings = int(sys.argv[2])
output_file = sys.argv[3]

TMP_FOLDER = os.path.join(root, "..", "tmp")

MAX_SMILES = 10000

with open(input_file, "r") as f:
    reader = csv.reader(f)
    next(reader)
    smiles_list = []
    for r in reader:
        smiles_list += [r[0]]

R = []
count = 0
for i in range(len(smiles_list)):
    gen_smiles = []
    for j in range(n_samplings):
        file_path = os.path.join(TMP_FOLDER, "result_{0}/pharm_{0}_result.txt".format(count))
        with open(file_path, "r") as f:
            for l in f:
                gen_smiles += [l.rstrip(os.linesep)]
        count += 1
    gen_smiles = list(set(gen_smiles))
    random.shuffle(gen_smiles)
    gen_smiles = gen_smiles[:MAX_SMILES]
    R += [gen_smiles]

header = ["smiles_{0}".format(str(i).zfill(4)) for i in range(MAX_SMILES)]
with open(output_file, "w") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for r in R:
        r = r + [""]*(len(header) - len(r))
        writer.writerow(r)