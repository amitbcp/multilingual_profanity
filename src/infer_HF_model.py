import os
import paths
import pandas as pd
import json
import argparse
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

def prepare_HF_model(model_id, gpu_memory_utilization, tensor_parallel_size, max_model_len) : 
    llm = LLM(model = model_id,
              gpu_memory_utilization = gpu_memory_utilization,
              tensor_parallel_size = tensor_parallel_size,
              max_model_len = max_model_len
              )
    return llm


def main(args) : 
    prepare_HF_model(args.model_id, args.gpu_memory, args.tensor_parallel_size, args.max_model_len)
    
if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description="Prepare HF model")
    parser.add_argument("--model_id", type=str, help="Model ID to be prepared", required=True)
    parser.add_argument("--gpu_memory", type=float, help="GPU memory utilization", required=True)
    parser.add_argument("--tensor_parallel_size", type=int, help="Tensor parallel size", required=True)
    parser.add_argument("--max_model_len", type=int, help="Maximum model length", required=True)
    
    args = parser.parse_args()
    main(args)