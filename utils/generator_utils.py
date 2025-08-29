import random
import unicodedata
from types import SimpleNamespace
from datetime import datetime, timedelta
from faker import Faker


fake = Faker("pt_BR")


def remove_accent_error(text: str) -> str:
    accented_letters = [
        c
        for c in text
        if unicodedata.category(c) != "Mn" and unicodedata.normalize("NFD", c) != c
    ]
    if not accented_letters:
        return text
    target_char = random.choice(accented_letters)
    char_without_accent = (
        unicodedata.normalize("NFD", target_char)
        .encode("ascii", "ignore")
        .decode("utf-8")
    )
    return text.replace(target_char, char_without_accent, 1)


def inject_text_error(text: str) -> str:
    error_type = random.choice(["accent", "typo", "case", "ocr", "none"])

    if error_type == "accent":
        return remove_accent_error(text)

    if error_type == "typo" and len(text) > 2:
        pos = random.randint(0, len(text) - 2)
        return text[:pos] + text[pos + 1] + text[pos] + text[pos + 2 :]

    if error_type == "case":
        return text.lower()

    if error_type == "ocr":
        ocr_errors = {"O": "0", "I": "1", "S": "5", "B": "8"}
        char_to_replace = random.choice(list(ocr_errors.keys()))
        if char_to_replace in text:
            return text.replace(char_to_replace, ocr_errors[char_to_replace], 1)

    return text


def generate_cpf_in_various_formats():
    base = fake.cpf().replace(".", "").replace("-", "")
    formats = [
        f"{base[:3]}.{base[3:6]}.{base[6:9]}-{base[9:]}",
        f"{base}",
        f"{base[:3]} {base[3:6]} {base[6:9]} {base[9:]}",
        f"{base[:3]}.{base[3:6]} {base[6:9]}-{base[9:]}",
    ]
    return random.choice(formats)


def introduce_inconsistency(data: dict) -> dict:
    if random.random() < 0.20:
        inconsistency_type = random.choice(
            [
                "data_conflitante",
                "cargo_repetido",
                "cep_cidade_incompativel",
            ]
        )

        if inconsistency_type == "cep_cidade_incompativel" and "endereco" in data.get(
            "empresa", {}
        ):
            endereco_original = data["empresa"]["endereco"]
            cidade_original = fake.city()
            cep_falso = generate_postcode_various_formats()
            data["empresa"][
                "endereco"
            ] = f"{fake.street_address()}, {cidade_original} - {fake.state_abbr()}, CEP {cep_falso}"

    return data


def generate_cnpj_various_formats() -> str:
    base = fake.cnpj().replace(".", "").replace("/", "").replace("-", "")
    formats = [
        f"{base[:2]}.{base[2:5]}.{base[5:8]}/{base[8:12]}-{base[12:]}",
        f"{base}",
        f"{base[:2]} {base[2:5]} {base[5:8]} {base[8:12]} {base[12:]}",
    ]
    return random.choice(formats)


def generate_phone_various_formats() -> str:
    base = (
        fake.phone_number()
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
    )

    formats = [
        f"({base[:2]}) {base[2:7]}-{base[7:]}",
        f"{base[:2]} {base[2:]}",
        f"+55{base}",
        f"+55 {base[:2]} {base[2:7]} {base[7:]}",
        f"{base[2:]}",
    ]
    return random.choice(formats)


def generate_postcode_various_formats() -> str:
    base = fake.postcode().replace("-", "")
    formats = [
        f"{base[:5]}-{base[5:]}",
        f"{base}",
        f"{base[:5]} {base[5:]}",
    ]
    return random.choice(formats)


def generate_email(name: str) -> str:
    domains = ["empresa.com.br", "provedor.org", "corporate.net", "br.corp.net"]
    clean_name = (
        unicodedata.normalize("NFD", name.lower())
        .encode("ascii", "ignore")
        .decode("utf-8")
        .replace(" ", ".")
    )
    username = clean_name + str(random.randint(1, 999))
    return f"{username}@{random.choice(domains)}"


def generate_person_entity(possible_positions: list) -> dict:
    name = fake.name()
    person_data = {
        "nome": name,
        "email": generate_email(name),
        "telefone": generate_phone_various_formats(),
        "documentos": {
            "cpf": generate_cpf_in_various_formats(),
            "rg": generate_rg(),
            "cnh": generate_cnh(),
        },
        "profissional": {
            "matricula": fake.random_number(digits=5, fix_len=True),
            "cargo": random.choice(possible_positions),
            "oab": (generate_oab() if random.random() < 0.1 else None),
        },
        "financeiro": {
            "cartao_de_credito": (
                generate_credit_card() if random.random() < 0.5 else None
            ),
        },
    }
    return person_data


def generate_company_entity(company_type: str, possible_positions: list) -> dict:
    name = fake.company()
    contact_name = fake.name()
    contact_person = {
        "nome": contact_name,
        "cargo": random.choice(possible_positions),
        "email": generate_email(contact_name),
        "telefone_comercial": generate_phone_various_formats(),
    }
    company_data = {
        "razao_social": name,
        "nome_fantasia": f"{name.split()[0]} {fake.bs().title()}",
        "cnpj": generate_cnpj_various_formats(),
        "endereco_fiscal": f"{fake.street_address()}, {fake.city()} - {fake.state_abbr()}, CEP {generate_postcode_various_formats()}",
        "contato_principal": contact_person,  # <-- Entidade aninhada!
        "financeiro": {
            "conta_bancaria": generate_bank_account_br(),
            "chave_pix": generate_pix_key(),
        },
        "juridico": {
            "processo_judicial": (
                generate_lawsuit_number() if random.random() < 0.2 else "N/A"
            )
        },
        "rede": {
            "ip_servidor_principal": fake.ipv4_public(),
            "mac_address_gateway": fake.mac_address(),
        },
    }
    return company_data


def generate_location_entity(location_names: list) -> dict:
    name = random.choice(location_names)
    return {
        "nome": name,
        "cnpj": generate_cnpj_various_formats(),
        "endereco": f"{fake.street_address()}, {fake.city()} - {fake.state_abbr()}, CEP {generate_postcode_various_formats()}",
        "telefone": generate_phone_various_formats(),
    }


def combine_blocks(block_dict: dict, min_blocks: int, max_blocks: int):
    num_blocks = random.randint(min_blocks, max_blocks)
    keys = random.sample(list(block_dict.keys()), k=num_blocks)
    return [random.choice(block_dict[key]) for key in keys], keys


def dict_to_namespace(d: dict) -> dict:
    return {k: SimpleNamespace(**v) if isinstance(v, dict) else v for k, v in d.items()}


def apply_persona_to_text(text: str, persona: dict) -> str:
    prefix = random.choice(persona["prefixos"])
    suffix = random.choice(persona["sufixos"])
    return f"{prefix} {text} {suffix}"


def generate_random_dates(
    incident_days_range=(10, 20), antecedent_days_range=(60, 180)
) -> dict:
    incident_date = datetime.now() - timedelta(
        days=random.randint(*incident_days_range)
    )
    report_date = incident_date + timedelta(days=2)
    warning_date = incident_date - timedelta(
        days=random.randint(*antecedent_days_range)
    )
    return {
        "data_incidente": incident_date.strftime("%d/%m/%Y"),
        "data_relatorio": report_date.strftime("%d/%m/%Y"),
        "data_advertencia": warning_date.strftime("%d/%m/%Y"),
    }


def generate_rg() -> str:
    base = fake.rg().replace(".", "").replace("-", "")
    return f"{base[:2]}.{base[2:5]}.{base[5:8]}-{base[8:]}"


def generate_cnh() -> str:
    return fake.random_number(digits=11, fix_len=True)


def generate_oab() -> str:
    return f"{fake.random_number(digits=random.randint(4, 6))}/{fake.state_abbr()}"


def generate_credit_card() -> str:
    return fake.credit_card_number()


def generate_bank_account_br() -> str:
    agencia = f"{fake.random_number(digits=4, fix_len=True)}-{fake.random_digit()}"
    conta = f"{fake.random_number(digits=6, fix_len=True)}-{fake.random_digit()}"
    return f"Ag: {agencia} / CC: {conta}"


def generate_pix_key() -> str:
    tipo = random.choice(["cpf", "cnpj", "email", "telefone", "evp"])
    if tipo == "cpf":
        return generate_cpf_in_various_formats()
    if tipo == "cnpj":
        return generate_cnpj_various_formats()
    if tipo == "email":
        return fake.email()
    if tipo == "telefone":
        return f"+55{fake.msisdn()}"
    if tipo == "evp":
        return str(fake.uuid4())
    return ""


def generate_lawsuit_number() -> str:
    return f"{fake.random_number(digits=7, fix_len=True)}-{fake.random_number(digits=2, fix_len=True)}.{fake.random_number(digits=4, fix_len=True)}.{fake.random_digit()}.{fake.random_number(digits=2, fix_len=True)}.{fake.random_number(digits=4, fix_len=True)}"


class SafeNamespace(SimpleNamespace):
    def __getattr__(self, name):
        return f"{{{name}_NAO_ENCONTRADO}}"


def dict_to_safe_namespace(d: dict):
    if not isinstance(d, dict):
        return d

    for key, value in d.items():
        d[key] = dict_to_safe_namespace(value)

    return SafeNamespace(**d)


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
