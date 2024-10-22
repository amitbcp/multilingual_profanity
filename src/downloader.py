import os
import gdown
import zipfile
from paths import drive_info, dataset_paths, inference_paths

# Define URLs for external use
url_drive = f"https://drive.google.com/drive/folders/{drive_info['drive_id']}"
url_metrics = f"https://drive.google.com/drive/folders/{drive_info['metrics_id']}"

def download_folder_if_not_exists(folder_name, url):
    if os.path.exists(folder_name):
        print(f"\n{folder_name} folder already exists, skipping download.\n")
    else:
        print(f"\nDownloading {folder_name} folder...\n")
        gdown.download_folder(url, quiet=False, use_cookies=False)
        print(f"\n{folder_name} folder downloaded!!\n")

        # Unzip the downloaded file if it's the "drive" folder
        if folder_name == 'drive':
            zip_file_name = [f for f in os.listdir(folder_name) if f.endswith('.zip')]
            if zip_file_name:
                zip_file_path = os.path.join(folder_name, zip_file_name[0])
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(folder_name)
                print(f"\n{zip_file_name[0]} extracted to {folder_name}.\n")
                # Optionally, remove the zip file after extraction
                os.remove(zip_file_path)
                print(f"\n{zip_file_name[0]} removed after extraction.\n")

def main():
    # Download folders
    download_folder_if_not_exists('drive', url_drive)
    download_folder_if_not_exists('metrics', url_metrics)

if __name__ == "__main__":
    main()



