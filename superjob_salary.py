import os
import requests
from dotenv import load_dotenv


load_dotenv()

SUPERJOB_API_KEY = os.getenv("SUPERJOB_API_KEY")


def get_programmer_vacancies():
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": SUPERJOB_API_KEY
    }

    params = {
        "keyword": "Программист",
        "town": "Москва",
        "count": 20
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        vacancies = response.json().get("objects", [])

        for vacancy in vacancies:
            profession = vacancy.get("profession")
            town = vacancy.get("town", {}).get("title")
            print(f"{profession}, {town}")
    else:
        print(f"Ошибка при запросе: {response.status_code}")


get_programmer_vacancies()
