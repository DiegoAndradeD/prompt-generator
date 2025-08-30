import random
import unicodedata
from faker import Faker
from fordev import generators


class PIIGenerator:
    def __init__(self):
        self.fake = Faker("pt_BR")

    def get_person_profile(self, sex="R"):
        try:
            person_data = generators.people(sex=sex, data_only=True)[0]
        except Exception:
            person_data = {
                "nome": self.fake.name(),
                "data_nasc": self.fake.date_of_birth().strftime("%d/%m/%Y"),
                "cpf": generators.cpf(data_only=True),
                "endereco": self.fake.street_name(),
                "numero": str(random.randint(1, 9999)),
                "cep": self.fake.postcode(),
                "cidade": self.fake.city(),
                "estado": self.fake.state_abbr(),
            }

        person_data["job"] = self.fake.job()
        first_name = person_data["nome"].split(" ")[0].lower()
        first_name = self._normalize_string(first_name)
        last_name = self._normalize_string(self.fake.last_name().lower())
        person_data["email"] = f"{first_name}.{last_name}@empresa-ficticia.com"

        person_data["phone"] = self.fake.phone_number()

        person_data["name"] = person_data.pop("nome", person_data.get("name", ""))
        person_data["birth_date"] = person_data.pop(
            "data_nasc", person_data.get("birth_date", "")
        )

        endereco = person_data.pop("endereco", "")
        numero = person_data.pop("numero", "")
        person_data["address"] = (
            f"{endereco}, {numero}" if endereco and numero else self.fake.address()
        )

        return person_data

    def _normalize_string(self, text):

        normalized = unicodedata.normalize("NFD", text)
        return "".join(c for c in normalized if unicodedata.category(c) != "Mn")

    def get_vehicle_info(self):
        try:
            brand_code = random.choice([27, 33, 29, 85, 82, 37])
            vehicle_data = generators.vehicle(brand_code=brand_code, data_only=True)

            return {
                "vehicle": f"{vehicle_data.get('brand', 'Marca')} {vehicle_data.get('model', 'Modelo')}",
                "vehicle_plate": generators.vehicle_plate(data_only=True),
                "renavam": generators.renavam(data_only=True),
            }
        except Exception:
            return {
                "vehicle": f"{self.fake.word().title()} {self.fake.word().title()}",
                "vehicle_plate": f"{self.fake.lexify('???-????').upper()}",
                "renavam": f"{random.randint(10000000000, 99999999999)}",
            }

    def get_corporate_expense_info(self):
        try:
            card_data = generators.credit_card(
                bank=random.choice([1, 2]), data_only=True
            )
            return {
                "credit_card": card_data.get("credit_card", ""),
                "credit_card_brand": card_data.get("credit_card_brand", "Visa"),
                "expense_value": f"R$ {random.randint(150, 800)},00",
            }
        except Exception:
            return {
                "credit_card": self.fake.credit_card_number(),
                "credit_card_brand": random.choice(["Visa", "Mastercard", "Elo"]),
                "expense_value": f"R$ {random.randint(150, 800)},00",
            }

    def get_previous_employer_info(self):
        try:
            company_data = generators.company(data_only=True)
            return {
                "previous_employer_name": company_data.get("nome", ""),
                "previous_employer_cnpj": company_data.get("cnpj", ""),
            }
        except Exception:
            return {
                "previous_employer_name": f"{self.fake.company()} {random.choice(['Ltda', 'S.A.', 'EIRELI'])}",
                "previous_employer_cnpj": generators.cnpj(data_only=True),
            }

    def get_medical_info(self):
        cids = ["A09", "J06.9", "K02.1", "M54.5", "Z76.5"]
        return {
            "cid": random.choice(cids),
            "doctor_name": f"Dr(a). {self.fake.name()}",
            "hospital": f"Hospital {self.fake.city()}",
        }

    def get_legal_info(self):
        return {
            "legal_case_number": f"{random.randint(10000, 99999)}-{random.randint(10,99)}.{self.fake.year()}.5.02.{random.randint(1000,9999)}",
            "lawyer_name": f"Dr(a). {self.fake.name()}",
        }

    def get_full_profile(self, sex="R"):
        try:
            profile = self.get_person_profile(sex)
            profile.update(self.get_vehicle_info())
            profile.update(self.get_corporate_expense_info())
            profile.update(self.get_previous_employer_info())
            profile.update(self.get_medical_info())
            profile.update(self.get_legal_info())

            return profile
        except Exception as e:
            print(f"Erro ao gerar perfil completo: {e}")
            return {}
