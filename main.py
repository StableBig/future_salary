import requests


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


def get_vacancy_statistics(language):
    url = "https://api.hh.ru/vacancies"
    search_params = {
        "text": f"Программист {language}",
        "area": 1,
        "date_from": "2024-10-10",
        "per_page": 20
    }

    response = requests.get(url, params=search_params)
    if response.status_code != 200:
        print(f"Ошибка при запросе для {language}: {response.status_code}")
        return None

    vacancies = response.json()
    salaries = []

    for vacancy in vacancies.get("items", []):
        salary = predict_rub_salary(vacancy)
        if salary:
            salaries.append(salary)

    vacancies_found = vacancies.get("found", 0)
    vacancies_processed = len(salaries)
    average_salary = int(sum(salaries) / vacancies_processed) if vacancies_processed > 0 else None

    return {
        "vacancies_found": vacancies_found,
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }


languages = ["Python", "Java", "JavaScript", "C++", "C#", "Ruby", "PHP", "Swift", "Go", "Kotlin"]
language_statistics = {}

for language in languages:
    stats = get_vacancy_statistics(language)
    if stats:
        language_statistics[language] = stats

print(language_statistics)
