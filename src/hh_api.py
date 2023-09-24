import requests
import json
import time


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
    __data_path = 'data/vacancies.json'

    def __init__(self, id_employer):
        self.id_employer = id_employer
        self.get_vacancy = self.get_vacancies()

    def get_vacancies(self):
        vacancies_data = []

        for page in range(0, 10):
            params = {
                "employer_id": f"{self.id_employer}",
                "page": page,
                'per_page': 20,
            }
            data = requests.get('https://api.hh.ru/vacancies', params=params).json()
            vacancies_data.extend(data.get('items'))
            time.sleep(0.22)

        with open(self.__data_path, "w", encoding="utf-8") as f:
            json.dump(vacancies_data, f, ensure_ascii=False, indent=4)
        return vacancies_data

    def add_vacancies_to_list(self):
        vacancies_list = []
        vacancies = self.get_vacancy

        for data in range(len(vacancies)):
            salary_from = 0 if (vacancies[data]['salary'] is None or vacancies[data]['salary']['from'] == 0 or
                                vacancies[data]['salary']['from'] is None) else vacancies[data]['salary']['from'],
            salary_to = 0 if (vacancies[data]['salary'] is None or vacancies[data]['salary']['to'] == 0 or
                              vacancies[data]['salary']['to'] is None) else vacancies[data]['salary']['to']

            vacancy_data = {
                'id_vacancy': vacancies[data].get('id'),
                'name_vacancy': vacancies[data].get('name'),
                'id_employer': 0 if vacancies[data]['employer']['id'] is None else vacancies[data]['employer'][
                    'id'],
                'name_employer': "Не указано" if vacancies[data]['employer']['name'] is None
                else self.get_vacancy[data]['employer']['name'],
                'city': "Не указано" if vacancies[data]['area']['name'] is None else vacancies[data]['area'][
                    'name'],
                'salary_from': salary_from,
                'salary_to': salary_to,
                'salary_avg': (salary_from if salary_to == 0 else (salary_from + salary_to) / 2) or (
                    salary_to if salary_from == 0 else (salary_to + salary_to) / 2),
                'experience': vacancies[data]['experience'].get('name'),
                'url': vacancies[data].get('alternate_url'),
                "requirement": "Не указано" if vacancies[data]['snippet']['requirement'] else
                vacancies[data]['snippet']['requirement'],
            }
            vacancies_list.append(vacancy_data)
        return vacancies_list
