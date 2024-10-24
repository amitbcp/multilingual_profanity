import os
import gdown
import pandas as pd
import argparse
from load_dataset import get_prompts, get_model_inferences
from paths import drive_info
from load_dataset import download_resources


def get_dataset_length_case_1(language): 
    """
    Input: language of prompts and slang words to get the dataset length dynamically
    Output: length of the dataset (robust to any modifications)
    """
    dataset = get_prompts(1, language, language)  # model_id doesn't matter
    return len(dataset)

def get_dataset_length_case_2(language): 
    """
    Input: language of slang words to get the dataset length dynamically (prompts are always in English)
    Output: length of the dataset (robust to any modifications)
    """
    dataset = get_prompts(2, language, language)  # model_id doesn't matter
    return len(dataset)

def get_dataset_length_case_3(language):
    """
    Input: language of slang words (transliterated) to get the dataset length dynamically (prompts are always in English)
    Output: length of the dataset (robust to any modifications)
    """
    dataset = get_prompts(3, language, language)  # model_id doesn't matter
    return len(dataset)

def main():
    parser = argparse.ArgumentParser(description="Get the dataset length based on language and case.")
    parser.add_argument("language", type=str, help="Language code (e.g., 'en', 'es')")
    parser.add_argument("case", type=int, choices=[1, 2], help="Choose case (1 for prompts in the same language, 2 for prompts in English)")

    args = parser.parse_args()
    
    # Download resources once
    download_resources()
    
    if args.case == 1:
        length = get_dataset_length_case_1(args.language)
        print(f"The dataset length for case 1 in {args.language} is: {length}")
    elif args.case == 2:
        length = get_dataset_length_case_2(args.language)
        print(f"The dataset length for case 2 in {args.language} is: {length}")

if __name__ == "__main__":
    main()
