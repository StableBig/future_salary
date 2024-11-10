import requests
import time


def predict_rub_salary(vacancy):
    salary_info = vacancy.get("salary")

    if salary_info and salary_info.get("currency") == "RUR":
        min_salary = salary_info.get("from")
        max_salary = salary_info.get("to")

        if min_salary and max_salary:
            return (min_salary + max_salary) / 2
        elif min_salary:
            return min_salary * 1.2
        elif max_salary:
            return max_salary * 0.8
    return None


def get_all_vacancies(language):
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
            salary = predict_rub_salary(vacancy)
            if salary:
                all_salaries.append(salary)

        page += 1
        time.sleep(0.2)

    return all_salaries, vacancies_page.get("found", 0)


def get_language_statistics(language):
    all_salaries, vacancies_found = get_all_vacancies(language)
    vacancies_processed = len(all_salaries)
    average_salary = int(sum(all_salaries) / vacancies_processed) if vacancies_processed > 0 else None

    return {
        "vacancies_found": vacancies_found,
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }


languages = ["Python", "Java", "JavaScript", "C++", "C#", "Ruby", "PHP", "Swift", "Go", "Kotlin"]
language_statistics = {}

for language in languages:
    language_statistics[language] = get_language_statistics(language)

print(language_statistics)
