import requests


class HHParser:
    '''класс получения данных с HH.py'''

    def get_employers(self):
        '''получаем данные для БД от определенных работодателей'''

        employers = []
        employer_ids = [9694561, 1651663, 959366, 30637, 1491512, 4156856, 3949847,
                        6053439, 1373, 10061101]
        for employer_id in employer_ids:
            url = f'https://api.hh.ru/employers/{employer_id}'
            data = requests.get(url).json()
            employers.append({"id": data["id"], "name": data["name"], "company_url": data["alternate_url"]})

        return employers

    def get_vacancies(self):
        '''получаем вакансии от определенных работодателей'''

        vacancies = []
        employer_ids = [9694561, 1651663, 959366, 30637, 1491512, 4156856, 3949847,
                        6053439, 1373, 10061101]
        for employer_id in employer_ids:
            url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
            response = requests.get(url)
            if response.status_code == 200:
                vacancy = response.json()["items"]
                vacancies.extend(vacancy)
            else:
                print("ошибка")

        return vacancies

    def get_vacancies_list(self):
        '''получаем данные для БД'''

        vacancies = self.get_vacancies()
        vacancies_list = []
        for vacancy in vacancies:
            try:
                salary_from = vacancy["salary"]["from"]
            except:
                salary_from = 0
            try:
                salary_to = vacancy["salary"]["to"]
            except:
                salary_to = 0
            vacancies_list.append({
                "id": vacancy["id"],
                "name": vacancy["name"],
                "salary_from": salary_from,
                "salary_to": salary_to,
                "url": vacancy["alternate_url"],
                "area": vacancy["area"]["name"],
                "employer": vacancy["employer"]["id"]
            })
        return vacancies_list


# hh = HHParser()
# print(hh.get_vacancies_list())

