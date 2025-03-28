import os
import csv
import tarfile
import urllib.request
import shutil

def extract_tar_strip_top(tar_path, dest_path):
    """
    Extracts the tar.gz file located at tar_path into dest_path.
    If all members have a common top-level directory, it strips that directory.
    """
    with tarfile.open(tar_path, "r:gz") as tar:
        members = tar.getmembers()
        # Get member names that include a directory separator
        names = [member.name for member in members if "/" in member.name]
        common_prefix = os.path.commonprefix(names) if names else ""
        
        # If all members with "/" start with the same prefix, remove it
        if common_prefix and all(member.name.startswith(common_prefix) for member in members if "/" in member.name):
            prefix_len = len(common_prefix)
            for member in members:
                if member.name.startswith(common_prefix):
                    member.name = member.name[prefix_len:].lstrip("/")
        tar.extractall(path=dest_path, members=members)

def process_csv(csv_file="results-with-build-information.csv"):
    # Read all rows (excluding header/empty lines)
    rows = []
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if not row or row[0] == "project":
                continue
            rows.append(row)
    
    # Calculate total unique (project, merge commit) keys
    unique_keys = {(row[0], row[1]) for row in rows}
    total_unique = len(unique_keys)
    
    processed = set()  # Set to keep track of processed (project, merge commit) keys
    processed_count = 0

    for row in rows:
        project = row[0]
        merge_commit = row[1]
        release_hash = row[9]  # "realistic case path" column holds the release hash

        key = (project, merge_commit)
        # If this key has already been processed, skip download/extraction
        if key in processed:
            print(f"Project {project}, commit {merge_commit} has already been processed. Skipping it.")
            continue

        processed.add(key)
        processed_count += 1
        percentage = (processed_count / total_unique) * 100

        # Build directory paths
        project_dir = project
        merge_commit_dir = os.path.join(project_dir, merge_commit)
        target_dir = os.path.join(merge_commit_dir, "original-without-dependencies")

        # If the target folder exists, remove it to avoid duplicate extraction
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)

        # Create the necessary folder(s)
        os.makedirs(target_dir, exist_ok=True)

        # Build the download URL:
        # 'https://github.com/victorlira/' + project + '/releases/download/build-' + release_hash + '/result.tar.gz'
        url = f"https://github.com/victorlira/{project}/releases/download/build-{release_hash}/result.tar.gz"
        tar_path = os.path.join(target_dir, "result.tar.gz")

        try:
            #print(f"Downloading from {url} to {tar_path}...")
            urllib.request.urlretrieve(url, tar_path)
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            continue

        # Extract the tar.gz file into the target directory (stripping top-level folder if applicable)
        try:
            extract_tar_strip_top(tar_path, target_dir)
        except Exception as e:
            print(f"Error extracting {tar_path}: {e}")
            continue

        # Remove the downloaded tar.gz file after extraction
        try:
            os.remove(tar_path)
        except Exception as e:
            print(f"Error removing {tar_path}: {e}")

        # Print processing completion message with percentage of commits processed
        print(f"Project {project}, commit {merge_commit} processed. {percentage:.2f}%.")

if __name__ == '__main__':
    process_csv()
