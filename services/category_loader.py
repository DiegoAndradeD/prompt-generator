import json
from pathlib import Path
from typing import Dict, Optional
from models.category import Category, Example


class CategoryLoader:
    """Responsável por carregar categorias de arquivos JSON"""

    def __init__(self, examples_dir: Path):
        self.examples_dir = examples_dir

    def load_all_categories(self) -> Dict[str, Category]:
        """Carrega todas as categorias disponíveis"""
        categories = {}

        if not self._ensure_directory_exists():
            return categories

        json_files = list(self.examples_dir.glob("*.json"))

        if not json_files:
            print(f"⚠️  Nenhum arquivo de exemplo encontrado em {self.examples_dir}")
            return categories

        for file_path in json_files:
            category = self._load_category_from_file(file_path)
            if category:
                categories[category.nome] = category

        return categories

    def _ensure_directory_exists(self) -> bool:
        """Garante que o diretório existe"""
        if not self.examples_dir.exists():
            print(f"⚠️  Diretório {self.examples_dir} não existe. Criando...")
            self.examples_dir.mkdir(exist_ok=True)
            return False
        return True

    def _load_category_from_file(self, file_path: Path) -> Optional[Category]:
        """Carrega uma categoria de um arquivo específico"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            category_name = data.get("categoria", file_path.stem)
            description = data.get("descricao", f"Prompts de {category_name}")

            examples = []
            for ex_data in data.get("exemplos", []):
                example = Example(
                    prompt=ex_data.get("prompt", ex_data.get("texto", "")),
                    subcategoria=ex_data.get("subcategoria", "geral"),
                    complexidade=ex_data.get("nivel_complexidade", "medio"),
                    metadata=ex_data.get("metadata", {}),
                )
                examples.append(example)

            category = Category(
                nome=category_name,
                descricao=description,
                exemplos=examples,
                diretrizes_especificas=data.get("diretrizes_especificas", []),
                metricas_qualidade=data.get("metricas_qualidade", {}),
            )

            print(
                f"✅ Carregada categoria '{category_name}' com {len(examples)} exemplos"
            )
            return category

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"❌ Erro ao carregar {file_path}: {e}")
            return None
