import os
import glob
import subprocess
#from pdbfixer import PDBFixer
#from openmm.app import PDBFile

# Directories
INPUT_DIR = "/hits/fast/mbm/gruenefn/ProgramDev/martinize-examples/AllAtomProteins/alphalfold/pdb2gmx_structures"
OUTPUT_DIR = "martinized_structures_2"
FF_DIR = "/hits/fast/mbm/gruenefn/ProgramDev/martinize-examples/AllAtomProteins"
FF_NAME = "charmm36-jul2022-vermouth.ff"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.chdir(OUTPUT_DIR)

#def add_hydrogens_pdbfixer(input_pdb, output_pdb):
#   """Add missing hydrogens using PDBFixer."""
#   fixer = PDBFixer(filename=input_pdb)
#   fixer.findMissingResidues()
#   fixer.findMissingAtoms()
#   fixer.findNonstandardResidues()
#   fixer.addMissingAtoms()
#   fixer.addMissingHydrogens(pH=7.0)  # Adjust pH if needed

#   with open(output_pdb, "w") as f:
#       PDBFile.writeFile(fixer.topology, fixer.positions, f)
#   
#   print(f"Hydrogens added: {output_pdb}")

counter=0
# Process all PDB files
pdb_files = glob.glob(os.path.join(INPUT_DIR, "*.pdb"))
for pdb_file in pdb_files:
    pdb_name = os.path.basename(pdb_file).replace(".pdb", "")
    struct_dir = os.path.join(pdb_name)
    os.makedirs(struct_dir, exist_ok=True)

    pdb_h_file = os.path.join(struct_dir, f"{pdb_name}_H.pdb")

    # Add hydrogens
    add_hydrogens_pdbfixer(pdb_file, pdb_h_file)
    os.chdir(struct_dir)
    # Run martinize2
    command = [
        "martinize2",
        "-f", f"{pdb_name}_H.pdb",
        "-ff-dir", f"{FF_DIR}",
        "-ff", FF_NAME,
        "-bonds-fudge", "1.1",
        "-noscfix",
        "-from", FF_NAME,
        "-x", "out.pdb",
        "-o", "topol.top",
        "-ignore", "SOL"
    ]

    print(f"Running martinize2 for {pdb_name}...")
    with open("martinize2.log", "w") as log_file:
        subprocess.run(command, stdout=log_file, stderr=log_file)
    os.chdir("../")
    counter += 1
    if counter > 100:
        break
    print(f"Done processing {pdb_name}.")
print("All structures processed successfully.")

