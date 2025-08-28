import json
from concurrent.futures import ThreadPoolExecutor
from gerar_prompt_curriculos import gerar_prompt_curriculo
from gerar_prompt_finaceiro import gerar_prompt_financeiro
from gerar_prompt_suspensao import gerar_prompt_suspensao
import random

NUM_PROMPTS = 5000  # quantidade de prompts de cada tipo


# -------------------------
# Funções auxiliares
# -------------------------
def limpar_texto(texto: str) -> str:
    """Remove quebras de linha e espaços extras do texto."""
    return " ".join(texto.splitlines()).strip()


def gerar_um_prompt(i: int):
    """Gera os 3 tipos de prompts para um índice."""
    prompts = []
    for func in [
        gerar_prompt_curriculo,
        gerar_prompt_suspensao,
        gerar_prompt_financeiro,
    ]:
        # Se possível, modifique as funções para já retornarem dicionário
        prompt_json = json.loads(func(i))
        prompts.append({"text": limpar_texto(prompt_json["text"])})
    return prompts


# -------------------------
# Função principal
# -------------------------
def gerar_prompts(num_prompts=NUM_PROMPTS):
    """Gera todos os prompts e salva em JSONL de forma eficiente."""

    # --- Paralelização ---
    with ThreadPoolExecutor() as executor:
        all_prompts_nested = list(
            executor.map(gerar_um_prompt, range(1, num_prompts + 1))
        )

    # Flatten da lista
    all_prompts = [p for sublist in all_prompts_nested for p in sublist]

    # Embaralhar
    random.shuffle(all_prompts)

    # Escrever diretamente no arquivo
    with open("prompts.jsonl", "w", encoding="utf-8") as f:
        for idx, prompt in enumerate(all_prompts, start=1):
            f.write(
                json.dumps(
                    {"id": f"prompt_{idx:03d}", "text": prompt["text"]},
                    ensure_ascii=False,
                )
                + "\n"
            )

    print(f"{len(all_prompts)} prompts gerados e salvos em prompts.jsonl")


# -------------------------
# Funções de teste
# -------------------------
def testar_prompts(func, n=5):
    for i in range(1, n + 1):
        prompt_json = json.loads(func(i))
        print(limpar_texto(prompt_json["text"]))
        print("---------------------------")


if __name__ == "__main__":
    gerar_prompts()  # descomente para gerar todos os prompts

    # Exemplos de teste
    # testar_prompts(gerar_prompt_curriculo)
    # testar_prompts(gerar_prompt_suspensao)
    # testar_prompts(gerar_prompt_financeiro)
