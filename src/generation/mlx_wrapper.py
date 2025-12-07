import os
from typing import Any, List, Optional
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from dotenv import load_dotenv

load_dotenv()

# --- CRITICAL FIX: Handle Import Error ---
try:
    from mlx_lm import load, generate
    HAS_MLX = True
except ImportError:
    HAS_MLX = False
# ----------------------------------------

class MLXLLM(LLM):
    """Custom LangChain Wrapper for MLX Models (with Cloud Fallback)"""
    
    model_id: str = os.getenv("MODEL_ID", "mlx-community/Llama-3.2-3B-Instruct-4bit")
    model: Any = None
    tokenizer: Any = None
    max_tokens: int = int(os.getenv("MAX_TOKENS", 512))
    pipeline: Any = None # For Cloud Fallback

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        if HAS_MLX:
            print(f"🚀 Loading MLX Model: {self.model_id}")
            self.model, self.tokenizer = load(self.model_id)
        else:
            print(f"⚠️ MLX not found. Falling back to HuggingFace Transformers (CPU/Cloud).")
            # Fallback: Use standard Transformers
            from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
            
            # Use the MODEL_ID env var (set to 'gpt2' or 'facebook/opt-125m' in HF Secrets)
            # Do NOT use the MLX model ID here, as it requires MLX format.
            cloud_model_id = os.getenv("MODEL_ID", "gpt2") 
            
            self.pipeline = pipeline(
                "text-generation", 
                model=cloud_model_id, 
                max_new_tokens=self.max_tokens
            )

    @property
    def _llm_type(self) -> str:
        return "mlx_llama" if HAS_MLX else "transformers_fallback"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        if HAS_MLX:
            # MLX Generation Logic
            messages = [{"role": "user", "content": prompt}]
            formatted_prompt = self.tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            response = generate(
                self.model, 
                self.tokenizer, 
                prompt=formatted_prompt, 
                verbose=False, 
                max_tokens=self.max_tokens
            )
            return response
        else:
            # Cloud/CPU Fallback Logic
            # Simple text generation for MVP
            response = self.pipeline(prompt)[0]['generated_text']
            # Remove the prompt from the response if needed
            return response[len(prompt):]
