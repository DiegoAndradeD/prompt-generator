from pathlib import Path
from modular_prompt_generator import ModularPromptGenerator
from utils.export_utils import PromptExporter


def main():
    """Exemplo de funcionalidades de exportação"""
    print("\n" + "=" * 60)
    print("EXEMPLO 4: EXPORTAÇÃO DE DADOS")
    print("=" * 60)

    generator = ModularPromptGenerator()

    # Gerar alguns prompts
    prompts = generator.batch_generate(num_prompts=100)

    if not prompts:
        print("❌ Nenhum prompt para exportar")
        return

    # Exportar para JSON
    json_file = Path("outputs/prompts_export.jsonl")
    json_file.parent.mkdir(exist_ok=True)

    success_jsonl = PromptExporter.export_to_jsonl(prompts, json_file)

    if success_jsonl:
        print("✅ Dados exportados com sucesso para JSON e CSV!")


if __name__ == "__main__":
    main()
