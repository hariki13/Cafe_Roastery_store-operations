#!/usr/bin/env python3
"""
Script to import coffee bean images from uploaded ZIP files
Usage: python upload_images.py <zip_file_path> <roast_level>
Example: python upload_images.py uploads/my_images.zip medium
"""

import sys
from image_collector import ImageCollector

def main():
    if len(sys.argv) < 3:
        print("Usage: python upload_images.py <zip_file_path> <roast_level>")
        print("\nAvailable roast levels:")
        print("  - light")
        print("  - light_medium")
        print("  - medium")
        print("  - medium_dark")
        print("  - dark")
        print("  - very_dark")
        print("\nExample:")
        print("  python upload_images.py uploads/beans.zip medium")
        sys.exit(1)
    
    zip_path = sys.argv[1]
    roast_level = sys.argv[2]
    
    collector = ImageCollector()
    
    valid_levels = ['light', 'light_medium', 'medium', 'medium_dark', 'dark', 'very_dark']
    if roast_level not in valid_levels:
        print(f"❌ Invalid roast level: {roast_level}")
        print(f"Valid levels: {', '.join(valid_levels)}")
        sys.exit(1)
    
    print(f"📦 Importing images from: {zip_path}")
    print(f"🎯 Target roast level: {roast_level}")
    collector.import_from_zip(zip_path, roast_level)
    print("✅ Done!")

if __name__ == '__main__':
    main()
