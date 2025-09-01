import ollama
from config.settings import LLMConfig


class LLMService:
    """Serviço para interação com modelos LLM"""

    def __init__(self, config: LLMConfig):
        self.config = config

    def generate_response(self, prompt: str) -> str:
        """Gera resposta usando o modelo LLM"""
        try:
            response = ollama.chat(
                model=self.config.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um especialista em RH focado em criar prompts de alta qualidade. Sempre responda de forma precisa, detalhada e profissional.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                options={
                    "temperature": self.config.temperature,
                    "top_p": self.config.top_p,
                    "top_k": self.config.top_k,
                    "repeat_penalty": self.config.repeat_penalty,
                    "num_predict": self.config.num_predict,
                    "stop": self.config.stop_tokens,
                },
            )
            return response["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar resposta do LLM: {e}")
