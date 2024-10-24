import os
import pandas as pd
import gdown
import paths
import argparse
from downloader import download_folder_if_not_exists, url_drive, url_metrics
from paths import drive_info, dataset_paths, inference_paths

def get_filenames_in_folder(folder_path):
    filenames = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            filenames.append(file_path)
    return filenames

def download_resources():
    download_folder_if_not_exists("drive", url_drive)
    download_folder_if_not_exists("metrics", url_metrics)

def get_swear_words(language: str):
    """
    Input : string variable mentioning language of swear words
    Output : Dataframe containing the respective swear words
    """
    swear_words_excel = paths.swear_words_excel
    df_swear = pd.read_excel(swear_words_excel)
    df_swear_language = df_swear[df_swear['language'].str.lower() == language.lower()]
    
    return df_swear_language

def get_prompts(case: int, prompt_language: str, slang_language: str):
    """
    Input : case, prompt_language, slang_language
    Output : Dataframe containing the respective prompts
    """
    prompts_case_1_directory = dataset_paths["prompts"]["case_1"]
    prompts_case_2_directory = dataset_paths["prompts"]["case_2"]
    
    if case == 1:
        file_list = get_filenames_in_folder(prompts_case_1_directory)
        for file in file_list:
            if (prompt_language.lower() in file.lower() and 
                slang_language.lower() in file.lower()):
                df_prompts = pd.read_csv(file)
                print(f"Loaded prompts from: {file}") 
                return df_prompts
        print("\n\nNo such file found!!\n\n")
        return None
    else:
        file_list = get_filenames_in_folder(prompts_case_2_directory)
        for file in file_list:
            df_prompts = pd.read_csv(file)
            df_prompts = df_prompts[df_prompts["Slang_Language"].str.lower() == slang_language.lower()]
            print(f"Loaded prompts from: {file}") 
            return df_prompts
        print("\n\nNo such file found!!\n\n")
        return None

def get_model_inferences(case, prompt_language, slang_language, model_name):
    """
    Input : case, prompt_language, slang_language & model_name
    Output : Dataframe containing the respective prompts
    """
    inference_case_1_directory = inference_paths["case_1"]
    inference_case_2_directory = inference_paths["case_2"]
    
    if case == 1:
        file_list = get_filenames_in_folder(inference_case_1_directory)
        for file in file_list:
            if (prompt_language.lower() in file.lower() and 
                slang_language.lower() in file.lower() and 
                model_name.lower() in file.lower()):
                df_model_inference = pd.read_excel(file)
                return df_model_inference
        print("\n\nNo such file found!!\n\n")
        return None
    else:
        file_list = get_filenames_in_folder(inference_case_2_directory)
        for file in file_list:
            if model_name.lower() in file.lower():
                df_model_inference = pd.read_excel(file)
                return df_model_inference
        print("\n\nNo such file found!!\n\n")
        return None

def main(args):
    download_resources()  # Call this once at the beginning
    
    swear_words_dataset = get_swear_words(args.slang_language)
    if swear_words_dataset is not None:
        print(len(swear_words_dataset))
    else:
        print("No such swear words dataset exists")
        
    prompts_dataset = get_prompts(args.case, args.prompt_language, args.slang_language)
    if prompts_dataset is not None:
        print(len(prompts_dataset))
    else:
        print("No such prompts dataset exists")
        
    model_inference_dataset = get_model_inferences(args.case, args.prompt_language, args.slang_language, args.model_id)
    if model_inference_dataset is not None:
        print(len(model_inference_dataset))
    else:
        print("No such model inference dataset exists")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--case', type=int, help='Case number', required=True)
    parser.add_argument('--prompt_language', type=str, help='Prompt language', required=False)
    parser.add_argument('--slang_language', type=str, help='Slang language', required=False)
    parser.add_argument('--model_id', type=str, help='Model ID', required=False)
    
    args = parser.parse_args()
    main(args)
