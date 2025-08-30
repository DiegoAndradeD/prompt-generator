import json
from pathlib import Path
import random
import re
import ollama

from pii_generator import PIIGenerator


class ModularPromptGenerator:
    def __init__(self, examples_dir="examples"):
        self.examples_dir = Path(examples_dir)
        self.pii_factory = PIIGenerator()
        self.categories = {}
        self.load_all_categories()

    def load_all_categories(self):
        if not self.examples_dir.exists():
            print(f"⚠️  Diretório {self.examples_dir} não existe. Criando...")
            self.examples_dir.mkdir(exist_ok=True)
            return

        json_files = list(self.examples_dir.glob("*.json"))

        if not json_files:
            print(f"⚠️  Nenhum arquivo de exemplo encontrado em {self.examples_dir}")
            return

        for file_path in json_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    categoria = data.get("categoria", file_path.stem)
                    self.categories[categoria] = data
                    print(
                        f"✅ Carregada categoria '{categoria}' com {len(data.get('exemplos', []))} exemplos"
                    )
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"❌ Erro ao carregar {file_path}: {e}")

    def get_examples_by_category(self, categoria, max_examples=3):
        if categoria not in self.categories:
            return []

        exemplos = self.categories[categoria].get("exemplos", [])
        if not exemplos:
            return []

        random.shuffle(exemplos)
        selected = exemplos[:max_examples]

        return [
            {
                "categoria": categoria,
                "subcategoria": ex.get("subcategoria", "geral"),
                "complexidade": ex.get("nivel_complexidade", "medio"),
                "prompt": ex.get("prompt", ex.get("texto", "")),
            }
            for ex in selected
        ]

    def build_specialized_prompt(self, categoria, profiles, num_examples=3):
        examples = self.get_examples_by_category(categoria, num_examples)

        if not examples:
            return None

        categoria_info = self.categories[categoria]
        descricao = categoria_info.get("descricao", f"Prompts de {categoria}")

        examples_text = ""
        for i, ex in enumerate(examples, 1):
            examples_text += f"\n{'='*60}\n"
            examples_text += (
                f"EXEMPLO {i} - {categoria.upper()} ({ex['subcategoria']})\n"
            )
            examples_text += f"Complexidade: {ex['complexidade']}\n"
            examples_text += f"{'='*60}\n"
            examples_text += f'"{ex["prompt"]}"\n'

        prompt = f"""
Você é um especialista sênior em Recursos Humanos, especializado em {descricao.lower()}.

CATEGORIA FOCO: {categoria.upper()}
EXPERTISE: {descricao}

EXEMPLOS DE REFERÊNCIA DE ALTA QUALIDADE:
{examples_text}

PERFIS FICTÍCIOS DISPONÍVEIS:
{[str(p) for p in profiles]}

MISSÃO:
Crie UM prompt profissional e detalhado da categoria {categoria.upper()}, seguindo exatamente o padrão dos exemplos acima.

DIRETRIZES ESPECÍFICAS PARA {categoria.upper()}:
✅ Use dados específicos dos perfis (nomes, CPFs, números, datas)
✅ Inclua detalhes técnicos relevantes para {categoria}
✅ Mantenha o nível de complexidade similar aos exemplos
✅ Linguagem professional, dissertativa e fluida
✅ Entre 200-500 palavras
✅ Inclua próximos passos e responsáveis quando aplicável

IMPORTANTE: Responda APENAS com o texto do prompt final, sem comentários adicionais.
"""
        return prompt

    def generate_prompt(self, num_profiles=3, num_examples=4):
        if not self.categories:
            print("❌ Nenhuma categoria disponível!")
            return None

        categoria_escolhida = random.choice(list(self.categories.keys()))

        print(f"🎲 Categoria sorteada: {categoria_escolhida.upper()}")

        profiles = [
            self.pii_factory.get_full_profile(sex=random.choice(["M", "F"]))
            for _ in range(num_profiles)
        ]

        prompt = self.build_specialized_prompt(
            categoria_escolhida, profiles, num_examples
        )

        if not prompt:
            print(f"❌ Erro ao construir prompt para categoria '{categoria_escolhida}'")
            return None

        print(f">>> Gerando prompt especializado em '{categoria_escolhida.upper()}'...")

        response = ollama.chat(
            model="llama3:8b",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um especialista em RH focado em criar prompts de alta qualidade. Sempre responda de forma precisa, detalhada e profissional.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            options={
                "temperature": 0.65,
                "top_p": 0.87,
                "top_k": 45,
                "repeat_penalty": 1.12,
                "num_predict": 650,
                "stop": ["---", "EXEMPLO", "DIRETRIZES", "OBSERVAÇÃO", "\n\nNota:"],
            },
        )

        return self.clean_response(response["message"]["content"], categoria_escolhida)

    def clean_response(self, texto, categoria):
        prefixes = [r"^(Prompt:|Texto:|Aqui está.*?:|Para.*?:)\s*"]
        for prefix in prefixes:
            texto = re.sub(prefix, "", texto.strip(), flags=re.IGNORECASE)

        suffixes = [
            r"\s*(---.*|EXEMPLO.*|NOTA:.*|OBSERVAÇÃO:.*|Espero.*|Fico.*|Aguardo.*)$"
        ]
        for suffix in suffixes:
            texto = re.sub(suffix, "", texto, flags=re.IGNORECASE | re.DOTALL)

        return texto.strip()

    def evaluate_quality(self, texto, categoria=None):
        base_metrics = {
            "word_count": len(texto.split()),
            "has_cpf": bool(re.search(r"\d{3}\.?\d{3}\.?\d{3}-?\d{2}", texto)),
            "has_names": bool(re.search(r"[A-Z][a-z]+\s+[A-Z][a-z]+", texto)),
            "has_specific_data": bool(
                re.search(r"(\d{1,2}/\d{1,2}/\d{4}|R\$\s*\d+|\d{5}-?\d{3})", texto)
            ),
            "ideal_length": 200 <= len(texto.split()) <= 500,
        }

        category_metrics = {}
        if categoria == "suspensao":
            category_metrics = {
                "has_evidence": bool(
                    re.search(
                        r"(evidência|testemunha|relatório|laudo)", texto, re.IGNORECASE
                    )
                ),
                "has_period": bool(
                    re.search(r"(\d+\s*(dia|semana|mês))", texto, re.IGNORECASE)
                ),
            }
        elif categoria == "financeiro":
            category_metrics = {
                "has_values": bool(re.search(r"R\$\s*[\d.,]+", texto)),
                "has_calculations": bool(
                    re.search(
                        r"(análise|cálculo|auditoria|crédito)", texto, re.IGNORECASE
                    )
                ),
            }
        elif categoria == "avaliacao":
            category_metrics = {
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
            }

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


def main():
    generator = ModularPromptGenerator()
    texto_gerado = generator.generate_prompt(num_profiles=3, num_examples=4)
    if not texto_gerado:
        print("❌ Falha na geração do prompt")
        return

    print(f"\n{'='*80}")
    print(f"🎯 PROMPT GERADO")
    print(f"{'='*80}")
    print(texto_gerado)
    print(f"{'='*80}")

    metrics, score, max_score = generator.evaluate_quality(texto_gerado)

    print(f"\n📊 MÉTRICAS DE QUALIDADE:")
    print(f"- Palavras: {metrics['word_count']}")
    print(f"- CPF presente: {'✅' if metrics['has_cpf'] else '❌'}")
    print(f"- Nomes próprios: {'✅' if metrics['has_names'] else '❌'}")
    print(f"- Dados específicos: {'✅' if metrics['has_specific_data'] else '❌'}")
    print(f"- Comprimento ideal: {'✅' if metrics['ideal_length'] else '❌'}")
    print(f"- Score final: {score}/{max_score}")


if __name__ == "__main__":
    main()
