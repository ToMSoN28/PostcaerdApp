from flask import Flask, jsonify, request
import json, base64
from .dbService import DbService


class RestApi:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routs()
        self.dbService = DbService()

    def setup_routs(self):
        self.app.add_url_rule('/login', 'login', self.login, methods=['POST'])
        self.app.add_url_rule('/postcard/all', 'get_all_postcards', self.get_all_postcards, methods=['GET'])
        self.app.add_url_rule('/postcard/user', 'get_user_postcards', self.get_user_postcards, methods=['GET'])
        self.app.add_url_rule('/postcard/<int:postcard_id>', 'get_single_postcard', self.get_single_postcard, methods=['GET'])
        self.app.add_url_rule('/postcard/add', 'create_postcard', self.create_postcard, methods=['POST'])
        self.app.add_url_rule('/postcard/update/<int:postcard_id>', 'update_postcard', self.update_postcard, methods=['PATCH'])
        self.app.add_url_rule('/postcard/delete/<int:postcard_id>', 'delete_postcard', self.delete_postcard, methods=['DELETE'])

    def login(self):
        user_data = json.loads(request.data)
        username = user_data['name']
        if not user_data['email']:  # User from db
            password = user_data['password']
            token = self.dbService.login(username, password)
        else:   # User from google
            email = user_data['email']
            token = self.dbService.login_google(username, email)

        if token:
            return jsonify({
                'info': "Logged in successfully",
                'token': token
            }), 200
        else:
            return jsonify({
                'info': "Incorrect login or password",
                'token': ""
            }), 401

    def get_all_postcards(self):
        token = request.headers["Authorization"]
        code, postcards = self.dbService.get_all_postcards(token)
        if code == 1:
            return jsonify({
                'info': "List of all postcards",
                'postcards': postcards
            }), 200
        else:
            return jsonify({
                'info': "No access",
                'postcards': []
            }), 498

    def get_user_postcards(self):
        token = request.headers["Authorization"]
        code, postcards = self.dbService.get_user_postcards(token)
        if code == 1:
            return jsonify({
                'info': "List of your postcards",
                'postcards': postcards
            }), 200
        else:
            return jsonify({
                'info': "No access",
                'postcards': []
            }), 498

    def get_single_postcard(self, postcard_id):
        token = request.headers["Authorization"]
        code, postcard = self.dbService.get_single_postcard(postcard_id, token)
        if code == -1:
            return jsonify({
                'info': "Not in db",
                'postcard': ""
            }), 404
        if code == 0:
            return jsonify({
                'info': "No access",
                'postcard': ""
            }), 498
        if code == 1:
            return jsonify({
                'info': f"Postcard id: {postcard_id}",
                'postcard': postcard
            }), 200

    def create_postcard(self):
        token = request.headers["Authorization"]
        postcard_data = json.loads(request.data)

        city = postcard_data['city']
        country = postcard_data['country']
        date = postcard_data['date']
        from_whom = postcard_data['from_whom']
        photo = postcard_data['photo']

        code, postcard = self.dbService.create_postcard(city, country, date, from_whom, photo, token)
        if code == 0:
            return jsonify({
                'info': "No access",
                'postcard': ""
            }), 498
        if code == 1:
            return jsonify({
                'info': f"Created successful",
                'postcard': postcard
            }), 200

    def update_postcard(self, postcard_id):
        token = request.headers["Authorization"]
        postcard_data = json.loads(request.data)

        city = postcard_data['city']
        country = postcard_data['country']
        date = postcard_data['date']
        from_whom = postcard_data['from_whom']
        photo = postcard_data['photo']

        code, postcard = self.dbService.update_postcard(postcard_id, city, country, date, from_whom, photo, token)
        if code == -1:
            return jsonify({
                'info': "Not in db",
                'postcard': ""
            }), 404
        if code == 0:
            return jsonify({
                'info': "No access",
                'postcard': ""
            }), 498
        if code == 1:
            return jsonify({
                'info': f"Postcard id: {postcard_id}, updated successfully",
                'postcard': postcard
            }), 200

    def delete_postcard(self, postcard_id):
        token = request.headers["Authorization"]

        code = self.dbService.delete_postcard(postcard_id, token)
        if code == -1:
            return jsonify({
                'info': "Not in db",
            }), 404
        if code == 0:
            return jsonify({
                'info': "No access",
            }), 498
        if code == 1:
            return jsonify({
                'info': f"Postcard id: {postcard_id}, deleted successfully",
            }), 200

    def run(self,host='0.0.0.0', port=5000):
        self.app.run(host=host, port=port)

