import os
import requests
from dotenv import load_dotenv


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
    salary_info = vacancy.get("salary")
    if salary_info and salary_info.get("currency") == "RUR":
        return predict_salary(salary_info.get("from"), salary_info.get("to"))
    return None


def predict_rub_salary_sj(vacancy):
    if vacancy.get("currency") == "rub":
        return predict_salary(vacancy.get("payment_from"), vacancy.get("payment_to"))
    return None


def get_programmer_vacancies_with_salary():
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
            expected_salary = predict_rub_salary_sj(vacancy)
            print(f"{profession}, {town}, {expected_salary}")
    else:
        print(f"Ошибка при запросе: {response.status_code}")


get_programmer_vacancies_with_salary()
