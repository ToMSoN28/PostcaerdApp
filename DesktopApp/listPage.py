import base64
from email.utils import parsedate_to_datetime

import customtkinter as ctk
import tkinter as tk

from shered import PictureService

class ListPage:
    main_frame = None
    ps_json_list = None
    token = None
    userBtn = None
    text = None

    pictureService = PictureService()

    def __init__(self, main_frame, ps_json_list, userBtn, text):
        self.main_frame = main_frame
        self.ps_json_list = ps_json_list
        self.token = userBtn.token
        self.userBtn = userBtn
        self.text = text
        pass

    def list_page(self):
        frame = ctk.CTkFrame(master=self.main_frame, width=700, height=500, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.userBtn.user_btn_show(frame=frame)

        if self.text == 'all':
            tmp = 'All postcards'
        else:
            tmp = 'My postcards'
        info_label = ctk.CTkLabel(master=frame, text=self.userBtn.languageMode.get_phrase(tmp),
                                  font=('Bold', 25), width=200, anchor='center')
        info_label.place(x=250, y=10)

        list_frame = ctk.CTkScrollableFrame(master=frame, width=540, height=400, corner_radius=10 )
        list_frame.place(x=80, y=50)

        for i in range(len(self.ps_json_list)):
            list_frame.rowconfigure(i*2 + 1, weight=5)
            list_frame.rowconfigure(i*2, weight=1)

        for i in range(len(self.ps_json_list)):
            ps_json = self.ps_json_list[i]
            ps_frame = ctk.CTkFrame(master=list_frame, width=520, height=130, corner_radius=7)
            ps_frame.grid(row=i*2 + 1, column=0)
            # ps_frame.columnconfigure(0, weight=5)
            # ps_frame.columnconfigure(2, weight=5)
            # ps_frame.columnconfigure(2, weight=6)
            # ps_frame.columnconfigure(3, weight=4)

            city_label = ctk.CTkLabel(master=ps_frame, width=100, text=ps_json['city'], font=('Normal', 17), anchor='center')
            country_label = ctk.CTkLabel(master=ps_frame, width=100, text=ps_json['country'], font=('Normal', 17), anchor='center')
            date_str = ps_json['date']
            date_datetime = parsedate_to_datetime(date_str)
            date_format = date_datetime.strftime("%Y-%m-%d")
            date_label = ctk.CTkLabel(master=ps_frame, width=100, text=date_format, font=('Normal', 17), anchor='center')
            photo = self.pictureService.bytes_to_picture(base64.b64decode(ps_json['photo'].encode('utf-8')))
            ps_photo = ctk.CTkImage(light_image=photo, size=(80, 60))
            view_photo_label = ctk.CTkLabel(master=ps_frame, image=ps_photo, text='')
            moreBtn = ctk.CTkButton(master=ps_frame, width=10, height=10, text="...", font=('Bold', 20), corner_radius=5, command=lambda json=ps_json: self.view_postcard(json))
            space1 = ctk.CTkLabel(master=ps_frame, text="      ")
            space1.grid(row=1, column=2)
            space2 = ctk.CTkLabel(master=ps_frame, text="      ")
            space2.grid(row=1, column=4)
            space3 = ctk.CTkLabel(master=ps_frame, text="      ")
            space3.grid(row=1, column=6)
            space4 = ctk.CTkLabel(master=ps_frame, text="            ")
            space4.grid(row=1, column=8)
            space5 = ctk.CTkLabel(master=ps_frame, text="    ")
            space5.grid(row=1, column=0)
            space6 = ctk.CTkLabel(master=ps_frame, text="    ", font=('Normal', 5))
            space6.grid(row=0, column=1)
            # space7 = ctk.CTkLabel(master=ps_frame, text="    ", font=('Normal', 5))
            # space7.grid(row=2, column=1)

            city_label.grid(row=1, column=1)
            country_label.grid(row=1, column=3)
            date_label.grid(row=1, column=5)
            view_photo_label.grid(row=1, column=7)
            moreBtn.grid(row=1, column=9)


    def view_postcard(self, ps_json):
        print(ps_json['id'])
        self.userBtn.view_page(ps_json)

