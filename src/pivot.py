### this script is used to do all kinds of tasks.
### it can be used to call any functions

import os
import pandas as pd
import paths
from load_dataset import get_swear_words, get_prompts, get_model_inferences
#from infer_model import get_model_inference, prepare_HF_model, infer_model
from calculate_metrics import evaluation_script_case_1, evaluation_script_case_2, get_details_case_1, get_details_case_2, get_details_by_categories_case_1, get_details_by_categories_case_2

dataset = get_model_inferences(2, "english", "hindi", "llama31_70b")
print(len(dataset))
print(dataset.head())
metrics = evaluation_script_case_2(dataset)
details = get_details_case_2(dataset)
cat = get_details_by_categories_case_2(dataset)
print(metrics)
print(details)

for key, value in cat.items():
    print(f"{key}: {value}")
    print()

## args - cli, parameters
## metrics dump
## test a model