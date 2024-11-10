import os
import requests
from dotenv import load_dotenv


load_dotenv()

SUPERJOB_API_KEY = os.getenv("SUPERJOB_API_KEY")


def get_vacancy_titles():
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": SUPERJOB_API_KEY
    }

    params = {
        "town": "Москва",
        "count": 20
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        vacancies = response.json().get("objects", [])

        # Выводим названия вакансий
        for vacancy in vacancies:
            print(vacancy.get("profession"))
    else:
        print(f"Ошибка при запросе: {response.status_code}")


get_vacancy_titles()
