import customtkinter as ctk
import tkinter as tk

class MainPage:
    main_frame = None
    token = None
    userBtn = None

    def __init__(self, main_frame, userBtn):
        self.main_frame = main_frame
        self.token = userBtn.token
        self.userBtn = userBtn
        pass

    def main_page(self):
        frame = ctk.CTkFrame(master=self.main_frame, width=700, height=500, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.userBtn.user_btn_show(frame=frame)

        welcome_label = ctk.CTkLabel(master=frame, width=300, text=self.userBtn.languageMode.get_phrase('Welcome in your\npostcard album'), font=('Bold', 25), anchor='center')
        welcome_label.place(x=200, y=30)
        info_label = ctk.CTkLabel(master=frame, width=400, text=self.userBtn.languageMode.get_phrase('Save your trips with our app!!!'), font=('Normal', 20), anchor='center')
        info_label.place(x=150, y=120)

        my_ps_btn = ctk.CTkButton(master=frame, text=self.userBtn.languageMode.get_phrase("My postcards"), width=200, font=('Normal', 15), command=lambda: self.my_ps_page())
        my_ps_btn.place(x=250, y=180)
        add_btn = ctk.CTkButton(master=frame, text=self.userBtn.languageMode.get_phrase("Add postcard"), width=200, font=('Normal', 15), command=lambda: self.add_page())
        add_btn.place(x=250, y=250)
        logout_btn = ctk.CTkButton(master=frame, text=self.userBtn.languageMode.get_phrase("Logout"), width=200, font=('Normal', 15), command=lambda: self.logout_page())
        logout_btn.place(x=250, y=320)

    def my_ps_page(self):
        self.userBtn.my_postcard()

    def add_page(self):
        self.userBtn.create_ps_page()

    def logout_page(self):
        self.userBtn.log_out()

