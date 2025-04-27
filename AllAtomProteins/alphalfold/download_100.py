import os
import random
import tarfile
import gzip
from ftplib import FTP
from Bio import PDB

# Create a directory for downloaded structures
output_dir = "alphafold_structures"
os.makedirs(output_dir, exist_ok=True)

# FTP connection to AlphaFold database
ftp = FTP('ftp.ebi.ac.uk')
ftp.login()
ftp.cwd('/pub/databases/alphafold/latest/')

# Get available .tar files
files = ftp.nlst()
tar_files = [f for f in files if f.lower().endswith('.tar')]

if not tar_files:
    print("No .tar files found.")
    ftp.quit()
    exit()

# Select a subset of tar files to download
num_required = 100
downloaded_structures = []
random.shuffle(tar_files)

for tar_file in tar_files:
    if len(downloaded_structures) >= num_required:
        break

    print(f"Downloading {tar_file}...")
    local_tar_path = os.path.join(output_dir, tar_file)

    with open(local_tar_path, 'wb') as f:
        ftp.retrbinary('RETR ' + tar_file, f.write)

    print(f"Extracting {tar_file}...")
    with tarfile.open(local_tar_path) as tar:
        cif_files = [m for m in tar.getnames() if m.endswith('.cif.gz')]
        random.shuffle(cif_files)

        for cif_file in cif_files:
            if len(downloaded_structures) >= num_required:
                break
            
            tar.extract(cif_file, path=output_dir)
            downloaded_structures.append(os.path.join(output_dir, cif_file))
    
    os.remove(local_tar_path)  # Clean up tar file after extraction

ftp.quit()

# Convert .cif.gz to .pdb
parser = PDB.MMCIFParser(QUIET=True)
io = PDB.PDBIO()

for cif_gz_file in downloaded_structures:
    cif_file = cif_gz_file[:-3]  # Remove .gz extension
    pdb_file = cif_file.replace(".cif", ".pdb")

    # Decompress .gz file
    with gzip.open(cif_gz_file, 'rb') as f_in, open(cif_file, 'wb') as f_out:
        f_out.write(f_in.read())

    # Parse and convert to .pdb
    try:
        structure = parser.get_structure("protein", cif_file)
        io.set_structure(structure)
        io.save(pdb_file)
        print(f"Converted {cif_file} -> {pdb_file}")
    except Exception as e:
        print(f"Failed to convert {cif_file}: {e}")

    # Clean up intermediate files
    os.remove(cif_gz_file)
    os.remove(cif_file)

print(f"Downloaded and converted {len(downloaded_structures)} structures to PDB.")

