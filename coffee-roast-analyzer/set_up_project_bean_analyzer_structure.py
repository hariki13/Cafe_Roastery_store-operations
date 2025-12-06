"""
Run this script to create your project structure automatically
Save this as: setup_project. py
Then run: python setup_project.py
"""

import os
from pathlib import Path

def create_project_structure():
    """Create all necessary folders and files"""
    
    # Define project structure
    structure = {
        'data': {
            'raw': {
                'light': [],
                'light_medium': [],
                'medium': [],
                'medium_dark': [],
                'dark': [],
                'very_dark': []
            },
            'processed': [],
            'examples': []
        },
        'models': {
            'checkpoints': []
        },
        'scripts': [],
        'web_interface': {
            'templates': [],
            'static': {
                'css': [],
                'js': [],
                'images': []
            }
        },
        'api': [],
        'uploads': [],
        'logs': [],
        'notebooks': []
    }
    
    def create_dirs(base_path, structure_dict):
        """Recursively create directories"""
        for name, content in structure_dict.items():
            path = base_path / name
            path. mkdir(exist_ok=True)
            print(f"✅ Created: {path}")
            
            if isinstance(content, dict):
                create_dirs(path, content)
            elif isinstance(content, list):
                # Create . gitkeep to track empty folders
                (path / '.gitkeep').touch()
    
    # Create structure
    base_path = Path('.')
    create_dirs(base_path, structure)
    
    # Create essential files
    files_to_create = {
        'requirements.txt': '',
        'README.md': '# Coffee Bean Roast Analyzer\n\nAI-powered coffee roast classification system.',
        '. gitignore': '''
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# Model files
*.pth
*. onnx
models/checkpoints/*
!models/checkpoints/.gitkeep

# Data
data/raw/*
data/processed/*
uploads/*

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
logs/*
*.log
        '''. strip(),
        'config.py': '''
"""
Configuration file for the project
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Data directories
DATA_DIR = BASE_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'

# Model directories
MODELS_DIR = BASE_DIR / 'models'
CHECKPOINTS_DIR = MODELS_DIR / 'checkpoints'

# Upload directory
UPLOAD_DIR = BASE_DIR / 'uploads'

# Roast levels configuration
ROAST_LEVELS = {
    'light': 0,
    'light_medium': 1,
    'medium': 2,
    'medium_dark': 3,
    'dark': 4,
    'very_dark': 5
}

# Model configuration
MODEL_NAME = 'google/vit-base-patch16-224'
IMAGE_SIZE = 224
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
NUM_EPOCHS = 15

# API configuration
API_HOST = '0.0.0.0'
API_PORT = 5000
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
        '''.strip()
    }
    
    for filename, content in files_to_create.items():
        filepath = Path(filename)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✅ Created: {filepath}")
    
    print("\n" + "="*60)
    print("✅ Project structure created successfully!")
    print("="*60)
    print("\nNext steps:")
    print("1.  Activate virtual environment: venv\\Scripts\\activate (Windows)")
    print("2.  Install requirements: pip install -r requirements.txt")
    print("3. Start collecting coffee bean images!")

if __name__ == "__main__":
    create_project_structure()