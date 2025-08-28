import json
import random
from types import SimpleNamespace
from faker import Faker

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

fake = Faker("pt_BR")


class SafeNamespace(SimpleNamespace):
    def __getattr__(self, name):
        return f"{{{name}_NAO_ENCONTRADO}}"


def dict_to_safe_namespace(d: dict):
    if not isinstance(d, dict):
        return d

    for key, value in d.items():
        d[key] = dict_to_safe_namespace(value)

    return SafeNamespace(**d)


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
    "Financeiro": {
        "prefixos": [
            "Conforme análise financeira,",
            "Segue relatório para aprovação:",
            "Para conhecimento e providências necessárias:",
            "Encaminho os dados financeiros consolidados:",
            "Com base na análise orçamentária:",
        ],
        "sufixos": [
            "Aguardo aprovação para prosseguir com os lançamentos.",
            "Dados conferidos pelo controller {controller.nome}.",
            "Favor validar antes do fechamento mensal.",
            "Documentação disponível para auditoria interna.",
            "Atenciosamente, Departamento Financeiro.",
        ],
        "chance_de_erro": 0.02,
    },
    "Controladoria": {
        "prefixos": [
            "Para controle e acompanhamento:",
            "Conforme auditoria interna,",
            "Segundo análise de custos,",
            "Para fins de compliance financeiro:",
            "Baseado nos indicadores de performance:",
        ],
        "sufixos": [
            "Favor manter registros atualizados para próxima auditoria.",
            "Dados validados conforme normas internas.",
            "Relatório aprovado pelo controller {controller.nome}.",
            "Informações sensíveis - manter confidencialidade.",
            "Arquivar para consultas futuras de compliance.",
        ],
        "chance_de_erro": 0.01,
    },
}

TIPOS_ANALISE_FINANCEIRA = {
    "folha_pagamento": "análise detalhada da folha de pagamento mensal",
    "custos_departamento": "levantamento de custos por departamento/centro de custo",
    "beneficios_colaborador": "relatório de benefícios e vantagens por colaborador",
    "provisoes_trabalhistas": "cálculo de provisões trabalhistas e encargos",
    "budget_anual": "elaboração do budget anual de pessoas",
    "turnover_custos": "análise de custos de turnover e reposição",
    "horas_extras": "relatório de horas extras e seus impactos financeiros",
    "absenteismo_financeiro": "impacto financeiro do absenteísmo na operação",
    "terceirizacao_vs_clt": "análise comparativa de custos entre terceirização e CLT",
    "reajuste_salarial": "estudo de impacto de reajustes salariais",
    "rescisoes_custos": "levantamento de custos com rescisões e demissões",
    "plr_bonus": "cálculo e distribuição de PLR/bônus variáveis",
}

BANCOS_BRASILEIROS = [
    "Banco do Brasil",
    "Bradesco",
    "Itaú Unibanco",
    "Santander Brasil",
    "Caixa Econômica Federal",
    "Banco BTG Pactual",
    "Banco Safra",
    "Banco Votorantim",
    "Banco Original",
    "Nubank",
]

EMPRESAS_CONTABILIDADE = [
    "Contabilidade Santos & Associados",
    "Escritório Fiscal Bahia",
    "Assessoria Contábil Salvador",
    "BF Contadores Associados",
    "Consultoria Tributária Regional",
    "Grupo Contábil Nordeste",
    "Excellence Contabilidade",
    "Precision Accounting Services",
    "Fiscal Partners Consultoria",
    "Strategic Tax Advisory",
]

blocos_de_contexto = {
    "analise_financeira": {
        "tarefa_principal": [
            "Elabore um relatório financeiro detalhado sobre {tipo_analise_descritivo} do colaborador {funcionario.nome}, CPF {funcionario.documentos.cpf}, matrícula {funcionario.profissional.matricula}, lotado no departamento de {departamento.nome}.",
            "Prepare uma análise de {tipo_analise_descritivo} referente ao período de {data_inicio} a {data_fim}, com foco no impacto orçamentário e projeções.",
            "Desenvolva um estudo financeiro sobre {tipo_analise_descritivo}, incluindo comparativos históricos e benchmarking de mercado.",
            "Produza um relatório executivo de {tipo_analise_descritivo} para apresentação à diretoria, destacando principais variações e tendências.",
        ],
        "contexto_dados": [
            "Os dados foram extraídos do sistema ERP corporativo pelo analista {controller.nome} e validados pela auditoria interna da {empresa_contabilidade.razao_social}.",
            "As informações financeiras foram consolidadas a partir dos centros de custo {centro_custo_1} e {centro_custo_2}, com cut-off em {data_relatorio}.",
            "Base de dados obtida através da integração com o banco {banco_principal.nome} (conta corrente {conta_bancaria_empresa}) e sistemas de folha internos.",
            "Números conferidos pelo controller {controller.nome} (CRC: {controller.profissional.crc}) em conjunto com a empresa contábil {empresa_contabilidade.razao_social}.",
        ],
        "narrativa": {
            "folha_pagamento": [
                "A folha de pagamento atual totaliza R$ {valor_folha_total}, sendo R$ {valor_salarios} em salários base, R$ {valor_beneficios} em benefícios, R$ {valor_encargos} em encargos patronais, processada através da conta {conta_bancaria_empresa} do {banco_principal.nome}. O colaborador {funcionario_destaque.nome} representa o maior custo individual com R$ {salario_individual}.",
                "Análise comparativa mensal mostra variação de {percentual_variacao}% em relação ao mês anterior, impactada principalmente por admissões no setor {departamento.nome}.",
                "Os custos com terceirizados através da {fornecedor.razao_social} (CNPJ: {fornecedor.cnpj}) somam R$ {valor_terceirizados}, representando {percentual_terceirizados}% do custo total de pessoas.",
            ],
            "custos_departamento": [
                "O departamento {departamento.nome}, sob gestão de {gestor_departamento.nome}, apresenta custo mensal de R$ {custo_departamento}, distribuído entre {qtd_colaboradores} colaboradores ativos. O e-mail do gestor é {gestor_departamento.email} para esclarecimentos adicionais.",
                "Centro de custo {centro_custo_1} registra os maiores gastos com R$ {valor_centro_custo_1}, seguido pelo {centro_custo_2} com R$ {valor_centro_custo_2}.",
                "Projeção anual indica necessidade de ajuste orçamentário de R$ {ajuste_orcamentario} considerando inflação e reajustes programados.",
            ],
            "beneficios_colaborador": [
                "O pacote de benefícios do colaborador {funcionario.nome} totaliza R$ {valor_beneficios_total} mensais, incluindo vale-alimentação, plano de saúde (operadora: {operadora_saude.nome}), vale-transporte e outros auxílios. Cartão corporativo: {funcionario.financeiro.cartao_de_credito}.",
                "Análise do custo-benefício dos auxílios oferecidos indica ROI positivo de {roi_beneficios}% em retenção de talentos.",
                "Comparativo com mercado mostra que nossos benefícios estão {percentual_mercado}% acima da média regional, conforme pesquisa da {consultoria.razao_social}.",
            ],
            "provisoes_trabalhistas": [
                "As provisões trabalhistas totalizam R$ {valor_provisoes_total}, sendo R$ {valor_ferias} em férias, R$ {valor_13_salario} em 13º salário, R$ {valor_fgts} em FGTS e R$ {valor_inss} em INSS patronal. Conta de provisão: {conta_provisoes} no {banco_principal.nome}.",
                "O colaborador {funcionario.nome} possui provisão individual de R$ {provisao_individual}, com base em seu salário atual de R$ {salario_atual} e tempo de casa de {tempo_casa} anos.",
                "Auditoria conduzida pela {empresa_contabilidade.razao_social} confirma adequação das provisões conforme legislação vigente e parecer do contador {contador.nome} (CRC: {contador.profissional.crc}).",
            ],
            "budget_anual": [
                "O orçamento anual de pessoas foi estabelecido em R$ {budget_total}, contemplando inflação projetada de {inflacao_projetada}%, reajustes setoriais e crescimento de headcount de {crescimento_headcount}%. Aprovação da diretoria em {data_aprovacao_budget}.",
                "Distribuição orçamentária por departamento: {departamento.nome} (R$ {orcamento_departamento}), representando {percentual_orcamento_dept}% do total.",
                "Reserva de contingência de R$ {reserva_contingencia} foi estabelecida para cobrir variações cambiais e ajustes não previstos, conforme recomendação da {consultoria.razao_social}.",
            ],
            "horas_extras": [
                "No período analisado, foram registradas {total_horas_extras} horas extras, totalizando R$ {valor_horas_extras} em custos adicionais. O colaborador {funcionario_horas_extras.nome} (mat. {funcionario_horas_extras.profissional.matricula}) registrou o maior volume com {horas_individuais} horas.",
                "A média salarial por hora dos colaboradores em extra é de R$ {valor_hora_media}, impactando o orçamento em {percentual_impacto_orcamento}%.",
                "Departamento {departamento.nome} concentra {percentual_horas_departamento}% do total de horas extras, sinalizando possível necessidade de reforço no quadro.",
            ],
        },
        "bloco_secundario": {
            "indicadores_financeiros": [
                "O custo médio por colaborador é de R$ {custo_medio_colaborador}, com variação de ±{variacao_custo_medio}% em relação ao benchmark setorial.",
                "Índice de rotatividade financeira indica custo de R$ {custo_turnover} por substituição, considerando rescisões, admissões e treinamentos.",
                "Margem de contribuição por colaborador atinge {margem_contribuicao}%, demonstrando eficiência operacional da equipe.",
                "ROI em treinamento e desenvolvimento apresenta retorno de R$ {roi_treinamento} para cada R$ 1,00 investido.",
            ],
            "comparativos_mercado": [
                "Pesquisa salarial conduzida pela {consultoria.razao_social} posiciona nossos salários {posicionamento_salarial}% acima da mediana do mercado regional.",
                "Benchmark de benefícios com empresas similares indica competitividade de {competitividade_beneficios}% em nosso pacote atual.",
                "Custo total de pessoas representa {percentual_receita_liquida}% da receita líquida, dentro da faixa considerada adequada pelo setor.",
                "Produtividade por colaborador de R$ {produtividade_colaborador} supera a média setorial em {superacao_produtividade}%.",
            ],
            "projecoes_orcamentarias": [
                "Projeção para os próximos 12 meses indica necessidade orçamentária de R$ {projecao_12_meses}, considerando cenário conservador de crescimento.",
                "Impacto de dissídio coletivo estimado em R$ {impacto_dissidio} adicionais ao orçamento anual, com vigência a partir de {data_vigencia_dissidio}.",
                "Cenário otimista projeta economia de R$ {economia_otimista} através de iniciativas de eficiência operacional e renegociação de benefícios.",
                "Budget de contratações para {ano_proximo} prevê {numero_contratacoes} novas admissões, totalizando R$ {custo_novas_contratacoes} em custos incrementais.",
            ],
            "analise_tributaria": [
                "Carga tributária sobre folha totaliza R$ {carga_tributaria_total}, representando {percentual_carga_tributaria}% dos custos diretos com pessoas.",
                "Contribuição patronal ao INSS: R$ {contribuicao_inss_patronal}, FGTS: R$ {contribuicao_fgts}, Sistema S: R$ {contribuicao_sistema_s}, conforme apuração da {empresa_contabilidade.razao_social}.",
                "Oportunidades de otimização tributária identificadas pela consultoria fiscal podem gerar economia anual de R$ {economia_tributaria}.",
                "Compliance trabalhista auditado pela {empresa_contabilidade.razao_social} confirma adequação de 98,5% dos processos aos requisitos legais.",
            ],
            "fluxo_caixa": [
                "Desembolso mensal com folha ocorre nos dias 5 e 20, via TED da conta {conta_bancaria_empresa} ({banco_principal.nome}), totalizando R$ {desembolso_mensal}.",
                "Cronograma de pagamentos: salários (dia 5), 13º salário (novembro/dezembro), férias (conforme escala), rescisões (até 10 dias úteis).",
                "Reserva de caixa para folha mantida em R$ {reserva_caixa_folha}, equivalente a {meses_reserva_caixa} meses de operação normal.",
                "Integração bancária via API permite reconciliação automática de 97% dos lançamentos, reduzindo tempo de fechamento em {reducao_tempo_fechamento} dias.",
            ],
            "riscos_contingencias": [
                "Análise de riscos trabalhistas indica exposição potencial de R$ {exposicao_trabalhista} em ações em curso, acompanhadas pelo escritório {escritorio_advocacia.razao_social}.",
                "Contingenciamento de R$ {valor_contingenciamento} foi estabelecido para cobrir possíveis passivos de períodos anteriores.",
                "Seguro de responsabilidade civil para executivos cobre até R$ {cobertura_seguro_executivos}, com apólice {numero_apolice}.",
                "Monitoramento mensal de indicadores de risco sugere probabilidade baixa (menor que 15%) de materialização de contingências significativas.",
            ],
            "recomendacoes_acoes": [
                "Recomenda-se revisão da estrutura salarial do departamento {departamento.nome} para alinhamento com práticas de mercado até {data_recomendacao}.",
                "Implementação de sistema de gestão de ponto integrado pode gerar economia de R$ {economia_sistema_ponto} anuais em controles manuais.",
                "Renegociação do contrato com {fornecedor.razao_social} para benefícios pode reduzir custos em {percentual_reducao_beneficios}% sem perda de qualidade.",
                "Plano de sucessão para posições críticas deve ser priorizado, considerando custo médio de substituição de R$ {custo_substituicao_critica}.",
            ],
            "validacao_auditoria": [
                "Relatório validado pelo controller {controller.nome} em {data_validacao} e arquivado sob protocolo {protocolo_arquivo}.",
                "Auditoria interna da {empresa_contabilidade.razao_social} confirma consistência dos dados e aderência aos princípios contábeis.",
                "Conciliação bancária da conta {conta_bancaria_empresa} apresenta divergência zero, validada pelo gerente de relacionamento {gerente_banco.nome}.",
                "Documentação comprobatória arquivada no sistema documental corporativo, acessível via login {usuario_sistema}.",
            ],
        },
    }
}


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


def generate_department_entity():
    departamentos = [
        "Tecnologia da Informação",
        "Recursos Humanos",
        "Financeiro",
        "Comercial",
        "Operações",
        "Marketing",
        "Jurídico",
        "Logística",
    ]
    return {
        "nome": random.choice(departamentos),
        "codigo": f"DEPT{random.randint(100, 999)}",
        "centro_custo": f"{random.randint(1000, 9999)}",
    }


def format_currency(value):
    """Format number as Brazilian currency"""
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def generate_financial_values():
    """Generate all financial values needed for the templates"""
    return {
        # Basic payroll values
        "valor_folha_total": format_currency(random.randint(150000, 800000)),
        "valor_salarios": format_currency(random.randint(100000, 500000)),
        "valor_beneficios": format_currency(random.randint(20000, 80000)),
        "valor_encargos": format_currency(random.randint(30000, 150000)),
        "salario_individual": format_currency(random.randint(8000, 25000)),
        "custo_departamento": format_currency(random.randint(50000, 200000)),
        "budget_total": format_currency(random.randint(2000000, 10000000)),
        # Percentages and metrics
        "percentual_variacao": round(random.uniform(-5.0, 15.0), 1),
        "percentual_terceirizados": round(random.uniform(10.0, 35.0), 1),
        "percentual_receita_liquida": round(random.uniform(25.0, 45.0), 1),
        "percentual_orcamento_dept": round(random.uniform(15.0, 35.0), 1),
        "percentual_mercado": round(random.uniform(5.0, 25.0), 1),
        "percentual_impacto_orcamento": round(random.uniform(2.0, 8.0), 1),
        "percentual_horas_departamento": round(random.uniform(20.0, 60.0), 1),
        "percentual_carga_tributaria": round(random.uniform(35.0, 45.0), 1),
        "percentual_reducao_beneficios": round(random.uniform(5.0, 15.0), 1),
        # Quantities and counts
        "qtd_colaboradores": random.randint(15, 150),
        # Cost centers and accounts
        "centro_custo_1": f"CC{random.randint(1000, 9999)}",
        "centro_custo_2": f"CC{random.randint(1000, 9999)}",
        "valor_centro_custo_1": format_currency(random.randint(80000, 300000)),
        "valor_centro_custo_2": format_currency(random.randint(60000, 250000)),
        "conta_bancaria_empresa": fake.random_number(digits=8, fix_len=True),
        "conta_provisoes": fake.random_number(digits=8, fix_len=True),
        # Cash flow and reserves
        "desembolso_mensal": format_currency(random.randint(150000, 800000)),
        "reserva_caixa_folha": format_currency(random.randint(300000, 2000000)),
        # Detailed financial values
        "valor_terceirizados": format_currency(random.randint(30000, 120000)),
        "ajuste_orcamentario": format_currency(random.randint(50000, 200000)),
        "valor_beneficios_total": format_currency(random.randint(3000, 12000)),
        "valor_provisoes_total": format_currency(random.randint(80000, 300000)),
        "valor_ferias": format_currency(random.randint(25000, 100000)),
        "valor_13_salario": format_currency(random.randint(20000, 80000)),
        "valor_fgts": format_currency(random.randint(15000, 60000)),
        "valor_inss": format_currency(random.randint(20000, 80000)),
        "provisao_individual": format_currency(random.randint(5000, 20000)),
        "salario_atual": format_currency(random.randint(4000, 15000)),
        "orcamento_departamento": format_currency(random.randint(200000, 800000)),
        "reserva_contingencia": format_currency(random.randint(100000, 500000)),
        "valor_horas_extras": format_currency(random.randint(15000, 60000)),
        "valor_hora_media": format_currency(random.randint(25, 80)),
        # Performance indicators
        "custo_medio_colaborador": format_currency(random.randint(8000, 25000)),
        "variacao_custo_medio": round(random.uniform(2.0, 12.0), 1),
        "custo_turnover": format_currency(random.randint(15000, 50000)),
        "margem_contribuicao": round(random.uniform(15.0, 35.0), 1),
        "roi_treinamento": format_currency(random.uniform(2.5, 8.0)),
        "roi_beneficios": round(random.uniform(15.0, 35.0), 1),
        "posicionamento_salarial": round(random.uniform(5.0, 25.0), 1),
        "competitividade_beneficios": round(random.uniform(80.0, 120.0), 1),
        "produtividade_colaborador": format_currency(random.randint(50000, 200000)),
        "superacao_produtividade": round(random.uniform(5.0, 20.0), 1),
        # Projections and budget
        "projecao_12_meses": format_currency(random.randint(1800000, 9600000)),
        "impacto_dissidio": format_currency(random.randint(100000, 500000)),
        "economia_otimista": format_currency(random.randint(50000, 300000)),
        "custo_novas_contratacoes": format_currency(random.randint(200000, 800000)),
        # Tax and compliance
        "carga_tributaria_total": format_currency(random.randint(60000, 300000)),
        "contribuicao_inss_patronal": format_currency(random.randint(30000, 120000)),
        "contribuicao_fgts": format_currency(random.randint(12000, 50000)),
        "contribuicao_sistema_s": format_currency(random.randint(8000, 30000)),
        "economia_tributaria": format_currency(random.randint(25000, 100000)),
        # Risk and contingencies
        "exposicao_trabalhista": format_currency(random.randint(500000, 2000000)),
        "valor_contingenciamento": format_currency(random.randint(200000, 800000)),
        "cobertura_seguro_executivos": format_currency(
            random.randint(5000000, 20000000)
        ),
        # Recommendations and savings
        "economia_sistema_ponto": format_currency(random.randint(50000, 200000)),
        "custo_substituicao_critica": format_currency(random.randint(80000, 300000)),
    }


def generate_additional_financial_dates():
    from datetime import datetime, timedelta

    base_date = datetime.now()
    return {
        "data_inicio": (base_date - timedelta(days=90)).strftime("%d/%m/%Y"),
        "data_fim": (base_date - timedelta(days=1)).strftime("%d/%m/%Y"),
        "data_aprovacao_budget": (base_date - timedelta(days=180)).strftime("%d/%m/%Y"),
        "data_vigencia_dissidio": (base_date + timedelta(days=30)).strftime("%d/%m/%Y"),
        "data_validacao": (base_date - timedelta(days=2)).strftime("%d/%m/%Y"),
        "data_recomendacao": (base_date + timedelta(days=60)).strftime("%d/%m/%Y"),
        "ano_proximo": (base_date.year + 1),
    }


def generate_financial_metadata():
    return {
        "protocolo_arquivo": f"PROT{random.randint(100000, 999999)}",
        "usuario_sistema": f"usr{random.randint(1000, 9999)}",
        "numero_apolice": f"{random.randint(100000, 999999)}-{random.randint(10, 99)}",
        "inflacao_projetada": round(random.uniform(3.5, 8.0), 1),
        "crescimento_headcount": round(random.uniform(5.0, 20.0), 1),
        "total_horas_extras": random.randint(200, 1500),
        "horas_individuais": random.randint(20, 80),
        "tempo_casa": random.randint(1, 15),
        "meses_reserva_caixa": random.randint(2, 6),
        "numero_contratacoes": random.randint(5, 50),
        "reducao_tempo_fechamento": random.randint(1, 5),
    }


def gerar_prompt_financeiro(prompt_id: int):
    persona_chave = random.choice(list(PERSONAS.keys()))
    persona = PERSONAS[persona_chave]
    intencao = "analise_financeira"
    dados_dict = gerar_dados_financeiros()
    blocos = blocos_de_contexto[intencao]

    partes_do_prompt = []

    # Adicionar tarefa principal
    partes_do_prompt.append(random.choice(blocos["tarefa_principal"]))

    # Adicionar contexto dos dados
    partes_do_prompt.append(random.choice(blocos["contexto_dados"]))

    # Adicionar narrativa específica do tipo de análise
    tipo_analise = dados_dict["tipo_analise_chave"]
    if tipo_analise in blocos["narrativa"]:
        partes_do_prompt.append(random.choice(blocos["narrativa"][tipo_analise]))

    # Adicionar blocos secundários
    blocos_secundarios, _ = combine_blocks(blocos["bloco_secundario"], 3, 5)
    partes_do_prompt.extend(blocos_secundarios)

    conteudo_prompt = " ".join(partes_do_prompt)
    prompt_completo = apply_persona_to_text(conteudo_prompt, persona)
    dados_obj = dict_to_safe_namespace(dados_dict)
    texto_final = prompt_completo.format(**vars(dados_obj))

    if random.random() < persona["chance_de_erro"]:
        texto_final = inject_text_error(texto_final)

    return json.dumps(
        {
            "text": texto_final,
        },
        ensure_ascii=False,
        indent=2,
    )
