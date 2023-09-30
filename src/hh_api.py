import json
import time
import requests


class HeadHunter:
    __data_path = 'data/employers_data.json'

    def __init__(self, data: str):
        self.data = data

    @property
    def get_company(self):
        """Возвращает работодателей с сайта"""
        employers = []
        params = {
            "text": f"{self.data}",
            "area": 1,
            "only_with_vacancies": True,
            "pages": 1,
            "per_page": 20,
        }
        employers.extend(requests.get('https://api.hh.ru/employers', params=params).json()["items"])

        with open(self.__data_path, "w", encoding="utf-8") as f:
            json.dump(employers, f, ensure_ascii=False, indent=4)
        return employers

    def __len__(self):
        return len(self)


class Vacancy:
    """Собирает с сайта HeadHunter вакансии по номеру айди работодателя"""

    __file_path = 'data/vacancies.json'

    def __init__(self, id_employer):
        self.id_employer = id_employer
        self.get_vacancy = self.get_vacancy()

    def get_vacancy(self):
        """Возвращает вакансии по номеру айди работодателя"""
        vacancies_data = []

        for page in range(0, 10):
            params = {
                "employer_id": f"{self.id_employer}",
                "page": page,
                'per_page': 20,
            }
            data = requests.get("https://api.hh.ru/vacancies", params=params).json()
            vacancies_data.extend(data.get('items'))
            time.sleep(0.22)

        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(vacancies_data, f, ensure_ascii=False, indent=4)

        return vacancies_data

    def add_vacancies_to_list(self):
        """Записывает найденные вакансии с нужными ключами в список словарей"""
        list_vacancy = []
        vacancies = self.get_vacancy

        for i in range(len(vacancies)):
            salary_from = 0 if (vacancies[i]['salary'] is None or vacancies[i]['salary']['from'] == 0 or
                                vacancies[i]['salary']['from'] is None) else vacancies[i]['salary'][
                'from']
            salary_to = 0 if (vacancies[i]['salary'] is None or vacancies[i]['salary']['to'] == 0 or
                              vacancies[i]['salary']['to'] is None) else vacancies[i]['salary']['to']
            vacancy_data = {
                'id_vacancy': vacancies[i].get('id'),
                'name_vacancy': vacancies[i].get('name'),
                'id_employer': 0 if vacancies[i]['employer']['id'] is None else vacancies[i]['employer'][
                    'id'],
                'name_employer': "Не указано" if vacancies[i]['employer']['name'] is None else
                self.get_vacancy[i]['employer']['name'],
                'city': "Не указано" if vacancies[i]['area']['name'] is None else vacancies[i]['area'][
                    'name'],
                'salary_from': salary_from,
                'salary_to': salary_to,
                'salary_avg': (salary_from if salary_to == 0 else (salary_from + salary_to) / 2) or (
                    salary_to if salary_from == 0 else (salary_to + salary_to) / 2),
                'experience': vacancies[i]['experience'].get('name'),
                'url': vacancies[i].get('alternate_url'),
                "requirement": "Не указано" if vacancies[i]['snippet']['requirement'] else
                vacancies[i]['snippet']['requirement'],
            }

            list_vacancy.append(vacancy_data)
        return list_vacancy
