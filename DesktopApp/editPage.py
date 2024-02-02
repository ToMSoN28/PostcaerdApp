import base64

import customtkinter as ctk
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_ALL
from PIL import Image
from tkcalendar import Calendar
from datetime import date, datetime
import os
from shered import RequestService, TokenService, PictureService
from email.utils import parsedate_to_datetime


class EditPage:
    requestService = RequestService()
    pictureService = PictureService()
    token = None
    main_frame = None
    view_frame = None
    userBtn = None

    photo_entry = None
    date_button = None
    photo_path = "None"
    add_btn = None
    cancel_btn = None

    json = None
    id = None
    city = None
    country = None
    date = date.today()
    from_whom = None
    photo = None

    def __init__(self, frame, userBtn, json):
        self.token = userBtn.token
        self.main_frame = frame
        self.userBtn = userBtn
        tmp_date = datetime.strptime(json['date'], '%a, %d %b %Y %H:%M:%S GMT').date()
        self.date = datetime.combine(tmp_date, datetime.min.time())
        self.city = json['city']
        self.country = json['country']
        self.from_whom = json['from_whom']
        self.photo = base64.b64decode(json['photo'].encode('utf-8'))
        self.id = json['id']
        self.json = json
        pass

    def delete_page(self):
        for frame in self.main_frame.winfo_children():
            frame.destroy()

    def get_path(self, event):
        self.photo_path = event.data
        print(self.photo_path)
        file_name = os.path.basename(self.photo_path)
        print(file_name)
        self.photo_variable.set(file_name)
        self.photo_entry.configure(textvariable=self.photo_variable)
        ps_photo = ctk.CTkImage(light_image=Image.open(self.photo_path), size=(272, 204))
        view_photo_label = ctk.CTkLabel(master=self.view_frame, image=ps_photo, corner_radius=5, text="")
        view_photo_label.place(x=150 + 64, y=50 + 200)
        view_remove_btn = ctk.CTkButton(master=view_photo_label, text="X", font=("Bold", 7), anchor='center',
                                        command=lambda: self.close_view_photo_label_create(view_photo_label, self.photo_entry),
                                        width=10, height=10, fg_color='red', hover_color='#CC0000')
        view_remove_btn.place(x=272 - 15, y=5)
        self.photo = self.pictureService.picture_to_bytes_path(self.photo_path)
        pass

    def close_view_photo_label_create(self, label, pe):
        self.photo_path = None
        self.photo = None
        label.destroy()
        self.photo_variable.set(self.userBtn.languageMode.get_phrase("drag & drop photo"))
        pe.configure(textvariable=None)
        pass

    def show_calender(self, frame):
        cal_frame = ctk.CTkFrame(master=frame, width=235, height=200, corner_radius=7)
        cal_frame.place(x=460, y=50)
        cal = Calendar(master=cal_frame, selectmode='day', font=("normal", 9),
                       showweeknumbers=False, cursor="hand2", date_pattern='y-mm-dd',
                       borderwidth=0, bordercolor='white', year=self.date.year, month=self.date.month, day=self.date.day)
        cal.place(x=3, y=7)
        ok_btn = ctk.CTkButton(master=cal_frame, width=60, height=15, fg_color="green", hover_color="#00CC00", text="Ok", command=lambda: self.get_date_from_calender(cal, cal_frame))
        ok_btn.place(x=35, y=175)
        cl_btn = ctk.CTkButton(master=cal_frame, width=60, height=15, fg_color='red', hover_color="#CC0000", text=self.userBtn.languageMode.get_phrase("Cancel"), command=lambda: self.close_calender(cal_frame))
        cl_btn.place(x=135, y=175)
        # cal.bind("<<CalendarSelected>>", self.get_date_from_calender())

    def get_date_from_calender(self, cal, frame):
        print(cal.get_date())
        selected_date = datetime.strptime(cal.get_date(), "%Y-%m-%d").date()
        self.date = datetime.combine(selected_date, datetime.min.time())
        frame.destroy()
        self.date_button.configure(text=selected_date.strftime('%Y-%m-%d'))
        pass

    def close_calender(self, frame):
        frame.destroy()

    def edit_ps_page(self):
        self.delete_page()
        frame = ctk.CTkFrame(master=self.main_frame, width=700, height=500, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.view_frame = frame
        self.userBtn.user_btn_show(frame=frame)
        x_label = 150
        y_label = 50

        info_label = ctk.CTkLabel(master=frame, text=self.userBtn.languageMode.get_phrase("Edit postcard"),
                                  font=('Bold', 25), width=200, anchor='center')
        info_label.place(x=250, y=10)

        city_label = ctk.CTkLabel(master=frame, text=self.userBtn.languageMode.get_phrase("City: "), font=('Normal', 20), width=200, anchor='e')
        city_label.place(x=x_label, y=y_label)
        city_variable = ctk.StringVar()
        city_variable.set(self.city)
        city_entry = ctk.CTkEntry(master=frame, width=100, placeholder_text=self.userBtn.languageMode.get_phrase('city name'), textvariable=city_variable)
        city_entry.place(x=x_label+200, y=y_label)

        country_label = ctk.CTkLabel(master=frame, text=self.userBtn.languageMode.get_phrase("Country: "), font=('Normal', 20), width=200, anchor='e')
        country_label.place(x=x_label, y=y_label+40)
        country_variable = ctk.StringVar()
        country_variable.set(self.country)
        country_entry = ctk.CTkEntry(master=frame, width=100, placeholder_text=self.userBtn.languageMode.get_phrase('country name'), textvariable=country_variable)
        country_entry.place(x=x_label+200, y=y_label+40)

        date_label = ctk.CTkLabel(master=frame, text=self.userBtn.languageMode.get_phrase("Date: "), font=('Normal', 20), width=200, anchor='e')
        date_label.place(x=x_label, y=y_label+80)
        self.date_button = ctk.CTkButton(master=frame, anchor='w', width=100, text=self.date.strftime('%Y-%m-%d'), command=lambda: self.show_calender(frame))
        self.date_button.place(x=x_label+200, y=y_label+80)

        from_whom_label = ctk.CTkLabel(master=frame, text=self.userBtn.languageMode.get_phrase("From whom: "), font=('Normal', 20), width=200, anchor='e')
        from_whom_label.place(x=x_label, y=y_label+120)
        fw_variable = ctk.StringVar()
        fw_variable.set(self.from_whom)
        from_whom_entry = ctk.CTkEntry(master=frame, width=100, placeholder_text=self.userBtn.languageMode.get_phrase('from whom?'), textvariable=fw_variable)
        from_whom_entry.place(x=x_label+200, y=y_label+120)

        photo_label = ctk.CTkLabel(master=frame, text=self.userBtn.languageMode.get_phrase("Photo: "), font=('Normal', 20), width=200, anchor='e')
        photo_label.place(x=x_label, y=y_label+160)
        self.photo_variable = ctk.StringVar()
        self.photo_variable.set(self.userBtn.languageMode.get_phrase("postcard"))
        self.photo_entry = ctk.CTkEntry(master=frame, state='disable', width=100, textvariable=self.photo_variable)
        self.photo_entry.place(x=x_label+200, y=y_label+160)
        self.photo_entry.drop_target_register(DND_ALL)
        self.photo_entry.dnd_bind("<<Drop>>", self.get_path)

        photo = self.pictureService.bytes_to_picture(self.photo)
        ps_photo = ctk.CTkImage(light_image=photo, size=(272, 204))
        view_photo_label = ctk.CTkLabel(master=self.view_frame, image=ps_photo, corner_radius=5, text="")
        view_photo_label.place(x=150 + 64, y=50 + 200)
        view_remove_btn = ctk.CTkButton(master=view_photo_label, text="X", font=("Bold", 10), anchor='center',
                                        command=lambda: self.close_view_photo_label_create(view_photo_label,
                                                                                           self.photo_entry),
                                        width=15, height=15, fg_color='red', hover_color='#CC0000', corner_radius=0)
        view_remove_btn.place(x=272 - 10, y=0)

        apply_btn = ctk.CTkButton(master=frame, text=self.userBtn.languageMode.get_phrase("Apply"), fg_color="green", hover_color="#00CC00", width=80, command=lambda: self.apply(city_entry.get(), country_entry.get(), from_whom_entry.get()))
        apply_btn.place(x=350-40-80, y=465)
        cancel_btn = ctk.CTkButton(master=frame, text=self.userBtn.languageMode.get_phrase("Cancel"), fg_color="red", hover_color="#CC0000", width=80, command=lambda: self.cancel())
        cancel_btn.place(x=350+40, y=465)

    def apply(self, city, country, from_whom):
        print('przed if')
        if self.photo and city != "" and country != "" and from_whom != "":
            # photo = Image.open(self.photo_path)
            bytes_photo = self.photo
            code, json = self.requestService.update_postcard(token=self.token, postcard_id=self.id, city=city, country=country, date=self.date, from_whom=from_whom, photo=bytes_photo)
            print(code)
            if code == 200:
                ps_json = json['postcard']
                # print(ps_json)
                self.userBtn.view_page(ps_json)
            else:
                print("login")
                self.userBtn.log_out()
        pass

    def cancel(self):
        self.userBtn.view_page(self.json)


