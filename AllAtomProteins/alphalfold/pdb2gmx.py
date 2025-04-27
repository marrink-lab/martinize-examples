import os
import glob
import subprocess
from pdbfixer import PDBFixer
from openmm.app import PDBFile

# Directories
INPUT_DIR = "/hits/fast/mbm/gruenefn/ProgramDev/martinize-examples/AllAtomProteins/alphalfold/alphafold_structures"
OUTPUT_DIR = "pdb2gmx_structures"
FF_DIR = "/hits/fast/mbm/gruenefn/ProgramDev/martinize-examples/AllAtomProteins"
FF_NAME = "charmm36-jul2022-patched.ff"
FF_SEL = "charmm36-jul2022-patched"
# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.chdir(OUTPUT_DIR)

counter=0
# Process all PDB files
pdb_files = glob.glob(os.path.join(INPUT_DIR, "*.pdb"))
for pdb_file in pdb_files:
    pdb_name = os.path.basename(pdb_file).replace(".pdb", "")
    struct_dir = os.path.join(pdb_name)
    os.makedirs(struct_dir, exist_ok=True)
    os.chdir(struct_dir)
    source = os.path.join(FF_DIR, FF_NAME)
    os.symlink(source, f"./{FF_NAME}")
    # Run martinize2
    command = [
        "gmx", "pdb2gmx",
        "-f", pdb_file,
        "-ignh",
        "-water" , "none", 
        "-ff", f"{FF_SEL}"]

    print(f"Running martinize2 for {pdb_name}...")
    subprocess.run(command)
    os.chdir("../")
    counter += 1
    if counter > 100:
        break
    print(f"Done processing {pdb_name}.")
print("All structures processed successfully.")

