import json
import random
from datetime import timedelta

from faker import Faker

fake = Faker("pt_BR")
fake_en = Faker()
Faker.seed(4321)
random.seed(4321)

# Lista de DDDs válidos no Brasil
valid_ddd = [
    "11", "12", "13", "14", "15", "16", "17", "18", "19",  # São Paulo
    "21", "22", "24",  # Rio de Janeiro
    "27", "28",  # Espírito Santo
    "31", "32", "33", "34", "35", "37", "38",  # Minas Gerais
    "41", "42", "43", "44", "45", "46",  # Paraná
    "47", "48", "49",  # Santa Catarina
    "51", "53", "54", "55",  # Rio Grande do Sul
    "61",  # Distrito Federal
    "62", "64",  # Goiás
    "63",  # Tocantins
    "65", "66",  # Mato Grosso
    "67",  # Mato Grosso do Sul
    "68",  # Acre
    "69",  # Rondônia
    "71", "73", "74", "75", "77",  # Bahia
    "79",  # Sergipe
    "81", "87",  # Pernambuco
    "82",  # Alagoas
    "83",  # Paraíba
    "84",  # Rio Grande do Norte
    "85", "88",  # Ceará
    "86", "89",  # Piauí
    "91", "93", "94",  # Pará
    "92", "97",  # Amazonas
    "95",  # Roraima
    "96",  # Amapá
    "98", "99"  # Maranhão
]

def generate_brazil_phone_number():
    ddd = random.choice(valid_ddd)
    return f"+55 {ddd} 9{fake.msisdn()[3:7]}-{fake.msisdn()[7:11]}"


def generate_synthetic_data(num_records):
    data = []

    for i in range(num_records):
        call_id = i + 1
        phone_number = generate_brazil_phone_number()
        start_time = fake.date_time_this_year()
        end_time = start_time + timedelta(minutes=random.randint(1, 30))
        call_status = random.choices(
            ["completa", "incompleta", "falha"], weights=[0.7, 0.25, 0.05]
        )[0]
        num_system_messages = random.randint(5, 15)
        num_user_messages = num_system_messages + random.choice([-1, 0, 1])
        history_messages = {
            "usuario": [fake_en.sentence() for _ in range(num_user_messages)],
            "sistema": [fake_en.sentence() for _ in range(num_system_messages)],
        }
        service = random.choices(["agendamento", "informação"], weights=[0.775, 0.225])[
            0
        ]
        reviewed = random.choices([True, False], weights=[0.6, 0.4])[0]
        rating = random.randint(1, 10) if reviewed else None

        record = {
            "id_chamada": call_id,
            "numero_telefone": phone_number,
            "hora_inicio": start_time.isoformat(),
            "hora_fim": end_time.isoformat(),
            "status_chamada": call_status,
            "historico_mensagens": history_messages,
            "servico": service,
            "avaliada": reviewed,
            "avaliacao": rating,
        }

        data.append(record)

    return data


num_records = 10000
synthetic_data = generate_synthetic_data(num_records)

# Save to a JSON file
with open("conversas.json", "w", encoding="utf-8") as f:
    json.dump(synthetic_data, f, indent=4, ensure_ascii=False)

print(f"Foram gerados {num_records} registros sintéticos e salvos em conversas.json")
