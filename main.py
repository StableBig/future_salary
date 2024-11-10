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


url = "https://api.hh.ru/vacancies"
search_params = {
    "text": "Программист Python",
    "area": 1,
    "date_from": "2024-10-10",
    "per_page": 20
}

response = requests.get(url, params=search_params)

if response.status_code == 200:
    vacancies = response.json().get("items", [])

    for vacancy in vacancies:
        expected_salary = predict_rub_salary(vacancy)
        print(expected_salary)
else:
    print(f"Ошибка при запросе: {response.status_code}")
