from kaggle.api.kaggle_api_extended import KaggleApi
import os

# Initialize API
api = KaggleApi()
api.authenticate()

# Create folder
download_path = './kaggle_coffee_data_set'
if not os.path.exists(download_path):
    os.makedirs(download_path)

# Dataset list
datasets = [
    'alejandromendozaarv/roast-coffee-shop-2023-financials',  # #20
    'wardabilal/exploring-coffee-sales-with-eda-and-visualization',  # #12
    'viramatv/coffee-shop-data',  # #13
    'mannarmohamedsayed/coffee-shop-analysis'  # #17
]

# Download datasets
for idx, dataset_ref in enumerate(datasets, 1):
    print(f"\n[{idx}/4] Downloading: {dataset_ref}")
    try:
        api.dataset_download_files(dataset_ref, path=download_path, unzip=True)
        print(f"✓ Successfully downloaded: {dataset_ref}")
    except Exception as e:
        print(f"✗ Error: {e}")

print("\n✓ All downloads completed!")
