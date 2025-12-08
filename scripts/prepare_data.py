"""
Prepare and split dataset for training
Save this in scripts/prepare_data.py
Run: python scripts/prepare_data. py
"""

import os
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split
from PIL import Image
import json
from tqdm import tqdm

class CoffeeDatasetPreparer:
    def __init__(self, raw_data_dir='data/raw', output_dir='data/processed', 
                 val_split=0.2, test_split=0.1):
        self.raw_data_dir = Path(raw_data_dir)
        self.output_dir = Path(output_dir)
        self.val_split = val_split
        self. test_split = test_split
        
        self.roast_levels = {
            'light': 0,
            'light_medium': 1,
            'medium': 2,
            'medium_dark': 3,
            'dark': 4,
            'very_dark': 5
        }
    
    def validate_images(self):
        """Check and validate all images"""
        print("\n🔍 Validating images...")
        valid_images = []
        invalid_images = []
        
        for roast_level in self.roast_levels.keys():
            roast_dir = self.raw_data_dir / roast_level
            if not roast_dir.exists():
                print(f"⚠️  Directory not found: {roast_dir}")
                continue
            
            image_files = list(roast_dir.glob('*.*'))
            print(f"\n📁 Checking {roast_level}: {len(image_files)} files")
            
            for img_path in tqdm(image_files, desc=f"Validating {roast_level}"):
                if img_path.suffix.lower() in ['.jpg', '.jpeg', '. png', '.bmp']:
                    try:
                        img = Image.open(img_path)
                        img.verify()
                        valid_images.append((img_path, roast_level))
                    except Exception as e:
                        invalid_images.append((img_path, str(e)))
                        print(f"❌ Invalid: {img_path. name}")
        
        print(f"\n✅ Valid images: {len(valid_images)}")
        print(f"❌ Invalid images: {len(invalid_images)}")
        
        return valid_images, invalid_images
    
    def prepare_splits(self, valid_images):
        """Split data into train, validation, and test sets"""
        print("\n✂️  Splitting dataset...")
        
        images_by_level = {}
        for img_path, roast_level in valid_images:
            if roast_level not in images_by_level:
                images_by_level[roast_level] = []
            images_by_level[roast_level]. append(img_path)
        
        train_images = []
        val_images = []
        test_images = []
        
        for roast_level, images in images_by_level.items():
            if len(images) < 10:
                print(f"⚠️  Warning: Only {len(images)} images for {roast_level}")
            
            # Split: train/val/test
            train_val, test = train_test_split(
                images, test_size=self.test_split, random_state=42
            )
            train, val = train_test_split(
                train_val, 
                test_size=self. val_split / (1 - self.test_split),
                random_state=42
            )
            
            train_images.extend([(img, roast_level) for img in train])
            val_images.extend([(img, roast_level) for img in val])
            test_images.extend([(img, roast_level) for img in test])
            
            print(f"  {roast_level:15s}: {len(train):3d} train, {len(val):3d} val, {len(test):3d} test")
        
        print(f"\n📊 Total Split:")
        print(f"  Train:      {len(train_images)}")
        print(f"  Validation: {len(val_images)}")
        print(f"  Test:       {len(test_images)}")
        
        return train_images, val_images, test_images
    
    def copy_images(self, images, split_name):
        """Copy images to split directory"""
        split_dir = self.output_dir / split_name
        split_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📋 Processing {split_name} set...")
        
        metadata = []
        for idx, (img_path, roast_level) in enumerate(tqdm(images, desc=f"Copying {split_name}")):
            new_filename = f"{roast_level}_{idx:04d}{img_path.suffix}"
            new_path = split_dir / new_filename
            
            # Resize and save
            img = Image.open(img_path). convert('RGB')
            
            # Resize if too large
            max_size = 800
            if max(img.size) > max_size:
                img. thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            img.save(new_path, quality=95)
            
            metadata.append({
                'file_name': new_filename,
                'roast_level': roast_level,
                'label': self.roast_levels[roast_level],
                'original_path': str(img_path)
            })
        
        # Save metadata
        with open(split_dir / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Saved {len(images)} images to {split_dir}")
    
    def create_label_mapping(self):
        """Create label mapping file"""
        mapping = {
            'id2label': {v: k for k, v in self.roast_levels.items()},
            'label2id': self.roast_levels,
            'num_labels': len(self.roast_levels)
        }
        
        with open(self.output_dir / 'label_mapping. json', 'w') as f:
            json.dump(mapping, f, indent=2)
        
        print(f"✅ Label mapping saved")
    
    def prepare(self):
        """Run complete preparation pipeline"""
        print("="*60)
        print("COFFEE DATASET PREPARATION")
        print("="*60)
        
        valid_images, invalid_images = self.validate_images()
        
        if len(valid_images) < 50:
            print("\n❌ Not enough images!  Need at least 50 total.")
            print("Please collect more images first.")
            return False
        
        train, val, test = self.prepare_splits(valid_images)
        
        self.copy_images(train, 'train')
        self.copy_images(val, 'val')
        self.copy_images(test, 'test')
        
        self.create_label_mapping()
        
        print("\n" + "="*60)
        print("✅ DATA PREPARATION COMPLETE!")
        print("="*60)
        print(f"\nOutput directory: {self.output_dir}")
        print("\nNext step: python scripts/train_model.py")
        
        return True

if __name__ == "__main__":
    preparer = CoffeeDatasetPreparer()
    preparer.prepare()