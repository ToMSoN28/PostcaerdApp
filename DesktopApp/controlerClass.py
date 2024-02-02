import customtkinter as ctk
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_ALL
from PIL import Image
from shered import RequestService, TokenService
from addPostcardPage import AddPostcardPage
from loginPage import LoginPage
from viewPostcardPage import ViewPostcardPage
from userBtn import UserBtn


class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)
class ControlerClass:
    token = None
    username = 'testing'
    is_admin = None
    menuBar = None
    main_frame = None
    photo_path = None
    requestService = RequestService()
    tokenService = TokenService()

    root = Tk()
    root.geometry('800x600')
    root.title('My Postcard Album')

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    main_frame = ctk.CTkFrame(root, corner_radius=0)
    main_frame.pack()
    main_frame.pack_propagate(False)
    main_frame.configure(width=800, height=600)

    def appRun(self):
        userBtn = UserBtn(self.main_frame)
        login = LoginPage(self.main_frame, userBtn)
        login.login_page()
        self.root.mainloop()

if __name__ == "__main__":
    app = ControlerClass()
    app.appRun()