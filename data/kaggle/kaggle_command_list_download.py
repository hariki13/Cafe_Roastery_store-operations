import subprocess
import sys
import argparse

#!/usr/bin/env python3
"""
Script to list and browse Kaggle datasets
"""

def list_kaggle_datasets(search_term=None, sort_by="hottest", page=1):
    """
    List Kaggle datasets using the Kaggle API
    
    Args:
        search_term: Optional search term to filter datasets
        sort_by: Sort order (hottest, votes, updated, active)
        page: Page number for pagination
    """
    try:
        # If no search term provided, default to "coffeeshop"
        if search_term is None:
            search_term = "coffeeshop"
        
        cmd = ["kaggle", "datasets", "list"]
        cmd.extend(["--search", search_term])
        cmd.extend(["--sort-by", sort_by])
        cmd.extend(["--page", str(page)])
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: Kaggle CLI not found. Install with: pip install kaggle", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="List Kaggle datasets")
    parser.add_argument("--search", help="Search term to filter datasets")
    parser.add_argument("--sort-by", default="hottest", 
                       choices=["hottest", "votes", "updated", "active"],
                       help="Sort order")
    parser.add_argument("--page", type=int, default=1, help="Page number")
    
    args = parser.parse_args()
    list_kaggle_datasets(args.search, args.sort_by, args.page)

    # download data set
    cmd_download = ["kaggle", "datasets", "download", "-d", "ryanalphaaugust/coffee-store-location/Coffee Store Location in Indonesia", "--unzip", "-p", "data/raw/light/coffeeshop_section/"]
    try:
        result = subprocess.run(cmd_download, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading dataset: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: Kaggle CLI not found. Install with: pip install kaggle", file=sys.stderr)
        sys.exit(1)
    # list files in the downloaded directory
    cmd_list_files = ["ls", "-l", "data/raw/light/coffeeshop_section/"]
    try:
        result = subprocess.run(cmd_list_files, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error listing files: {e.stderr}", file=sys.stderr)
        sys.exit(1)
        convert_to_csv=False,
        quiet=False
        )
    else:
        print(f"\n📤 Updating existing dataset: {dataset_name}")
        self.api.dataset_create_version(
                    folder=str(data_path),
                    version_notes="Updated dataset",
                    convert_to_csv=False,
                    quiet=False
                )
    # command in terminal for download dataset
    cmd = ["kaggle", "datasets", "download", "-d", "ryanalphaaugust/coffee-store-location/Coffee Store Location in Indonesia", "--unzip", "-p", "data/raw/light/coffeeshop_section/"]
    subprocess.run(cmd)

    # ls -lh command
    cmd_ls = ["ls", "-lh", "data/raw/light/coffeeshop_section/"]
    subprocess.run(cmd_ls)
    # terminal = ls -lh /workspaces/Cafe_Roastery_store-operations/data/kaggle/*csv (list all csv files in kaggle folder)

    # head command
    cmd_head = ["head", "-n", "10", "data/raw/light/coffeeshop_section/coffee-store-locations.csv"]
    subprocess.run(cmd_head)    
    print(result.stdout)
    # terminal = $ cd /workspaces/Cafe_Roastery_store-operations/.venv/bin/pythonscripts/kaggle/ "dataset-name"

    # command list kaggle data set
    cmd_list = ["kaggle", "datasets", "list", "-s", "coffee store location"]
    subprocess.run(cmd_list)
    print(result.stdout) 
    # terminal = $ cd /workspaces/Cafe_Roastery_store-operations/.venv/bin/pythonscripts/kaggle_search.py search "name of dataset"

    # command to view dataset details
    cmd_view = ["kaggle", "datasets", "view", "-d", "ryanalphaaugust/coffee-store-location/Coffee Store Location in Indonesia"]
    subprocess.run(cmd_view)
    print(result.stdout)

    # command to search dataset
    cmd_search = ["kaggle", "datasets", "list", "-s", "coffee"]
    subprocess.run(cmd_search)
    print(result.stdout)

    # command to log in to kaggle API
    cmd_login = ["kaggle", "config", "set", "username", "your_username"]
    subprocess.run(cmd_login)
    cmd_key = ["kaggle", "config", "set", "key", "your_key"]
    subprocess.run(cmd_key)
    print("Kaggle API configured.")

    # command to check kaggle API configuration
    cmd_check = ["kaggle", "config", "view"]
    subprocess.run(cmd_check)
    print(result.stdout)

    # command to run .kaggle/kaggle.json file
    cmd_kaggle_json = ["cat", "~/.kaggle/kaggle.json"]
    subprocess.run(cmd_kaggle_json)
    print(result.stdout)

    # move file to a specific folder
    cmd_move = ["mv", "kaggle.json", "~/.kaggle/"]
    subprocess.run(cmd_move)
    print("kaggle.json moved to ~/.kaggle/")
    mv /workspaces/Cafe_Roastery_store-operations/data/raw/light/coffeeshop_section/kaggle_command_list_download.py /workspaces/Cafe_Roastery_store-operations/data/kaggle/ && echo ""
    "✅ File moved successfully"

    
