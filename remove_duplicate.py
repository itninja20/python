#!/usr/bin/env python3

import os
import hashlib
import concurrent.futures
import pickle
from tqdm import tqdm

def get_file_hash(file_path):
    """Calculate the MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_and_remove_duplicate(directory, scanned_folders, scanned_files, total_files):
    """Find and remove duplicate files, keeping only the original."""
    file_hash_dict = {}
    duplicate_files = []

    with tqdm(total=total_files, desc="Scanning files", unit="files") as pbar:
        for root, _, files in os.walk(directory, followlinks=False):
            if root in scanned_folders:
                continue

            for file in files:
                file_path = os.path.join(root, file)

                # Check if the path is a symbolic link, and skip if it is.
                if os.path.islink(file_path):
                    continue

                # Check if the file is in the scanned_files set, indicating it was previously scanned.
                if file_path in scanned_files:
                    continue

                file_hash = get_file_hash(file_path)

                if file_hash in file_hash_dict:
                    duplicate_files.append((file_path, file_hash_dict[file_hash]))
                    os.remove(file_path)
                    print(f"Deleted duplicate file: {file_path}")
                else:
                    file_hash_dict[file_hash] = file_path

                # Add the file to the scanned_files set to mark it as scanned.
                scanned_files.add(file_path)
                pbar.update(1)

            # Add the scanned folder to the set of scanned_folders.
            scanned_folders.add(root)

    return duplicate_files

def save_scan_status(scanned_folders, scanned_files):
    """Save the scan status to a file."""
    with open("scan_status.pickle", "wb") as file:
        pickle.dump((scanned_folders, scanned_files), file)

def load_scan_status():
    """Load the scan status from a file."""
    scanned_folders = set()
    scanned_files = set()

    if os.path.exists("scan_status.pickle"):
        with open("scan_status.pickle", "rb") as file:
            scanned_folders, scanned_files = pickle.load(file)

    return scanned_folders, scanned_files

def count_total_files(directory):
    """Count the total number of files in the given directory."""
    total_files = 0
    for root, _, files in os.walk(directory):
        total_files += len(files)
    return total_files

if __name__ == "__main__":
    # directory_to_search = "/path/to/your/directory"
    parser = argparse.ArgumentParser(description="Find and remove duplicate files.")
    parser.add_argument("directory", help="Path to the directory to search for duplicate files.")
    args = parser.parse_args()

    directory_to_search = args.directory


    # Load scan status from file or initialize empty sets if the file doesn't exist.
    scanned_folders, scanned_files = load_scan_status()

    # Get the total number of files in the directory.
    total_files = count_total_files(directory_to_search)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        try:
            duplicate_files = executor.submit(find_and_remove_duplicate, directory_to_search, scanned_folders, scanned_files, total_files).result()
        except (Exception, KeyboardInterrupt) as e:
            print("\nAn error occurred during the scan:", e)
            save_scan_status(scanned_folders, scanned_files)
            raise e

    # Save the scan status after successful completion or KeyboardInterrupt.
    save_scan_status(scanned_folders, scanned_files)

    if duplicate_files:
        print("Duplicate files found and removed.")
    else:
        print("No duplicate files found.")


