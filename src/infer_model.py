import os
import pandas as pd
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch
from vllm import LLM, SamplingParams
from dotenv import load_dotenv
from load_dataset import get_swear_words, get_prompts, get_model_inferences
from calculate_metrics import evaluation_script_case_1, evaluation_script_case_2, calculate_percentage_case_1, calculate_percentage_case_2

load_dotenv()
os.environ["HF_TOKEN"] = os.getenv("HF_KEY")
os.environ["CUDA_DEVICE_ORDER"] = os.getenv("CUDA_DEVICE_ORDER")
os.environ["CUDA_VISIBLE_DEVICES"] = os.getenv("CUDA_VISIBLE_DEVICES_1")
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = os.getenv("PYTORCH_CUDA_ALLOC_CONF")


languages = ["english", "spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]
indices = {"english": 0, "spanish": 1, "french": 2, "german": 3, "hindi": 4, "marathi": 5, "bengali": 6, "gujarati": 7}
columns_case_1 = ["model_name", "english", "spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]
columns_case_2 = ["model_name", "spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]


def get_model_inference(prompts_dataset, model, model_id, temperature, max_tokens) : 
    
    prompts = [t for t in prompts_dataset['Prompts']]
    
    sampling_params = SamplingParams(temperature=temperature, max_tokens=max_tokens)
    outputs = model.generate(prompts, sampling_params)
    prompts_dataset['outputs'] = [ {"model_name": model_id, "response": output.outputs[0].text} for output in outputs ]
    
    return prompts_dataset


def prepare_HF_model(model_id, gpu_memory_utilization, tensor_parallel_size, max_model_len) : 
    llm = LLM(model = model_id,
              gpu_memory_utilization = gpu_memory_utilization,
              tensor_parallel_size = tensor_parallel_size,
              max_model_len = max_model_len
              )
    return llm


def infer_model(case, prompt_language, swear_language, model_id) : 
    
    metrics = []
    metrics_percentage = []
    metrics.append(model_id)
    metrics_percentage.append(model_id)
    
    if (case == 1) : 
        for i in languages : 
            dataset_path = get_prompts(case, i, i, model_id) ## just an example
            prompts_dataset = pd.read_excel(dataset_path)
            
            llm = prepare_HF_model(model_id, 0.9, 2, 1024)
            
            prompts_dataset = get_model_inference(prompts_dataset, llm, model_id, 0.0, 1024)
            
            metric = evaluation_script_case_1(prompts_dataset) ## returns count for each language, so we append it to the list, metrics
            metrics.append(metric)
            prompts_dataset.to_excel(dataset_path)
            
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
        dataset_path = get_prompts(case, prompt_language, swear_language, model_id)
        prompts_dataset = pd.read_excel(dataset_path)
        
        llm = prepare_HF_model(model_id, 0.9, 2, 1024)
        
        prompts_dataset = get_model_inference(prompts_dataset, llm, model_id, 0.0, 1024)
        
        metrics.append(evaluation_script_case_2(prompts_dataset)) ## case 2 evaluation script returns a list containing counts for each language
        prompts_dataset.to_excel(dataset_path)
        
        metrics_file_path = "metrics/case_2.xlsx"
        if os.path.exists(metrics_file_path):
            existing_metrics_df = pd.read_excel(metrics_file_path)
            new_metrics_df = pd.DataFrame([metrics], columns = columns_case_2)
            updated_metrics_df = pd.concat([existing_metrics_df, new_metrics_df])
        else:
            updated_metrics_df = pd.DataFrame([metrics], columns=languages)
            
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