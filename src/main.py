from src.config import config
from src.dbmanager import DBManager


def user_interaction():
    '''функция взаимодействия с пользователем'''

    params = config()
    db = DBManager(**params)
    db.create_table()
    db.save_to_database()

    print("Привет!\nВыберите команду:\n1 - Список всех компаний и количество их вакансий.\n"
          "2 - Список всех вакансий с информацией по каждой.\n"
          "3 - Указать среднюю зарплату.\n4 - Список вакансий с зарплатой выше средней.\n"
          "5 - Поиск по ключевому слову.\n")
    user_input = int(input())
    if user_input == 1:
        all_companies = db.get_companies_and_vacancies_count()
        print(all_companies)
    elif user_input == 2:
        all_vacancies = db.get_all_vacancies()
        print(all_vacancies)
    elif user_input == 3:
        avg_salary = db.get_avg_salary()
        print(avg_salary)
    elif user_input == 4:
        high_salary = db.get_vacancies_with_higher_salary()
        print(high_salary)
    elif user_input == 5:
        keyword_input = input("Введите ключевое слово...")
        vacancy_with_keyword = db.get_vacancies_with_keyword(keyword_input)
        print(vacancy_with_keyword)


if __name__ == "__main__":
    user_interaction()
