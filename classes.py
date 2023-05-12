import requests
import json
import os
from abc import ABC, abstractmethod
from utils import salary_trier


class Connector:
    def __init__(self, filename):
        self.__data_file = filename

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        self.__data_file = value
        self.__connect()

    def __connect(self):
        if self.__data_file not in os.listdir('.'):
            with open(self.__data_file, 'w+') as new_file:
                new_file.write(json.dumps({}))
            pass
        pass

    def insert(self, data):
        with open(self.__data_file, 'w+') as f:
            json.dump(data, f)


class Engine(ABC):

    @abstractmethod
    def get_request(self, page: int):
        pass

    @staticmethod
    def get_connector(filename):
        return Connector(filename)


class HH(Engine):

    def __init__(self, keyword='Python'):
        self._endpoint = 'https://api.hh.ru/vacancies'
        self._headers = {'User-Agent': 'Skypro_CW (msktareo@gmail.com)'}
        self._keyword = keyword

    def get_request(self, page: int):
        response = requests.get(self._endpoint, headers=self._headers,
                                params={'text': self._keyword, 'page': page}).json()
        return response

    def dump_vacancies(self, filename='hh.json'):
        vac_list = []
        json_connector = self.get_connector(filename)
        for i in range(self.get_request(0)['pages']):
            for full_dict in self.get_request(i)['items']:
                vac_list.append({'title': f"{full_dict['employer']['name']} {full_dict['name']}",
                                 'description': f"{full_dict['snippet']['requirement']} "
                                                f"{full_dict['snippet']['responsibility']}",
                                 'link': full_dict['apply_alternate_url'],
                                 'salary': (salary_trier(full_dict['salary']['from'] if full_dict['salary'] else 0),
                                            salary_trier(full_dict['salary']['to'] if full_dict['salary'] else 0))})
        out_data = {'vacancies': vac_list, 'vac_number': len(vac_list), 'keyword': self._keyword}
        json_connector.insert(out_data)


class Superjob(Engine):
    def __init__(self, keyword='Python'):
        self._endpoint = 'https://api.superjob.ru/2.0/vacancies/'
        self._appkey = 'v3.r.137536777.3b86f' \
                       '7b9e5c6e1b4f7acba479bb52aca5719bda9.624633c4db24a4fc311d74e2c896be2eccf266f3'
        self._keyword = keyword

    def get_request(self, page: int):
        headers = {'X-Api-App-Id': self._appkey}
        response = requests.get(self._endpoint, headers=headers,
                                params={'keyword': self._keyword, 'count': 10, 'page': page})
        return json.loads(response.content.decode('utf-8').replace("'", "\""))

    def dump_vacancies(self, filename='superjob.json'):
        vac_list = []
        total_vacs = self.get_request(0)['total']
        json_connector = self.get_connector(filename)
        for i in range(total_vacs//10 + 1):
            for full_dict in self.get_request(i)['objects']:
                vac_list.append({'title': f"{full_dict['firm_name']} {full_dict['profession']}",
                                 'description': full_dict['vacancyRichText'],
                                 'link': full_dict['link'],
                                 'salary': (full_dict['payment_from'], full_dict['payment_to'])})

        out_data = {'vacancies': vac_list, 'vac_number': len(vac_list), 'keyword': self._keyword}
        json_connector.insert(out_data)
