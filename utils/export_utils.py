import json
import csv
from typing import List
from pathlib import Path
from datetime import datetime

from modular_prompt_generator import GeneratedPrompt


class PromptExporter:

    @staticmethod
    def export_to_json(prompts: List["GeneratedPrompt"], output_file: Path) -> bool:
        try:
            data = {
                "export_date": datetime.now().isoformat(),
                "total_prompts": len(prompts),
                "prompts": [prompt.to_dict() for prompt in prompts],
            }

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"✅ Prompts exportados para {output_file}")
            return True

        except Exception as e:
            print(f"❌ Erro ao exportar JSON: {e}")
            return False

    @staticmethod
    def export_to_csv(prompts: List["GeneratedPrompt"], output_file: Path) -> bool:
        try:
            with open(output_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)

                writer.writerow(
                    [
                        "categoria",
                        "descricao_categoria",
                        "content",
                        "word_count",
                        "quality_score",
                        "quality_percentage",
                        "has_cpf",
                        "has_names",
                        "has_specific_data",
                        "ideal_length",
                    ]
                )

                for prompt in prompts:
                    writer.writerow(
                        [
                            prompt.category.nome,
                            prompt.category.descricao,
                            prompt.content,
                            prompt.metrics.get("word_count", 0),
                            prompt.quality_score,
                            f"{prompt.quality_percentage:.1f}%",
                            prompt.metrics.get("has_cpf", False),
                            prompt.metrics.get("has_names", False),
                            prompt.metrics.get("has_specific_data", False),
                            prompt.metrics.get("ideal_length", False),
                        ]
                    )

            print(f"✅ Prompts exportados para {output_file}")
            return True

        except Exception as e:
            print(f"❌ Erro ao exportar CSV: {e}")
            return False

    @staticmethod
    def export_to_jsonl(prompts: List["GeneratedPrompt"], output_file: Path) -> bool:
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                for i, prompt in enumerate(prompts):
                    clean_text = " ".join(
                        prompt.content.replace("\n", " ")
                        .replace("\r", " ")
                        .replace("\t", " ")
                        .split()
                    )

                    jsonl_data = {
                        "prompt_id": i + 1,
                        "text": clean_text,
                    }

                    f.write(json.dumps(jsonl_data, ensure_ascii=False) + "\n")

            print(f"✅ Prompts exportados para {output_file} (formato JSONL)")
            return True

        except Exception as e:
            print(f"❌ Erro ao exportar JSONL: {e}")
            return False
