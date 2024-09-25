import os
import requests
from pathlib import Path
import shutil
import zipfile
import sys

def get_default_branch(repo_url):
    """
    Get the default branch of the GitHub repository using GitHub API.
    """
    api_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/")
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()["default_branch"]
    else:
        raise Exception(f"Failed to fetch repository details. Status code: {response.status_code}")

def download_github_repo(repo_url, local_dir, branch):
    """
    Clone the GitHub repository by downloading its contents using GitHub's zipball URL.
    """
    zip_url = f"{repo_url}/archive/refs/heads/{branch}.zip"
    zip_file_path = os.path.join(local_dir, "repo.zip")

    # Download the zip file
    response = requests.get(zip_url)
    
    if response.status_code == 200:
        with open(zip_file_path, 'wb') as file:
            file.write(response.content)
        print(f"Repository downloaded as zip file: {zip_file_path}")
    else:
        raise Exception(f"Failed to download repository. Status code: {response.status_code}")

    # Unzip the repository
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(local_dir)
    
    # Remove the zip file after extracting
    os.remove(zip_file_path)

def copy_java_files_to_current_dir(src_directory, target_directory):
    """
    Copy all .java files from the source directory to the target directory (create if not exists).
    """
    # Ensure target directory exists
    os.makedirs(target_directory, exist_ok=True)
    
    for root, dirs, files in os.walk(src_directory):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                # Copy the file to the target directory
                shutil.copy(file_path, target_directory)
                print(f"Copied: {file_path} -> {target_directory}")

def main():
    while True:
        # Ask for the GitHub URL
        github_url = input("Enter the GitHub URL (or 'Q' to quit): ")

        # Check if the user wants to quit
        if github_url.strip().upper() == "Q":
            print("Exiting the program.")
            break

        # Define your local directory for storing the repository
        local_directory = "./sample_project"

        try:
            # Get the default branch (main, master, etc.)
            default_branch = get_default_branch(github_url)
            print(f"Default branch: {default_branch}")

            # Download and unzip the repository
            download_github_repo(github_url, local_directory, default_branch)

            # Path to the extracted repository directory (may vary based on repo name)
            extracted_repo_dir = next(Path(local_directory).glob("*-main"))  # Assumes the '-main' suffix after extraction

            # Define the target directory (current directory + /java_files)
            target_directory = "./java_files"

            # Copy all Java files to the target directory
            copy_java_files_to_current_dir(extracted_repo_dir, target_directory)

            print(f"All Java files have been copied to {target_directory}.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
