import requests
import json
import os
import base64
from datetime import datetime
from dotenv import load_dotenv


class RequestService:

    def __init__(self):
        # Uzyskanie pełnej ścieżki do skryptu
        script_path = os.path.abspath(__file__)
        # print(f'Bieżąca ścieżka do skryptu: {script_path}')

        # Uzyskanie katalogu, w którym znajduje się skrypt
        script_directory = os.path.dirname(script_path)
        # print(f'Katalog skryptu: {script_directory}')

        # Uzyskanie pełnej ścieżki do pliku dev.json
        load_dotenv()
        # print(os.getenv("SERVER_USED"))
        if os.getenv("SERVER_USED") == 'prod':
            file_path = os.path.join(script_directory, 'prod.json')
        else:
            file_path = os.path.join(script_directory, 'dev.json')
        # print(f'Pełna ścieżka do pliku dev.json: {file_path}')

        with open(file_path, 'r') as file:
            self.url_map = json.load(file)

        pass

    def login(self, username, password):
        url = self.url_map['base_URL']+self.url_map['login']
        login_data = {
            'name': username,
            'email': "",
            'password': password
        }
        response = requests.post(url, json=login_data)
        code = response.status_code
        if code == 200 or code == 401:
            json = response.json()
        else:
            json = {}
        # print(code, json)
        return code, json

    def login_google(self, name, email):
        url = self.url_map['base_URL'] + self.url_map['login']
        login_data = {
            'name': name,
            'email': email,
            'password': ""
        }
        response = requests.post(url, json=login_data)
        code = response.status_code
        if code == 200 or code == 401:
            json = response.json()
        else:
            json = {}
        # print(code, json)
        return code, json

    def get_all_postcards(self, token):
        url = self.url_map['base_URL'] + self.url_map['get_all_ps']
        header = {'Authorization': token}
        response = requests.get(url, headers=header)
        code = response.status_code
        if code == 200 or code == 498:
            json = response.json()
        else:
            json = {}
        # print(code, json)
        return code, json

    def get_user_postcards(self, token):
        url = self.url_map['base_URL'] + self.url_map['get_user_ps']
        header = {'Authorization': token}
        response = requests.get(url, headers=header)
        code = response.status_code
        if code == 200 or code == 498:
            json = response.json()
        else:
            json = {}
        # print(code, json)
        return code, json

    def get_single_postcard(self, postcard_id, token):
        url = self.url_map['base_URL'] + self.url_map['get_single_ps']
        url = url.replace('<int:postcard_id>', str(postcard_id))
        header = {'Authorization': token}
        response = requests.get(url, headers=header)
        code = response.status_code
        if code == 200 or code == 498 or code == 404:
            json = response.json()
        else:
            json = {}
        # print(code, json)
        return code, json

    def create_postcard(self, token, city, country, date, from_whom, photo):
        url = self.url_map['base_URL'] + self.url_map['create_ps']
        my_datetime = datetime.combine(date, datetime.min.time())
        formatted_date = my_datetime.strftime('%a, %d %b %Y %H:%M:%S GMT')
        header = {'Authorization': token}
        postcard_data = {
            'city': city,
            'country': country,
            'date': formatted_date,
            'from_whom': from_whom,
            'photo': base64.b64encode(photo).decode('utf-8')
        }
        response = requests.post(url, headers=header, json=postcard_data)
        code = response.status_code
        if code == 200 or code == 498:
            json = response.json()
        else:
            json = {}
        return code, json

    def update_postcard(self, token, postcard_id, city, country, date, from_whom, photo):
        url = self.url_map['base_URL'] + self.url_map['update_ps']
        url = url.replace('<int:postcard_id>', str(postcard_id))
        my_datetime = datetime.combine(date, datetime.min.time())
        formatted_date = my_datetime.strftime('%a, %d %b %Y %H:%M:%S GMT')
        header = {'Authorization': token}
        postcard_data = {
            'id': postcard_id,
            'city': city,
            'country': country,
            'date': formatted_date,
            'from_whom': from_whom,
            'photo': base64.b64encode(photo).decode('utf-8')
        }
        response = requests.patch(url, headers=header, json=postcard_data)
        code = response.status_code
        if code == 200 or code == 498 or code == 404:
            json = response.json()
        else:
            json = {}
        return code, json

    def delete_postcard(self, token, postcard_id):
        url = self.url_map['base_URL'] + self.url_map['delete_ps']
        url = url.replace('<int:postcard_id>', str(postcard_id))
        header = {'Authorization': token}
        response = requests.delete(url, headers=header)
        code = response.status_code
        if code == 200 or code == 498 or code == 404:
            json = response.json()
        else:
            json = {}
        return code, json
