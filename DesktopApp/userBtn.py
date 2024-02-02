from loginPage import LoginPage
from addPostcardPage import AddPostcardPage
from viewPostcardPage import ViewPostcardPage
from logoutPage import LogoutPage
from editPage import EditPage
from listPage import ListPage
from mainPage import MainPage
from confirmationPage import ConfirmationPage
from shered import TokenService, RequestService, LanguageMode
import customtkinter as ctk
from PIL import Image


class UserBtn:
    frame = None
    token = None
    username = None
    is_admin = None
    last_list_page = 'my'
    json = None
    ps_json_list = None
    actual_page = 'login'
    requestService = RequestService()
    userBtn = None

    mode = True
    languageMode = LanguageMode()

    def __init__(self, frame):
        self.main_frame = frame
        pass

    def delete_page(self):
        for frame in self.main_frame.winfo_children():
            frame.destroy()

    def data(self):
        token_info = TokenService().verify_jwt_token(self.token)
        if token_info == 0:
            print("time login")
        else:
            self.username = token_info['username']
            self.is_admin = token_info['is_admin']

    def user_btn_show(self, frame):
        # self.userBtn = userBtn
        self.data()
        self.frame = frame
        if self.is_admin:
            option = [self.languageMode.get_phrase('My postcards'),
                      self.languageMode.get_phrase('All postcards'),
                      self.languageMode.get_phrase('Add postcard'),
                      self.languageMode.get_phrase('Logout')
                      ]
        else:
            option = [self.languageMode.get_phrase('My postcards'),
                      self.languageMode.get_phrase('Add postcard'),
                      self.languageMode.get_phrase('Logout')
                      ]

        tmp = len(self.username) * 10
        user_menu = ctk.CTkOptionMenu(master=self.frame, values=option, anchor="center",
                                      command=self.user_menu_callback, width=tmp, )
        user_menu.place(x=15, y=15)
        user_menu.set(self.username)
        # print(tmp, 715 - tmp - 50)

        self.show_mode_btn(self.frame, 700)

    def show_mode_btn(self, frame, x):
        img2 = ctk.CTkImage(light_image=Image.open("./sun1.png").resize((20, 20)), dark_image=Image.open("./moon1.png").resize((20, 20)))
        mode_btn = ctk.CTkButton(master=frame, image=img2, text="", width=30, height=30, command=lambda: self.change_mode())
        mode_btn.place(x=x - 45, y=15)

        language_menu = ctk.CTkOptionMenu(master=frame, width=100, values=[self.languageMode.get_phrase('English'),
                                                                                self.languageMode.get_phrase('Polish')],
                                          anchor='center', command=self.language_callback)
        language_menu.set(self.languageMode.get_phrase('Language'))
        language_menu.place(x=x - 160, y=15)

    def user_menu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)
        if choice == self.languageMode.get_phrase('Logout'):
            self.log_out()
        if choice == self.languageMode.get_phrase('Add postcard'):
            self.create_ps_page()
        if choice == self.languageMode.get_phrase('My postcards'):
            self.my_postcard()
        if choice == self.languageMode.get_phrase('All postcards'):
            self.all_postcard()

    def language_callback(self, choice):
        if choice == self.languageMode.get_phrase('English'):
            print("EN")
            self.languageMode.mode = 'english'
            self.reload_page()
        if choice == self.languageMode.get_phrase('Polish'):
            print('PL')
            self.languageMode.mode = 'polski'
            self.reload_page()

    def reload_page(self):
        if self.actual_page == 'login':
            self.login()
        elif self.actual_page == 'main':
            self.main_page()
        elif self.actual_page == 'add':
            self.create_ps_page()
        elif self.actual_page == 'view':
            self.view_page(self.json)
        elif self.actual_page == 'edit':
            self.edit_page(self.json)
        elif self.actual_page == 'confirm':
            self.confirm_delete_ps_page(self.json)
        elif self.actual_page == 'logout':
            self.log_out()
        elif self.actual_page == 'my_list':
            self.postcard_mode()
        elif self.actual_page == 'all_list':
            self.postcard_mode()


    def change_mode(self):
        if self.mode:
            ctk.set_appearance_mode("light")
            self.mode = False
        else:
            ctk.set_appearance_mode("dark")
            self.mode = True

    def log_out(self):
        self.actual_page = 'logout'
        self.token = None
        self.is_admin = None
        self.username = None
        self.delete_page()
        login_page = LogoutPage(self.main_frame, self.userBtn).logout_page()
        pass

    def create_ps_page(self):
        self.actual_page = 'add'
        self.delete_page()
        add = AddPostcardPage(self.main_frame, self.userBtn).create_ps_page()
        pass

    def view_page(self, json):
        self.actual_page = 'view'
        self.json = json
        self.delete_page()
        view = ViewPostcardPage(self.main_frame, json, self.userBtn).view_page()

    def edit_page(self, json):
        self.actual_page = 'edit'
        self.json = json
        self.delete_page()
        edit = EditPage(self.main_frame, self.userBtn, json).edit_ps_page()

    def login(self):
        self.actual_page = 'login'
        self.delete_page()
        login_page = LoginPage(self.main_frame, self.userBtn).login_page()
        pass

    def my_postcard(self):
        self.last_list_page = 'my'
        self.actual_page = 'my_list'
        self.delete_page()
        code, self.ps_json_list = self.requestService.get_user_postcards(self.token)
        if code == 200:
            # print(self.ps_json_list['postcards'][0]['city'])
            list = ListPage(self.main_frame, self.ps_json_list['postcards'], self.userBtn, self.last_list_page).list_page()
        else:
            self.log_out()

    def all_postcard(self):
        self.last_list_page = 'all'
        self.actual_page = 'all_list'
        self.delete_page()
        code, self.ps_json_list = self.requestService.get_all_postcards(self.token)
        if code == 200:
            # print(self.ps_json_list['postcards'][1]['city'])
            list = ListPage(self.main_frame, self.ps_json_list['postcards'], self.userBtn, self.last_list_page).list_page()
        else:
            self.log_out()

    def postcard_mode(self):
        list = ListPage(self.main_frame, self.ps_json_list['postcards'], self.userBtn, self.last_list_page).list_page()

    def main_page(self):
        self.actual_page = 'main'
        self.delete_page()
        main = MainPage(self.main_frame, self.userBtn).main_page()

    def confirm_delete_ps_page(self, json):
        self.actual_page = 'confirm'
        self.json = json
        self.delete_page()
        confirm = ConfirmationPage(self.main_frame, self.userBtn).confirmation_delete(json)
