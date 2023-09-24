from src.database_manager import DBManager
from src.hh_api import HeadHunter, Vacancy

params = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'qwerty'
}


def iterator(database: DBManager):
    value = 1
    while value <= 1:
        customer_name = input('Введите название компании: ')
        hh = HeadHunter(customer_name)
        data = hh.get_company
        for i in range(len(data)):
            id_emp = data[i]["id"]
            vac = Vacancy(id_emp)
            vacancy_list = vac.add_vacancies_to_list()

            database.save_employers_to_db(data)
            database.save_vacancies_to_db(vacancy_list)
        value += 1


def main():
    database = DBManager('hh_database', params)
    database.db_create()
    iterator(database)
    while True:
        db_manager = DBManager('hh_database', params)
        emp_and_count = db_manager.get_companies_and_vacancies_count()

        print('\nНажмите 1, чтобы просмотреть сколько вакансий в компании.')
        print('Нажмите 2, чтобы узнать среднюю зарплату.')
        print('Нажмите 3, чтобы узнать вакансии, зарплата по которым выше средней из найденных.')
        print('Нажмите 4, чтобы посмотреть все вакансии по ключевому слову.')
        print('Нажмите 5, чтобы закончить работу программы.')

        user_number = input()

        if user_number == '1':
            print(f"Cписок всех компаний и количество вакансий у каждой компании: \n{emp_and_count}")
        elif user_number == '2':
            print(f"Средняя зарплата среди всех найденных: {db_manager.get_avg_salary()}")
        elif user_number == '3':
            print(f'Это вакансии, зарплата по которым выше средней из найденных: '
                  f'\n{db_manager.get_vacancies_with_higher_salary()}')
        elif user_number == '4':
            word_key = input('Введите ключевое слово:  ')
            print(f'Эти вакансии найдены по Вашему ключевому слову: '
                  f'\n{db_manager.get_vacancies_with_keyword(word_key)}')
        elif user_number == '5':
            exit('До свидания!')
        else:
            print("Такого варианта нет, попробуйте еще раз")
            print('Показать еще меню? ДА/НЕТ')

            choice = input().upper()

            if choice == 'ДА':
                continue
            else:
                print('Программа завершает работу')
                break


if __name__ == '__main__':
    main()
