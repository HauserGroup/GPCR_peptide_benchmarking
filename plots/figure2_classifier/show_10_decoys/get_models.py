import pathlib
import os


def run_main():
    download_dir = "~/Downloads/glr_human"
    download_dir = pathlib.Path(download_dir).expanduser()
    script_dir = pathlib.Path(__file__).parent.absolute()
    out_dir = script_dir / "models"
    out_dir.mkdir(exist_ok=True)
    for subdir in download_dir.iterdir():
        if not subdir.is_dir():
            continue
        # find pdb, which is subdir name + ".pdb"
        pdb = subdir / f"{subdir.name}.pdb"
        if not pdb.exists():
            print(f"Skipping {subdir}")
            continue
        new_p = out_dir / f"{subdir.name}.pdb"
        # copy
        os.system(f"cp {pdb} {new_p}")
        print(f"Copying {pdb} to {new_p}")


if __name__ == "__main__":
    run_main()
    print("Done!")
