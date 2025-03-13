"""
Call RIA for each .pdb file
"""
import pathlib
import subprocess
import threading



def get_all_pdbs_from_path(p:pathlib.Path):
    return [x for x in p.iterdir() if x.suffix == ".pdb"]


def run_RIA(pdb:pathlib.Path, out:pathlib.Path, python_p:str):
    # RIA
    print(f"Running RIA on {pdb.name}")
    # return if out exists
    if out.exists():
        print(f"{out.name} already exists")
        return
    cmd = f"{python_p} /projects/ilfgrid/data/Luuk/Classifier_models/rescore_scripts/RoseTTA_interface_analyzer.py -i {pdb} -o {out}"
    subprocess.run(cmd, shell=True)
    
def run_main():
    # data
    dir_with_subdirs = "/projects/ilfgrid/data/Luuk/Classifier_models/data"
    dir_with_subdirs = pathlib.Path(dir_with_subdirs)
    # subdirs = [x for x in dir_with_subdirs.iterdir() if x.is_dir()]
    subdirs = [
        dir_with_subdirs / 'AF3',
        dir_with_subdirs / 'Chai-1',
    ]

    python_p = "/projects/ilfgrid/data/Luuk/Luuk_env/luuk_conda_env/bin/python"

    all_pdbs = [p for p in subdirs for p in get_all_pdbs_from_path(p)]
    all_out_sc = [p.with_suffix(".sc") for p in all_pdbs]
    # remove from lists if out exists
    existing_indexes = [i for i, p in enumerate(all_out_sc) if p.exists()]
    print(f"Number of existing .sc files: {len(existing_indexes)}")
    all_pdbs = [p for i, p in enumerate(all_pdbs) if i not in existing_indexes]
    all_out_sc = [p for i, p in enumerate(all_out_sc) if i not in existing_indexes]

    print(f"Total number of pdbs: {len(all_pdbs)}")

    active_threads = []
    number_of_threads = 16
    
    # split pdbs and out_sc in number_of_threads
    pdb_sections = [all_pdbs[i:i+number_of_threads] for i in range(0, len(all_pdbs), number_of_threads)]
    out_sc_sections = [all_out_sc[i:i+number_of_threads] for i in range(0, len(all_out_sc), number_of_threads)]

    # run threads
    for section_i, section in enumerate(pdb_sections):
        for pdb_i, pdb in enumerate(section):
            out = out_sc_sections[section_i][pdb_i]
            t = threading.Thread(target=run_RIA, args=(pdb, out, python_p))
            t.start()
            active_threads.append(t)
        for t in active_threads:
            t.join()
    
    print("All done")


if __name__ == "__main__":
    run_main()
