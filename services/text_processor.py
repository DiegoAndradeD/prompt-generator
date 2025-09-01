import re
from typing import Tuple, Dict, Any


class TextProcessor:
    """Responsável pelo processamento e limpeza de texto"""

    @staticmethod
    def clean_response(texto: str, categoria: str) -> str:
        """Limpa e formata a resposta gerada"""
        # Remove prefixos desnecessários
        prefixes = [r"^(Prompt:|Texto:|Aqui está.*?:|Para.*?:)\s*"]
        for prefix in prefixes:
            texto = re.sub(prefix, "", texto.strip(), flags=re.IGNORECASE)

        # Remove sufixos desnecessários
        suffixes = [
            r"\s*(---.*|EXEMPLO.*|NOTA:.*|OBSERVAÇÃO:.*|Espero.*|Fico.*|Aguardo.*)$"
        ]
        for suffix in suffixes:
            texto = re.sub(suffix, "", texto, flags=re.IGNORECASE | re.DOTALL)

        return texto.strip()


class QualityEvaluator:
    """Avalia a qualidade dos prompts gerados"""

    def __init__(self, min_words: int = 200, max_words: int = 500):
        self.min_words = min_words
        self.max_words = max_words

    def evaluate_quality(
        self, texto: str, categoria: str = None
    ) -> Tuple[Dict[str, Any], int, int]:
        """Avalia a qualidade do texto gerado"""
        base_metrics = self._get_base_metrics(texto)
        category_metrics = self._get_category_metrics(texto, categoria)

        all_metrics = {**base_metrics, **category_metrics}

        score_items = [
            all_metrics["has_cpf"],
            all_metrics["has_names"],
            all_metrics["has_specific_data"],
            all_metrics["ideal_length"],
            *category_metrics.values(),
        ]

        score = sum(score_items)
        max_score = len(score_items)

        return all_metrics, score, max_score

    def _get_base_metrics(self, texto: str) -> Dict[str, Any]:
        """Obtém métricas base do texto"""
        word_count = len(texto.split())
        return {
            "word_count": word_count,
            "has_cpf": bool(re.search(r"\d{3}\.?\d{3}\.?\d{3}-?\d{2}", texto)),
            "has_names": bool(re.search(r"[A-Z][a-z]+\s+[A-Z][a-z]+", texto)),
            "has_emails": bool(
                re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", texto)
            ),
            "has_phones": bool(re.search(r"\(?\d{2}\)?\s?\d{4,5}-\d{4}", texto)),
            "has_specific_data": bool(
                re.search(r"(\d{1,2}/\d{1,2}/\d{4}|R\$\s*\d+|\d{5}-?\d{3})", texto)
            ),
            "ideal_length": self.min_words <= word_count <= self.max_words,
        }

    def _get_category_metrics(self, texto: str, categoria: str) -> Dict[str, bool]:
        """Obtém métricas específicas da categoria"""
        if not categoria:
            return {}

        metrics_map = {
            "suspensao": {
                "has_evidence": bool(
                    re.search(
                        r"(evidência|testemunha|relatório|laudo)", texto, re.IGNORECASE
                    )
                ),
                "has_period": bool(
                    re.search(r"(\d+\s*(dia|semana|mês))", texto, re.IGNORECASE)
                ),
            },
            "financeiro": {
                "has_values": bool(re.search(r"R\$\s*[\d.,]+", texto)),
                "has_calculations": bool(
                    re.search(
                        r"(análise|cálculo|auditoria|crédito)", texto, re.IGNORECASE
                    )
                ),
            },
            "avaliacao": {
                "has_experience": bool(
                    re.search(
                        r"(experiência|formação|cargo|empresa)", texto, re.IGNORECASE
                    )
                ),
                "has_skills": bool(
                    re.search(
                        r"(competência|habilidade|certificação)", texto, re.IGNORECASE
                    )
                ),
            },
            "comunicacao_interna": {
                "mentions_date_time": bool(
                    re.search(r"\d{1,2}/\d{1,2}/\d{2,4}|\d{1,2}h", texto)
                ),
                "has_objective": bool(
                    re.search(
                        r"(objetivo|assunto|tema|propósito)", texto, re.IGNORECASE
                    )
                ),
            },
        }

        return metrics_map.get(categoria, {})
