import os
import requests
import time
from dotenv import load_dotenv
from terminaltables import AsciiTable


load_dotenv()

SUPERJOB_API_KEY = os.getenv("SUPERJOB_API_KEY")


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8
    return None


def predict_rub_salary_hh(vacancy):
    salary_details = vacancy.get("salary")
    if salary_details and salary_details.get("currency") == "RUR":
        return predict_salary(salary_details.get("from"), salary_details.get("to"))
    return None


def predict_rub_salary_sj(vacancy):
    if vacancy.get("currency") == "rub":
        return predict_salary(vacancy.get("payment_from"), vacancy.get("payment_to"))
    return None


def get_all_vacancies_hh(language):
    url = "https://api.hh.ru/vacancies"
    all_salaries = []
    page = 0
    per_page = 100

    while True:
        search_params = {
            "text": f"Программист {language}",
            "area": 1,
            "date_from": "2024-10-10",
            "per_page": per_page,
            "page": page
        }

        response = requests.get(url, params=search_params)

        if response.status_code != 200:
            print(f"Ошибка при запросе для {language}, страница {page}: {response.status_code}")
            break

        vacancies_page = response.json()
        vacancies = vacancies_page.get("items", [])

        if not vacancies:
            break

        print(f"Загружаю {language}, страница {page + 1}")

        for vacancy in vacancies:
            salary = predict_rub_salary_hh(vacancy)
            if salary:
                all_salaries.append(salary)

        page += 1
        time.sleep(0.2)

    return all_salaries, vacancies_page.get("found", 0)


def get_language_statistics_hh(language):
    all_salaries, vacancies_found = get_all_vacancies_hh(language)
    vacancies_processed = len(all_salaries)
    average_salary = int(sum(all_salaries) / vacancies_processed) if vacancies_processed > 0 else None

    return {
        "vacancies_found": vacancies_found,
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }


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
            "page": page,
            "count": 100
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
            salary = predict_rub_salary_sj(vacancy)
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


def print_statistics_table(title, statistics):
    table_data = [
        ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
    ]

    for language, stats in statistics.items():
        table_data.append([
            language,
            stats["vacancies_found"],
            stats["vacancies_processed"],
            stats["average_salary"]
        ])

    table = AsciiTable(table_data, title)
    print(table.table)


languages = ["Python", "Java", "JavaScript", "C++", "C#", "Ruby", "PHP", "Swift", "Go", "Kotlin"]

hh_statistics = {language: get_language_statistics_hh(language) for language in languages}
print_statistics_table("HeadHunter Moscow", hh_statistics)

sj_statistics = {language: get_superjob_vacancies(language) for language in languages}
print_statistics_table("SuperJob Moscow", sj_statistics)
