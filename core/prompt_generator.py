import json
import random

from utils.generator_utils import (
    apply_persona_to_text,
    combine_blocks,
    dict_to_safe_namespace,
    inject_text_error,
)


class PromptGenerator:
    def __init__(self, intent_config: dict, data_generator_func: callable):
        """
        Inicializa o gerador de prompts.
        :param intent_config: Um dicionário contendo 'personas', 'blocos_de_contexto' e 'intent_name'.
        :param data_generator_func: A função que gera os dados fictícios para o prompt.
        """
        self.personas = intent_config["personas"]
        self.blocos = intent_config["blocos_de_contexto"]
        self.intent_name = intent_config["intent_name"]
        self.data_generator = data_generator_func

    def _assemble_prompt_parts(self, dados: dict) -> list:
        """
        Monta as partes do prompt com base na configuração.
        Este método pode ser sobrescrito por subclasses se a montagem for mais complexa.
        """
        partes = []
        blocos_intent = self.blocos[self.intent_name]

        # Estrutura padrão de montagem
        partes.append(random.choice(blocos_intent["tarefa_principal"]))

        # Bloco de justificativa/contexto pode ter nomes diferentes
        if "justificativa" in blocos_intent:
            partes.append(random.choice(blocos_intent["justificativa"]))
        elif "contexto_dados" in blocos_intent:
            partes.append(random.choice(blocos_intent["contexto_dados"]))

        # Lógica para o bloco de narrativa baseado em uma chave dos dados
        # O nome da chave (ex: 'motivo_chave', 'tipo_analise_chave') deve estar nos dados
        narrativa_key = dados.get("motivo_chave") or dados.get("tipo_analise_chave")
        if narrativa_key and narrativa_key in blocos_intent["narrativa"]:
            partes.append(random.choice(blocos_intent["narrativa"][narrativa_key]))

        # Blocos secundários
        blocos_secundarios, _ = combine_blocks(blocos_intent["bloco_secundario"], 4, 6)
        partes.extend(blocos_secundarios)

        return partes

    def generate(self, prompt_id: int):
        """
        Executa o fluxo completo de geração de um prompt.
        """
        # 1. Escolher Persona
        persona_chave = random.choice(list(self.personas.keys()))
        persona = self.personas[persona_chave]

        # 2. Gerar Dados
        dados_dict = self.data_generator()

        # 3. Montar o conteúdo do prompt
        partes_do_prompt = self._assemble_prompt_parts(dados_dict)
        conteudo_prompt = " ".join(partes_do_prompt)

        # 4. Aplicar Persona
        prompt_com_persona = apply_persona_to_text(conteudo_prompt, persona)

        # 5. Formatar com dados
        dados_obj = dict_to_safe_namespace(dados_dict)
        texto_final = prompt_com_persona.format(**vars(dados_obj))

        # 6. Injetar Erro
        if random.random() < persona.get("chance_de_erro", 0.05):
            texto_final = inject_text_error(texto_final)

        # 7. Retornar JSON
        return json.dumps(
            {
                # "id": prompt_id,
                # "intent": self.intent_name,
                # "persona": persona_chave,
                "text": texto_final,
            },
            ensure_ascii=False,
            indent=2,
        )
