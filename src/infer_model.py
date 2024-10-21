import os
import paths
import pandas as pd
import json
import paths
import gdown
import argparse
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch
from vllm import LLM, SamplingParams
from dotenv import load_dotenv
from load_dataset import get_swear_words, get_prompts, get_model_inferences
from calculate_metrics import evaluation_script_case_1, evaluation_script_case_2, calculate_percentage_case_1, calculate_percentage_case_2
from infer_HF_model import prepare_HF_model

url_drive = f"https://drive.google.com/drive/folders/{paths.drive_id}"
url_metrics = f"https://drive.google.com/drive/folders/{paths.metrics_id}"

languages = ["english", "spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]
indices = {"english": 0, "spanish": 1, "french": 2, "german": 3, "hindi": 4, "marathi": 5, "bengali": 6, "gujarati": 7}
columns_case_1 = ["model_name", "english", "spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]
columns_case_2 = ["model_name", "spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]


def get_model_inference(prompts_dataset, model, model_id, temperature, max_tokens) : 
    
    prompts = [[{
            "role": "user",
            "content": t,
            }] for t in prompts_dataset['Prompts']]
    
    sampling_params = SamplingParams(temperature=temperature, max_tokens=max_tokens)
    outputs = model.chat(prompts, sampling_params)
    prompts_dataset['outputs'] = [ {"model_name": model_id, "response": output.outputs[0].text} for output in outputs ]
    
    return prompts_dataset


def infer_model(case, prompt_language, swear_language, model_id, temperature, max_tokens) : 
    
    metrics = []
    metrics_percentage = []
    metrics.append(model_id)
    metrics_percentage.append(model_id)
    
    if (case == 1) : 
        for language in languages : 
            dataset = get_prompts(case, language, language) ## because prompt_lang & slang_lang is same for case_1
            
            llm = prepare_HF_model(model_id, 0.9, 2, max_tokens)
            
            prompts_dataset = get_model_inference(dataset, llm, model_id, temperature, max_tokens)
            path = paths.inference_case_1_excel + "/" + language + "_prompts_" + language + "_slangs_" + model_id + ".xlsx"
            prompts_dataset.to_excel(path, index=False)
            
            prompts_dataset = pd.read_excel(path)
            
            metric = evaluation_script_case_1(prompts_dataset) ## returns count for each language, so we append it to the list, metrics
            metrics.append(metric)
            
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
        metrics_percentage.append(calculate_percentage_case_2(metrics))
        percentage_metrics_file_path = "metrics/percentage_case_2.xlsx"
        if os.path.exists(percentage_metrics_file_path):
            existing_metrics_df = pd.read_excel(percentage_metrics_file_path)
            new_metrics_df = pd.DataFrame([metrics], columns = columns_case_1)
            updated_metrics_df = pd.concat([existing_metrics_df, new_metrics_df])
        else:
            updated_metrics_df = pd.DataFrame([metrics], columns = columns_case_1)
        
    else : 
        dataset = get_prompts(case, prompt_language, swear_language)
        
        llm = prepare_HF_model(model_id, 0.9, 2, max_tokens)
        
        prompts_dataset = get_model_inference(dataset, llm, model_id, temperature, max_tokens)
        
        path = paths.inference_case_2_excel + "/" + prompt_language + "_prompts_" + model_id + ".xlsx"
        prompts_dataset.to_excel(path, index=False)
        
        prompts_dataset = pd.read_excel(path)
        
        metrics.append(evaluation_script_case_2(prompts_dataset)) ## case 2 evaluation script returns a list containing counts for each language
        
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
            

def main(args) : 
    
    if not os.path.exists("drive") : 
        print("\n Downloading drive folder... \n")
        gdown.download_folder(url_drive, quiet=True, use_cookies=False)
        print("\n drive folder downloaded!! \n")
    if not os.path.exists("metrics") : 
        print("\n Downloading metrics folder... \n")
        gdown.download_folder(url_metrics, quiet=True, use_cookies=False)
        print("\n metrics folder downloaded!! \n")
    
    infer_model(args.case, args.prompt_language, args.slang_language, args.model_id, args.temperature, args.max_tokens)


if __name__ == "__main__" : 
    parser = argparse.ArgumentParser(description = "Model inference script")
    parser.add_argument("--case", type=int, required=True, help="specify if case 1 or 2")
    parser.add_argument("--prompt_language", type=str, required=True, help="prompt language")
    parser.add_argument("--slang_language", type=str, required=True, help="slang language")
    parser.add_argument("--model_id", type=str, required=True, help="Model ID to use for inference")
    parser.add_argument("--temperature", type=float, default=0.0, help="Sampling temperature")
    parser.add_argument("--max_tokens", type=int, default=1024, help="Maximum tokens to generate")
    
    args = parser.parse_args()
    main(args)