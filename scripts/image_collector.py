import os
import shutil
from pathlib import Path
from PIL import Image
import zipfile
from datetime import datetime

class ImageCollector:
    def __init__(self, output_dir='data/raw'):
        self.output_dir = Path(output_dir)
        self.roast_levels = [
            'light',
            'light_medium',
            'medium',
            'medium_dark',
            'dark',
            'very_dark'
        ]
        
        # Create directories
        for level in self.roast_levels:
            (self.output_dir / level).mkdir(parents=True, exist_ok=True)
    
    def show_guide(self):
        """Show photography guide"""
        guide_image_path = 'data/guide/photography_guide.jpg'
        if os.path.exists(guide_image_path):
            img = Image.open(guide_image_path)
            img.show()
        else:
            print("Guide image not found.")
    
    def import_from_zip(self, zip_path, roast_level):
        """Import images from a ZIP file"""
        zip_path = Path(zip_path)
        
        if not zip_path.exists():
            print(f"❌ ZIP file not found: {zip_path}")
            return
        
        if not zip_path.suffix.lower() == '.zip':
            print(f"❌ File is not a ZIP file: {zip_path}")
            return
        
        # Valid image extensions
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
        
        imported = 0
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Extract to temporary directory
                temp_dir = Path('temp_extract')
                temp_dir.mkdir(exist_ok=True)
                
                print(f"📦 Extracting ZIP file...")
                zip_ref.extractall(temp_dir)
                
                # Import all images from extracted folder
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = Path(root) / file
                        if file_path.suffix.lower() in valid_extensions:
                            try:
                                # Verify it's a valid image
                                img = Image.open(file_path)
                                img.verify()
                                
                                # Copy to destination
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                new_name = f"{roast_level}_{timestamp}_{imported:04d}_{file}"
                                dest_path = self.output_dir / roast_level / new_name
                                
                                # Reopen image (verify() closes it)
                                img = Image.open(file_path)
                                img.save(dest_path)
                                
                                imported += 1
                                print(f"✅ Imported: {file}")
                            
                            except Exception as e:
                                print(f"❌ Failed to import {file}: {e}")
                
                # Clean up temp directory
                shutil.rmtree(temp_dir)
                
        except Exception as e:
            print(f"❌ Failed to extract ZIP file: {e}")
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
            return
        
        print(f"\n✅ Imported {imported} images to {roast_level}")
    
    def import_from_folder(self, source_folder, roast_level):
        """Import images from a folder"""
        source_path = Path(source_folder)
        
        if not source_path.exists():
            print(f"❌ Folder not found: {source_folder}")
            return
        
        # Valid image extensions
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
        
        imported = 0
        for img_file in source_path.iterdir():
            if img_file.suffix.lower() in valid_extensions:
                try:
                    # Verify it's a valid image
                    img = Image.open(img_file)
                    img.verify()
                    
                    # Copy to destination
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    new_name = f"{roast_level}_{timestamp}_{img_file.name}"
                    dest_path = self.output_dir / roast_level / new_name
                    
                    shutil.copy2(img_file, dest_path)
                    imported += 1
                    print(f"✅ Imported: {img_file.name}")
                
                except Exception as e:
                    print(f"❌ Failed to import {img_file.name}: {e}")
        
        print(f"\n✅ Imported {imported} images to {roast_level}")
    
    def show_statistics(self):
        """Show collection statistics"""
        print("\n" + "="*60)
        print("COLLECTION STATISTICS")
        print("="*60)
        
        total = 0
        for level in self.roast_levels:
            folder = self.output_dir / level
            count = len(list(folder.glob('*.*')))
            total += count
            
            status = "✅" if count >= 50 else "⚠️" if count >= 20 else "❌"
            print(f"{status} {level:15s}: {count:3d} images")
        
        print("-"*60)
        print(f"{'TOTAL':15s}: {total:3d} images")
        print("="*60)
        
        if total >= 300:
            print("✅ Great! You have enough data to start training")
        elif total >= 150:
            print("⚠️ You can start training, but more data would be better")
        else:
            print("❌ Need more images. Aim for at least 300 total")
    
    def interactive_menu(self):
        """Interactive collection menu"""
        while True:
            print("\n" + "="*60)
            print("IMAGE COLLECTION MENU")
            print("="*60)
            print("1. 📁 Import from folder")
            print("2. 📦 Import from ZIP file")
            print("3. 📊 Show statistics")
            print("4. 📖 Show guide")
            print("5. ✅ Done - proceed to next step")
            print("0. ❌ Exit")
            print("="*60)
            
            choice = input("\nEnter choice: ").strip()
            
            if choice == '1':
                print("\nRoast Levels:")
                for i, level in enumerate(self.roast_levels, 1):
                    print(f"{i}. {level}")
                
                level_choice = input("\nSelect roast level (1-6): ").strip()
                folder_path = input("Enter folder path with images: ").strip()
                
                try:
                    idx = int(level_choice) - 1
                    if 0 <= idx < len(self.roast_levels):
                        self.import_from_folder(folder_path, self.roast_levels[idx])
                    else:
                        print("❌ Invalid choice")
                except ValueError:
                    print("❌ Invalid input")
            
            elif choice == '2':
                print("\nRoast Levels:")
                for i, level in enumerate(self.roast_levels, 1):
                    print(f"{i}. {level}")
                
                level_choice = input("\nSelect roast level (1-6): ").strip()
                zip_path = input("Enter path to ZIP file: ").strip()
                
                try:
                    idx = int(level_choice) - 1
                    if 0 <= idx < len(self.roast_levels):
                        self.import_from_zip(zip_path, self.roast_levels[idx])
                    else:
                        print("❌ Invalid choice")
                except ValueError:
                    print("❌ Invalid input")
            
            elif choice == '3':
                self.show_statistics()
            
            elif choice == '4':
                self.show_guide()
            
            elif choice == '5':
                self.show_statistics()
                confirm = input("\nProceed to data preparation? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    print("\n✅ Great! Run: python scripts/prepare_data.py")
                    break
            
            elif choice == '0':
                print("👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid choice")

if __name__ == "__main__":
    collector = ImageCollector()
    collector.interactive_menu()
