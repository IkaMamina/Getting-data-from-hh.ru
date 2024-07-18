import psycopg2
from src.api import HHParser


class DBManager:
    '''класс для работы с БД. Создание и сохранение данных в БД'''
    def __init__(self, dbname: str, user: str, password: str, host: str, port: int):
        self.connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    def create_table(self):
        '''создание таблиц БД'''

        cursor = self.connection.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS employers
                       (id SERIAL PRIMARY KEY,
                       name VARCHAR UNIQUE NOT NULL,
                       company_url TEXT);
                       """)
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS vacancies(
                        id int PRIMARY KEY,
                        name VARCHAR,
                        salary_from INT,
                        salary_to INT,
                        url VARCHAR(255),
                        area VARCHAR(255),
                        employer INTEGER REFERENCES employers(id) NOT NULL);
                        """)

        self.connection.commit()
        cursor.close()

    def save_to_database(self):
        """сохранение данных в БД"""

        hh = HHParser()
        employers = hh.get_employers()
        vacancies = hh.get_vacancies_list()
        cursor = self.connection.cursor()
        for employer in employers:
            cursor.execute("""
                           INSERT INTO employers (id, name, company_url) VALUES (%s, %s, %s)""",
                           (employer["id"], employer["name"], employer["company_url"]))

        for vacancy in vacancies:
            cursor.execute("""
                           INSERT INTO vacancies (id, name, salary_from, salary_to, url, area, employer) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                           (vacancy["id"], vacancy["name"],
                            vacancy["salary_from"], vacancy["salary_to"],
                            vacancy["url"], vacancy["area"], vacancy["employer"]))

        self.connection.commit()
        cursor.close()

    def get_companies_and_vacancies_count(self):
        '''получает список всех компаний и количество вакансий у каждой компании.'''

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT employers.name,
            COUNT (vacancies.id) FROM employers
            LEFT JOIN vacancies ON employers.id = vacancies.employer
            GROUP BY employers.name;
            """)
        return cursor.fetchall()

    def get_all_vacancies(self=None):
        '''получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию'''

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT employers.name, vac.name, salary_from, url
            FROM vacancies as vac
            LEFT JOIN employers ON vac.employer = employers.id;
            """)
        return cursor.fetchall()

    def get_avg_salary(self):
        '''получает среднюю зарплату по вакансиям.'''

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT vacancies.name, round(AVG(salary_from)) AS average_salary
            FROM vacancies
            GROUP BY vacancies.name
            ORDER BY average_salary DESC;
            """)
        return cursor.fetchall()

    def get_vacancies_with_higher_salary(self):
        '''получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.'''

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT vacancies.name, salary_from
            FROM vacancies
            WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)
            ORDER BY salary_from DESC;
            """)

        return cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        '''получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.'''

        cursor = self.connection.cursor()
        cursor.execute(
            f"SELECT vacancies.name FROM vacancies WHERE LOWER(name) LIKE '%{keyword}%'")
        return cursor.fetchall()