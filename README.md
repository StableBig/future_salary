# Анализ зарплат для программистов на основе данных HeadHunter и SuperJob

Этот проект анализирует вакансии программистов на популярных платформах **HeadHunter** и **SuperJob** и вычисляет статистику по зарплатам для различных языков программирования. Итоговая информация выводится в удобной таблице с данными о количестве вакансий, обработанных объявлениях и средней зарплате для каждого языка программирования.

## 🚀 Установка и запуск

1. **Клонируйте репозиторий и перейдите в директорию проекта:**

    ```bash
    git clone https://github.com/StableBig/future_salary
    cd future_salary
    ```

2. **Создайте виртуальную среду и активируйте её:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # для macOS/Linux
    venv\Scripts\activate     # для Windows
    ```

3. **Установите зависимости:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Создайте файл `.env` для переменных окружения:**

    В корневой папке создайте файл `.env` и добавьте в него API-ключ для **SuperJob**:

    ```plaintext
    SUPERJOB_API_KEY=ваш_секретный_ключ
    ```

   > Получить API-ключ можно на [странице разработчиков SuperJob](https://api.superjob.ru/).

5. **Запуск проекта:**

    Выполните следующую команду, чтобы запустить анализ и вывести статистику по зарплатам:

    ```bash
    python job_salary_statistics.py
    ```

## 📊 Результат

Скрипт выведет две таблицы в консоли:

- **HeadHunter Moscow**: статистика по зарплатам для программистов в Москве, найденных на платформе HeadHunter.
- **SuperJob Moscow**: аналогичная статистика с платформы SuperJob.

Каждая таблица содержит:

- Название языка программирования
- Количество найденных вакансий
- Количество обработанных вакансий
- Среднюю зарплату

## 🛠 Зависимости

Основные зависимости:

- `requests` — для выполнения HTTP-запросов к API.
- `python-dotenv` — для загрузки переменных окружения.
- `terminaltables` — для форматирования и отображения таблиц в консоли.

Все зависимости указаны в `requirements.txt`.

---

# Programmer Salary Analysis Based on HeadHunter and SuperJob Data

This project analyzes programmer job postings on popular platforms **HeadHunter** and **SuperJob** and calculates salary statistics for various programming languages. The final output displays a neat table with information on the number of job postings, processed entries, and the average salary for each programming language.

## 🚀 Installation and Setup

1. **Clone the repository and navigate to the project directory:**

    ```bash
    git clone https://github.com/StableBig/future_salary
    cd future_salary
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    venv\Scripts\activate     # Windows
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create an `.env` file for environment variables:**

    In the root directory, create an `.env` file and add the API key for **SuperJob**:

    ```plaintext
    SUPERJOB_API_KEY=your_secret_key
    ```

   > You can obtain the API key from the [SuperJob Developer page](https://api.superjob.ru/).

5. **Run the project:**

    Execute the following command to start the analysis and view salary statistics:

    ```bash
    python job_salary_statistics.py
    ```

## 📊 Output

The script will display two tables in the console:

- **HeadHunter Moscow**: salary statistics for programmers in Moscow from HeadHunter.
- **SuperJob Moscow**: similar statistics from SuperJob.

Each table contains:

- Programming language name
- Number of job postings found
- Number of processed postings
- Average salary

## 🛠 Dependencies

Key dependencies:

- `requests` — for HTTP requests to the APIs.
- `python-dotenv` — for loading environment variables.
- `terminaltables` — for formatting and displaying tables in the console.

All dependencies are listed in `requirements.txt`. 
