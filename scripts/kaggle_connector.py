#!/usr/bin/env python3
"""
Kaggle Connector for Coffee Roastery Operations
Uploads coffee roast images and metadata to Kaggle datasets
"""

import os
import sys
import json
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi

class KaggleConnector:
    def __init__(self):
        """Initialize Kaggle API connection"""
        self.api = KaggleApi()
        try:
            self.api.authenticate()
            print("✅ Successfully connected to Kaggle!")
        except Exception as e:
            print("❌ Failed to authenticate with Kaggle")
            print(f"Error: {e}")
            print("\n📋 Setup Instructions:")
            print("1. Go to https://www.kaggle.com/settings/account")
            print("2. Scroll to 'API' section and click 'Create New Token'")
            print("3. This downloads kaggle.json")
            print("4. Place it at: ~/.kaggle/kaggle.json (Linux/Mac) or C:\\Users\\<username>\\.kaggle\\kaggle.json (Windows)")
            print("5. Run: chmod 600 ~/.kaggle/kaggle.json (Linux/Mac only)")
            sys.exit(1)
    
    def list_datasets(self, search_term=None):
        """List your Kaggle datasets"""
        try:
            if search_term:
                datasets = self.api.dataset_list(search=search_term, user=self.api.get_config_value('username'))
            else:
                datasets = self.api.dataset_list(user=self.api.get_config_value('username'))
            
            print(f"\n📊 Your Kaggle Datasets:")
            for ds in datasets:
                print(f"  - {ds.ref}")
            return datasets
        except Exception as e:
            print(f"❌ Error listing datasets: {e}")
            return []
    
    def create_dataset_metadata(self, dataset_name, title, description, data_dir):
        """Create dataset-metadata.json for Kaggle dataset"""
        metadata = {
            "title": title,
            "id": f"{self.api.get_config_value('username')}/{dataset_name}",
            "licenses": [{"name": "CC0-1.0"}],
            "keywords": ["coffee", "roastery", "image-classification", "deep-learning"],
            "description": description
        }
        
        metadata_path = Path(data_dir) / "dataset-metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Created metadata file: {metadata_path}")
        return metadata_path
    
    def upload_dataset(self, data_dir, dataset_name, title, description, is_new=True):
        """
        Upload or update a dataset to Kaggle
        
        Args:
            data_dir: Directory containing the data files
            dataset_name: Kaggle dataset slug (e.g., 'coffee-roast-images')
            title: Dataset title
            description: Dataset description
            is_new: True for new dataset, False to update existing
        """
        data_path = Path(data_dir)
        
        if not data_path.exists():
            print(f"❌ Data directory not found: {data_dir}")
            return False
        
        # Create metadata
        self.create_dataset_metadata(dataset_name, title, description, data_dir)
        
        try:
            if is_new:
                print(f"\n📤 Creating new dataset: {dataset_name}")
                self.api.dataset_create_new(
                    folder=str(data_path),
                    dir_mode='tar',
                    convert_to_csv=False,
                    public=True
                )
                print(f"✅ Dataset created successfully!")
                print(f"🔗 View at: https://www.kaggle.com/datasets/{self.api.get_config_value('username')}/{dataset_name}")
            else:
                print(f"\n📤 Updating dataset: {dataset_name}")
                self.api.dataset_create_version(
                    folder=str(data_path),
                    version_notes="Updated with new images",
                    dir_mode='tar',
                    convert_to_csv=False
                )
                print(f"✅ Dataset updated successfully!")
            
            return True
        
        except Exception as e:
            print(f"❌ Error uploading dataset: {e}")
            return False
    
    def download_dataset(self, dataset_ref, download_path='data/kaggle'):
        """
        Download a dataset from Kaggle
        
        Args:
            dataset_ref: Dataset reference (username/dataset-name)
            download_path: Where to download the dataset
        """
        download_dir = Path(download_path)
        download_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            print(f"\n⬇️  Downloading dataset: {dataset_ref}")
            self.api.dataset_download_files(
                dataset=dataset_ref,
                path=str(download_dir),
                unzip=True
            )
            print(f"✅ Dataset downloaded to: {download_dir}")
            return True
        except Exception as e:
            print(f"❌ Error downloading dataset: {e}")
            return False
    
    def upload_coffee_roast_data(self, is_new=True):
        """Upload the coffee roast dataset with all roast levels"""
        dataset_name = "coffee-roast-images"
        title = "Coffee Bean Roast Level Classification Dataset"
        description = """
# Coffee Bean Roast Level Classification Dataset

This dataset contains images of coffee beans at different roast levels for machine learning classification tasks.

## Roast Levels
- Light
- Light-Medium  
- Medium
- Medium-Dark
- Dark
- Very Dark

## Dataset Structure
Each roast level has its own directory with timestamped images.

## Use Cases
- Image classification
- Computer vision
- Deep learning model training
- Coffee roast analysis

## Source
Collected from cafe roastery operations.
        """.strip()
        
        data_dir = "data/raw"
        
        return self.upload_dataset(data_dir, dataset_name, title, description, is_new)


def main():
    """Main function with CLI interface"""
    if len(sys.argv) < 2:
        print("🔧 Kaggle Connector - Usage:")
        print("\n  python kaggle_connector.py <command> [options]")
        print("\nCommands:")
        print("  test              - Test Kaggle connection")
        print("  list              - List your datasets")
        print("  upload-new        - Upload coffee roast data as NEW dataset")
        print("  upload-update     - Update existing coffee roast dataset")
        print("  download <ref>    - Download a dataset (e.g., username/dataset-name)")
        print("\nExamples:")
        print("  python kaggle_connector.py test")
        print("  python kaggle_connector.py upload-new")
        print("  python kaggle_connector.py download username/coffee-dataset")
        sys.exit(1)
    
    command = sys.argv[1]
    connector = KaggleConnector()
    
    if command == "test":
        print("✅ Kaggle connection successful!")
        print(f"👤 Username: {connector.api.get_config_value('username')}")
    
    elif command == "list":
        connector.list_datasets()
    
    elif command == "upload-new":
        connector.upload_coffee_roast_data(is_new=True)
    
    elif command == "upload-update":
        connector.upload_coffee_roast_data(is_new=False)
    
    elif command == "download":
        if len(sys.argv) < 3:
            print("❌ Please provide dataset reference: username/dataset-name")
            sys.exit(1)
        dataset_ref = sys.argv[2]
        connector.download_dataset(dataset_ref)
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
