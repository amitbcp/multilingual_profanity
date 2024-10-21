import os
import gdown
import paths

url_drive = f"https://drive.google.com/drive/folders/{paths.drive_id}"
url_metrics = f"https://drive.google.com/drive/folders/{paths.metrics_id}"

if not os.path.exists("metrics") : 
        print("\n Downloading metrics folder... \n")
        gdown.download_folder(url_metrics, quiet=True, use_cookies=False)
        print("\n metrics folder downloaded!! \n")

if not os.path.exists("drive") : 
        print("\n Downloading drive folder... \n")
        gdown.download_folder(url_drive, quiet=False, use_cookies=False)
        print("\n drive folder downloaded!! \n")