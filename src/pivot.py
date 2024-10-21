### this script is used to do all kinds of tasks.
### it can be used to call any functions

import os
import pandas as pd
import paths
import openpyxl
from load_dataset import get_swear_words, get_prompts, get_model_inferences
#from infer_model import get_model_inference, prepare_HF_model, infer_model
from calculate_metrics import evaluation_script_case_1, evaluation_script_case_2, get_details_case_1, get_details_case_2, get_details_by_categories_case_1, get_details_by_categories_case_2, calculate_percentage_case_1, calculate_percentage_case_2

languages = ["english", "spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]
languages_case_2 = ["spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]
indices = {"english": 0, "spanish": 1, "french": 2, "german": 3, "hindi": 4, "marathi": 5, "bengali": 6, "gujarati": 7}
columns_case_1 = ["model_name", "english", "spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]
columns_case_2 = ["model_name", "spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]
models = [
    "llama3_1_70b_instruct",
    "llama3_1_8b_instruct",
    "llama3_2_1b_instruct",
    "llama3_2_3b_instruct",
    "llama3_8b_instruct",
    "llama3_70b_instruct",
    "mistral_7b_instruct_v1",
    "mistral_7b_instruct_v2",    
    "mistral_7b_instruct_v3",
    "mixtral_8x22b_instruct_v01",
    "mixtral_8x7b_instruct_v01",
    "phi_3_5_moe_instruct",
    "phi_3_small_8k_instruct",
    "qwen_2_5_7b_instruct",
    "qwen_2_5_14b_instruct"
]

"""def get_filenames_in_folder(folder_path):
    filenames = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            filenames.append(file)
    return filenames"""


"""def evaluate_case_1(df, model_id) : 
    metrics = []
    metrics_percentage = []
    metrics.append(model_id)
    metrics_percentage.append(model_id)
    
    metric = evaluation_script_case_1(df)
    metrics.append(metric)
    
    metrics_file_path = "metrics/case_1.xlsx"
    if os.path.exists(metrics_file_path):
        existing_metrics_df = pd.read_excel(metrics_file_path)
        new_metrics_df = pd.DataFrame([metrics], columns = columns_case_1)
        updated_metrics_df = pd.concat([existing_metrics_df, new_metrics_df], ignore_index=True)
    else:
        updated_metrics_df = pd.DataFrame([metrics], columns = columns_case_1)
        
    updated_metrics_df.to_excel(metrics_file_path, index=False)

    metrics_percentage.append(calculate_percentage_case_1(metrics))
    percentage_metrics_file_path = "metrics/percentage_case_2.xlsx"
    if os.path.exists(percentage_metrics_file_path):
        existing_metrics_df = pd.read_excel(percentage_metrics_file_path)
        new_metrics_df = pd.DataFrame([metrics], columns = columns_case_1)
        updated_metrics_df = pd.concat([existing_metrics_df, new_metrics_df])
    else:
        updated_metrics_df = pd.DataFrame([metrics], columns = columns_case_1)
        
    updated_metrics_df.to_excel(percentage_metrics_file_path, index=False)
    

def evaluate_case_2(df, model_id) : 
    
    metrics = []
    metrics_percentage = []
    metrics.append(model_id)
    metrics_percentage.append(model_id)
    
    metrics.append(evaluation_script_case_2(df)) 
        
    metrics_file_path = "metrics/case_2.xlsx"
    if os.path.exists(metrics_file_path):
        existing_metrics_df = pd.read_excel(metrics_file_path)
        new_metrics_df = pd.DataFrame([metrics], columns = columns_case_2)
        updated_metrics_df = pd.concat([existing_metrics_df, new_metrics_df])
    else:
        updated_metrics_df = pd.DataFrame([metrics], columns = columns_case_2)
            
    updated_metrics_df.to_excel(metrics_file_path, index=False)
        
    metrics_percentage.append(calculate_percentage_case_2(metrics))
    percentage_metrics_file_path = "metrics/percentage_case_2.xlsx"
    if os.path.exists(percentage_metrics_file_path):
        existing_metrics_df = pd.read_excel(percentage_metrics_file_path)
        new_metrics_df = pd.DataFrame([metrics], columns = columns_case_2)
        updated_metrics_df = pd.concat([existing_metrics_df, new_metrics_df])
    else:
        updated_metrics_df = pd.DataFrame([metrics], columns = columns_case_2)"""


"""## case 1
folder_path = "drive/model_inference/case_1"
print("\nDumping case 1 metrics...\n")
for file in get_filenames_in_folder(folder_path) : 
    for language in languages : 
    print(file)
    path = folder_path + "/" + file
    df = pd.read_excel(path, engine='openpyxl')
    model_id = file.split('_')[4] ## to extract model_id from file_name
    evaluate_case_1(df, model_id)
    print(f"\nDumped metrics for {file}")
print("\nCase 1 metrics dumped!!\n")
    
    
## case 2
folder_path = "drive/model_inference/case_2"
print("\nDumping case 2 metrics...\n")
for file in get_filenames_in_folder(folder_path) : 
    print(file)
    path = folder_path + "/" + file
    df = pd.read_excel(path, engine='openpyxl')
    model_id = file.split('_')[2]
    evaluate_case_2(df, model_id)
    print(f"\nDumped metrics for {file}")
print("\nCase 1 metrics dumped!!\n")"""


def calculate_metrics(case) : 
    
    
    if (case == 1) : 
        for model_id in models : 
            print(f"\nDumping metrics for {model_id}\n")
            metrics = []
            metrics_percentage = []
            metrics.append(model_id)
            metrics_percentage.append(model_id)
            
            for language in languages : 
                print(f"\nDumping metrics for {model_id} -> {language}\n")
                dataset = get_model_inferences(case, language, language, model_id) ## because prompt_lang & slang_lang is same for case_1
                
                metric = evaluation_script_case_1(dataset) ## returns count for each language, so we append it to the list, metrics
                metrics.append(metric)
                
                print(f"\nCalculated metrics for {model_id} -> {language}!!\n")
            
            print(metrics)
            
            ## updating the metrics to destination file
            metrics_file_path = "metrics/case_1.xlsx"
            if os.path.exists(metrics_file_path):
                existing_metrics_df = pd.read_excel(metrics_file_path)
                new_metrics_df = pd.DataFrame([metrics], columns = columns_case_1)
                updated_metrics_df = pd.concat([existing_metrics_df, new_metrics_df], ignore_index=True)
            else:
                updated_metrics_df = pd.DataFrame([metrics], columns = columns_case_1)
            
            # Save the updated metrics to the file
            updated_metrics_df.to_excel(metrics_file_path, index=False)
            
            ## percentage
            metrics_percentage.append(calculate_percentage_case_1(metrics))
            percentage_metrics_file_path = "metrics/percentage_case_2.xlsx"
            if os.path.exists(percentage_metrics_file_path):
                existing_metrics_df = pd.read_excel(percentage_metrics_file_path)
                new_metrics_df = pd.DataFrame([metrics], columns = columns_case_1)
                updated_metrics_df = pd.concat([existing_metrics_df, new_metrics_df])
            else:
                updated_metrics_df = pd.DataFrame([metrics], columns = columns_case_1)
                
            updated_metrics_df.to_excel(percentage_metrics_file_path, index=False)
            
            print(f"\nDumped metrics for {model_id}!!")
    else :
        
        for model_id in models : 
            print(f"\nDumping metrics for {model_id}\n")
            metrics = []
            metrics_percentage = []
            metrics.append(model_id)
            metrics_percentage.append(model_id)
            
            dataset = get_model_inferences(case, "english", "english", model_id) ## languages don't matter, dataset wrt the model_id will be returned
            
            metrics.append(evaluation_script_case_2(dataset)) ## case 2 evaluation script returns a list containing counts for each language
            
            metrics_file_path = "metrics/case_2.xlsx"
            if os.path.exists(metrics_file_path):
                existing_metrics_df = pd.read_excel(metrics_file_path)
                new_metrics_df = pd.DataFrame([metrics], columns = columns_case_2)
                updated_metrics_df = pd.concat([existing_metrics_df, new_metrics_df])
            else:
                updated_metrics_df = pd.DataFrame([metrics], columns = columns_case_2)
                
            updated_metrics_df.to_excel(metrics_file_path, index=False)
            
            ## percentage
            metrics_percentage.append(calculate_percentage_case_2(metrics))
            percentage_metrics_file_path = "metrics/percentage_case_2.xlsx"
            if os.path.exists(percentage_metrics_file_path):
                existing_metrics_df = pd.read_excel(percentage_metrics_file_path)
                new_metrics_df = pd.DataFrame([metrics], columns = columns_case_2)
                updated_metrics_df = pd.concat([existing_metrics_df, new_metrics_df])
            else:
                updated_metrics_df = pd.DataFrame([metrics], columns = columns_case_2)
                
            updated_metrics_df.to_excel(percentage_metrics_file_path, index=False)
            
            print(f"\nDumped metrics for {model_id}!!")

## case 1
print("Dumping metrics for case 1...\n")
calculate_metrics(1)
print("\nDumped metrics for case 1!!\n")

## case 2
print("Dumping metrics for case 2...\n")
calculate_metrics(2)
print("\nDumped metrics for case 2!!\n")


## args - cli, parameters
## metrics dump
## test a model