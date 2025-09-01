from typing import List
from models.category import Category
from pii_generator import PIIGenerator


class PromptBuilder:
    """Responsável por construir prompts especializados"""

    def __init__(self):
        self.pii_factory = PIIGenerator()

    def build_specialized_prompt(
        self, category: Category, profiles: List, num_examples: int = 3
    ) -> str:
        """Constrói um prompt especializado para a categoria"""
        examples = category.get_random_examples(num_examples)

        if not examples:
            raise ValueError(
                f"Nenhum exemplo disponível para categoria '{category.nome}'"
            )

        examples_text = self._format_examples(examples, category.nome)
        guidelines_text = self._format_guidelines(category)

        prompt = f"""
Você é um especialista sênior em Recursos Humanos, especializado em {category.descricao.lower()}.

CATEGORIA FOCO: {category.nome.upper()}
EXPERTISE: {category.descricao}

EXEMPLOS DE REFERÊNCIA DE ALTA QUALIDADE:
{examples_text}

PERFIS FICTÍCIOS DISPONÍVEIS:
{[str(p) for p in profiles]}

MISSÃO:
Crie UM prompt profissional e detalhado da categoria {category.nome.upper()}, seguindo exatamente o padrão dos exemplos acima.

{guidelines_text}

IMPORTANTE: Responda APENAS com o texto do prompt final, sem comentários adicionais.
"""
        return prompt

    def _format_examples(self, examples: List, category_name: str) -> str:
        """Formata exemplos para o prompt"""
        examples_text = ""
        for i, ex in enumerate(examples, 1):
            examples_text += f"\n{'='*60}\n"
            examples_text += (
                f"EXEMPLO {i} - {category_name.upper()} ({ex.subcategoria})\n"
            )
            examples_text += f"Complexidade: {ex.complexidade}\n"
            examples_text += f"{'='*60}\n"
            examples_text += f'"{ex.prompt}"\n'
        return examples_text

    def _format_guidelines(self, category: Category) -> str:
        """Formata diretrizes específicas da categoria"""
        guidelines_text = f"DIRETRIZES ESPECÍFICAS PARA {category.nome.upper()}:\n"

        # Diretrizes padrão
        default_guidelines = [
            "✅ Use dados específicos dos perfis (nomes, CPFs, números, datas)",
            f"✅ Inclua detalhes técnicos relevantes para {category.nome}",
            "✅ Use PIIs de forma relevante e contextualizada, evitando excesso que prejudique a naturalidade do texto.",
            "✅ Varie a referência aos perfis (nome completo, primeiro nome, sobrenome ou pronomes), mantendo clareza."
            "✅ Mantenha o nível de complexidade similar aos exemplos",
            "✅ Linguagem professional, dissertativa e fluida",
            "✅ Entre 300-700 palavras",
            "✅ Inclua próximos passos e responsáveis quando aplicável",
        ]

        # Adiciona diretrizes específicas da categoria se existirem
        all_guidelines = default_guidelines + category.diretrizes_especificas

        for guideline in all_guidelines:
            guidelines_text += f"{guideline}\n"

        return guidelines_text
