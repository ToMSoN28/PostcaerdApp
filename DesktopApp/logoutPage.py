import customtkinter as ctk
import tkinter as tk


class LogoutPage:
    frame = None
    userBtn = None

    def __init__(self, frame, userBtn):
        self.main_frame = frame
        self.userBtn = userBtn

    def delete_page(self):
        for frame in self.main_frame.winfo_children():
            frame.destroy()

    def logout_page(self):
        # self.delete_page()
        frame = ctk.CTkFrame(master=self.main_frame, width=320, height=260, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.userBtn.show_mode_btn(frame, 320)

        l2 = ctk.CTkLabel(master=frame, text=self.userBtn.languageMode.get_phrase("You are logged out."), font=('Bold', 25), width=220, anchor="center")
        l2.place(x=50, y=55)
        l3 = ctk.CTkLabel(master=frame, text=self.userBtn.languageMode.get_phrase("Log in again or close\nthe application"),
                          font=('Normal', 20), width=220, anchor="center")
        l3.place(x=50, y=110)

        button1 = ctk.CTkButton(master=frame, width=220,
                                text=self.userBtn.languageMode.get_phrase("Login"), corner_radius=6,
                                command=lambda: self.login())
        button1.place(x=50, y=190)

    def login(self):
        print("login")
        self.userBtn.token = None
        self.userBtn.username = None
        self.userBtn.is_admin = None
        self.userBtn.login()

