import random
from faker import Faker

from modules.financial.config import BANCOS_BRASILEIROS, TIPOS_ANALISE_FINANCEIRA
from utils.generator_utils import (
    generate_additional_financial_dates,
    generate_company_entity,
    generate_department_entity,
    generate_financial_metadata,
    generate_financial_values,
    generate_location_entity,
    generate_person_entity,
    generate_random_dates,
    introduce_inconsistency,
)


def gerar_dados_financeiros():
    cargos_financeiros = ["Controller", "Analista Financeiro Sr", "Gerente Financeiro"]
    cargos_gestao = ["Gerente de RH", "Diretor de Pessoas", "Coordenador de Folha"]
    cargos_operacionais = [
        "Analista de Folha",
        "Assistente Financeiro",
        "Auxiliar de DP",
    ]
    cargos_externos = ["Contador", "Auditor Externo", "Consultor Financeiro"]

    dados = {
        "funcionario": generate_person_entity(cargos_operacionais + cargos_gestao),
        "funcionario_destaque": generate_person_entity(cargos_gestao),
        "funcionario_horas_extras": generate_person_entity(cargos_operacionais),
        "controller": generate_person_entity(cargos_financeiros),
        "gestor_departamento": generate_person_entity(cargos_gestao),
        "contador": generate_person_entity(["Contador"]),
        "gerente_banco": generate_person_entity(["Gerente de Relacionamento"]),
        "empresa_contabilidade": generate_company_entity(
            "Contabilidade", ["Contador", "Auditor"]
        ),
        "consultoria": generate_company_entity("Consultoria", ["Consultor Senior"]),
        "fornecedor": generate_company_entity("Fornecedor", ["Gerente Comercial"]),
        "operadora_saude": generate_company_entity(
            "Operadora", ["Analista de Benefícios"]
        ),
        "escritorio_advocacia": generate_company_entity(
            "Advocacia", ["Advogado Sênior"]
        ),
        "banco_principal": generate_location_entity(BANCOS_BRASILEIROS),
        "departamento": generate_department_entity(),
    }

    # Adicionar dados específicos financeiros
    tipo_analise_chave = random.choice(list(TIPOS_ANALISE_FINANCEIRA.keys()))
    dados["tipo_analise_chave"] = tipo_analise_chave
    dados["tipo_analise_descritivo"] = TIPOS_ANALISE_FINANCEIRA[tipo_analise_chave]

    # Gerar valores financeiros realistas
    dados.update(generate_financial_values())

    # Adicionar datas
    datas = generate_random_dates()
    dados.update(datas)
    dados.update(generate_additional_financial_dates())

    # Adicionar outros dados específicos
    dados.update(generate_financial_metadata())

    dados = introduce_inconsistency(dados)
    return dados


fake = Faker("pt_BR")
