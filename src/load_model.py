import os
import argparse
from vllm import LLM, SamplingParams
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set environment variables for CUDA
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = 'expandable_segments:False'

class HFModel:
    def __init__(self, model_id: str, gpu_memory_utilization: float, tensor_parallel_size: int):
        self.model_id = model_id
        self.gpu_memory_utilization = gpu_memory_utilization
        self.tensor_parallel_size = tensor_parallel_size
        self.model = self.prepare_model()

    def prepare_model(self) -> LLM:
        """Prepare the Hugging Face model with the specified parameters."""
        print(f"Starting to load model '{self.model_id}'...")  # Start loading message
        llm = LLM(
            model=self.model_id,
            gpu_memory_utilization=self.gpu_memory_utilization,
            tensor_parallel_size=self.tensor_parallel_size,
        )
        print(f"Model '{self.model_id}' loaded successfully.")  # Success message
        return llm

    def run_inference(self, prompts_dataset, temperature, max_tokens):
        """Run inference on the provided prompts."""
        prompts = [[{"role": "user", "content": t}] for t in prompts_dataset['Prompts']]
        
        sampling_params = SamplingParams(temperature=temperature, max_tokens=max_tokens)
        outputs = self.model.chat(prompts, sampling_params)
        
        prompts_dataset['outputs'] = [{"model_name": self.model_id, "response": output.outputs[0].text} for output in outputs]
        
        return prompts_dataset

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Prepare Hugging Face model.")
    parser.add_argument("--model_id", type=str, required=True, help="Model ID to be prepared")
    parser.add_argument("--gpu_memory", type=float, required=True, help="GPU memory utilization")
    parser.add_argument("--tensor_parallel_size", type=int, required=True, help="Tensor parallel size")

    return parser.parse_args()

def main() -> None:
    """Main entry point for the script."""
    args = parse_arguments()
    
    try:
        hf_model = HFModel(args.model_id, args.gpu_memory, args.tensor_parallel_size)
        # Example usage of run_inference (you would replace 'prompts_dataset', 'temperature', and 'max_tokens' with actual values)
        # hf_model.run_inference(prompts_dataset, temperature=1.0, max_tokens=50)
    except Exception as e:
        print(f"An error occurred while preparing the model: {e}")

if __name__ == "__main__":
    main()
