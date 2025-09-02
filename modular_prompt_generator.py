import random
from typing import List, Optional, Dict, Any

import concurrent

from tqdm import tqdm

from config.settings import AppConfig
from services.category_loader import CategoryLoader
from services.prompt_builder import PromptBuilder
from services.llm_service import LLMService
from services.text_processor import TextProcessor, QualityEvaluator
from models.category import Category
from pii_generator import PIIGenerator


class GeneratedPrompt:
    """Representa um prompt gerado com suas métricas"""

    def __init__(
        self,
        content: str,
        category: Category,
        profiles: List,
        metrics: Dict[str, Any],
        quality_score: int,
        max_quality_score: int,
    ):
        self.content = content
        self.category = category
        self.profiles = profiles
        self.metrics = metrics
        self.quality_score = quality_score
        self.max_quality_score = max_quality_score

    @property
    def quality_percentage(self) -> float:
        if self.max_quality_score == 0:
            return 0.0
        return (self.quality_score / self.max_quality_score) * 100

    def display_summary(self) -> None:
        print(f"\n{'='*80}")
        print(f"🎯 PROMPT GERADO - CATEGORIA: {self.category.nome.upper()}")
        print(f"{'='*80}")
        print(self.content)
        print(f"{'='*80}")
        self.display_metrics()

    def display_metrics(self) -> None:
        print(f"\n📊 MÉTRICAS DE QUALIDADE:")
        print(f"- Categoria: {self.category.nome}")
        print(f"- Palavras: {self.metrics.get('word_count', 0)}")
        print(f"- CPF presente: {'✅' if self.metrics.get('has_cpf') else '❌'}")
        print(f"- Nomes próprios: {'✅' if self.metrics.get('has_names') else '❌'}")
        print(
            f"- Dados específicos: {'✅' if self.metrics.get('has_specific_data') else '❌'}"
        )
        print(
            f"- Comprimento ideal: {'✅' if self.metrics.get('ideal_length') else '❌'}"
        )

        category_metrics = {
            k: v
            for k, v in self.metrics.items()
            if k
            not in [
                "word_count",
                "has_cpf",
                "has_names",
                "has_specific_data",
                "ideal_length",
            ]
        }
        if category_metrics:
            print(f"- Métricas específicas de {self.category.nome}:")
            for metric, value in category_metrics.items():
                print(f"  • {metric}: {'✅' if value else '❌'}")

        print(
            f"- Score final: {self.quality_score}/{self.max_quality_score} ({self.quality_percentage:.1f}%)"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "category": {
                "nome": self.category.nome,
                "descricao": self.category.descricao,
            },
            "metrics": self.metrics,
            "quality_score": self.quality_score,
            "max_quality_score": self.max_quality_score,
            "quality_percentage": self.quality_percentage,
        }


class ModularPromptGenerator:
    """Sistema principal para geração modular de prompts"""

    def __init__(self, config: Optional[AppConfig] = None):
        self.config = config or AppConfig()
        self._initialize_services()
        self.categories: Dict[str, Category] = {}
        self.load_all_categories()

    def _initialize_services(self):
        self.category_loader = CategoryLoader(self.config.examples_dir)
        self.prompt_builder = PromptBuilder()
        self.llm_service = LLMService(self.config.llm_config)
        self.text_processor = TextProcessor()
        self.quality_evaluator = QualityEvaluator(
            self.config.min_word_count, self.config.max_word_count
        )
        self.pii_factory = PIIGenerator()

    def load_all_categories(self) -> None:
        self.categories = self.category_loader.load_all_categories()
        if not self.categories:
            print("❌ Nenhuma categoria foi carregada!")

    def get_available_categories(self) -> List[str]:
        return list(self.categories.keys())

    def get_category(self, category_name: str) -> Optional[Category]:
        return self.categories.get(category_name)

    def generate_prompt(
        self,
        category_name: Optional[str] = None,
        num_profiles: Optional[int] = None,
        num_examples: Optional[int] = None,
    ) -> Optional[GeneratedPrompt]:
        if not self.categories:
            print("❌ Nenhuma categoria disponível!")
            return None

        num_profiles = num_profiles or self.config.default_profiles
        num_examples = num_examples or self.config.default_examples

        if category_name:
            if category_name not in self.categories:
                print(f"❌ Categoria '{category_name}' não encontrada!")
                return None
            selected_category = self.categories[category_name]
        else:
            category_name = random.choice(list(self.categories.keys()))
            selected_category = self.categories[category_name]

        print(
            f"🎲 Categoria {'sorteada' if not category_name else 'selecionada'}: {category_name.upper()}"
        )

        try:
            profiles = self._generate_profiles(num_profiles)
            specialized_prompt = self.prompt_builder.build_specialized_prompt(
                selected_category, profiles, num_examples
            )
            print(f">>> Gerando prompt especializado em '{category_name.upper()}'...")
            raw_response = self.llm_service.generate_response(specialized_prompt)
            cleaned_response = self.text_processor.clean_response(
                raw_response, category_name
            )
            metrics, score, max_score = self.quality_evaluator.evaluate_quality(
                cleaned_response, category_name
            )

            return GeneratedPrompt(
                content=cleaned_response,
                category=selected_category,
                profiles=profiles,
                metrics=metrics,
                quality_score=score,
                max_quality_score=max_score,
            )
        except Exception as e:
            print(f"❌ Erro durante geração: {e}")
            return None

    def _generate_profiles(self, num_profiles: int) -> List:
        return [
            self.pii_factory.get_full_profile(sex=random.choice(["M", "F"]))
            for _ in range(num_profiles)
        ]

    def batch_generate(
        self, num_prompts: int = 5, category_filter: Optional[List[str]] = None
    ) -> List[GeneratedPrompt]:
        results = []
        available_categories = (
            category_filter if category_filter else self.get_available_categories()
        )

        if not available_categories:
            print("❌ Nenhuma categoria disponível para geração em lote!")
            return results

        # Cria uma lista de categorias para gerar, uma para cada prompt
        categories_to_generate = [
            random.choice(available_categories) for _ in range(num_prompts)
        ]

        print(f"\n🔄 Gerando {num_prompts} prompts em paralelo...")

        # Usa ThreadPoolExecutor para executar as gerações em paralelo
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # O executor.map aplica a função generate_prompt a cada categoria na lista
            # e coleta os resultados. O tqdm cria uma barra de progresso.
            future_to_prompt = {
                executor.submit(self.generate_prompt, cat): cat
                for cat in categories_to_generate
            }

            for future in tqdm(
                concurrent.futures.as_completed(future_to_prompt),
                total=num_prompts,
                desc="Gerando Prompts",
            ):
                prompt = future.result()
                if prompt:
                    results.append(prompt)
                else:
                    category = future_to_prompt[future]
                    print(f"❌ Falha ao gerar prompt para a categoria '{category}'")

        return results
