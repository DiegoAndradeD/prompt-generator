import json
import random
from concurrent.futures import ThreadPoolExecutor

from core.prompt_generator import PromptGenerator
from modules.financial.config import CONFIG_FINANCEIRO
from modules.financial.data_generator import gerar_dados_financeiros
from modules.resumes.config import CONFIG_CURRICULOS
from modules.resumes.data_generator import generate_curriculum_data
from modules.suspension.config import CONFIG_SUSPENSAO
from modules.suspension.data_generator import gerar_dados_aninhados

suspensao_generator = PromptGenerator(CONFIG_SUSPENSAO, gerar_dados_aninhados)
financeiro_generator = PromptGenerator(CONFIG_FINANCEIRO, gerar_dados_financeiros)
curriculos_generator = PromptGenerator(CONFIG_CURRICULOS, generate_curriculum_data)

NUM_PROMPTS = 5000


def limpar_texto(texto: str) -> str:
    return " ".join(texto.splitlines()).strip()


def gerar_um_prompt(i: int):
    prompts = []
    for generator in [curriculos_generator, suspensao_generator, financeiro_generator]:
        prompt_json = generator.generate(prompt_id=i)

        if isinstance(prompt_json, str):
            prompt_json = json.loads(prompt_json)

        prompts.append({"text": limpar_texto(prompt_json["text"])})
    return prompts


def gerar_prompts(num_prompts=NUM_PROMPTS):
    with ThreadPoolExecutor() as executor:
        all_prompts_nested = list(
            executor.map(gerar_um_prompt, range(1, num_prompts + 1))
        )

    all_prompts = [p for sublist in all_prompts_nested for p in sublist]

    random.shuffle(all_prompts)

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


def testar_prompts(generator, n=5):
    for i in range(1, n + 1):
        prompt_json = generator.generate(prompt_id=i)
        print(limpar_texto(prompt_json["text"]))
        print("---------------------------")


if __name__ == "__main__":
    gerar_prompts()

    # Exemplos de teste
    # testar_prompts(curriculos_generator)
    # testar_prompts(suspensao_generator)
    # testar_prompts(financeiro_generator)
