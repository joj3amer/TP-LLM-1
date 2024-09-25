import github
import os
from pathlib import Path
import shutil
import connect_chatgpt
import get_cfg_rust

def main():
    while True:
        # Ask for the GitHub URL
        github_url = input("Enter the GitHub URL (or 'Q' to quit): ")

        target_directory = "./java_files"

        # Check if the user wants to quit
        if github_url.strip().upper() == "Q":
            print("Exiting the program.")
            break

        # Define your local directory for storing the repository
        local_directory = "./"

        try:
            # Download and unzip the repository
            github.download_github_repo(github_url, local_directory, github.get_default_branch(github_url))

            # Path to the extracted repository directory (the repository name might vary)
            extracted_repo_dir = next(Path(local_directory).glob("*-"+github.get_default_branch(github_url)))  # This assumes the '-main' suffix after extraction

            # Define the target directory (current directory + /java_files)

            # Ensure target directory exists
            os.makedirs(target_directory, exist_ok=True)

            # Explore all subdirectories and copy Java files
            for root, dirs, files in os.walk(extracted_repo_dir):
                for file in files:
                    if file.endswith(".java"):
                        file_path = os.path.join(root, file)
                        shutil.copy(file_path, target_directory)
                        print(f"Copied: {file_path} -> {target_directory}")

            print(f"All Java files have been copied to {target_directory}.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # After main, read the content of the copied Java files and store it in a list
        java_files_content = []

        for root, dirs, files in os.walk(target_directory):
            for file in files:
                if file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                        java_files_content.append(file_content)

        print(f"Total number of Java files: {len(java_files_content)}")
        return java_files_content

if __name__ == "__main__":
    java_files_content = main()

    get_cfg_rust.generate_graph_cfg(connect_chatgpt.ask_chatgpt(java_files_content))
