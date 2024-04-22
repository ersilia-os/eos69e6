import sys
import os
import shutil
import csv

ROOT = os.path.dirname(os.path.abspath(__file__))

from utils.smiles2ppgraph import smiles2ppgraph
from utils.file_utils import export_ep_text


file_path = sys.argv[1]
n_samplings = int(sys.argv[2])


TMP_FOLDER = os.path.join(ROOT, "..", "..", "tmp")
if os.path.exists(TMP_FOLDER):
    shutil.rmtree(TMP_FOLDER)
os.makedirs(TMP_FOLDER)


with open(file_path, "r") as f:
    reader = csv.reader(f)
    next(reader)
    smiles_list = []
    for r in reader:
        smiles_list += [r[0]]


counts = 0
for i, smiles in enumerate(smiles_list):
    for j in range(n_samplings):
        g, _ = smiles2ppgraph(smiles)
        file_path = os.path.join(TMP_FOLDER, "pharm_{0}.edgep".format(counts))
        text = export_ep_text(g)
        with open(file_path, "w") as f:
            f.write(text)
        counts += 1