# src/generation/mlx_wrapper.py
import os
from typing import Any, List, Optional
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from mlx_lm import load, generate
from dotenv import load_dotenv

load_dotenv()

class MLXLLM(LLM):
    """Custom LangChain Wrapper for MLX Models"""
    
    model_id: str = os.getenv("MODEL_ID", "mlx-community/Llama-3.2-3B-Instruct-4bit")
    model: Any = None
    tokenizer: Any = None
    max_tokens: int = int(os.getenv("MAX_TOKENS", 512))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(f"🚀 Loading MLX Model: {self.model_id}")
        self.model, self.tokenizer = load(self.model_id)

    @property
    def _llm_type(self) -> str:
        return "mlx_llama"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

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
