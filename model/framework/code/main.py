import csv
import os
import random
import sys
import tempfile
from pathlib import Path

DEFAULT_N_SAMPLINGS = 10
DEFAULT_N_MOL_PER_PHARM = 500
DEFAULT_DEVICE = "cpu"
DEFAULT_FILTER = True
DEFAULT_BATCH_SIZE = 512
MAX_SMILES = 1000

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root, "SQUID"))

def main():
    if len(sys.argv) < 3:
        print("Usage: python assemble_results.py <input.csv> <output.csv>")
        sys.exit(1)

    input_csv = Path(sys.argv[1]).resolve()
    output_csv = Path(sys.argv[2]).resolve()

    code_root = Path(__file__).resolve().parent
    pgmg_root = (code_root / "PGMG").resolve()

    sys.path.insert(0, str(pgmg_root))

    from generate_pharmacophores import read_smiles_csv, write_pharmacophore_edgep_files
    from generate import load_model, generate_smiles_from_pharmacophore_file

    model_path = pgmg_root / "weights" / "chembl_fold0_epoch32.pth"
    tokenizer_path = pgmg_root / "weights" / "tokenizer.pkl"

    smiles_list = read_smiles_csv(input_csv)

    model, tokenizer = load_model(model_path, tokenizer_path)
    model.eval()
    model.to(DEFAULT_DEVICE)

    header = [f"smiles_{str(i).zfill(4)}" for i in range(MAX_SMILES)]

    rows: list[list[str]] = []

    with tempfile.TemporaryDirectory(prefix="pgmg_tmp_") as tmpdir:
        tmpdir = Path(tmpdir)

        pharm_files = write_pharmacophore_edgep_files(
            smiles_list=smiles_list,
            n_samplings=DEFAULT_N_SAMPLINGS,
            out_dir=tmpdir,
            prefix="pharm_",
        )

        idx = 0
        for _smiles in smiles_list:
            gen_set: set[str] = set()

            for _ in range(DEFAULT_N_SAMPLINGS):
                pharm_fp = pharm_files[idx]
                idx += 1

                gen_smiles = generate_smiles_from_pharmacophore_file(
                    file_path=pharm_fp,
                    model=model,
                    tokenizer=tokenizer,
                    n_mol=DEFAULT_N_MOL_PER_PHARM,
                    device=DEFAULT_DEVICE,
                    do_filter=DEFAULT_FILTER,
                    batch_size=DEFAULT_BATCH_SIZE,
                )
                gen_set.update(gen_smiles)

            gen_list = list(gen_set)
            random.shuffle(gen_list)
            gen_list = gen_list[:MAX_SMILES]

            gen_list += [""] * (MAX_SMILES - len(gen_list))
            rows.append(gen_list)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"Done. Wrote: {output_csv}")


if __name__ == "__main__":
    main()
