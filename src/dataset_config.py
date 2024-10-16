import os
import pandas as pd
from load_dataset import get_swear_words, get_prompts


def get_dataset_length_case_1(language) : 
    """
    Input : language of prompts and slang words to get the dataset length dynamically
    Output : length of the dataset (robust to any modifications)
    """
    
    dataset_path = get_prompts(1, language, language, "llama3") # model_id doesn't matter, as dataset length would be same for all
    dataset = pd.read_excel(dataset_path)
    return len(dataset)


def get_dataset_length_case_2(language) : 
    """
    Input : language of slang words to get the dataset length dynamically (prompts are always in english)
    Output : length of the dataset (robust to any modifications)
    """
    
    dataset_path = get_prompts(2, language, language, "llama3") # model_id doesn't matter, as dataset length would be same for all
    dataset = pd.read_excel(dataset_path)
    return len(dataset)
    
    