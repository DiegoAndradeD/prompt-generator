import json
import random
from types import SimpleNamespace
from faker import Faker

# Supondo que todas as suas funções geradoras (novas e antigas)
# estão em um arquivo chamado `utils.generator_utils`.
from utils.generator_utils import (
    apply_persona_to_text,
    combine_blocks,
    generate_company_entity,
    generate_location_entity,
    generate_person_entity,
    generate_random_dates,
    inject_text_error,
    introduce_inconsistency,
)

# --- SETUP ---
fake = Faker("pt_BR")


# Classe auxiliar para formatar strings sem erro se a chave não existir
class SafeNamespace(SimpleNamespace):
    """
    Uma versão de SimpleNamespace que não levanta AttributeError.
    Se um atributo não for encontrado, retorna um texto indicando a chave faltante.
    """

    def __getattr__(self, name):
        # Retorna um placeholder em vez de quebrar o programa
        return f"{{{name}_NAO_ENCONTRADO}}"


def dict_to_safe_namespace(d: dict):
    """
    Converte recursivamente um dicionário em um SafeNamespace.
    Isso permite o acesso aninhado (ex: dados.funcionario.documentos.cpf)
    de forma segura.
    """
    if not isinstance(d, dict):
        return d

    # Converte todos os sub-dicionários recursivamente
    for key, value in d.items():
        d[key] = dict_to_safe_namespace(value)

    return SafeNamespace(**d)


# Personas (sem alterações)
PERSONAS = {
    "Gestor Direto": {
        "prefixos": [
            "Urgente:",
            "Rápido:",
            "Para ontem:",
            "Ação imediata:",
            "Precisamos priorizar:",
            "Não podemos atrasar:",
            "Atenção imediata:",
            "Prioridade máxima:",
        ],
        "sufixos": [
            "Preciso disso resolvido até o fim do dia.",
            "Agilize, por favor.",
            "Sem mais delongas.",
            "Aguardo retorno urgente.",
            "Não deixe pendente.",
        ],
        "chance_de_erro": 0.10,
    },
    "Analista Detalhista": {
        "prefixos": [
            "Prezados, bom dia.",
            "Segue para análise e processamento a seguinte demanda:",
            "Venho por meio deste solicitar formalmente:",
            "Olá, equipe.",
            "Encaminho com instruções detalhadas:",
            "Solicito revisão cuidadosa sobre o seguinte:",
            "Favor conferir atentamente:",
        ],
        "sufixos": [
            "Desde já, agradeço a atenção.",
            "Qualquer dúvida, estou à disposição para esclarecimentos.",
            "Favor arquivar a documentação comprobatória.",
            "Agradeço se puderem confirmar o recebimento.",
            "Peço feedback após a análise completa.",
        ],
        "chance_de_erro": 0.05,
    },
    "Colega Informal": {
        "prefixos": [
            "Oi gente, tudo bem?",
            "E aí, preciso de uma ajuda aqui:",
            "Seguinte:",
            "Alguém pode dar uma força com isso?",
            "Galera, rapidinho:",
            "Pessoal, me deem um toque sobre:",
            "Então, pessoal, olha só:",
        ],
        "sufixos": [
            "Valeu!",
            "Brigado!",
            "Abs!",
            "Depois me avisem quando estiver pronto, vlw!!",
            "Fico no aguardo :)",
            "Qualquer coisa, chama no chat!",
        ],
        "chance_de_erro": 0.30,
    },
    "RH": {
        "prefixos": [
            "Prezados,",
            "Encaminho para ciência e providências:",
            "Conforme deliberação anterior:",
            "Informamos para registro interno:",
            "Segue comunicado oficial do RH:",
        ],
        "sufixos": [
            "Atenciosamente, Departamento de Recursos Humanos.",
            "Fica o registro nos autos do setor de pessoal.",
            "Providenciem a devida comunicação formal ao envolvido.",
            "Favor manter confidencialidade conforme política interna.",
            "Registro arquivado para futuras auditorias.",
        ],
        "chance_de_erro": 0.03,
    },
    "Jurídico": {
        "prefixos": [
            "Conforme legislação vigente,",
            "Considerando os dispositivos legais aplicáveis e o parecer do nosso advogado {advogado_interno.nome},",
            "Nos termos do Art. 482 da CLT,",
            "À luz do parecer jurídico interno,",
            "Em observância às normas legais e regulatórias,",
        ],
        "sufixos": [
            "Este comunicado deve observar o rito disciplinar previsto.",
            "Manter registro arquivado junto ao departamento jurídico para fins de auditoria.",
            "Garantir o contraditório e a ampla defesa do colaborador é mandatório.",
            "Recomenda-se acompanhamento jurídico antes de qualquer ação.",
            "As providências devem seguir estritamente a legislação vigente.",
        ],
        "chance_de_erro": 0.02,
    },
    "Cliente Exigente": {
        "prefixos": [
            "Atente-se,",
            "Importante:",
            "Gostaria de reforçar que:",
            "Por favor, observe com atenção:",
        ],
        "sufixos": [
            "Espero uma resposta rápida e precisa.",
            "Não aceito atrasos nesta entrega.",
            "Favor confirmar cada detalhe antes do envio.",
            "Conto com máxima prioridade nesta demanda.",
        ],
        "chance_de_erro": 0.15,
    },
    "Mentor/Coach": {
        "prefixos": [
            "Reflita sobre:",
            "Considere o seguinte ponto:",
            "Para seu desenvolvimento:",
            "Uma sugestão baseada na experiência:",
        ],
        "sufixos": [
            "Pense nisso antes de tomar decisões.",
            "Recomendo analisar cuidadosamente os detalhes.",
            "Estamos aqui para aprender juntos.",
            "Esta reflexão pode ajudá-lo a melhorar seus resultados.",
        ],
        "chance_de_erro": 0.05,
    },
}


# --- FONTES DE DADOS (sem alterações) ---
MOTIVOS_DISCIPLINARES = {
    "atestado_suspeito": "apresentação de um atestado médico com suspeita de fraude",
    "insubordinacao": "insubordinação direta a um superior",
    "atraso_reiterado": "reiterados atrasos sem justificativa",
    "conduta_inadequada": "conduta inadequada em ambiente corporativo",
    "uso_incorreto_recursos": "uso indevido de recursos da empresa para fins pessoais",
    "assedio": "comportamento caracterizado como assédio moral contra colegas",
    "embriaguez": "comparecimento ao trabalho sob efeito de álcool",
    "negligencia": "negligência no cumprimento de atividades críticas",
    "conflito_interno": "conflito aberto com outro colaborador em ambiente de trabalho",
    "quebra_sigilo": "quebra de sigilo de informações estratégicas da empresa",
    "desrespeito_politicas": "desrespeito às políticas internas da empresa",
    "falta_repetida": "faltas recorrentes sem justificativa formal",
    "divulgacao_informacoes": "divulgação não autorizada de informações confidenciais",
    "associacao_inadequada": "associação com atividades externas que geram conflito de interesse",
    "uso_mau_conduta_digital": "uso inadequado de recursos digitais e redes corporativas",
    "insatisfacao_clientes": "comportamento que resultou em reclamações graves de clientes",
    "furtos": "apropriação indevida de bens da empresa",
    "violencia": "atos de violência ou ameaça contra colegas ou superiores",
    "discriminacao": "comportamento discriminatório com base em raça, gênero ou orientação sexual",
    "violar_normas_seguranca": "descumprimento de normas de segurança do trabalho",
    "comportamento_abusivo": "atos de abuso verbal ou físico no ambiente corporativo",
}

HOSPITAIS = [
    "Hospital Central de Simões Filho",
    "Clínica Integrada da Bahia",
    "Hospital Esperança",
    "UPA de Camaçari",
    "Hospital Municipal de Lauro de Freitas",
    "Clínica São Lucas",
    "Hospital Regional de Santo Antônio de Jesus",
    "UPA de Feira de Santana",
    "Hospital de Urgência e Emergência de Salvador",
    "Clínica Vida Plena",
]

ORG_PUB = [
    "Prefeitura de Salvador",
    "Ministério do Trabalho e Emprego",
    "Secretaria Estadual de Saúde da Bahia",
    "Prefeitura de Salvador",
    "Tribunal de Contas do Estado da Bahia",
    "Ministério da Educação",
    "Secretaria Municipal de Segurança Pública",
    "Prefeitura de Camaçari",
    "Instituto Nacional do Seguro Social (INSS)",
    "Secretaria de Assistência Social do Estado da Bahia",
]


# --- BLOCOS DE CONTEXTO ATUALIZADOS ---
# ATENÇÃO: As chaves foram atualizadas para refletir a nova estrutura aninhada
blocos_de_contexto = {
    "documentar_suspensao": {
        "tarefa_principal": [
            "Elabore o comunicado de suspensão para o(a) funcionário(a) {funcionario.nome}, CPF {funcionario.documentos.cpf}, matrícula {funcionario.profissional.matricula}, ocupante do cargo de {funcionario.profissional.cargo}.",
            "Redija o documento de suspensão disciplinar referente ao(a) colaborador(a) {funcionario.nome}, considerando seu histórico e o incidente recente.",
            "Produza um relatório formal de suspensão para {funcionario.nome}, detalhando o incidente e os procedimentos adotados.",
            "Prepare a notificação de suspensão para {funcionario.nome}, com referência ao histórico funcional e registros internos.",
        ],
        "justificativa": [
            "A medida se justifica em razão de {motivo_descritivo}, que viola diretamente nossas políticas internas.",
            "O afastamento temporário é necessário considerando a gravidade de {motivo_descritivo}, conforme apurado pelo gestor {supervisor.nome}.",
            "A suspensão é aplicada para resguardar a integridade do ambiente de trabalho diante de {motivo_descritivo}.",
            "O procedimento atende às normas internas e à legislação vigente, tendo em vista {motivo_descritivo}.",
        ],
        "narrativa": {
            "atestado_suspeito": [
                "O(A) colaborador(a) apresentou atestado médico do {hospital.nome} (CNPJ: {hospital.cnpj}), localizado em {hospital.endereco}, que levantou suspeitas após verificação de autenticidade pelo RH {rh_responsavel.nome}, especialmente porque a testemunha {testemunha.nome} (mat. {testemunha.profissional.matricula}) relatou ter visto o funcionário em outro local na mesma data.",
                "Verificações adicionais conduzidas pelo RH indicaram inconsistências no atestado apresentado, motivando a suspensão preventiva de {funcionario.nome}.",
                "O documento médico apresentado não corresponde às informações oficiais, conforme conferido com {hospital.nome}, justificando a medida disciplinar.",
            ],
            "insubordinacao": [
                "Durante a execução de um projeto para o cliente {cliente.razao_social}, o(a) colaborador(a) se recusou a cumprir instruções diretas de seu supervisor {supervisor.nome}, na presença do auditor {auditor_externo.nome}, o que constitui clara insubordinação.",
                "O comportamento insubordinado foi registrado em ata de reunião datada de {data_incidente}, evidenciando a recusa em seguir protocolos internos.",
                "A insubordinação gerou impacto direto no andamento das atividades, sendo necessária a intervenção formal do RH.",
            ],
            "atraso_reiterado": [
                "Registros de ponto eletrônico, auditados por {auditor_externo.nome}, indicam atrasos frequentes e não justificados que impactaram entregas ao cliente {cliente.razao_social}, cujo contato principal é {cliente.contato_principal.nome} ({cliente.contato_principal.email}).",
                "Os atrasos recorrentes comprometeram prazos críticos, motivando a suspensão disciplinar como medida corretiva.",
                "Apesar de advertências anteriores, o funcionário manteve padrão de atrasos, afetando a operação da equipe.",
            ],
            "conduta_inadequada": [
                "Houve relatos de conduta inadequada em reuniões com representantes da {cliente.razao_social}, confirmados pela testemunha {testemunha.nome}, o que gerou uma queixa formalizada.",
                "O comportamento do colaborador violou normas de etiqueta corporativa, registradas pelo RH e testemunhas presentes.",
                "Ocorreram manifestações verbais e atitudes consideradas impróprias durante o expediente, necessitando registro formal.",
            ],
            "uso_incorreto_recursos": [
                "Uma auditoria interna conduzida por {auditor_externo.nome} detectou o uso do e-mail corporativo ({funcionario.email}) e do telefone {funcionario.telefone} para fins pessoais, violando os termos de uso de ativos da empresa. O IP de origem era {cliente.rede.ip_servidor_principal}.",
                "Foram identificadas transferências de dados não autorizadas utilizando recursos internos, conforme logs internos.",
                "O uso indevido de equipamentos da empresa para atividades pessoais foi confirmado em relatório detalhado do departamento de TI.",
            ],
            "assedio": [
                "Após denúncia formal, uma investigação interna conduzida pelo(a) responsável de RH {rh_responsavel.nome} e com parecer do advogado {advogado_interno.nome} (OAB: {advogado_interno.profissional.oab}) confirmou um padrão de comportamento de assédio moral contra colegas.",
                "Testemunhos e documentação interna corroboram a conduta abusiva, justificando a suspensão preventiva.",
                "O comportamento reiterado gerou desconforto e insegurança no ambiente de trabalho, caracterizando assédio moral.",
            ],
            "negligencia": [
                "Falhas críticas na operação, que geraram risco ao cumprimento de um contrato com o {org_publica.nome}, foram atribuídas à negligência do funcionário, conforme relatório de incidente datado de {data_incidente} e analisado pelo advogado {advogado_interno.nome}.",
                "A omissão no cumprimento de tarefas essenciais resultou em prejuízos à operação, necessitando medida disciplinar.",
                "A conduta negligente impactou diretamente a qualidade do serviço prestado e a segurança operacional.",
            ],
            "quebra_sigilo": [
                "Foi constatado que o funcionário compartilhou informações sigilosas sobre o projeto do cliente {cliente.razao_social} (Chave Pix: {cliente.financeiro.chave_pix}) com terceiros, o que representa uma grave quebra de confidencialidade e foi escalado para o departamento jurídico.",
                "O compartilhamento de dados internos violou políticas de segurança da informação e confidencialidade.",
                "Documentos sensíveis foram acessados e distribuídos sem autorização, caracterizando violação grave de sigilo corporativo.",
            ],
        },
        "bloco_secundario": {
            "impacto_operacional": [
                "O incidente causou um impacto direto no SLA acordado com o cliente {cliente.razao_social} (CNPJ: {cliente.cnpj}).",
                "A conduta afetou negativamente a imagem da empresa perante a {org_publica.nome}, com quem temos um contrato vigente.",
                "Houve atrasos significativos em processos internos, impactando a produtividade da equipe e os prazos de entrega.",
                "A operação do setor foi comprometida, exigindo realocação de tarefas para manter a continuidade do serviço.",
            ],
            "referencia_normativa": [
                "A conduta infringe o Art. 482 da CLT e o item 7.4 do nosso Código de Ética e Conduta. Processo relacionado: {cliente.juridico.processo_judicial}",
                "Conforme parecer do nosso jurídico, a ação se enquadra como falta grave, passível de medidas disciplinares severas.",
                "O comportamento do funcionário está em desacordo com o Regulamento Interno da empresa e normas legais aplicáveis.",
                "As práticas identificadas violam políticas internas, protocolos de compliance e legislação vigente.",
            ],
            "consequencia": [
                "Fica determinada a suspensão de {dias_suspensao} dias úteis, com afastamento integral das atividades a partir de amanhã.",
                "A reincidência neste tipo de comportamento resultará em desligamento por justa causa, conforme orientação do advogado {advogado_interno.nome}.",
                "O colaborador deverá cumprir suspensão preventiva de {dias_suspensao} dias, sem prejuízo de medidas adicionais caso haja reincidência.",
                "Medidas corretivas adicionais podem ser aplicadas após revisão do RH e do departamento jurídico.",
            ],
            "evidencias": [
                "As evidências incluem e-mails trocados, logs de sistema (MAC Address: {cliente.rede.mac_address_gateway}), o depoimento formal da testemunha {testemunha.nome} e o relatório do auditor {auditor_externo.nome}.",
                "Anexos: cópia do atestado (RG do funcionário: {funcionario.documentos.rg}), registros de ponto e o relatório de incidente de {data_relatorio}.",
                "Documentação adicional inclui prints, gravações e relatórios internos corroborando os fatos relatados.",
                "O relatório do auditor {auditor_externo.nome} detalha todas as inconsistências observadas e os procedimentos adotados.",
            ],
            "historico": [
                "O colaborador já possui um registro de advertência por motivo similar em {data_advertencia}, evidenciando um padrão de reincidência. CNH para registro: {funcionario.documentos.cnh}",
                "Não há registros anteriores de desvios de conduta, sendo este o primeiro incidente registrado pelo RH.",
                "Histórico funcional demonstra padrão consistente de condutas adequadas, exceto pelos eventos recentes documentados.",
                "O colaborador apresenta histórico de advertências leves, mas o incidente atual é considerado grave.",
            ],
            "encaminhamento": [
                "O registro do ocorrido será formalizado no sistema interno de RH pelo analista {rh_responsavel.nome} e arquivado.",
                "O colaborador deverá comparecer a uma reunião com seu gestor {supervisor.nome} e um representante do RH no seu dia de retorno.",
                "Providencie acompanhamento do colaborador durante o período de suspensão para garantir cumprimento das normas internas.",
                "Os gestores envolvidos devem documentar todas as interações relacionadas ao incidente para fins de compliance.",
            ],
            "reacoes_colaborador": [
                "Durante a notificação, o funcionário se apresentou alterado e não quis assinar o termo de ciência.",
                "O colaborador se mostrou arrependido e ciente da gravidade de suas ações, assinando a notificação.",
                "Houve resistência inicial, mas após explicações do RH, o funcionário compreendeu a necessidade da medida.",
                "O colaborador demonstrou surpresa e solicitou esclarecimentos adicionais sobre a suspensão.",
            ],
            "proximas_etapas": [
                "O RH, sob responsabilidade de {rh_responsavel.nome}, encaminhará o colaborador para um treinamento obrigatório de ética e compliance.",
                "A equipe jurídica, liderada por {advogado_interno.nome}, irá monitorar possíveis desdobramentos legais do caso.",
                "Será realizado acompanhamento periódico para avaliar a reintegração do colaborador às atividades normais.",
                "O gestor direto deverá fornecer relatórios semanais sobre comportamento e cumprimento das normas durante a suspensão.",
            ],
            "risco_associado": [
                "Existe um risco legal moderado de que o caso evolua para uma ação judicial ou denúncia junto ao {org_publica.nome}.",
                "O risco de reputação é alto, especialmente se os detalhes do incidente com o cliente {cliente.razao_social} se tornarem públicos.",
                "Há possibilidade de impacto negativo na equipe, caso não haja comunicação adequada e acompanhamento do caso.",
                "O incidente pode gerar questionamentos internos sobre a consistência da aplicação de políticas disciplinares.",
            ],
        },
    }
}


# --- MOTOR DE GERAÇÃO ATUALIZADO ---
def gerar_dados_aninhados():
    """Gera entidades interconectadas e dados contextuais para o prompt."""
    # Define listas de cargos para reutilização
    cargos_base = [
        "Analista de Sistemas",
        "Assistente Administrativo",
        "Técnico de Suporte",
    ]
    cargos_gestao = ["Gerente de Projetos", "Coordenador de Operações"]
    cargos_apoio = [
        "Analista Jr",
        "Estagiário",
        "Analista de RH Sênior",
        "Advogado Corporativo",
        "Auditor Externo",
        "Consultor",
    ]
    todos_os_cargos = cargos_base + cargos_gestao + cargos_apoio

    dados = {
        "funcionario": generate_person_entity(cargos_base),
        "supervisor": generate_person_entity(cargos_gestao),
        "testemunha": generate_person_entity(cargos_apoio),
        "rh_responsavel": generate_person_entity(["Analista de RH Sênior"]),
        "advogado_interno": generate_person_entity(["Advogado Corporativo"]),
        "auditor_externo": generate_person_entity(["Auditor Externo", "Consultor"]),
        # Passa a lista de cargos para gerar o contato interno da empresa
        "cliente": generate_company_entity("Cliente", todos_os_cargos),
        "hospital": generate_location_entity(HOSPITAIS),
        "org_publica": generate_location_entity(ORG_PUB),
    }

    motivo_chave = random.choice(list(MOTIVOS_DISCIPLINARES.keys()))
    dados["motivo_chave"] = motivo_chave
    dados["motivo_descritivo"] = MOTIVOS_DISCIPLINARES[motivo_chave]
    dados["dias_suspensao"] = random.choice([1, 3, 5, 10])

    datas = generate_random_dates()
    dados.update(datas)

    dados = introduce_inconsistency(dados)
    return dados


def gerar_prompt_suspensao(prompt_id: int):
    """Gera um prompt completo de suspensão, incluindo persona, narrativa e blocos secundários."""
    persona_chave = random.choice(list(PERSONAS.keys()))
    persona = PERSONAS[persona_chave]
    intencao = "documentar_suspensao"

    dados_dict = gerar_dados_aninhados()
    blocos = blocos_de_contexto[intencao]
    partes_do_prompt = []

    # Tarefa principal + justificativa
    partes_do_prompt.append(random.choice(blocos["tarefa_principal"]))
    partes_do_prompt.append(random.choice(blocos["justificativa"]))

    # Narrativa principal
    motivo_narrativa = dados_dict["motivo_chave"]
    if motivo_narrativa in blocos["narrativa"]:
        partes_do_prompt.append(random.choice(blocos["narrativa"][motivo_narrativa]))

    # Blocos secundários
    blocos_secundarios, _ = combine_blocks(blocos["bloco_secundario"], 4, 6)
    partes_do_prompt.extend(blocos_secundarios)

    conteudo_prompt = " ".join(partes_do_prompt)
    prompt_completo = apply_persona_to_text(conteudo_prompt, persona)

    # **AQUI ESTÁ A MUDANÇA PRINCIPAL**
    # 1. Converte o dicionário para o nosso novo "SafeNamespace"
    dados_obj = dict_to_safe_namespace(dados_dict)

    # 2. Usa o método .format() padrão, que agora é seguro por causa do objeto
    texto_final = prompt_completo.format_map(vars(dados_obj))

    # Aplica erro textual baseado na persona
    if random.random() < persona["chance_de_erro"]:
        texto_final = inject_text_error(texto_final)

    return json.dumps(
        {
            "id": f"prompt_{prompt_id:04d}",
            # "persona_gerada": persona_chave,
            # "motivo_principal": motivo_narrativa,
            "texto": texto_final,
        },
        ensure_ascii=False,
        indent=2,
    )
