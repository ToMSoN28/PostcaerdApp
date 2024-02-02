import os

import customtkinter as ctk
import tkinter as tk

from PIL import ImageTk, Image
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
from shered import RequestService, TokenService


class LoginPage:
    requestService = RequestService()
    tokenService = TokenService()

    main_frame = None
    info_frame = None
    userBtn = None

    token = None
    username = None
    is_admin = None

    def __init__(self, main_frame, userBtn):
        self.main_frame = main_frame
        self.userBtn = userBtn
        self.userBtn.userBtn = userBtn
        pass

    def delete_page(self):
        for frame in self.main_frame.winfo_children():
            frame.destroy()

    def login_click_on(self, username, passwd, frame, entry_passwd):
        name = username
        password = passwd
        print(name, password)
        code, user_json = self.requestService.login(name, password)
        if code == 200:
            self.token = user_json['token']
            user = self.tokenService.verify_jwt_token(self.token)
            self.username = user['username']
            self.is_admin = user['is_admin']
            self.main_page()
        elif code == 401:
            self.info_frame = ctk.CTkFrame(master=frame, fg_color='red', corner_radius=7, width=220, height=30)
            self.info_frame.place(x=50, y=202)
            l3 = ctk.CTkLabel(master=self.info_frame, text=self.userBtn.languageMode.get_phrase("Incorrect login or password"), font=('Normal', 14),
                              text_color='white')
            l3.place(x=5, y=0)
            x_btn = ctk.CTkButton(master=self.info_frame, text="X", font=('Normal', 14), width=20, height=20,
                                  fg_color='red', anchor="center", hover_color="#CC0000",
                                  command=lambda: self.close_info_frame())
            x_btn.place(x=220-28, y=3)
            entry_passwd.delete(0, len(passwd))
        else:
            self.info_frame = ctk.CTkFrame(master=frame, fg_color='red', corner_radius=5, width=220,
                                           height=30)
            self.info_frame.place(x=50, y=202)
            l3 = ctk.CTkLabel(master=self.info_frame, text=self.userBtn.languageMode.get_phrase("Server error, try later"), font=('Century Gothic', 12),
                              text_color='white')
            l3.place(x=5, y=0)
            x_btn = ctk.CTkButton(master=self.info_frame, text="X", font=('Normal', 14), width=20, height=20,
                                  fg_color='red', anchor="center", hover_color="#CC0000",
                                  command=lambda: self.close_info_frame())
            x_btn.place(x=220 - 28, y=3)

    def close_info_frame(self):
        self.info_frame.destroy()

    def google_login(self, frame):
        script_path = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_path)
        credentials = os.path.join(script_directory, 'credentials.json')

        flow = InstalledAppFlow.from_client_secrets_file(credentials,
                                                         ["openid", "https://www.googleapis.com/auth/userinfo.email",
                                                          "https://www.googleapis.com/auth/userinfo.profile"])
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())

        service = googleapiclient.discovery.build('people', 'v1', credentials=creds)
        user_info = service.people().get(resourceName='people/me', personFields='emailAddresses,names').execute()

        print("Email:", user_info['emailAddresses'][0]['value'])
        print("Imię:", user_info['names'][0]['givenName'])
        print("Nazwisko:", user_info['names'][0]['familyName'])

        name = user_info['names'][0]['givenName'] + " " + user_info['names'][0]['familyName']
        email = user_info['emailAddresses'][0]['value']

        code, user_json = self.requestService.login_google(name, email)
        if code == 200:
            self.token = user_json['token']
            user = self.tokenService.verify_jwt_token(self.token)
            self.username = user['username']
            self.is_admin = user['is_admin']
            self.main_page()

    def login_page(self):
        # self.delete_page()
        frame = ctk.CTkFrame(master=self.main_frame, width=320, height=360, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.userBtn.show_mode_btn(frame, 320)

        l2 = ctk.CTkLabel(master=frame, text=self.userBtn.languageMode.get_phrase("Log into your Account"), font=('Normal', 20), width=220, anchor="center")
        l2.place(x=50, y=55)

        entry1 = ctk.CTkEntry(master=frame, width=220, placeholder_text=self.userBtn.languageMode.get_phrase('Username'))
        entry1.place(x=50, y=110)

        entry2 = ctk.CTkEntry(master=frame, width=220, placeholder_text=self.userBtn.languageMode.get_phrase('Password'), show="*")
        entry2.place(x=50, y=165)

        button1 = ctk.CTkButton(master=frame, width=220,
                                text=self.userBtn.languageMode.get_phrase("Login"), corner_radius=6,
                                command=lambda: self.login_click_on(entry1.get(), entry2.get(), frame, entry2))
        button1.place(x=50, y=240)

        img2 = ctk.CTkImage(Image.open("./googleLogo.png").resize((20, 20)))
        button2 = ctk.CTkButton(master=frame, width=220, image=img2,
                                corner_radius=6, text="Google",
                                command=lambda: self.google_login(frame))
        button2.place(x=50, y=290)

    def main_page(self):
        self.userBtn.userBtn = self.userBtn
        self.userBtn.token = self.token
        self.userBtn.my_postcard()
