from typing import List, Dict, Any
from collections import defaultdict, Counter
import statistics


class PromptAnalytics:
    """Análises avançadas dos prompts gerados"""

    @staticmethod
    def generate_report(prompts: List["GeneratedPrompt"]) -> Dict[str, Any]:
        """Gera relatório completo de análise"""
        if not prompts:
            return {"error": "Nenhum prompt para analisar"}

        report = {
            "summary": PromptAnalytics._get_summary_stats(prompts),
            "quality_analysis": PromptAnalytics._get_quality_analysis(prompts),
            "category_analysis": PromptAnalytics._get_category_analysis(prompts),
            "content_analysis": PromptAnalytics._get_content_analysis(prompts),
        }

        return report

    @staticmethod
    def _get_summary_stats(prompts: List["GeneratedPrompt"]) -> Dict[str, Any]:
        """Estatísticas gerais dos prompts"""
        qualities = [p.quality_percentage for p in prompts]
        word_counts = [p.metrics.get("word_count", 0) for p in prompts]

        return {
            "total_prompts": len(prompts),
            "avg_quality": statistics.mean(qualities),
            "median_quality": statistics.median(qualities),
            "min_quality": min(qualities),
            "max_quality": max(qualities),
            "avg_word_count": statistics.mean(word_counts),
            "median_word_count": statistics.median(word_counts),
            "quality_distribution": {
                "excellent (>80%)": sum(1 for q in qualities if q > 80),
                "good (60-80%)": sum(1 for q in qualities if 60 <= q <= 80),
                "fair (40-60%)": sum(1 for q in qualities if 40 <= q < 60),
                "poor (<40%)": sum(1 for q in qualities if q < 40),
            },
        }

    @staticmethod
    def _get_quality_analysis(prompts: List["GeneratedPrompt"]) -> Dict[str, Any]:
        """Análise detalhada de qualidade"""
        metrics_count = defaultdict(int)
        total_prompts = len(prompts)

        for prompt in prompts:
            for metric, value in prompt.metrics.items():
                if isinstance(value, bool) and value:
                    metrics_count[metric] += 1

        return {
            "metrics_performance": {
                metric: {"count": count, "percentage": (count / total_prompts) * 100}
                for metric, count in metrics_count.items()
            },
            "common_issues": PromptAnalytics._identify_common_issues(prompts),
        }

    @staticmethod
    def _get_category_analysis(prompts: List["GeneratedPrompt"]) -> Dict[str, Any]:
        """Análise por categoria"""
        category_stats = defaultdict(list)

        for prompt in prompts:
            category_stats[prompt.category.nome].append(prompt.quality_percentage)

        analysis = {}
        for category, qualities in category_stats.items():
            analysis[category] = {
                "count": len(qualities),
                "avg_quality": statistics.mean(qualities),
                "min_quality": min(qualities),
                "max_quality": max(qualities),
                "consistency": statistics.stdev(qualities) if len(qualities) > 1 else 0,
            }

        return analysis

    @staticmethod
    def _get_content_analysis(prompts: List["GeneratedPrompt"]) -> Dict[str, Any]:
        """Análise de conteúdo dos prompts"""
        all_content = " ".join([p.content for p in prompts])
        words = all_content.lower().split()

        return {
            "most_common_words": dict(Counter(words).most_common(20)),
            "avg_sentence_length": PromptAnalytics._calculate_avg_sentence_length(
                prompts
            ),
            "readability_score": PromptAnalytics._calculate_readability(prompts),
        }

    @staticmethod
    def _identify_common_issues(prompts: List["GeneratedPrompt"]) -> List[str]:
        """Identifica problemas comuns nos prompts"""
        issues = []
        total = len(prompts)

        # Verifica métricas com baixa performance
        metrics_performance = defaultdict(int)
        for prompt in prompts:
            for metric, value in prompt.metrics.items():
                if isinstance(value, bool) and value:
                    metrics_performance[metric] += 1

        for metric, count in metrics_performance.items():
            percentage = (count / total) * 100
            if percentage < 50:
                issues.append(f"Baixa performance em {metric} ({percentage:.1f}%)")

        # Verifica comprimento
        word_counts = [p.metrics.get("word_count", 0) for p in prompts]
        short_prompts = sum(1 for wc in word_counts if wc < 200)
        if short_prompts > total * 0.3:
            issues.append(f"Muitos prompts muito curtos ({short_prompts}/{total})")

        return issues

    @staticmethod
    def _calculate_avg_sentence_length(prompts: List["GeneratedPrompt"]) -> float:
        """Calcula média de palavras por sentença"""
        total_sentences = 0
        total_words = 0

        for prompt in prompts:
            sentences = (
                prompt.content.count(".")
                + prompt.content.count("!")
                + prompt.content.count("?")
            )
            sentences = max(sentences, 1)  # Evita divisão por zero
            words = len(prompt.content.split())

            total_sentences += sentences
            total_words += words

        return total_words / total_sentences if total_sentences > 0 else 0

    @staticmethod
    def _calculate_readability(prompts: List["GeneratedPrompt"]) -> str:
        """Calcula score de legibilidade simplificado"""
        avg_word_length = []

        for prompt in prompts:
            words = prompt.content.split()
            if words:
                avg_length = sum(len(word) for word in words) / len(words)
                avg_word_length.append(avg_length)

        if not avg_word_length:
            return "N/A"

        avg = statistics.mean(avg_word_length)

        if avg < 5:
            return "Muito Fácil"
        elif avg < 6:
            return "Fácil"
        elif avg < 7:
            return "Médio"
        elif avg < 8:
            return "Difícil"
        else:
            return "Muito Difícil"
