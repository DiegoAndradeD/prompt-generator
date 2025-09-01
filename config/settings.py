from dataclasses import dataclass
from pathlib import Path


@dataclass
class LLMConfig:
    model: str = "llama3:8b"
    temperature: float = 0.65
    top_p: float = 0.87
    top_k: int = 45
    repeat_penalty: float = 1.12
    num_predict: int = 650
    stop_tokens: list = None

    def __post_init__(self):
        if self.stop_tokens is None:
            self.stop_tokens = [
                "---",
                "EXEMPLO",
                "DIRETRIZES",
                "OBSERVAÇÃO",
                "\n\nNota:",
            ]


@dataclass
class AppConfig:
    examples_dir: Path = Path("examples")
    default_profiles: int = 3
    default_examples: int = 4
    min_word_count: int = 200
    max_word_count: int = 500
    llm_config: LLMConfig = None

    def __post_init__(self):
        if self.llm_config is None:
            self.llm_config = LLMConfig()
