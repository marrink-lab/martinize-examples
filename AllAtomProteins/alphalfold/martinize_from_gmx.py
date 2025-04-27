import os
import glob
import subprocess
#from pdbfixer import PDBFixer
#from openmm.app import PDBFile
import gromacs 

# Directories
INPUT_DIR = "/hits/fast/mbm/gruenefn/ProgramDev/martinize-examples/AllAtomProteins/alphalfold/pdb2gmx_structures"
OUTPUT_DIR = "martinized_structures_run2"
FF_DIR = "/hits/fast/mbm/gruenefn/ProgramDev/martinize-examples/AllAtomProteins"
FF_NAME = "charmm36-jul2022-vermouth.ff"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.chdir(OUTPUT_DIR)

def add_hydrogens_pdbfixer(input_pdb, output_pdb):
    """Add missing hydrogens using PDBFixer."""
    fixer = PDBFixer(filename=input_pdb)
    fixer.findMissingResidues()
    fixer.findMissingAtoms()
    fixer.findNonstandardResidues()
    fixer.addMissingAtoms()
    fixer.addMissingHydrogens(pH=7.0)  # Adjust pH if needed

    with open(output_pdb, "w") as f:
        PDBFile.writeFile(fixer.topology, fixer.positions, f)
    
    print(f"Hydrogens added: {output_pdb}")

counter=0
# Process all PDB files
for folder_name in os.listdir(INPUT_DIR):
    folder_path = os.path.join(INPUT_DIR, folder_name)
    if os.path.isdir(folder_path):  # Ensure it's a directory
        # make the output directory
        struct_dir = os.path.join(folder_name)
        os.makedirs(struct_dir, exist_ok=True)
        os.chdir(struct_dir)

        filename = "conf.gro"
        file_path = os.path.join(folder_path, filename)
        gromacs.editconf(f=file_path, o=f"{folder_name}.pdb")

        # Run martinize2
        command = [
            "martinize2",
            "-f", f"{folder_name}.pdb",
            "-ff-dir", f"{FF_DIR}",
            "-ff", FF_NAME,
            "-noscfix",
            "-from", FF_NAME,
            "-x", "out.pdb",
            "-maxwarn", "10000",
            "-o", "topol.top",
            "-ignore", "SOL"
        ]
        
        print(f"Running martinize2 for {folder_name}...")
        with open("martinize2.log", "w") as log_file:
            subprocess.run(command, stdout=log_file, stderr=log_file)
        os.chdir("../")
        counter += 1
        if counter > 100:
            break
        print(f"Done processing {folder_name}.")
print("All structures processed successfully.")

