import tkinter as tk
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
import os

class GoogleOAuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Google OAuth App")

        self.auth_button = tk.Button(root, text="Zaloguj się z Google", command=self.authenticate)
        self.auth_button.pack(pady=20)

        script_path = os.path.abspath(__file__)
        # print(f'Bieżąca ścieżka do skryptu: {script_path}')

        # Uzyskanie katalogu, w którym znajduje się skrypt
        script_directory = os.path.dirname(script_path)
        # print(f'Katalog skryptu: {script_directory}')

        # Uzyskanie pełnej ścieżki do pliku dev.json
        self.file_path = os.path.join(script_directory, 'credentials.json')
        print(f'Pełna ścieżka do pliku dev.json: {self.file_path}')

    def authenticate(self):
        # Konfiguracja autoryzacji Google
        flow = InstalledAppFlow.from_client_secrets_file(self.file_path, ["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"])
        creds = flow.run_local_server(port=0)

        # Zapisz dane autoryzacyjne
        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())

        # Uzyskaj dostęp do danych użytkownika
        service = googleapiclient.discovery.build('people', 'v1', credentials=creds)
        user_info = service.people().get(resourceName='people/me', personFields='emailAddresses,names').execute()

        # Wyświetl dane użytkownika
        print("Email:", user_info['emailAddresses'][0]['value'])
        print("Imię:", user_info['names'][0]['givenName'])
        print("Nazwisko:", user_info['names'][0]['familyName'])

if __name__ == "__main__":
    root = tk.Tk()
    app = GoogleOAuthApp(root)
    root.mainloop()
