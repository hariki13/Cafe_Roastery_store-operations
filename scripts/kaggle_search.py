#!/usr/bin/env python3
"""
Kaggle Dataset Search Tool
Search and browse datasets on Kaggle
"""

import sys
from kaggle.api.kaggle_api_extended import KaggleApi

def search_datasets(search_term="", page=1, max_results=20):
    """Search for datasets on Kaggle"""
    api = KaggleApi()
    api.authenticate()
    
    print(f"\n🔍 Searching Kaggle for: '{search_term}'\n")
    print("=" * 80)
    
    datasets = api.dataset_list(search=search_term, page=page)
    
    for i, ds in enumerate(datasets[:max_results], 1):
        print(f"\n{i}. 📊 {ds.ref}")
        print(f"   Title: {ds.title}")
        print(f"   URL: https://www.kaggle.com/datasets/{ds.ref}")
        if hasattr(ds, 'downloadCount'):
            print(f"   Downloads: {ds.downloadCount:,}")
        if hasattr(ds, 'voteCount'):
            print(f"   Votes: {ds.voteCount}")
        if hasattr(ds, 'lastUpdated'):
            print(f"   Updated: {ds.lastUpdated}")
    
    print("\n" + "=" * 80)
    print(f"\nShowing {min(max_results, len(datasets))} results")
    
    return datasets[:max_results]

def list_my_datasets():
    """List datasets owned by the authenticated user"""
    api = KaggleApi()
    api.authenticate()
    
    username = api.get_config_value('username')
    
    print(f"\n📊 Your Datasets (Username: {username})\n")
    print("=" * 80)
    
    datasets = api.dataset_list(user=username)
    
    if not datasets:
        print("\n  No datasets found. Upload your first dataset!")
        print(f"  Create at: https://www.kaggle.com/datasets")
    else:
        for i, ds in enumerate(datasets, 1):
            print(f"\n{i}. 📊 {ds.ref}")
            print(f"   Title: {ds.title}")
            print(f"   URL: https://www.kaggle.com/datasets/{ds.ref}")
    
    print("\n" + "=" * 80)
    print(f"\nTotal datasets: {len(datasets)}")
    
    return datasets

def get_dataset_info(dataset_ref):
    """Get detailed information about a specific dataset"""
    api = KaggleApi()
    api.authenticate()
    
    print(f"\n📊 Dataset Details: {dataset_ref}\n")
    print("=" * 80)
    
    try:
        # Get dataset metadata
        dataset = api.dataset_view(dataset_ref)
        
        print(f"\nTitle: {dataset.title}")
        print(f"URL: https://www.kaggle.com/datasets/{dataset_ref}")
        print(f"Owner: {dataset.ownerName}")
        
        if hasattr(dataset, 'description'):
            print(f"\nDescription:\n{dataset.description[:500]}...")
        
        if hasattr(dataset, 'downloadCount'):
            print(f"\nDownloads: {dataset.downloadCount:,}")
        
        if hasattr(dataset, 'voteCount'):
            print(f"Votes: {dataset.voteCount}")
        
        if hasattr(dataset, 'usabilityRating'):
            print(f"Usability: {dataset.usabilityRating}/10")
        
        # List files in the dataset
        print("\n📁 Files in this dataset:")
        files = api.dataset_list_files(dataset_ref)
        for f in files.files:
            size_mb = f.size / (1024 * 1024) if hasattr(f, 'size') else 0
            print(f"  - {f.name} ({size_mb:.2f} MB)")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"❌ Error: {e}")

def search_by_category():
    """Browse datasets by popular categories"""
    api = KaggleApi()
    api.authenticate()
    
    categories = {
        '1': ('coffee', 'Coffee & Cafe'),
        '2': ('image classification', 'Image Classification'),
        '3': ('food', 'Food & Nutrition'),
        '4': ('machine learning', 'Machine Learning'),
        '5': ('deep learning', 'Deep Learning'),
        '6': ('computer vision', 'Computer Vision'),
        '7': ('business', 'Business & Sales'),
        '8': ('restaurant', 'Restaurant Data')
    }
    
    print("\n📚 Browse by Category:\n")
    for key, (_, name) in categories.items():
        print(f"  {key}. {name}")
    
    choice = input("\nSelect category (1-8): ").strip()
    
    if choice in categories:
        search_term, name = categories[choice]
        print(f"\n🔍 Searching for: {name}")
        return search_datasets(search_term)
    else:
        print("Invalid choice")
        return []

def main():
    """Main CLI interface"""
    
    if len(sys.argv) < 2:
        print("\n🔧 Kaggle Dataset Search Tool\n")
        print("Usage:")
        print("  python kaggle_search.py <command> [options]\n")
        print("Commands:")
        print("  search <term>     - Search for datasets (e.g., 'coffee', 'food')")
        print("  my-datasets       - List your own datasets")
        print("  info <dataset>    - Get details about a dataset (e.g., username/dataset-name)")
        print("  browse            - Browse datasets by category")
        print("  trending          - Show trending datasets\n")
        print("Examples:")
        print("  python kaggle_search.py search coffee")
        print("  python kaggle_search.py my-datasets")
        print("  python kaggle_search.py info fatihb/coffee-quality-data-cqi")
        print("  python kaggle_search.py browse")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "search":
        search_term = sys.argv[2] if len(sys.argv) > 2 else ""
        search_datasets(search_term)
    
    elif command == "my-datasets":
        list_my_datasets()
    
    elif command == "info":
        if len(sys.argv) < 3:
            print("❌ Please provide dataset reference (username/dataset-name)")
            sys.exit(1)
        dataset_ref = sys.argv[2]
        get_dataset_info(dataset_ref)
    
    elif command == "browse":
        search_by_category()
    
    elif command == "trending":
        print("\n🔥 Trending Datasets:\n")
        search_datasets("", page=1, max_results=15)
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
