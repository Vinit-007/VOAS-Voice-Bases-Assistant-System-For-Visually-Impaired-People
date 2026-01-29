#!/usr/bin/env python3
"""
VisionAssist Pro Setup Script
Automatically downloads required YOLOv3 model files and sets up the environment
"""

import os
import sys
import urllib.request
import subprocess
from pathlib import Path

def download_file(url, filename, description):
    """Download a file with progress indication"""
    print(f"Downloading {description}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"✓ Successfully downloaded {description}")
        return True
    except Exception as e:
        print(f"✗ Error downloading {description}: {e}")
        return False

def check_file_exists(filename, description):
    """Check if a file exists"""
    if os.path.exists(filename):
        print(f"✓ {description} already exists")
        return True
    return False

def install_requirements():
    """Install Python requirements"""
    print("Installing Python requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False

def setup_environment():
    """Set up environment file"""
    env_file = ".env"
    env_example = ".env.example"
    
    if not os.path.exists(env_file) and os.path.exists(env_example):
        print("Creating .env file from template...")
        try:
            import secrets
            secret_key = secrets.token_hex(24)
            
            with open(env_example, 'r') as f:
                content = f.read()
            
            content = content.replace('your_secure_secret_key_here', secret_key)
            
            with open(env_file, 'w') as f:
                f.write(content)
            
            print("✓ Environment file created with secure secret key")
            return True
        except Exception as e:
            print(f"✗ Error creating environment file: {e}")
            return False
    elif os.path.exists(env_file):
        print("✓ Environment file already exists")
        return True
    else:
        print("✗ Environment template file not found")
        return False

def main():
    """Main setup function"""
    print("🚀 VisionAssist Pro Setup")
    print("=" * 40)
    
    # File URLs and descriptions
    files_to_download = [
        {
            "url": "https://pjreddie.com/media/files/yolov3.weights",
            "filename": "yolov3.weights",
            "description": "YOLOv3 weights (248MB)"
        },
        {
            "url": "https://github.com/pjreddie/darknet/raw/master/cfg/yolov3.cfg",
            "filename": "yolov3.cfg", 
            "description": "YOLOv3 configuration"
        },
        {
            "url": "https://github.com/pjreddie/darknet/raw/master/data/coco.names",
            "filename": "coco.names",
            "description": "COCO class names"
        }
    ]
    
    success_count = 0
    total_steps = len(files_to_download) + 2  # +2 for requirements and env setup
    
    # Step 1: Install requirements
    if install_requirements():
        success_count += 1
    
    # Step 2: Setup environment
    if setup_environment():
        success_count += 1
    
    # Step 3: Download model files
    for file_info in files_to_download:
        if not check_file_exists(file_info["filename"], file_info["description"]):
            if download_file(file_info["url"], file_info["filename"], file_info["description"]):
                success_count += 1
        else:
            success_count += 1
    
    print("\n" + "=" * 40)
    print(f"Setup Complete: {success_count}/{total_steps} steps successful")
    
    if success_count == total_steps:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Run: python app.py")
        print("2. Open: http://localhost:5000")
        print("3. Register as admin or user")
    else:
        print("⚠️  Setup completed with some issues. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
