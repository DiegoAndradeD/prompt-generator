import random
from faker import Faker

from modules.resumes.config import AREAS_ATUACAO, CERTIFICACOES, UNIVERSIDADES
from utils.generator_utils import (
    generate_company_entity,
    generate_person_entity,
)


fake = Faker("pt_BR")


def generate_curriculum_data():
    """Gera dados específicos para análise de currículo."""
    # Cargos específicos por área
    cargos_tech = [
        "Desenvolvedor Full Stack",
        "Arquiteto de Software",
        "DevOps Engineer",
        "Data Scientist",
    ]
    cargos_gestao = [
        "Gerente de Projetos",
        "Coordenador de Equipe",
        "Supervisor de Operações",
    ]
    cargos_comercial = ["Analista Comercial", "Consultor de Vendas", "Account Manager"]
    cargos_apoio = ["Analista Jr", "Especialista", "Coordenador"]

    area_chave = random.choice(list(AREAS_ATUACAO.keys()))

    # Seleciona cargo baseado na área
    if area_chave == "tecnologia":
        vaga_pretendida = random.choice(cargos_tech)
    elif area_chave in ["vendas", "marketing"]:
        vaga_pretendida = random.choice(cargos_comercial)
    else:
        vaga_pretendida = random.choice(cargos_gestao + cargos_apoio)

    dados = {
        "candidato": generate_person_entity(cargos_apoio),
        "empresa_anterior": generate_company_entity("Empresa", cargos_gestao),
        "referencia": generate_person_entity(cargos_gestao),
        "universidade": {"nome": random.choice(UNIVERSIDADES)},
        "vaga_pretendida": vaga_pretendida,
        "area_principal": AREAS_ATUACAO[area_chave],
        "anos_experiencia": random.randint(2, 15),
        "curso_superior": random.choice(
            ["Engenharia de Software", "Administração", "Economia"]
        ),
        "pos_graduacao": random.choice(
            ["MBA em Gestão Estratégica", "Especialização em Digital Business"]
        ),
        "certificacao_principal": random.choice(CERTIFICACOES),
        "competencia_tecnica": random.choice(
            ["Python e Machine Learning", "React e Node.js"]
        ),
        "ferramenta_especifica": random.choice(
            ["Salesforce", "Tableau", "Jenkins", "Docker", "Kubernetes"]
        ),
        "metodologia_trabalho": random.choice(["Scrum", "Kanban", "Design Thinking"]),
        "area_especializacao": random.choice(
            ["Inteligência Artificial", "Marketing Digital"]
        ),
        "cargo_anterior": random.choice(cargos_gestao + cargos_tech),
        "tamanho_equipe": random.randint(3, 20),
        "valor_economia": f"{random.randint(50, 500)}.000",
        "percentual_melhoria": random.randint(15, 80),
        "area_inovacao": random.choice(
            ["automação de processos", "experiência do cliente"]
        ),
        "percentual_crescimento": random.randint(10, 150),
        "meses_gap": random.randint(2, 8),
        "tecnologia_faltante": random.choice(
            ["Kubernetes", "Machine Learning", "Blockchain"]
        ),
        "salario_pretendido": f"{random.randint(8, 25)}.000",
        "situacao_salario": random.choice(["acima", "dentro", "abaixo"]),
        "prazo_inicio": random.randint(15, 60),
        "valor_investimento": f"{random.randint(5, 50)}.000",
    }

    # Adiciona endereço para o candidato
    dados["candidato"]["endereco"] = f"{fake.city()} - {fake.state_abbr()}"

    return dados
