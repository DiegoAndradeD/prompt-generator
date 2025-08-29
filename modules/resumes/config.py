PERSONAS = {
    "Recrutador Técnico": {
        "prefixos": [
            "Analisando o perfil técnico:",
            "Avaliação especializada do candidato:",
            "Revisão técnica detalhada:",
            "Análise de competências específicas:",
            "Parecer técnico sobre o currículo:",
        ],
        "sufixos": [
            "Favor validar as competências técnicas mencionadas.",
            "Recomendo entrevista técnica aprofundada.",
            "Sugiro verificação das certificações apresentadas.",
            "Avaliar compatibilidade com stack tecnológico atual.",
            "Confirmar experiência prática nas tecnologias citadas.",
        ],
        "chance_de_erro": 0.08,
    },
    "Gerente de RH": {
        "prefixos": [
            "Prezados, segue análise do candidato:",
            "Encaminho parecer sobre perfil profissional:",
            "Avaliação inicial de adequação cultural:",
            "Relatório de triagem de currículo:",
            "Análise comportamental preliminar:",
        ],
        "sufixos": [
            "Aguardo feedback dos gestores técnicos.",
            "Candidato aprovado para próxima fase do processo seletivo.",
            "Recomendo entrevista comportamental detalhada.",
            "Perfil alinhado com cultura organizacional da empresa.",
            "Favor avaliar fit cultural antes da contratação.",
        ],
        "chance_de_erro": 0.05,
    },
    "Headhunter": {
        "prefixos": [
            "Identifiquei um perfil interessante:",
            "Candidate em potencial para a vaga:",
            "Prospecção de talento especializado:",
            "Perfil executivo mapeado:",
            "Talent sourcing - candidato qualificado:",
        ],
        "sufixos": [
            "Este profissional está disponível no mercado.",
            "Salário pretendido dentro do budget aprovado.",
            "Disponibilidade imediata para início das atividades.",
            "Referências profissionais já foram validadas.",
            "Forte potencial de retenção no médio prazo.",
        ],
        "chance_de_erro": 0.15,
    },
    "Gestor Contratante": {
        "prefixos": [
            "Analisando para minha equipe:",
            "Candidato para posição em aberto:",
            "Avaliação para vaga crítica:",
            "Perfil para posição sênior:",
            "Análise de adequação à equipe:",
        ],
        "sufixos": [
            "Acredito que seria um bom fit para nossa equipe.",
            "Experiência condizente com nossas necessidades atuais.",
            "Poderia contribuir significativamente com nossos projetos.",
            "Perfil complementar às competências já existentes.",
            "Recomendo prosseguir com o processo de seleção.",
        ],
        "chance_de_erro": 0.12,
    },
    "Consultor de Carreira": {
        "prefixos": [
            "Orientação sobre perfil profissional:",
            "Análise de desenvolvimento de carreira:",
            "Mapeamento de competências do candidato:",
            "Avaliação de posicionamento no mercado:",
            "Consultoria em transição de carreira:",
        ],
        "sufixos": [
            "Recomendo desenvolvimento de soft skills específicas.",
            "Perfil com potencial de crescimento acelerado.",
            "Sugestão de certificações complementares.",
            "Alinhamento de expectativas de carreira necessário.",
            "Perfil pronto para posições de liderança.",
        ],
        "chance_de_erro": 0.07,
    },
}

AREAS_ATUACAO = {
    "tecnologia": "Desenvolvimento de software e soluções tecnológicas",
    "marketing": "Marketing digital e estratégias de comunicação",
    "vendas": "Vendas corporativas e relacionamento com clientes",
    "financeiro": "Controladoria e análises financeiras",
    "operacoes": "Gestão operacional e processos internos",
    "juridico": "Assessoria jurídica e compliance corporativo",
    "rh": "Gestão de pessoas e desenvolvimento organizacional",
    "logistica": "Supply chain e logística de distribuição",
    "qualidade": "Gestão da qualidade e melhoria contínua",
    "projetos": "Gerenciamento de projetos estratégicos",
}

UNIVERSIDADES = [
    "Universidade Federal da Bahia (UFBA)",
    "Universidade Católica do Salvador (UCSAL)",
    "Universidade Salvador (UNIFACS)",
    "Instituto Federal da Bahia (IFBA)",
    "Faculdade Ruy Barbosa (FRB)",
    "Universidade Estadual de Feira de Santana (UEFS)",
    "Centro Universitário FTC",
    "Faculdade de Tecnologia e Ciências (FTC)",
    "Universidade do Estado da Bahia (UNEB)",
    "Faculdade Maurício de Nassau",
]

EMPRESAS_ANTERIORES = [
    "Petrobras S.A.",
    "Braskem S.A.",
    "Suzano Papel e Celulose",
    "Banco do Brasil S.A.",
    "Caixa Econômica Federal",
    "Accenture Brasil",
    "IBM Brasil",
    "Microsoft Brasil",
    "Ambev S.A.",
    "JBS S.A.",
]

CERTIFICACOES = [
    "Project Management Professional (PMP)",
    "Certified Scrum Master (CSM)",
    "AWS Certified Solutions Architect",
    "Google Analytics Certified",
    "Salesforce Administrator",
    "ITIL Foundation Certificate",
    "Six Sigma Green Belt",
    "Microsoft Azure Fundamentals",
    "Cisco Certified Network Associate (CCNA)",
    "Oracle Database Administrator Certified",
]


blocos_de_contexto = {
    "analisar_curriculo": {
        "tarefa_principal": [
            "Analise o currículo do candidato {candidato.nome}, CPF {candidato.documentos.cpf}, que se candidatou para a posição de {vaga_pretendida} em nossa empresa.",
            "Realize uma avaliação completa do perfil de {candidato.nome}, considerando experiência profissional e adequação à vaga de {vaga_pretendida}.",
            "Faça a triagem do currículo de {candidato.nome}, portador do RG {candidato.documentos.rg}, para a posição em aberto de {vaga_pretendida}.",
            "Conduza análise detalhada do background profissional de {candidato.nome}, avaliando fit para a vaga de {vaga_pretendida}.",
        ],
        "experiencia_profissional": [
            "O candidato possui {anos_experiencia} anos de experiência na área de {area_principal}, tendo atuado em empresas como {empresa_anterior.razao_social} (CNPJ: {empresa_anterior.cnpj}) no cargo de {cargo_anterior}.",
            "Profissional com trajetória consolidada em {area_principal}, destacando-se sua passagem pela {empresa_anterior.razao_social}, onde desenvolveu competências específicas em {competencia_tecnica}.",
            "Experiência robusta de {anos_experiencia} anos no setor, com histórico em {empresa_anterior.razao_social}, localizada em {empresa_anterior.endereco_fiscal}, onde liderou projetos estratégicos.",
        ],
        "formacao_academica": [
            "Formação acadêmica em {curso_superior} pela {universidade.nome}, complementada por certificação em {certificacao_principal} e especialização em {area_especializacao}.",
            "Graduado em {curso_superior} pela renomada {universidade.nome}, com pós-graduação em {pos_graduacao} e certificações técnicas relevantes.",
            "Background educacional sólido com diploma de {curso_superior} pela {universidade.nome} e formação continuada em {area_especializacao}.",
        ],
        "competencias_tecnicas": [
            "Demonstra domínio avançado em {competencia_tecnica}, com experiência prática em {ferramenta_especifica} e conhecimento em {metodologia_trabalho}.",
            "Portfolio técnico inclui expertise em {competencia_tecnica}, certificação {certificacao_principal} e experiência hands-on com {ferramenta_especifica}.",
            "Competências técnicas alinhadas com nossa stack: {competencia_tecnica}, {ferramenta_especifica} e metodologias ágeis como {metodologia_trabalho}.",
        ],
        "bloco_secundario": {
            "soft_skills": [
                "O candidato demonstra forte capacidade de liderança, tendo gerenciado equipes de até {tamanho_equipe} pessoas em projetos complexos na {empresa_anterior.razao_social}.",
                "Perfil colaborativo e orientado a resultados, com histórico de melhorias de processos e otimização de performance em ambientes corporativos.",
                "Excelentes habilidades de comunicação e capacidade analítica, fundamentais para o sucesso na posição pretendida.",
                "Demonstra adaptabilidade e resiliência, tendo navegado com sucesso por mudanças organizacionais significativas.",
            ],
            "idiomas": [
                "Fluência em inglês comprovada através de certificação internacional, com experiência em negociações com clientes da {empresa_anterior.razao_social}.",
                "Conhecimento avançado em inglês e espanhol, facilitando comunicação em projetos internacionais e expansão de mercado.",
                "Multilíngue com certificações em inglês e francês, competência valorizada para nossa operação global.",
            ],
            "realizacoes": [
                "Responsável pela implementação de projeto que resultou em economia de R$ {valor_economia} para a {empresa_anterior.razao_social}, demonstrando ROI significativo.",
                "Liderou iniciativa de transformação digital que aumentou a eficiência operacional em {percentual_melhoria}% na empresa anterior.",
                "Reconhecido com prêmio interno de inovação na {empresa_anterior.razao_social} por desenvolvimento de solução disruptiva em {area_inovacao}.",
                "Contribuiu para crescimento de {percentual_crescimento}% nas vendas da divisão, superando metas estabelecidas pela gestão.",
            ],
            "fit_cultural": [
                "Perfil alinhado com nossos valores corporativos, demonstrando integridade e foco em excelência operacional durante toda sua trajetória.",
                "Histórico de trabalho em empresas com cultura similar à nossa, facilitando adaptação e integração à equipe existente.",
                "Valores pessoais compatíveis com nossa missão organizacional, especialmente no que tange sustentabilidade e responsabilidade social.",
                "Mentalidade empreendedora e orientação para inovação, características essenciais para nosso ambiente de trabalho dinâmico.",
            ],
            "pontos_atencao": [
                "Observa-se gap de {meses_gap} meses entre as últimas duas experiências profissionais, que deve ser esclarecido durante entrevista.",
                "Experiência limitada com {tecnologia_faltante}, que é utilizada em alguns de nossos projetos atuais, mas pode ser desenvolvida com treinamento.",
                "Pretensão salarial de R$ {salario_pretendido} está {situacao_salario} da faixa orçamentária aprovada para a posição.",
                "Localização atual em {candidato.endereco} pode impactar disponibilidade para reuniões presenciais no escritório principal.",
            ],
            "referencias": [
                "Referências profissionais incluem {referencia.nome} ({referencia.email}), ex-gestor na {empresa_anterior.razao_social}, que confirma excelente performance técnica.",
                "Validação com {referencia.nome}, telefone {referencia.telefone}, atesta competência técnica e capacidade de trabalho em equipe do candidato.",
                "Feedback positivo de supervisor direto na empresa anterior, destacando pontualidade, proatividade e qualidade das entregas.",
            ],
            "disponibilidade": [
                "Disponibilidade imediata para início das atividades, com período de aviso prévio já cumprido na empresa anterior.",
                "Pode iniciar atividades em {prazo_inicio} dias, respeitando compromissos profissionais atuais e transição adequada.",
                "Flexibilidade para modelo híbrido de trabalho, alinhado com nossa política atual de trabalho remoto.",
                "Disponível para viagens corporativas e participação em treinamentos externos conforme necessidades da função.",
            ],
            "investimentos_desenvolvimento": [
                "Candidato demonstra compromisso com aprendizado contínuo, tendo investido R$ {valor_investimento} em cursos e certificações nos últimos dois anos.",
                "Participação ativa em comunidades técnicas e eventos do setor, mantendo-se atualizado com tendências e melhores práticas.",
                "Histórico de desenvolvimento profissional constante, com especializações complementares à formação base.",
            ],
            "redes_contatos": [
                "Rede de contatos consolidada no setor, incluindo profissionais da {empresa_anterior.razao_social} e outras organizações relevantes do mercado.",
                "Presença ativa em plataformas profissionais e associações de classe, demonstrando networking estratégico bem desenvolvido.",
                "Relacionamentos comerciais que podem agregar valor aos nossos objetivos de expansão no segmento de {area_principal}.",
            ],
            "motivacao": [
                "Motivação clara para mudança de carreira baseada em busca por novos desafios e crescimento profissional acelerado.",
                "Interesse genuíno em nossa proposta de valor e alinhamento com os projetos estratégicos que temos em desenvolvimento.",
                "Expectativas de carreira compatíveis com nosso plano de sucessão e oportunidades de crescimento interno.",
            ],
        },
    }
}

CONFIG_CURRICULOS = {
    "personas": PERSONAS,
    "blocos_de_contexto": blocos_de_contexto,
    "intent_name": "analisar_curriculo",
    "assembly_plan": [
        {"block": "tarefa_principal", "count": 1},
        {"block": "experiencia_profissional", "count": 1},
        {"block": "formacao_academica", "count": 1},
        {"block": "competencias_tecnicas", "count": 1},
        {"block": "bloco_secundario", "count": "random(3,5)"},
    ],
}
