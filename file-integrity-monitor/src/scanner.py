import os
from integrity import calculate_hash

def scan_directory(directory_path):
    file_hashes = {}

    for root, _, files in os.walk(directory_path):
        for file in files:
            full_path = os.path.join(root, file)
            file_hashes[full_path] = calculate_hash(full_path)

    return file_hashes
