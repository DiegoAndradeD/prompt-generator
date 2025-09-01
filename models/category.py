from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class Example:

    prompt: str
    subcategoria: str = "geral"
    complexidade: str = "medio"
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class Category:
    nome: str
    descricao: str
    exemplos: List[Example]
    diretrizes_especificas: List[str] = None
    metricas_qualidade: Dict[str, str] = None

    def __post_init__(self):
        if self.diretrizes_especificas is None:
            self.diretrizes_especificas = []
        if self.metricas_qualidade is None:
            self.metricas_qualidade = {}

    def get_random_examples(self, max_examples: int = 3) -> List[Example]:
        import random

        if not self.exemplos:
            return []

        random.shuffle(self.exemplos)
        return self.exemplos[:max_examples]
