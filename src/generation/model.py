# src/generation/model.py
import sys

def load_model(model_path="mlx-community/Llama-3.2-3B-Instruct-4bit"):
    """
    Loads model conditionally based on environment.
    Local (Mac): Uses MLX for GPU acceleration.
    Cloud (Linux): Uses HuggingFace Transformers (CPU/CUDA).
    """
    try:
        from mlx_lm import load, generate
        print(f"Loading {model_path} with MLX on Apple Silicon...")
        model, tokenizer = load(model_path)
        return model, tokenizer, "mlx"
    except ImportError:
        # Fallback for Docker/Cloud if MLX isn't available
        print("MLX not found. Falling back to Transformers...")
        from transformers import AutoModelForCausalLM, AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(model_path)
        return model, tokenizer, "transformers"

if __name__ == "__main__":
    import mlx.core as mx
    
    # 1. Check Default Device
    device = mx.default_device()
    print(f"✅ Current MLX Device: {device}")  # Should say "gpu"
    
    # 2. Run Inference to trigger GPU
    model, tokenizer, backend = load_model()
    
    if backend == "mlx":
        from mlx_lm import generate
        prompt = "Explain quantum physics in one sentence."
        messages = [{"role": "user", "content": prompt}]
        prompt_formatted = tokenizer.apply_chat_template(messages, tokenize=False)
        
        print(f"\n🧪 Testing Inference (Watch your GPU stats now)...")
        response = generate(model, tokenizer, prompt=prompt_formatted, verbose=True)
        print(f"\n🤖 Response: {response}")

