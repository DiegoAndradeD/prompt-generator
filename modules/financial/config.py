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

CONFIG_FINANCEIRO = {
    "personas": PERSONAS,
    "blocos_de_contexto": blocos_de_contexto,
    "intent_name": "analise_financeira",
    "assembly_plan": [
        {"block": "tarefa_principal", "count": 1},
        {"block": "contexto_dados", "count": 1},
        {"block": "narrativa", "count": 1, "dynamic_key": "tipo_analise_chave"},
        {"block": "bloco_secundario", "count": "random(3,5)"},
    ],
}
