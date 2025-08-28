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
