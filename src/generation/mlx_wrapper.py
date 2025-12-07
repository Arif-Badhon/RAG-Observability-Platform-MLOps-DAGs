# src/generation/mlx_wrapper.py
from typing import Any, List, Optional
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from mlx_lm import load, generate

class MLXLLM(LLM):
    """Custom LangChain Wrapper for MLX Models"""
    
    model_id: str = "mlx-community/Llama-3.2-3B-Instruct-4bit"
    model: Any = None
    tokenizer: Any = None
    max_tokens: int = 512
    temp: float = 0.7

    def __init__(self, model_id: str, **kwargs):
        super().__init__(model_id=model_id, **kwargs)
        print(f"🚀 Loading MLX Model: {model_id}")
        self.model, self.tokenizer = load(model_id)

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

        # Format prompt for Llama 3 Instruct (simplified)
        # For better results, use the tokenizer's chat template, 
        # but raw prompt works for simple RAG.
        messages = [{"role": "user", "content": prompt}]
        formatted_prompt = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

        response = generate(
            self.model, 
            self.tokenizer, 
            prompt=formatted_prompt, 
            verbose=False, 
            max_tokens=self.max_tokens,
            temp=self.temp
        )
        return response
