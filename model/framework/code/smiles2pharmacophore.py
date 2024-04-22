import sys
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
print(ROOT)
sys.path.append(os.path.join(ROOT, "PGMG", "utils"))

from smiles2ppgraph import smiles2ppgraph

smiles = 'CC1=C(C(C)=O)C(N(C(CC)CC)C2=NC(NC3=NC=C(N4CCNCC4)C=C3)=NC=C12)=O'

ppgraph = smiles2ppgraph(smiles)

g_, smiles_code_res = smiles2ppgraph(smiles)

print(g_)
