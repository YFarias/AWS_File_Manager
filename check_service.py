import sys
import os

# Add src to path
sys.path.append(os.getcwd())

try:
    from src.application.media_service import MediaService
    print(f"Methods of MediaService: {dir(MediaService)}")
    if hasattr(MediaService, "upload_web_files"):
        print("SUCCESS: upload_web_files found")
    else:
        print("ERROR: upload_web_files NOT found")
except Exception as e:
    print(f"IMPORT ERROR: {e}")
