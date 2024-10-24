import os
import pandas as pd
import argparse
import logging
from load_dataset import get_prompts
from calculate_metrics import evaluation_script_case_1, evaluation_script_case_2, calculate_percentage_case_1, calculate_percentage_case_2
from load_model import HFModel
from paths import inference_paths
from utils import get_model_info

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

## constants
COLUMNS_CASE_1 = ["model_name", "english", "spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]
COLUMNS_CASE_2 = ["model_name", "spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]
COLUMNS_CASE_3 = ["model_name", "hindi", "marathi", "bengali", "gujarati"]
LANGUAGES_CASE_1 = ["english", "spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]
LANGUAGES_CASE_2 = ["spanish", "french", "german", "hindi", "marathi", "bengali", "gujarati"]
LANGUAGES_CASE_3 = ["hindi", "marathi", "bengali", "gujarati"]
INDICES_CASE_1 = {language: idx for idx, language in enumerate(LANGUAGES_CASE_1)}
INDICES_CASE_2 = {language: idx for idx, language in enumerate(LANGUAGES_CASE_2)}
INDICES_CASE_3 = {language: idx for idx, language in enumerate(LANGUAGES_CASE_3)}


def run_inference_and_save(llm, dataset, path, temperature, max_tokens):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    prompts_response = llm.run_inference(dataset, temperature, max_tokens)
    prompts_response.to_excel(path, index=False)
    logger.info(f"Inference completed and saved to {path}")
    return pd.read_excel(path)


def infer_model(case, prompt_language, swear_language, model_id, temperature, max_tokens, gpu_memory_utilization, tensor_parallel_size, all_languages):
    metrics = [model_id]
    llm = HFModel(model_id, gpu_memory_utilization=gpu_memory_utilization, tensor_parallel_size=tensor_parallel_size)

    if case == 1:
        if all_languages:
            for lang in LANGUAGES_CASE_1:
                dataset = get_prompts(case, lang, lang)
                model_saved_name = get_model_info(model_id)
                path = f"{inference_paths['case_1']}/{lang}_prompts_{lang}_slangs_{model_saved_name}.xlsx"
                
                if os.path.exists(path):
                    logger.info(f"File already exists: {path}. Skipping inference.")
                else:
                    run_inference_and_save(llm, dataset, path, temperature, max_tokens)
                    logger.info(f"Inference completed for language: {lang}, model: {model_id}")

        elif case == 2:
            dataset = get_prompts(case, prompt_language, swear_language)
            model_saved_name = get_model_info(model_id)
            path = f"{inference_paths['case_1']}/{prompt_language}_prompts_{swear_language}_slangs_{model_saved_name}.xlsx"
            
            if os.path.exists(path):
                logger.info(f"File already exists: {path}. Skipping inference.")
            else:
                run_inference_and_save(llm, dataset, path, temperature, max_tokens)
                logger.info(f"Inference completed for language: {prompt_language}, model: {model_id}")

    elif case == 2:
        prompt_language = "english"
        dataset = get_prompts(case, prompt_language, swear_language)
        model_saved_name = get_model_info(model_id)
        path = f"{inference_paths['case_2']}/{prompt_language}_prompts_{model_saved_name}.xlsx"
        
        if os.path.exists(path):
            logger.info(f"File already exists: {path}. Skipping inference.")
        else:
            run_inference_and_save(llm, dataset, path, temperature, max_tokens)
            logger.info(f"Inference completed for language: {prompt_language}, model: {model_id}")
            
    else:
        prompt_language = "english"
        dataset = get_prompts(case, prompt_language, swear_language)
        model_saved_name = get_model_info(model_id)
        path = f"{inference_paths['case_3']}/{prompt_language}_prompts_{model_saved_name}.xlsx"
        
        if os.path.exists(path):
            logger.info(f"File already exists: {path}. Skipping inference.")
        else:
            run_inference_and_save(llm, dataset, path, temperature, max_tokens)
            logger.info(f"Inference completed for language: {prompt_language}, model: {model_id}")


def main(args): 
    infer_model(
        args.case, 
        args.prompt_language, 
        args.slang_language, 
        args.model_id, 
        args.temperature, 
        args.max_tokens,
        args.gpu_memory_utilization,
        args.tensor_parallel_size,
        args.all_languages
    )

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description="Model inference script")
    parser.add_argument("--case", type=int, required=True, help="Specify if case 1 or 2")
    parser.add_argument("--prompt_language", type=str, required=True, help="Prompt language")
    parser.add_argument("--slang_language", type=str, required=True, help="Slang language")
    parser.add_argument("--model_id", type=str, required=True, help="Model ID to use for inference")
    parser.add_argument("--temperature", type=float, default=0.0, help="Sampling temperature")
    parser.add_argument("--max_tokens", type=int, default=1024, help="Maximum tokens to generate")
    parser.add_argument("--gpu_memory_utilization", type=float, default=0.98, help="GPU memory utilization")
    parser.add_argument("--tensor_parallel_size", type=int, default=1, help="Tensor parallel size")
    parser.add_argument("--all_languages", action='store_true', help="Run inference for all languages")

    args = parser.parse_args()
    main(args)
