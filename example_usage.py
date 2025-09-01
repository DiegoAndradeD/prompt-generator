from pathlib import Path
from main import ModularPromptGenerator
from config.settings import AppConfig, LLMConfig
from utils.export_utils import PromptExporter
from utils.analytics import PromptAnalytics


def example_basic_usage():
    """Exemplo básico de uso"""
    print("=" * 60)
    print("EXEMPLO 1: USO BÁSICO")
    print("=" * 60)

    # Configuração simples
    generator = ModularPromptGenerator()

    # Gerar um prompt aleatório
    prompt = generator.generate_prompt()
    if prompt:
        prompt.display_summary()


def example_custom_configuration():
    """Exemplo com configuração customizada"""
    print("\n" + "=" * 60)
    print("EXEMPLO 2: CONFIGURAÇÃO CUSTOMIZADA")
    print("=" * 60)

    # Configuração personalizada
    llm_config = LLMConfig(
        model="llama3:8b", temperature=0.8, top_p=0.95, num_predict=1000
    )

    app_config = AppConfig(
        examples_dir=Path("custom_examples"),
        default_profiles=5,
        default_examples=3,
        min_word_count=300,
        max_word_count=600,
        llm_config=llm_config,
    )

    generator = ModularPromptGenerator(app_config)

    # Gerar prompt para categoria específica
    categories = generator.get_available_categories()
    if categories:
        specific_category = categories[0]
        prompt = generator.generate_prompt(
            category_name=specific_category, num_profiles=4, num_examples=2
        )
        if prompt:
            prompt.display_summary()


def example_batch_generation_and_analysis():
    """Exemplo de geração em lote com análise"""
    print("\n" + "=" * 60)
    print("EXEMPLO 3: GERAÇÃO EM LOTE E ANÁLISE")
    print("=" * 60)

    generator = ModularPromptGenerator()

    # Geração em lote
    prompts = generator.batch_generate(num_prompts=5)

    if not prompts:
        print("❌ Nenhum prompt foi gerado")
        return

    print(f"\n✅ {len(prompts)} prompts gerados com sucesso!")

    # Análise dos resultados
    report = PromptAnalytics.generate_report(prompts)

    print("\n📊 RELATÓRIO DE ANÁLISE:")
    print("-" * 40)

    # Resumo
    summary = report["summary"]
    print(f"Qualidade média: {summary['avg_quality']:.1f}%")
    print(f"Palavras em média: {summary['avg_word_count']:.0f}")
    print(f"Distribuição de qualidade:")
    for level, count in summary["quality_distribution"].items():
        print(f"  • {level}: {count} prompts")

    # Análise por categoria
    print(f"\n📈 PERFORMANCE POR CATEGORIA:")
    for category, stats in report["category_analysis"].items():
        print(f"  • {category}: {stats['avg_quality']:.1f}% (n={stats['count']})")

    # Problemas identificados
    if report["quality_analysis"]["common_issues"]:
        print(f"\n⚠️  PROBLEMAS IDENTIFICADOS:")
        for issue in report["quality_analysis"]["common_issues"]:
            print(f"  • {issue}")


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


def example_quality_monitoring():
    """Exemplo de monitoramento de qualidade"""
    print("\n" + "=" * 60)
    print("EXEMPLO 5: MONITORAMENTO DE QUALIDADE")
    print("=" * 60)

    generator = ModularPromptGenerator()

    # Configurar thresholds de qualidade
    QUALITY_THRESHOLD = 70.0
    MIN_WORD_COUNT = 250

    successful_prompts = []
    attempts = 0
    max_attempts = 10

    while len(successful_prompts) < 3 and attempts < max_attempts:
        attempts += 1
        print(f"\n🔄 Tentativa {attempts}...")

        prompt = generator.generate_prompt()

        if prompt:
            quality_ok = prompt.quality_percentage >= QUALITY_THRESHOLD
            length_ok = prompt.metrics.get("word_count", 0) >= MIN_WORD_COUNT

            if quality_ok and length_ok:
                successful_prompts.append(prompt)
                print(
                    f"✅ Prompt aprovado! Qualidade: {prompt.quality_percentage:.1f}%"
                )
            else:
                issues = []
                if not quality_ok:
                    issues.append(f"qualidade baixa ({prompt.quality_percentage:.1f}%)")
                if not length_ok:
                    issues.append(
                        f"muito curto ({prompt.metrics.get('word_count', 0)} palavras)"
                    )
                print(f"❌ Prompt rejeitado: {', '.join(issues)}")

    print(f"\n📋 RESUMO DO MONITORAMENTO:")
    print(f"• Prompts aprovados: {len(successful_prompts)}")
    print(f"• Total de tentativas: {attempts}")
    print(f"• Taxa de aprovação: {(len(successful_prompts)/attempts)*100:.1f}%")


def example_category_specific_generation():
    """Exemplo de geração específica por categoria"""
    print("\n" + "=" * 60)
    print("EXEMPLO 6: GERAÇÃO ESPECÍFICA POR CATEGORIA")
    print("=" * 60)

    generator = ModularPromptGenerator()
    categories = generator.get_available_categories()

    if not categories:
        print("❌ Nenhuma categoria disponível")
        return

    # Testar cada categoria
    category_results = {}

    for category in categories:
        print(f"\n🎯 Testando categoria: {category.upper()}")

        # Gerar 2 prompts para esta categoria
        category_prompts = []
        for i in range(2):
            prompt = generator.generate_prompt(category_name=category)
            if prompt:
                category_prompts.append(prompt)

        if category_prompts:
            avg_quality = sum(p.quality_percentage for p in category_prompts) / len(
                category_prompts
            )
            category_results[category] = {
                "count": len(category_prompts),
                "avg_quality": avg_quality,
                "prompts": category_prompts,
            }
            print(
                f"  ✅ {len(category_prompts)} prompts gerados, qualidade média: {avg_quality:.1f}%"
            )
        else:
            print(f"  ❌ Falha ao gerar prompts para {category}")

    # Ranking de categorias por qualidade
    if category_results:
        print(f"\n🏆 RANKING DE CATEGORIAS POR QUALIDADE:")
        sorted_categories = sorted(
            category_results.items(), key=lambda x: x[1]["avg_quality"], reverse=True
        )

        for i, (category, stats) in enumerate(sorted_categories, 1):
            print(
                f"  {i}. {category}: {stats['avg_quality']:.1f}% ({stats['count']} prompts)"
            )


def main():
    """Executa todos os exemplos"""
    print("🚀 SISTEMA MODULAR DE GERAÇÃO DE PROMPTS")
    print("Executando exemplos de uso...")

    try:
        example_basic_usage()
        example_custom_configuration()
        example_batch_generation_and_analysis()
        example_export_functionality()
        example_quality_monitoring()
        example_category_specific_generation()

        print(f"\n{'='*60}")
        print("✅ TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO!")
        print(f"{'='*60}")

    except Exception as e:
        print(f"\n❌ ERRO DURANTE EXECUÇÃO: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
