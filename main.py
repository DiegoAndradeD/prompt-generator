import json
from pathlib import Path
import random
from config.settings import AppConfig, LLMConfig
from modular_prompt_generator import ModularPromptGenerator
from utils.export_utils import PromptExporter


def main():
    # Configuração LLM e App
    custom_llm_config = LLMConfig(temperature=0.7, top_p=0.9, num_predict=800)
    config = AppConfig(
        examples_dir=Path("examples"),
        default_profiles=3,
        default_examples=4,
        llm_config=custom_llm_config,
    )

    # Inicializa gerador
    generator = ModularPromptGenerator(config)

    # Exibe categorias disponíveis
    categories = generator.get_available_categories()
    if categories:
        print(f"📂 Categorias disponíveis: {', '.join(categories)}")

    # Gera um prompt único
    generated_prompt = generator.generate_prompt(category_name="comunicacao_interna")
    if generated_prompt:
        generated_prompt.display_summary()
    else:
        print("❌ Falha na geração do prompt")

    # Geração em lote
    # print(f"\n{'='*80}")
    # print("🔄 EXEMPLO DE GERAÇÃO EM LOTE")
    # print(f"{'='*80}")

    # batch_results = generator.batch_generate(
    #     num_prompts=5
    # )  # você pode alterar a quantidade

    # if batch_results:
    #     avg_quality = sum(p.quality_percentage for p in batch_results) / len(
    #         batch_results
    #     )
    #     print(f"\n📈 Resumo do lote:")
    #     print(f"- Prompts gerados: {len(batch_results)}")
    #     print(f"- Qualidade média: {avg_quality:.1f}%")

    #     # Estatísticas por categoria
    #     category_stats = {}
    #     for prompt in batch_results:
    #         cat = prompt.category.nome
    #         if cat not in category_stats:
    #             category_stats[cat] = []
    #         category_stats[cat].append(prompt.quality_percentage)
    #     print(f"- Por categoria:")
    #     for cat, qualities in category_stats.items():
    #         avg_cat_quality = sum(qualities) / len(qualities)
    #         print(f"  • {cat}: {avg_cat_quality:.1f}% ({len(qualities)} prompts)")

    #     # Exibe todos os prompts gerados com detalhes
    #     print(f"\n{'='*80}")
    #     print("📄 TODOS OS PROMPTS GERADOS")
    #     print(f"{'='*80}")
    #     for i, prompt in enumerate(batch_results, start=1):
    #         print(f"\n--- Prompt {i} ---")
    #         prompt.display_summary()


def example_export_functionality():
    """Exemplo de funcionalidades de exportação"""
    print("\n" + "=" * 60)
    print("EXEMPLO 4: EXPORTAÇÃO DE DADOS")
    print("=" * 60)

    generator = ModularPromptGenerator()

    # Gerar alguns prompts
    prompts = generator.batch_generate(num_prompts=3)

    if not prompts:
        print("❌ Nenhum prompt para exportar")
        return

    # Exportar para JSON
    json_file = Path("outputs/prompts_export.json")
    json_file.parent.mkdir(exist_ok=True)

    success_json = PromptExporter.export_to_json(prompts, json_file)

    # Exportar para CSV
    csv_file = Path("outputs/prompts_export.csv")
    success_csv = PromptExporter.export_to_csv(prompts, csv_file)

    if success_json and success_csv:
        print("✅ Dados exportados com sucesso para JSON e CSV!")


if __name__ == "__main__":
    example_export_functionality()
