import psycopg2


class DBManager:
    """Создает и заполняет базы данных"""

    def __init__(self, database_name: str, params: dict) -> None:
        self.database_name = database_name
        self.params = params

    def db_create(self):
        """Создание базы данных и таблиц для сохранения данных о работодателях и вакансиях."""
        db_connection = psycopg2.connect(dbname='postgres', **self.params)
        db_connection.autocommit = True
        db_cursor = db_connection.cursor()

        db_cursor.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
        db_cursor.execute(f"CREATE DATABASE {self.database_name}")

        db_cursor.close()
        db_connection.close()

        with psycopg2.connect(dbname=self.database_name, **self.params) as db_connection:
            print("Successfully connected to the database.")
            with db_connection.cursor() as db_cursor:
                db_cursor.execute(
                    """
                    CREATE TABLE employers (
                        id_employer INT PRIMARY KEY,
                        name_employer VARCHAR(100) NOT NULL,
                        open_vacancies VARCHAR,
                        url_employer TEXT
                    )""")

            with db_connection.cursor() as db_cursor:
                db_cursor.execute(
                    """
                    CREATE TABLE vacancies (
                        id_vacancy INT PRIMARY KEY,
                        name_vacancy VARCHAR(100) NOT NULL,
                        id_employer INT REFERENCES employers(id_employer),
                        name_employer VARCHAR NOT NULL,
                        salary_from INT,
                        salary_to INT,
                        salary_avg INT,
                        city VARCHAR(100),
                        experience TEXT,
                        requirement TEXT,
                        url TEXT
                    )""")

    def save_employers_to_db(self, data):
        print("Successfully save employers to the database.")
        with psycopg2.connect(dbname=self.database_name, **self.params) as db_connection:
            with db_connection.cursor() as db_cursor:
                for employer in data:
                    db_cursor.execute(
                        """
                        INSERT INTO employers (id_employer, name_employer, open_vacancies, url_employer)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (id_employer) DO NOTHING
                        RETURNING id_employer
                        """,
                        (employer['id'], employer['name'], employer['open_vacancies'], employer['alternate_url']))

    def save_vacancies_to_db(self, data):
        print("Successfully save vacancies to the database.")
        with psycopg2.connect(dbname=self.database_name, **self.params) as db_connection:
            with db_connection.cursor() as db_cursor:
                for vacancy in data:
                    db_cursor.execute(
                        """
                        INSERT INTO vacancies (id_vacancy, name_vacancy, id_employer, name_employer, city, salary_from, 
                        salary_to, salary_avg, experience, requirement, url)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (vacancy['id_vacancy'], vacancy['name_vacancy'], vacancy['id_employer'],
                         vacancy['name_employer'],
                         vacancy['city'], vacancy['salary_from'], vacancy['salary_to'], vacancy['salary_avg'],
                         vacancy['experience'], vacancy['requirement'], vacancy['url']))

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        with psycopg2.connect(dbname=self.database_name, **self.params) as db_connection:
            list_companies_and_vacancies_count = []
            with db_connection.cursor() as db_cursor:
                db_cursor.execute("SELECT name_employer, open_vacancies FROM employers")
                rows = db_cursor.fetchall()
                for row in rows:
                    list_companies_and_vacancies_count.append(row)
                return list_companies_and_vacancies_count

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии
        и зарплаты, и ссылки, на вакансию."""
        with psycopg2.connect(dbname=self.database_name, **self.params) as db_connection:
            list_all_vacancies = []
            with db_connection.cursor() as db_cursor:
                db_cursor.execute("SELECT name_employer, name_vacancy, salary_from, salary_to, url FROM vacancies")
                rows = db_cursor.fetchall()
                for row in rows:
                    list_all_vacancies.append(row)
                return list_all_vacancies

    def get_avg_salary(self):
        """ Получает среднюю зарплату по вакансиям."""
        with psycopg2.connect(dbname=self.database_name, **self.params) as db_connection:
            with db_connection.cursor() as db_cursor:
                db_cursor.execute("SELECT ROUND(AVG(salary_avg)) as avg_salary FROM vacancies")
                return db_cursor.fetchall()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with psycopg2.connect(dbname=self.database_name, **self.params) as db_connection:
            list_with_higher_salary_vacancies = []
            with db_connection.cursor() as db_cursor:
                db_cursor.execute(
                    "SELECT name_employer, name_vacancy, salary_avg, url FROM vacancies"
                    " WHERE salary_avg > (SELECT AVG(salary_avg) FROM vacancies)"
                )
                rows = db_cursor.fetchall()
                for row in rows:
                    list_with_higher_salary_vacancies.append(row)
                return list_with_higher_salary_vacancies

    def get_vacancies_with_keyword(self, word: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”."""
        with psycopg2.connect(dbname=self.database_name, **self.params) as db_connection:
            list_with_keyword_vacancies = []
            with db_connection.cursor() as db_cursor:
                db_cursor.execute(
                    "SELECT * FROM vacancies"
                    f" WHERE name_vacancy LIKE '%{word}%'"
                )
                rows = db_cursor.fetchall()
                for row in rows:
                    list_with_keyword_vacancies.append(row)
                return list_with_keyword_vacancies
