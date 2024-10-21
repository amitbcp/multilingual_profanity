import os
import paths
import gdown
import pandas as pd
from load_dataset import get_swear_words, get_prompts

url_drive = f"https://drive.google.com/drive/folders/{paths.drive_id}"
url_metrics = f"https://drive.google.com/drive/folders/{paths.metrics_id}"

def get_dataset_length_case_1(language) : 
    """
    Input : language of prompts and slang words to get the dataset length dynamically
    Output : length of the dataset (robust to any modifications)
    """
    
    if not os.path.exists("drive") : 
        print("\n Downloading drive folder... \n")
        gdown.download_folder(url_drive, quiet=True, use_cookies=False)
        print("\n drive folder downloaded!! \n")
    if not os.path.exists("metrics") : 
        print("\n Downloading metrics folder... \n")
        gdown.download_folder(url_metrics, quiet=True, use_cookies=False)
        print("\n metrics folder downloaded!! \n")
    
    dataset_path = get_prompts(1, language, language) # model_id doesn't matter, as dataset length would be same for all
    dataset = pd.read_csv(dataset_path)
    return len(dataset)


def get_dataset_length_case_2(language) : 
    """
    Input : language of slang words to get the dataset length dynamically (prompts are always in english)
    Output : length of the dataset (robust to any modifications)
    """
    
    if not os.path.exists("drive") : 
        print("\n Downloading drive folder... \n")
        gdown.download_folder(url_drive, quiet=True, use_cookies=False)
        print("\n drive folder downloaded!! \n")
    if not os.path.exists("metrics") : 
        print("\n Downloading metrics folder... \n")
        gdown.download_folder(url_metrics, quiet=True, use_cookies=False)
        print("\n metrics folder downloaded!! \n")
    
    dataset_path = get_prompts(2, language, language) # model_id doesn't matter, as dataset length would be same for all
    dataset = pd.read_csv(dataset_path)
    return len(dataset)
    
    