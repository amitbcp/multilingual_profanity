import os
import pandas as pd
import paths
import openpyxl
import json
import argparse
from load_dataset import get_swear_words, get_prompts, get_model_inferences
from utils import model_metadata
from annotate_inference import annotate_inferences
from eval_utils import evaluate_case_1, evaluate_case_2, get_details_case_1, get_details_case_2, evaluate_case_3, get_details_case_3

INDICES = {"english": 0, "spanish": 1, "french": 2, "german": 3, "hindi": 4, "marathi": 5, "bengali": 6, "gujarati": 7}
COLUMNS_CASE_1 = ["model_name", "english", "spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]
COLUMNS_CASE_2 = ["model_name", "spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]
COLUMNS_CASE_3 = ["model_name", "hindi", "marathi", "bengali", "gujarati"]
LANGUAGES_CASE_1 = ["english", "spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]
LANGUAGES_CASE_2 = ["spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]
LANGUAGES_CASE_3 = ["hindi", "marathi", "bengali", "gujarati"]


## model_names from utils
MODELS = model_metadata.values()


def save_metrics(case, metrics, metrics_percentage) : 
    
    if case == 1 : 
        
        ## counts
        metrics_file_path = "metrics/case_1.xlsx"
        if os.path.exists(metrics_file_path):
            existing_metrics_df = pd.read_excel(metrics_file_path)
            updated_metrics_df = pd.concat([existing_metrics_df, pd.DataFrame([metrics], columns=COLUMNS_CASE_1)], ignore_index=True)
        else:
            updated_metrics_df = pd.DataFrame([metrics], columns=COLUMNS_CASE_1)
            
        updated_metrics_df.to_excel(metrics_file_path, index=False)
        
        ## percentage
        percentage_metrics_file_path = "metrics/percentage_case_1.xlsx"
        if os.path.exists(percentage_metrics_file_path):
            existing_percentage_metrics_df = pd.read_excel(percentage_metrics_file_path)
            updated_percentage_metrics_df = pd.concat([existing_percentage_metrics_df, pd.DataFrame([metrics_percentage], columns=COLUMNS_CASE_1)], ignore_index=True)
        else:
            updated_percentage_metrics_df = pd.DataFrame([metrics_percentage], columns=COLUMNS_CASE_1)
            
        updated_percentage_metrics_df.to_excel(percentage_metrics_file_path, index=False)
        
    elif case == 2 : 
        ## count
        metrics_file_path = "metrics/case_2.xlsx"
        if os.path.exists(metrics_file_path):
            existing_metrics_df = pd.read_excel(metrics_file_path)
            updated_metrics_df = pd.concat([existing_metrics_df, pd.DataFrame([metrics], columns=COLUMNS_CASE_2)], ignore_index=True)
        else:
            updated_metrics_df = pd.DataFrame([metrics], columns=COLUMNS_CASE_2)
            
        updated_metrics_df.to_excel(metrics_file_path, index=False)
        
        ## percentage
        percentage_metrics_file_path = "metrics/percentage_case_2.xlsx"
        if os.path.exists(percentage_metrics_file_path):
            existing_percentage_metrics_df = pd.read_excel(percentage_metrics_file_path)
            updated_percentage_metrics_df = pd.concat([existing_percentage_metrics_df, pd.DataFrame([metrics_percentage], columns=COLUMNS_CASE_2)], ignore_index=True)
        else:
            updated_percentage_metrics_df = pd.DataFrame([metrics_percentage], columns=COLUMNS_CASE_2)
            
        updated_percentage_metrics_df.to_excel(percentage_metrics_file_path, index=False)
        
    else : 
        ## count
        metrics_file_path = "metrics/case_3.xlsx"
        if os.path.exists(metrics_file_path):
            existing_metrics_df = pd.read_excel(metrics_file_path)
            updated_metrics_df = pd.concat([existing_metrics_df, pd.DataFrame([metrics], columns=COLUMNS_CASE_3)], ignore_index=True)
        else:
            updated_metrics_df = pd.DataFrame([metrics], columns=COLUMNS_CASE_3)
            
        updated_metrics_df.to_excel(metrics_file_path, index=False)
        
        ## percentage
        percentage_metrics_file_path = "metrics/percentage_case_3.xlsx"
        if os.path.exists(percentage_metrics_file_path):
            existing_percentage_metrics_df = pd.read_excel(percentage_metrics_file_path)
            updated_percentage_metrics_df = pd.concat([existing_percentage_metrics_df, pd.DataFrame([metrics_percentage], columns=COLUMNS_CASE_3)], ignore_index=True)
        else:
            updated_percentage_metrics_df = pd.DataFrame([metrics_percentage], columns=COLUMNS_CASE_3)
            
        updated_percentage_metrics_df.to_excel(percentage_metrics_file_path, index=False)


def save_details(case, details) :
    
    if case == 1:
        
        print("\nSaving details...\n")
        
        details_file_path = "details/case_1.json"
        
        if os.path.exists(details_file_path):
            with open(details_file_path, "r") as file:
                existing_details = json.load(file)
            existing_details.append(details)
            with open(details_file_path, "w") as file:
                json.dump(existing_details, file, indent=4)
        else:
            with open(details_file_path, "w") as file:
                json.dump([details], file, indent=4)
            
        print("Details saved!!")
        
    elif case == 2:
        print("\nSaving details...\n")
        
        details_file_path = "details/case_2.json"
        
        if os.path.exists(details_file_path):
            with open(details_file_path, "r") as file:
                existing_details = json.load(file)
            existing_details.append(details)
            with open(details_file_path, "w") as file:
                json.dump(existing_details, file, indent=4)
        else:
            with open(details_file_path, "w") as file:
                json.dump([details], file, indent=4)
                
        print("Details saved!!")
        
    else:
        print("\nSaving details...\n")
        
        details_file_path = "details/case_3.json"
        
        if os.path.exists(details_file_path):
            with open(details_file_path, "r") as file:
                existing_details = json.load(file)
            existing_details.append(details)
            with open(details_file_path, "w") as file:
                json.dump(existing_details, file, indent=4)
        else:
            with open(details_file_path, "w") as file:
                json.dump([details], file, indent=4)
                
        print("Details saved!!")



def calculate_metrics(case) : 
    
    if (case == 1) : 
        for model_id in MODELS : # MODELS -> model_names from utils
            
            print(f"\nDumping metrics for {model_id}\n")
            
            metrics = []
            metrics_percentage = []
            details = []
            metrics.append(model_id)
            metrics_percentage.append(model_id)
            details.append(model_id)
            
            for language in LANGUAGES_CASE_1 : 
                
                print(f"\nDumping metrics for {model_id} -> {language}\n")
                
                dataset = get_model_inferences(case, language, language, model_id) ## because prompt_lang & slang_lang is same for case_1
                metric = evaluate_case_1(dataset, language) ## returns count for each language, so we append it to the list, metrics
                
                metrics.append(metric)
                metrics_percentage.append(round(metric / len(dataset) * 100, 2))
                details.append(get_details_case_1(dataset, language))
                
                print(f"\nDumped metrics for {model_id} -> {language}!!\n")
            
            print(metrics)
            print(metrics_percentage)
            
            ## updating the metrics to destination file
            save_metrics(case, metrics, metrics_percentage)
            save_details(case, details)
            
            print(f"\nDumped metrics for {model_id}!!")
        
        ## annotating the inferences
        annotate_inferences(1)
            
    elif (case == 2) :
        
        for model_id in MODELS : 
            
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
            
        ## annotating the inferences
        annotate_inferences(2)
            
    else :
            
        for model_id in MODELS : 
                
            print(f"\nDumping metrics for {model_id}\n")
                
            metrics = []
            metrics_percentage = []
            details = []
            metrics.append(model_id)
            metrics_percentage.append(model_id)
            details.append(model_id)
                
            dataset = get_model_inferences(case, "english", "english", model_id) ## languages don't matter, dataset wrt the model_id will be returned
            metrics_3, metrics_percentage_3 = evaluate_case_3(dataset)
            
            details.append(get_details_case_3(dataset))
            
            for value in metrics_3 : 
                metrics.append(value) ## case 3 evaluation script returns a list containing counts for each language
            for value in metrics_percentage_3 :
                metrics_percentage.append(value) ## case 3 evaluation script returns a list containing percentages for each language
                
            print(metrics)
            print(metrics_percentage)
            
            save_metrics(case, metrics, metrics_percentage)
            save_details(case, details)
            
            print(f"\nDumped metrics for {model_id}!!")
            
        ## annotating the inferences
        annotate_inferences(3)
            

def main(args) : 
    
    metrics_path = f"metrics/case_{args.case}.xlsx"
    metrics_percentage_path = f"metrics/percentage_case_{args.case}.xlsx"
    details_path = f"details/case_{args.case}.json"
    
    ## removing them if they already exist
    if os.path.exists(metrics_path):
        os.remove(metrics_path)
        print(f"Deleted existing metrics file: {metrics_path}")
        
    if os.path.exists(metrics_percentage_path):
        os.remove(metrics_percentage_path)
        print(f"Deleted existing metrics percentage file: {metrics_percentage_path}")
        
    if os.path.exists(details_path):
        os.remove(details_path)
        print(f"Deleted existing details file: {details_path}")
        
    
    print(f"Dumping metrics for case {args.case}...\n")
    calculate_metrics(args.case)
    print(f"Dumped metrics for case {args.case}!!\n")

if __name__ == "__main__" : 
    
    parser = argparse.ArgumentParser(description="Metrics calculation script")
    parser.add_argument("--case", type=int, help="Case number")
    
    args = parser.parse_args()
    main(args)