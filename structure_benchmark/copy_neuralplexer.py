"""From the downloads dir, transfer and rename neuralplexer output."""

import os
import pathlib


def get_pdb_from_neuralplexer_sm(np_dir):
    # pdb files
    pdb_files = list(np_dir.glob("*.pdb"))
    candidates = list()
    for pdb_file in pdb_files:
        if pdb_file.name.startswith("prot_"):
            if pdb_file.name.endswith("_ligand.pdb"):
                candidates.append(pdb_file)

    assert len(candidates) == 1, f"For {np_dir}, found {len(candidates)} candidates."
    return candidates[0]


def run_main():
    # sm
    script_dir = pathlib.Path(__file__).parent
    sm_dir = "~/Downloads/predictions_sm"
    sm_dir = pathlib.Path(sm_dir).expanduser()
    out_dir = script_dir / "neuralplexer_sm"
    out_dir.mkdir(exist_ok=True)
    for subdir in sm_dir.iterdir():
        if not subdir.is_dir():
            continue
        pdb_id = subdir.name
        out_p = out_dir / f"{pdb_id}.pdb"
        if out_p.exists():
            print(f"Skipping {pdb_id} as {out_p} already exists.")
            continue
        pdb_file = get_pdb_from_neuralplexer_sm(subdir)
        pdb_file = pdb_file.resolve()
        print(f"Copying {pdb_file} to {out_p}")
        pathlib.Path(pdb_file).replace(out_p)

    # chain
    chain_dir = "~/Downloads/predictions_chain"
    chain_dir = pathlib.Path(chain_dir).expanduser()
    out_dir = script_dir / "neuralplexer_chain"
    out_dir.mkdir(exist_ok=True)
    for subdir in chain_dir.iterdir():
        if not subdir.is_dir():
            continue
        pdb_id = subdir.name
        pdb_file = subdir / "prot_input_no_lig.pdb"
        pdb_file = pdb_file.resolve()
        out_p = out_dir / f"{pdb_id}.pdb"
        if out_p.exists():
            print(f"Skipping {pdb_id} as {out_p} already exists.")
            continue
        print(f"Copying {pdb_file} to {out_p}")
        pathlib.Path(pdb_file).replace(out_p)

    # AF2, AF2_noTemplate, AF2_activeTemplate
    dir_names = ["AF2", "AF2_noTemplate", "AF2_activeTemplate"]
    for dir_name in dir_names:
        af2_dir = f"~/Downloads/predictions_{dir_name}"
        af2_dir = pathlib.Path(af2_dir).expanduser()
        out_dir = script_dir / dir_name
        out_dir.mkdir(exist_ok=True)
        for subdir in af2_dir.iterdir():
            print(subdir)


if __name__ == "__main__":
    run_main()
