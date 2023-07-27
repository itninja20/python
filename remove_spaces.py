#!/usr/bin/env python3

import os

def remove_spaces_from_filenames(directory_path):
    # Check if the provided directory exists
    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        return

    # Get a list of all files in the directory
    files = os.listdir(directory_path)

    for filename in files:
        # Skip directories
        file_path = os.path.join(directory_path, filename)
        if os.path.isdir(file_path):
            continue

        # Remove spaces from the filename
        new_filename = filename.replace(" ", "_")

        # Rename the file
        new_file_path = os.path.join(directory_path, new_filename)
        os.rename(file_path, new_file_path)

        print("found: " + file_path)
        print("rename: " + new_file_path)
        print("-"*70)

if __name__ == "__main__":
    target_directory = "/media/ninja/"
    remove_spaces_from_filenames(target_directory)

