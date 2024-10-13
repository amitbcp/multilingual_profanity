import os
import paths
import gdown
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
    swear_words_excel = paths.swear_words_url_excel
    folder_id = swear_words_excel.split('/')[-1]
    
    swear_words_directory = "temporary_storage/swear_words"
    if not os.path.exists(swear_words_directory):
        os.makedirs(swear_words_directory)

    #print(paths.prefix + folder_id)
    gdown.download(paths.prefix + folder_id, output = swear_words_directory, quiet=False, use_cookies=False, fuzzy=True)
    #gdd.download_file_from_google_drive(file_id = folder_id, dest_path = swear_words_directory)
    
    file_list = get_filenames_in_folder(swear_words_directory)
    
    for i in range(len(file_list)) : 
        if language.lower() in file_list[i].lower() : 
            return swear_words_directory + file_list[i]
    else : 
        print("\n\nNo such file found!!\n\n")
        return None


## get prompt file
def get_prompts(case: int, prompt_language: str, slang_language: str, model_name: str) :  
    required_prompt_path = ""
    prompts_case_1_directory = "temporary_storage/prompts_case_1"
    prompts_case_2_directory = "temporary_storage/prompts_case_2"
    
    if case == 1: 
        required_prompt_path = paths.prompts_case_1
        folder_id = required_prompt_path.split('/')[-1]
        
        if not os.path.exists(prompts_case_1_directory):
            os.makedirs(prompts_case_1_directory)
        
        gdown.download(paths.prefix + folder_id, output = prompts_case_1_directory, quiet=False, use_cookies=False, fuzzy=True)
    
        file_list = get_filenames_in_folder(prompts_case_1_directory)
        
        for i in range(len(file_list)) : 
            if (prompt_language.lower() in file_list[i].lower() and 
                slang_language.lower() in file_list[i].lower()) :
                return prompts_case_1_directory + file_list[i]
        else : 
            print("\n\nNo such file found!!\n\n")
            return None
        
    else: 
        required_prompt_path = paths.prompts_case_2
        folder_id = required_prompt_path.split('/')[-1]
        
        if not os.path.exists(prompts_case_2_directory):
            os.makedirs(prompts_case_2_directory)
        
        gdown.download(paths.prefix + folder_id, output = prompts_case_2_directory, quiet=False, use_cookies=False, fuzzy=True)
    
        file_list = get_filenames_in_folder(prompts_case_2_directory)
        
        for i in range(len(file_list)) : 
            if (prompt_language.lower() in file_list[i].lower() and 
                slang_language.lower() in file_list[i].lower() and 
                model_name.lower() in file_list[i].lower()):
                return prompts_case_2_directory + file_list[i]
        else : 
            print("\n\nNo such file found!!\n\n")
            return None
       
 
## get model inference file
def get_model_inferences(case, prompt_language, slang_language, model_name) : 
    required_inference_path = ""
    inference_case_1_directory = "temporary_storage/inference_case_1"
    inference_case_2_directory = "temporary_storage/inference_case_2"
    
    if (case == 1) : 
        required_inference_path = paths.inference_case_1_excel
        folder_id = required_inference_path.split('/')[-1]
        
        if not os.path.exists(inference_case_1_directory):
            os.makedirs(inference_case_1_directory)
            
        gdown.download(paths.prefix + folder_id, output = inference_case_1_directory, quiet=False, use_cookies=False, fuzzy=True)
    
        file_list = get_filenames_in_folder(inference_case_1_directory)
        
        for i in range(len(file_list)) : 
            if (prompt_language.lower() in file_list[i].lower() and 
                slang_language.lower() in file_list[i].lower() and 
                model_name.lower() in file_list[i].lower()):
                return inference_case_1_directory + file_list[i]
        else : 
            print("\n\nNo such file found!!\n\n")
            return None
        
    else : 
        required_inference_path = paths.inference_case_2_excel
        folder_id = required_inference_path.split('/')[-1]
        
        if not os.path.exists(inference_case_2_directory):
            os.makedirs(inference_case_2_directory)
            
        gdown.download(paths.prefix + folder_id, output = inference_case_2_directory, quiet=False, use_cookies=False, fuzzy=True)
    
        file_list = get_filenames_in_folder(inference_case_2_directory)
        
        for i in range(len(file_list)) : 
            if (prompt_language.lower() in file_list[i].lower() and 
                slang_language.lower() in file_list[i].lower() and 
                model_name.lower() in file_list[i].lower()):
                return inference_case_2_directory + file_list[i]
        else : 
            print("\n\nNo such file found!!\n\n")
            return None


#authenticate_google_drive()
get_swear_words("bengali")