import jwt
from datetime import datetime, timedelta


class TokenService:

    def __init__(self):
        self.secret_key = 'BostonCeltics'

    def generate_jwt_token(self, user_id, username, is_admin):

        expiration_time = datetime.utcnow() + timedelta(minutes=30)
        payload = {
            'user_id': user_id,
            'username': username,
            'is_admin': is_admin,
            'exp': expiration_time,
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token

    def verify_jwt_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms='HS256')
            # print( payload['username'])
            return payload
        except Exception as e:
            print("Błąd przy weryfikacji tokena: ", e)
            return 0
