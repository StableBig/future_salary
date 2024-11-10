import os
import requests
import time
from dotenv import load_dotenv


load_dotenv()

SUPERJOB_API_KEY = os.getenv("SUPERJOB_API_KEY")


def predict_rub_salary(vacancy):
    if vacancy.get("currency") == "rub":
        min_salary = vacancy.get("payment_from")
        max_salary = vacancy.get("payment_to")

        if min_salary and max_salary:
            return (min_salary + max_salary) / 2
        elif min_salary:
            return min_salary * 1.2
        elif max_salary:
            return max_salary * 0.8
    return None


def get_superjob_vacancies(language):
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": SUPERJOB_API_KEY
    }
    all_salaries = []
    page = 0

    while True:
        params = {
            "keyword": f"Программист {language}",
            "town": "Москва",
            "page": page
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Ошибка при запросе для {language}, страница {page}: {response.status_code}")
            break

        vacancies_page = response.json()
        vacancies = vacancies_page.get("objects", [])

        if not vacancies:
            break

        print(f"Загружаю {language}, страница {page + 1}")

        for vacancy in vacancies:
            salary = predict_rub_salary(vacancy)
            if salary:
                all_salaries.append(salary)

        page += 1
        time.sleep(0.2)

    vacancies_found = vacancies_page.get("total")
    vacancies_processed = len(all_salaries)
    average_salary = int(sum(all_salaries) / vacancies_processed) if vacancies_processed > 0 else None

    return {
        "vacancies_found": vacancies_found,
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }


languages = ["Python", "Java", "JavaScript", "C++", "C#", "Ruby", "PHP", "Swift", "Go", "Kotlin"]
superjob_statistics = {}

for language in languages:
    superjob_statistics[language] = get_superjob_vacancies(language)

print(superjob_statistics)
