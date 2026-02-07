import sys
import os
import csv
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent


from utils.smiles2ppgraph import smiles2ppgraph
from utils.file_utils import export_ep_text


def read_smiles_csv(file_path):
    file_path = Path(file_path)
    smiles_list = []
    with file_path.open("r", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)
        for r in reader:
            if not r:
                continue
            s = (r[0] or "").strip()
            if s:
                smiles_list.append(s)
    return smiles_list


def write_pharmacophore_edgep_files(smiles_list, n_samplings, out_dir, prefix="pharm_"):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    created = []
    counts = 0
    for smiles in smiles_list:
        for _ in range(int(n_samplings)):
            g, _ = smiles2ppgraph(smiles)
            fp = out_dir / "{0}{1}.edgep".format(prefix, counts)
            text = export_ep_text(g)
            with fp.open("w") as f:
                f.write(text)
            created.append(fp)
            counts += 1
    return created


def main():
    file_path = sys.argv[1]
    n_samplings = int(sys.argv[2])

    tmp_folder = (ROOT / ".." / ".." / "tmp").resolve()
    if tmp_folder.exists():
        shutil.rmtree(tmp_folder)
    tmp_folder.mkdir(parents=True, exist_ok=True)

    smiles_list = read_smiles_csv(file_path)
    write_pharmacophore_edgep_files(smiles_list, n_samplings, tmp_folder)


if __name__ == "__main__":
    main()
