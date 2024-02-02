import base64
import json
import tkinter as tk
from email.utils import parsedate_to_datetime

import customtkinter as ctk

from shered import PictureService


class ViewPostcardPage:
    main_frame = None
    ps_json = None
    token = None
    userBtn = None

    pictureService = PictureService()

    def __init__(self, main_frame, ps_json, userBtn):
        self.main_frame = main_frame
        self.ps_json = ps_json
        self.token = userBtn.token
        self.userBtn = userBtn
        pass

    def delete_page(self):
        for frame in self.main_frame.winfo_children():
            frame.destroy()

    def view_page(self):
        # self.delete_page()
        # self.load_json()
        date_str = self.ps_json['date']
        date_datetime = parsedate_to_datetime(date_str)
        date_format = date_datetime.strftime("%Y-%m-%d")

        frame = ctk.CTkFrame(master=self.main_frame, width=700, height=500, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.userBtn.user_btn_show(frame=frame)
        if self.userBtn.is_admin:
            info_frame = ctk.CTkFrame(master=frame, width=220, height=245, corner_radius=7)
        else:
            info_frame = ctk.CTkFrame(master=frame, width=220, height=205, corner_radius=7)
        info_frame.place(x=30, y=150)
        info_label = ctk.CTkLabel(master=info_frame, text=self.userBtn.languageMode.get_phrase("Postcard deletes:"), font=('Bold', 25), width=200, anchor='w')
        info_label.place(x=5, y=5)
        city_label = ctk.CTkLabel(master=info_frame, text=self.userBtn.languageMode.get_phrase("City: ")+self.ps_json['city'], font=('Normal', 20), width=200, anchor='w')
        city_label.place(x=5, y=45)
        country_label = ctk.CTkLabel(master=info_frame, text=self.userBtn.languageMode.get_phrase("Country: ")+self.ps_json['country'], font=('Normal', 20), width=200, anchor='w')
        country_label.place(x=5, y=85)
        date_label = ctk.CTkLabel(master=info_frame, text=self.userBtn.languageMode.get_phrase("Date: ")+date_format, font=('Normal', 20), width=200, anchor='w')
        date_label.place(x=5, y=125)
        from_whom_label = ctk.CTkLabel(master=info_frame, text=self.userBtn.languageMode.get_phrase("From whom: ")+self.ps_json['from_whom'], font=('Normal', 20), width=200, anchor='w')
        from_whom_label.place(x=5, y=165)
        if self.userBtn.is_admin:
            owner_label = ctk.CTkLabel(master=info_frame, text=self.userBtn.languageMode.get_phrase("Owner: ")+self.ps_json['owner_name'], font=('Normal', 20), width=200, anchor='w')
            owner_label.place(x=5, y=205)

        photo_frame = ctk.CTkFrame(master=frame, width=392, height=295, corner_radius=7)
        photo_frame.place(x=280, y=100)
        photo = self.pictureService.bytes_to_picture(base64.b64decode(self.ps_json['photo'].encode('utf-8')))
        ps_photo = ctk.CTkImage(light_image=photo, size=(380, 285))
        view_photo_label = ctk.CTkLabel(master=photo_frame, image=ps_photo, corner_radius=5, text='')
        view_photo_label.place(x=0, y=5)

        edit_btn = ctk.CTkButton(master=frame, text=self.userBtn.languageMode.get_phrase("Edit"), width=80, command=lambda: self.edit())
        edit_btn.place(x=350-40-80, y=455)
        delete_btn = ctk.CTkButton(master=frame, text=self.userBtn.languageMode.get_phrase("Delete"), width=80, fg_color="red", hover_color="#CC0000", command=lambda: self.delete())
        delete_btn.place(x=350+40, y=455)

    def edit(self):
        self.userBtn.edit_page(self.ps_json)
        print("edit")

    def delete(self):
        print("delete")
        self.userBtn.confirm_delete_ps_page(self.ps_json)
