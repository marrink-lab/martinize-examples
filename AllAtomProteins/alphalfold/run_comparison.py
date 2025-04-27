import os
import subprocess

# Define the main directory containing the folders
MAIN_DIR = "/hits/fast/mbm/gruenefn/ProgramDev/martinize-examples/AllAtomProteins/alphalfold/martinized_structures_run2"  # Change this to your actual path
OTHER_FOLDER = "/hits/fast/mbm/gruenefn/ProgramDev/martinize-examples/AllAtomProteins/alphalfold/pdb2gmx_structures"  # Change this if needed
COMP = "/hits/fast/mbm/gruenefn/ProgramDev/martinize-examples/AllAtomProteins/alphalfold/compare.py"
MDP = "/hits/fast/mbm/gruenefn/ProgramDev/martinize-examples/AllAtomProteins/md.mdp"

os.mkdir("comparison")
os.chdir("comparison")

# Loop over all subdirectories in MAIN_DIR
for folder_name in os.listdir(MAIN_DIR):
    folder_path = os.path.join(MAIN_DIR, folder_name)
    if os.path.isdir(folder_path):  # Ensure it's a directory
        c1 = f"out.pdb"
        c2 = f"{folder_name}.pdb"
        c1_path = os.path.join(folder_path, c1)
        c2_path = os.path.join(folder_path, c2)

        if os.path.exists(c1_path):  # Check if file exists
            top_file = os.path.join(folder_path, "system.top")
            other_top_file = os.path.join(OTHER_FOLDER, f"{folder_name}/topol.top")

            # Construct the command
            command = ["python", COMP, "-p", top_file, other_top_file, "-c", c1_path, c2_path, "-f", MDP, "-mol", folder_name]

            # Run the command
            print(f"Running: {' '.join(command)}")
            subprocess.run(command)

print("Processing complete.")

