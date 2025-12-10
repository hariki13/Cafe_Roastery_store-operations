"""
Kaggle Dataset Search and List Script
This script provides functions to list, search, and download Kaggle datasets
"""

from kaggle.api.kaggle_api_extended import KaggleApi
import os


def initialize_api():
    """Initialize and authenticate Kaggle API"""
    api = KaggleApi()
    api.authenticate()
    return api


def list_datasets(page=1, max_results=20):
    """
    List popular Kaggle datasets
    
    Args:
        page (int): Page number to retrieve
        max_results (int): Maximum number of results to display
    """
    api = initialize_api()
    datasets = api.dataset_list(page=page)
    
    print(f"\n{'='*100}")
    print(f"TOP {max_results} KAGGLE DATASETS (Page {page})")
    print(f"{'='*100}")
    print(f"{'#':<5} {'Dataset Reference':<50} {'Title'}")
    print(f"{'-'*100}")
    
    for idx, dataset in enumerate(datasets[:max_results], 1):
        print(f"{idx:<5} {dataset.ref:<50} {dataset.title}")
    
    print(f"{'='*100}\n")
    return datasets[:max_results]


def search_datasets(search_term, max_results=20):
    """
    Search for Kaggle datasets by keyword
    
    Args:
        search_term (str): Search keyword
        max_results (int): Maximum number of results to display
    """
    api = initialize_api()
    datasets = api.dataset_list(search=search_term)
    
    print(f"\n{'='*100}")
    print(f"SEARCH RESULTS FOR: '{search_term}' (Top {max_results} results)")
    print(f"{'='*100}")
    print(f"{'#':<5} {'Dataset Reference':<50} {'Title'}")
    print(f"{'-'*100}")
    
    for idx, dataset in enumerate(datasets[:max_results], 1):
        print(f"{idx:<5} {dataset.ref:<50} {dataset.title}")
    
    print(f"{'='*100}\n")
    return datasets[:max_results]


def download_dataset(dataset_ref, download_path='./downloads', unzip=True):
    """
    Download a specific Kaggle dataset
    
    Args:
        dataset_ref (str): Dataset reference (e.g., 'user/dataset-name')
        download_path (str): Path where to download the dataset
        unzip (bool): Whether to unzip the downloaded files
    """
    api = initialize_api()
    
    # Create download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    print(f"\nDownloading dataset: {dataset_ref}")
    print(f"Download path: {download_path}")
    print(f"Unzip: {unzip}")
    
    try:
        api.dataset_download_files(dataset_ref, path=download_path, unzip=unzip)
        print(f"✓ Successfully downloaded: {dataset_ref}")
        print(f"Dataset URL: https://www.kaggle.com/datasets/{dataset_ref}")
    except Exception as e:
        print(f"✗ Error downloading dataset: {e}")


def download_multiple_datasets(dataset_refs, download_path='./downloads', unzip=True):
    """
    Download multiple Kaggle datasets
    
    Args:
        dataset_refs (list): List of dataset references
        download_path (str): Path where to download the datasets
        unzip (bool): Whether to unzip the downloaded files
    """
    print(f"\n{'='*100}")
    print(f"DOWNLOADING {len(dataset_refs)} DATASETS")
    print(f"{'='*100}\n")
    
    for idx, dataset_ref in enumerate(dataset_refs, 1):
        print(f"[{idx}/{len(dataset_refs)}] ", end="")
        download_dataset(dataset_ref, download_path, unzip)
        print()


def get_dataset_info(dataset_ref):
    """
    Get detailed information about a specific dataset
    
    Args:
        dataset_ref (str): Dataset reference (e.g., 'user/dataset-name')
    """
    api = initialize_api()
    
    try:
        owner, dataset_name = dataset_ref.split('/')
        dataset_info = api.dataset_view(owner, dataset_name)
        
        print(f"\n{'='*100}")
        print(f"DATASET INFORMATION: {dataset_ref}")
        print(f"{'='*100}")
        print(f"Title: {dataset_info.title}")
        print(f"Owner: {dataset_info.ownerName}")
        print(f"Size: {dataset_info.totalBytes / (1024*1024):.2f} MB")
        print(f"Downloads: {dataset_info.downloadCount}")
        print(f"Vote Count: {dataset_info.voteCount}")
        print(f"Last Updated: {dataset_info.lastUpdated}")
        print(f"URL: https://www.kaggle.com/datasets/{dataset_ref}")
        print(f"{'='*100}\n")
        
        return dataset_info
    except Exception as e:
        print(f"Error getting dataset info: {e}")


# Example usage
if __name__ == "__main__":
    print("\n" + "="*100)
    print("KAGGLE DATASET SEARCH AND LIST TOOL")
    print("="*100)
    
    # Example 1: List top 20 datasets
    print("\n1. LISTING TOP DATASETS")
    datasets = list_datasets(page=1, max_results=20)
    
    # Example 2: Search for specific datasets
    print("\n2. SEARCHING FOR DATASETS")
    search_term = "coffee shop"
    coffee_datasets = search_datasets(search_term, max_results=30)
    
    # Example 3: Download a specific dataset (commented out to avoid accidental downloads)
    # download_dataset('wardabilal/spotify-global-music-dataset-20092025', download_path='./kaggle_data_set')
    
    # Example 4: Download multiple datasets
    dataset_list = [
         'alejandromendozaarv/roast-coffee-shop-2023-financials',
         'wardabilal/exploring-coffee-sales-with-eda-and-visualization',
         'viramatv/coffee-shop-data',
         'mannarmohamedsayed/coffee-shop-analysis']
    download_multiple_datasets(dataset_list, download_path='./kaggle_coffee_data_set')
    
    print("\n" + "="*100)
    print("Script completed!")
    print("="*100)