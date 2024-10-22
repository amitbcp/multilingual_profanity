import os
import pandas as pd
import paths
import openpyxl
import argparse
from load_dataset import get_swear_words, get_prompts, get_model_inferences
from utils import model_metadata
from eval_utils import evaluate_case_1, evaluate_case_2, get_details_case_1, get_details_case_2

languages = ["english", "spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]
languages_case_2 = ["spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]
indices = {"english": 0, "spanish": 1, "french": 2, "german": 3, "hindi": 4, "marathi": 5, "bengali": 6, "gujarati": 7}
columns_case_1 = ["model_name", "english", "spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]
columns_case_2 = ["model_name", "spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]

## model_names from utils
models = model_metadata.values()


def save_metrics(case, metrics, metrics_percentage) : 
    if case == 1 : 
        ## counts
        metrics_file_path = "metrics/case_1.xlsx"
        if os.path.exists(metrics_file_path) : 
            print("File exists, appending new data.")
            existing_metrics_df = pd.read_excel(metrics_file_path)
            new_metrics_df = pd.DataFrame([metrics], columns = columns_case_1)
            updated_metrics_df = pd.concat([existing_metrics_df, new_metrics_df], ignore_index=True)
        else : 
            print("File does not exist, creating new file.")
            updated_metrics_df = pd.DataFrame([metrics], columns = columns_case_1)
        
        updated_metrics_df.to_excel(metrics_file_path, index=False)
        
        ## percentage
        percentage_metrics_file_path = "metrics/percentage_case_1.xlsx"
        if os.path.exists(percentage_metrics_file_path):
            print("File exists, appending new data.")
            existing_metrics_df = pd.read_excel(percentage_metrics_file_path)
            new_metrics_df = pd.DataFrame([metrics_percentage], columns = columns_case_1)
            updated_percentage_metrics_df = pd.concat([existing_metrics_df, new_metrics_df])
        else:
            print("File does not exist, creating new file.")
            updated_percentage_metrics_df = pd.DataFrame([metrics_percentage], columns = columns_case_1)
                
        updated_percentage_metrics_df.to_excel(percentage_metrics_file_path, index=False)
        
    else : 
        ## count
        metrics_file_path = "metrics/case_2.xlsx"
        if os.path.exists(metrics_file_path) : 
            print(f"File {metrics_file_path} exists, appending new data.")
            existing_metrics_df = pd.read_excel(metrics_file_path)
            new_metrics_df = pd.DataFrame([metrics], columns = columns_case_2)
            updated_metrics_df = pd.concat([existing_metrics_df, new_metrics_df], ignore_index=True)
        else : 
            print("File does not exist, creating new file.")
            updated_metrics_df = pd.DataFrame([metrics], columns = columns_case_2)
        
        updated_metrics_df.to_excel(metrics_file_path, index=False)
        
        ## percentage
        percentage_metrics_file_path = "metrics/percentage_case_2.xlsx"
        if os.path.exists(percentage_metrics_file_path):
            print(f"File {metrics_file_path} exists, appending new data.")
            existing_metrics_df = pd.read_excel(percentage_metrics_file_path)
            new_metrics_df = pd.DataFrame([metrics_percentage], columns = columns_case_2)
            updated_percentage_metrics_df = pd.concat([existing_metrics_df, new_metrics_df])
        else:
            print("File does not exist, creating new file.")
            updated_percentage_metrics_df = pd.DataFrame([metrics_percentage], columns = columns_case_2)
                
        updated_percentage_metrics_df.to_excel(percentage_metrics_file_path, index=False)


def save_details(case, details) :
    
    if case == 1:
        
        print("Saving details...\n")
        
        details_file_path = "details/case_1.txt"
        
        if os.path.exists(details_file_path) :
            print(f"File {details_file_path} exists, appending new data.")
            with open(details_file_path, "a") as file:
                file.write(f"\n\n{details}\n\n")
        else : 
            with open(details_file_path, "w") as file:
                file.write(f"\n\n{details}\n\n")
                
        print("Details saved!!")
        
    else : 
        print("Saving details...\n")
        
        details_file_path = "details/case_2.txt"
        
        if os.path.exists(details_file_path) :
            print(f"File {details_file_path} exists, appending new data.")
            with open(details_file_path, "a") as file:
                file.write(f"\n\n{details}\n\n")
        else : 
            with open(details_file_path, "w") as file:
                file.write(f"\n\n{details}\n\n")
                
        print("Details saved!!")



def calculate_metrics(case) : 
    
    if (case == 1) : 
        for model_id in models : # models -> model_names from utils
            print(f"\nDumping metrics for {model_id}\n")
            metrics = []
            metrics_percentage = []
            details = []
            metrics.append(model_id)
            metrics_percentage.append(model_id)
            details.append(model_id)
            
            for language in languages : 
                print(f"\nDumping metrics for {model_id} -> {language}\n")
                dataset = get_model_inferences(case, language, language, model_id) ## because prompt_lang & slang_lang is same for case_1
                
                metric = evaluate_case_1(dataset, language) ## returns count for each language, so we append it to the list, metrics
                metrics.append(metric)
                metrics_percentage.append(metric / len(dataset) * 100)
                
                details.append(get_details_case_1(dataset, language))
                
                print(f"\nCalculated metrics for {model_id} -> {language}!!\n")
            
            print(metrics)
            print(metrics_percentage)
            
            ## updating the metrics to destination file
            save_metrics(case, metrics, metrics_percentage)
            save_details(case, details)
            
            print(f"\nDumped metrics for {model_id}!!")
            
    else :
        
        for model_id in models : 
            print(f"\nDumping metrics for {model_id}\n")
            metrics = []
            metrics_percentage = []
            details = []
            metrics.append(model_id)
            metrics_percentage.append(model_id)
            details.append(model_id)
            
            dataset = get_model_inferences(case, "english", "english", model_id) ## languages don't matter, dataset wrt the model_id will be returned
            
            metric_2, metrics_percentage_2 = evaluate_case_2(dataset)
            details.append(get_details_case_2(dataset))

            for value in metric_2 : 
                metrics.append(value) ## case 2 evaluation script returns a list containing counts for each language
            for value in metrics_percentage_2 :
                metrics_percentage.append(value) ## case 2 evaluation script returns a list containing percentages for each language
            
            print(metrics)
            print(metrics_percentage)
            
            save_metrics(case, metrics, metrics_percentage)
            save_details(case, details)
            
            print(f"\nDumped metrics for {model_id}!!")
            

def main(args) : 
    print(f"Dumping metrics for case {args.case}...\n")
    calculate_metrics(args.case)
    print(f"Dumped metrics for case {args.case}!!\n")

if __name__ == "__main__" : 
    parser = argparse.ArgumentParser(description="Metrics calculation script")
    parser.add_argument("--case", type=int, help="Case number")
    
    args = parser.parse_args()
    main(args)