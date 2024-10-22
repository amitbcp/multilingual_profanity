model_metadata = {
    "meta-llama/Llama-3.2-1B-Instruct": "llama3_2_1b_instruct",
    "meta-llama/Llama-3.1-70B": "llama3_1_70b_instruct",
    "meta-llama/Llama-3.2-3B-Instruct": "llama3_2_3b_instruct",
    #"meta-llama/Meta-Llama-3-70B-Instruct": "llama3_70b_instruct",
    "meta-llama/Meta-Llama-3-8B-Instruct": "llama3_8b_instruct",
    "meta-llama/Llama-3.1-8B-Instruct": "llama3_1_8b_instruct",
    "mistralai/Mistral-7B-Instruct-v0.1": "mistral_7b_instruct_v1",
    "mistralai/Mistral-7B-Instruct-v0.3": "mistral_7b_instruct_v2",
    "mistralai/Mistral-7B-Instruct-v0.3": "mistral_7b_instruct_v3",
    "mistralai/Mixtral-8x22B-Instruct-v0.1": "mixtral_8x22b_instruct_v01",
    "mistralai/Mixtral-8x7B-Instruct-v0.1": "mixtral_8x7b_instruct_v01",
    "microsoft/Phi-3.5-MoE-instruct": "phi_3_5_moe_instruct",
    "microsoft/Phi-3-small-8k-instruct": "phi_3_small_8k_instruct",
    "Qwen/Qwen2.5-14B-Instruct": "qwen_2_5_14b_instruct",
    "Qwen/Qwen2.5-7B-Instruct": "qwen_2_5_7b_instruct",
    # Add more models as needed
}

def get_model_info(model_name):
    """Retrieve metadata for a given model name."""
    normalized_model_metadata = {key.lower(): value for key, value in model_metadata.items()}
    return normalized_model_metadata.get(model_name.lower(), "Model not found.")