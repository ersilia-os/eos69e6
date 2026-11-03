import csv
import random
import sys
import tempfile
from pathlib import Path

from output_checks import OutputFilter

DEFAULT_N_SAMPLINGS = 10
DEFAULT_N_MOL_PER_PHARM = 50
DEFAULT_DEVICE = "cpu"
DEFAULT_FILTER = True
# Only the first DEFAULT_N_MOL_PER_PHARM sequences of a batch are kept, so decode no more.
DEFAULT_BATCH_SIZE = DEFAULT_N_MOL_PER_PHARM
MAX_SMILES = 100


class RowFailed(Exception):
    """A row that could not be filled.

    ``kind`` is "input" when the input is the cause (unusable input, or no
    pharmacophore could be drawn from it) and "model" when decoding failed. The
    run exits non-zero only if every row failed and one of them is a "model" failure.
    """

    def __init__(self, kind, message):
        super().__init__(message)
        self.kind = kind


def describe(exc):
    """One line for the log: a RowFailed message, or the type and first message line of any other error.

    Some libraries put a whole stack trace in the message of their errors (DGL does).
    """
    if isinstance(exc, RowFailed):
        return str(exc)
    lines = str(exc).strip().splitlines()
    return f"{type(exc).__name__}: {lines[0] if lines else ''}"


def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <input.csv> <output.csv>")
        sys.exit(1)

    input_csv = Path(sys.argv[1]).resolve()
    output_csv = Path(sys.argv[2]).resolve()

    code_root = Path(__file__).resolve().parent
    pgmg_root = (code_root / "PGMG").resolve()
    checkpoints_root = (code_root / ".." / ".." / "checkpoints").resolve()

    sys.path.insert(0, str(pgmg_root))

    from generate import generate_smiles_from_pharmacophore_file, load_model
    from generate_pharmacophores import (
        read_smiles_csv,
        write_pharmacophore_edgep_files,
    )

    model_path = checkpoints_root / "chembl_fold0_epoch32.pth"
    tokenizer_path = checkpoints_root / "tokenizer.pkl"

    smiles_list = read_smiles_csv(input_csv)

    model, tokenizer = load_model(model_path, tokenizer_path)
    model.eval()
    model.to(DEFAULT_DEVICE)

    header = [f"smi_{str(i).zfill(2)}" for i in range(MAX_SMILES)]

    def row_for(idx, smiles, tmpdir):
        """Up to MAX_SMILES checked molecules for one input, padded with empty strings."""
        checks = OutputFilter(smiles)
        if not checks.ok:
            raise RowFailed(
                "input",
                "input is empty, unparsable, multi-component or has no InChIKey",
            )

        kept = []
        failures = []  # (kind, message) of each failed sampling
        for k in range(DEFAULT_N_SAMPLINGS):
            # a fresh random pharmacophore hypothesis for each sampling; a molecule
            # with fewer than two pharmacophore features fails here (an input limit)
            try:
                pharm_fp = write_pharmacophore_edgep_files(
                    smiles_list=[smiles],
                    n_samplings=1,
                    out_dir=tmpdir,
                    prefix=f"pharm_{idx}_{k}_",
                )[0]
            except Exception as exc:
                failures.append(("input", describe(exc)))
                continue
            try:
                gen_smiles = generate_smiles_from_pharmacophore_file(
                    file_path=pharm_fp,
                    model=model,
                    tokenizer=tokenizer,
                    n_mol=DEFAULT_N_MOL_PER_PHARM,
                    device=DEFAULT_DEVICE,
                    do_filter=DEFAULT_FILTER,
                    batch_size=DEFAULT_BATCH_SIZE,
                )
            except Exception as exc:
                failures.append(("model", describe(exc)))
                continue
            for s in gen_smiles:
                out = checks.accept(s)
                if out is not None:
                    kept.append(out)

        if len(failures) == DEFAULT_N_SAMPLINGS:
            model_failures = [m for kind, m in failures if kind == "model"]
            raise RowFailed(
                "model" if model_failures else "input",
                f"all {DEFAULT_N_SAMPLINGS} pharmacophore samplings failed, first: "
                f"{(model_failures or [failures[0][1]])[0]}",
            )
        random.shuffle(kept)
        kept = kept[:MAX_SMILES]
        print(
            f"[INFO] {smiles} samplings_failed={len(failures)} {checks.summary()} "
            f"returned={len(kept)}"
        )
        return kept + [""] * (MAX_SMILES - len(kept))

    rows = []
    failed = []  # (kind, message) of each row that could not be filled

    with tempfile.TemporaryDirectory(prefix="pgmg_tmp_") as tmpdir:
        tmpdir = Path(tmpdir)

        for idx, smiles in enumerate(smiles_list):
            try:
                rows.append(row_for(idx, smiles, tmpdir))
            except Exception as exc:
                # anything unexpected counts as the model failing
                kind = getattr(exc, "kind", "model")
                print(f"[ERROR] {smiles!r}: {describe(exc)}", file=sys.stderr)
                failed.append((kind, describe(exc)))
                rows.append([""] * MAX_SMILES)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    # a file of unusable inputs is a valid (empty) answer; a broken model is not
    model_errors = [m for kind, m in failed if kind == "model"]
    if rows and len(failed) == len(rows) and model_errors:
        print(
            f"[ERROR] every input failed, first model error: {model_errors[0]}",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Done. Wrote: {output_csv}")


if __name__ == "__main__":
    main()
