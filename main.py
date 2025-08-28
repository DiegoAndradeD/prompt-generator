from gerar_prompt_suspensao import gerar_prompt_suspensao


if __name__ == "__main__":
    print(
        "--- Gerando prompts V4.0 com Multi-Contexto, Entidades Densas e Inconsistências ---\n"
    )
    for i in range(1, 25):  # Gerar exemplos
        print(gerar_prompt_suspensao(i))
