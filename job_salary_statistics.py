import os
import requests
import time
from dotenv import load_dotenv
from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):
    """Рассчитывает ожидаемую зарплату на основе диапазона."""
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8
    return None


def predict_rub_salary_hh(vacancy):
    """Возвращает ожидаемую зарплату для вакансии с HeadHunter в рублях."""
    salary_details = vacancy.get("salary")
    if salary_details and salary_details.get("currency") == "RUR":
        return predict_salary(salary_details.get("from"), salary_details.get("to"))
    return None


def predict_rub_salary_sj(vacancy):
    """Возвращает ожидаемую зарплату для вакансии с SuperJob в рублях."""
    if vacancy.get("currency") == "rub":
        return predict_salary(vacancy.get("payment_from"), vacancy.get("payment_to"))
    return None


def get_all_vacancies_hh(language):
    """Получает все вакансии для указанного языка программирования с HeadHunter."""
    url = "https://api.hh.ru/vacancies"
    all_salaries = []
    page = 0
    per_page = 100
    total_pages = 1

    while page < total_pages:
        search_params = {
            "text": f"Программист {language}",
            "area": 1,
            "date_from": "2024-10-10",
            "per_page": per_page,
            "page": page
        }

        response = requests.get(url, params=search_params)

        if not response.ok:
            print(f"Ошибка при запросе для {language}, страница {page}: {response.status_code}")
            break

        vacancies_page = response.json()
        vacancies = vacancies_page.get("items", [])
        total_pages = vacancies_page.get("pages", 1)

        if not vacancies:
            break

        print(f"Загружаю {language}, страница {page + 1} из {total_pages}")

        for vacancy in vacancies:
            salary = predict_rub_salary_hh(vacancy)
            if salary:
                all_salaries.append(salary)

        page += 1
        time.sleep(0.2)

    return all_salaries, vacancies_page.get("found", 0)


def get_language_statistics_hh(language):
    """Возвращает статистику по зарплатам для указанного языка программирования с HeadHunter."""
    all_salaries, vacancies_found = get_all_vacancies_hh(language)
    vacancies_processed = len(all_salaries)
    average_salary = int(sum(all_salaries) / vacancies_processed) if vacancies_processed else None

    return {
        "vacancies_found": vacancies_found,
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }


def get_superjob_vacancies(language, api_key):
    """Получает все вакансии для указанного языка программирования с SuperJob."""
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": api_key
    }
    all_salaries = []
    page = 0
    total_pages = 1

    while page < total_pages:
        params = {
            "keyword": f"Программист {language}",
            "town": "Москва",
            "page": page,
            "count": 100
        }

        response = requests.get(url, headers=headers, params=params)

        if not response.ok:
            print(f"Ошибка при запросе для {language}, страница {page}: {response.status_code}")
            break

        vacancies_page = response.json()
        vacancies = vacancies_page.get("objects", [])
        total_pages = (vacancies_page.get("total", 0) // 100) + 1

        if not vacancies:
            break

        print(f"Загружаю {language}, страница {page + 1} из {total_pages}")

        for vacancy in vacancies:
            salary = predict_rub_salary_sj(vacancy)
            if salary:
                all_salaries.append(salary)

        page += 1
        time.sleep(0.2)

    vacancies_found = vacancies_page.get("total")
    vacancies_processed = len(all_salaries)
    average_salary = int(sum(all_salaries) / vacancies_processed) if vacancies_processed else None

    return {
        "vacancies_found": vacancies_found,
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }


def print_statistics_table(title, statistics):
    """Выводит статистику по языкам программирования в виде таблицы."""
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


def main():
    load_dotenv()
    superjob_api_key = os.getenv("SUPERJOB_API_KEY")
    languages = ["Python", "Java", "JavaScript", "C++", "C#", "Ruby", "PHP", "Swift", "Go", "Kotlin"]

    hh_statistics = {language: get_language_statistics_hh(language) for language in languages}
    print_statistics_table("HeadHunter Moscow", hh_statistics)

    sj_statistics = {language: get_superjob_vacancies(language, superjob_api_key) for language in languages}
    print_statistics_table("SuperJob Moscow", sj_statistics)


if __name__ == "__main__":
    main()
