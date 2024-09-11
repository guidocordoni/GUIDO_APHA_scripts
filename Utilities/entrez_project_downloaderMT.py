import os
import concurrent.futures
from Bio import Entrez

# Configure your email to use NCBI Entrez
Entrez.email = "your_email@example.com"  # Replace with your email

# Step 1: Get all SRA Accessions from BioProject
def get_sra_accessions(bioproject_id):
    handle = Entrez.esearch(db="sra", term=bioproject_id, retmax=1000)  # Increase retmax if needed
    record = Entrez.read(handle)
    handle.close()
    return record['IdList']

# Step 2: Use Entrez EFetch to get run info for SRA accessions
def fetch_run_info(accession_ids):
    handle = Entrez.efetch(db="sra", id=",".join(accession_ids), rettype="runinfo", retmode="text")
    run_info = handle.read().decode('utf-8')  # Decode the bytes-like object to a string
    handle.close()
    return run_info

# Function to download a single SRA file
def download_sra_file(run_id, download_folder):
    print(f"Downloading {run_id} ...")
    # Download the .sra file into the folder
    os.system(f"prefetch {run_id} -O {download_folder}")
    # Optionally convert .sra to fastq using fastq-dump into the folder
    os.system(f"fastq-dump --split-files {run_id} -O {download_folder}")
    print(f"{run_id} downloaded and converted.")

# Step 3: Download SRA files using multithreading
def download_sra_files(run_info, download_folder, max_threads=4):
    # Create the folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    sra_run_ids = [line.split(',')[0] for line in run_info.strip().split('\n')[1:]]  # Extracting Run IDs
    
    # Use ThreadPoolExecutor to download multiple files in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Submit a thread for each download
        futures = [executor.submit(download_sra_file, run_id, download_folder) for run_id in sra_run_ids]
        # Ensure all threads finish
        for future in concurrent.futures.as_completed(futures):
            future.result()  # This will raise exceptions if any occurred during execution

# Main script
if __name__ == "__main__":
    # Ask for the BioProject ID
    bioproject_id = input("Enter the BioProject ID: ")
    download_folder = "downloaded_sequences"

    # Get all SRA accessions related to the BioProject
    accession_ids = get_sra_accessions(bioproject_id)

    if accession_ids:
        # Fetch run info for the accessions
        run_info = fetch_run_info(accession_ids)
        
        # Download SRA files into the 'downloaded_sequences' folder with multithreading
        max_threads = 4  # Number of threads to use (adjust based on your system)
        download_sra_files(run_info, download_folder, max_threads)
        print(f"All sequences have been downloaded into the folder: {download_folder}")
    else:
        print("No accessions found for the BioProject.")


