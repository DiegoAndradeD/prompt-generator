import random
from modules.suspension.config import HOSPITAIS, MOTIVOS_DISCIPLINARES, ORG_PUB
from utils.generator_utils import (
    generate_company_entity,
    generate_location_entity,
    generate_person_entity,
    generate_random_dates,
    introduce_inconsistency,
)


def gerar_dados_aninhados():
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
