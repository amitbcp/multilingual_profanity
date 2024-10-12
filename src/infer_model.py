import os
import pandas as pd
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch
from vllm import LLM, SamplingParams
from dotenv import load_dotenv
from load_dataset import get_swear_words, get_prompts, get_model_inferences

load_dotenv()
os.environ["HF_TOKEN"] = os.getenv("HF_KEY")


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


def infer_model() : 
    
    dataset_path = get_prompts(1, "german", "german", "llama_3_1_70b") ## just an example
    prompts_dataset = pd.read_excel(dataset_path)
    
    llm = prepare_HF_model("meta-llama/Llama-3.1-8B-Instruct", 0.9, 2, 1024)
    
    prompts_dataset = get_model_inference(prompts_dataset, llm, "Llama-3.1-8B-Instruct", 0.0, 1024)
    
    #calulate_metrics(prompts_dataset)
    prompts_dataset.to_excel(dataset_path)