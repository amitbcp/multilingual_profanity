import os
import pandas as pd
import paths
import gdown
import argparse
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import google.auth
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
from google_drive_downloader import GoogleDriveDownloader as gdd


def get_filenames_in_folder(folder_path):
    filenames = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            filenames.append(file_path)
    return filenames


## get swear words file
def get_swear_words(language: str) : 
    """
    Input : string variable mentioning language of swear words
    Output : Dataframe containing the respective swear words
    """
    swear_words_excel = paths.swear_words_excel
    
    df_swear = pd.read_excel(swear_words_excel)
    
    df_swear_language = df_swear[df_swear['language'].str.lower() == language.lower()]
    
    return df_swear_language


## get prompt file
def get_prompts(case: int, prompt_language: str, slang_language: str) :  
    """
    Input : case, prompt_language, slang_language
    Output : Dataframe containing the respective prompts
    """
    required_prompt_path = ""
    prompts_case_1_directory = paths.prompts_case_1
    prompts_case_2_directory = paths.prompts_case_2
    
    if case == 1: 
    
        file_list = get_filenames_in_folder(prompts_case_1_directory)
        
        for i in range(len(file_list)) : 
            if (prompt_language.lower() in file_list[i].lower() and slang_language.lower() in file_list[i].lower()) :
                df_prompts = pd.read_csv(file_list[i])
                return df_prompts
        else : 
            print("\n\nNo such file found!!\n\n")
            return None
        
    else: 
    
        file_list = get_filenames_in_folder(prompts_case_2_directory)
        
        for i in range(len(file_list)) : 
            df_prompts = pd.read_csv(file_list[i])
            df_prompts = df_prompts[df_prompts["Slang_Language"].str.lower() == slang_language.lower()]
            return df_prompts
        else : 
            print("\n\nNo such file found!!\n\n")
            return None
       
 
## get model inference file
def get_model_inferences(case, prompt_language, slang_language, model_name) : 
    """
    Input : case, prompt_language, slang_language & model_name
    Output : Dataframe containing the respective prompts
    """
    inference_case_1_directory = paths.inference_case_1_excel
    inference_case_2_directory = paths.inference_case_2_excel
    
    if (case == 1) : 
    
        file_list = get_filenames_in_folder(inference_case_1_directory)
        #print(len(file_list))
        for i in range(len(file_list)) : 
            if (prompt_language.lower() in file_list[i].lower() and 
                slang_language.lower() in file_list[i].lower() and 
                model_name.lower() in file_list[i].lower()):
                df_model_inference = pd.read_excel(file_list[i])
                return df_model_inference
        else : 
            print("\n\nNo such file found!!\n\n")
            return None
        
    else : 
    
        file_list = get_filenames_in_folder(inference_case_2_directory)
        #print(len(file_list))
        for i in range(len(file_list)) : 
            df_model_inference = pd.read_excel(file_list[i])
            #df_model_inference = df_model_inference[df_model_inference["Slang_Language"].str.lower() == slang_language.lower()]
            return df_model_inference
        else : 
            print("\n\nNo such file found!!\n\n")
            return None


## this can be used to verify if such a dataset exists
def main(args) : 
    swear_words_dataset = get_swear_words(args.slang_language)
    if swear_words_dataset is not None : 
        print(len(swear_words_dataset))
    else : 
        print("No such swear words dataset exists")
        
    prompts_dataset = get_prompts(args.case, args.prompt_language, args.slang_language)
    if prompts_dataset is not None : 
        print(len(prompts_dataset))
    else :
        print("No such prompts dataset exists")
        
    model_inference_dataset = get_model_inferences(args.case, args.prompt_language, args.slang_language, args.model_id)
    if model_inference_dataset is not None : 
        print(len(model_inference_dataset))
    else :
        print("No such model inference dataset exists")
    

if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--case', type=int, help='Case number', required=True)
    parser.add_argument('--prompt_language', type=str, help='Prompt language', required=False)
    parser.add_argument('--slang_language', type=str, help='Slang language', required=False)
    parser.add_argument('--model_id', type=str, help='Model ID', required=False)
    
    args = parser.parse_args()
    main(args)