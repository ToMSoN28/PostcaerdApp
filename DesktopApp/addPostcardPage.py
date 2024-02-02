import customtkinter as ctk
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_ALL
from PIL import Image
from tkcalendar import Calendar
from datetime import date
import os
from datetime import datetime
from shered import RequestService, TokenService, PictureService
from viewPostcardPage import ViewPostcardPage


# from userBtn import UserBtn


class AddPostcardPage:
    requestService = RequestService()
    pictureService = PictureService()
    token = None
    main_frame = None
    view_frame = None
    userBtn = None

    photo_entry = None
    date_button = None
    photo_path = None
    add_btn = None
    cancel_btn = None

    city = None
    country = None
    date = date.today()
    from_whom = None
    photo = None

    def __init__(self, frame, userBtn):
        self.token = userBtn.token
        self.main_frame = frame
        self.userBtn = userBtn
        pass

    def delete_page(self):
        for frame in self.main_frame.winfo_children():
            frame.destroy()

    def get_path(self, event):
        self.photo_path = event.data
        print(self.photo_path)
        file_name = os.path.basename(self.photo_path)
        print(file_name)
        # tmp = self.photo_entry.get()
        # self.photo_entry.delete(0, END)
        photo_txt = ctk.StringVar()
        photo_txt.set(file_name)
        self.photo_entry.configure(textvariable=photo_txt)
        # self.photo_entry.insert(0, file_name)
        ps_photo = ctk.CTkImage(light_image=Image.open(self.photo_path), size=(272, 204))
        view_photo_label = ctk.CTkLabel(master=self.view_frame, image=ps_photo, corner_radius=5, text="")
        view_photo_label.place(x=150 + 64, y=50 + 200)
        view_remove_btn = ctk.CTkButton(master=view_photo_label, text="X", font=("Bold", 10), anchor='center',
                                        command=lambda: self.close_view_photo_label_create(view_photo_label,
                                                                                           self.photo_entry),
                                        width=15, height=15, fg_color='red', hover_color='#CC0000', corner_radius=0)
        view_remove_btn.place(x=272 - 10, y=0)
        pass

    def close_view_photo_label_create(self, label, pe):
        self.photo_path = None
        label.destroy()
        text = ctk.StringVar()
        text.set(self.userBtn.languageMode.get_phrase('drag & drop photo'))
        pe.configure(textvariable=text)
        pass

    def show_calender(self, frame):
        self.calender_show = True
        # self.create_ps_page()
        cal_frame = ctk.CTkFrame(master=frame, width=235, height=200, corner_radius=7)
        cal_frame.place(x=460, y=50)
        cal = Calendar(master=cal_frame, selectmode='day', font=("normal", 9),
                       showweeknumbers=False, cursor="hand2", date_pattern='y-mm-dd',
                       borderwidth=0, bordercolor='white')
        cal.place(x=3, y=7)
        ok_btn = ctk.CTkButton(master=cal_frame, width=60, fg_color="green", hover_color="#00CC00", height=15,
                               text="Ok", command=lambda: self.get_date_from_calender(cal, cal_frame))
        ok_btn.place(x=35, y=175)
        cl_btn = ctk.CTkButton(master=cal_frame, width=60, height=15, fg_color='red', hover_color="#CC0000",
                               text=self.userBtn.languageMode.get_phrase("Cancel"),
                               command=lambda: self.close_calender(cal_frame))
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

    def create_ps_page(self):
        # self.delete_page()
        frame = ctk.CTkFrame(master=self.main_frame, width=700, height=500, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.view_frame = frame
        self.userBtn.user_btn_show(frame=frame)
        x_label = 150
        y_label = 50

        info_label = ctk.CTkLabel(master=frame, text=self.userBtn.languageMode.get_phrase("Add postcard"),
                                  font=('Bold', 25), width=200, anchor='center')
        info_label.place(x=250, y=10)

        city_label = ctk.CTkLabel(master=frame, text=self.userBtn.languageMode.get_phrase("City: "),
                                  font=('Normal', 20), width=200, anchor='e')
        city_label.place(x=x_label, y=y_label)
        city_entry = ctk.CTkEntry(master=frame, width=100,
                                  placeholder_text=self.userBtn.languageMode.get_phrase('city name'))
        city_entry.place(x=x_label + 200, y=y_label)

        country_label = ctk.CTkLabel(master=frame, text=self.userBtn.languageMode.get_phrase("Country: "),
                                     font=('Normal', 20), width=200, anchor='e')
        country_label.place(x=x_label, y=y_label + 40)
        country_entry = ctk.CTkEntry(master=frame, width=100,
                                     placeholder_text=self.userBtn.languageMode.get_phrase('country name'))
        country_entry.place(x=x_label + 200, y=y_label + 40)

        date_label = ctk.CTkLabel(master=frame, text=self.userBtn.languageMode.get_phrase("Date: "),
                                  font=('Normal', 20), width=200, anchor='e')
        date_label.place(x=x_label, y=y_label + 80)
        self.date_button = ctk.CTkButton(master=frame, anchor='w', width=100, text=self.date,
                                         command=lambda: self.show_calender(frame))
        self.date_button.place(x=x_label + 200, y=y_label + 80)

        from_whom_label = ctk.CTkLabel(master=frame, text=self.userBtn.languageMode.get_phrase("From whom: "),
                                       font=('Normal', 20), width=200, anchor='e')
        from_whom_label.place(x=x_label, y=y_label + 120)
        from_whom_entry = ctk.CTkEntry(master=frame, width=100,
                                       placeholder_text=self.userBtn.languageMode.get_phrase('from whom?'))
        from_whom_entry.place(x=x_label + 200, y=y_label + 120)

        photo_label = ctk.CTkLabel(master=frame, text=self.userBtn.languageMode.get_phrase("Photo: "),
                                   font=('Normal', 20), width=200, anchor='e')
        photo_label.place(x=x_label, y=y_label + 160)
        text = ctk.StringVar()
        text.set(self.userBtn.languageMode.get_phrase('drag & drop photo'))
        self.photo_entry = ctk.CTkEntry(master=frame, state='disable', width=100, textvariable=text)
        self.photo_entry.place(x=x_label + 200, y=y_label + 160)
        self.photo_entry.drop_target_register(DND_ALL)
        self.photo_entry.dnd_bind("<<Drop>>", self.get_path)

        add_btn = ctk.CTkButton(master=frame, text=self.userBtn.languageMode.get_phrase("Add"), fg_color="green",
                                hover_color="#00CC00", width=80,
                                command=lambda: self.add(city_entry.get(), country_entry.get(), from_whom_entry.get()))
        add_btn.place(x=350 - 40 - 80, y=465)
        cancel_btn = ctk.CTkButton(master=frame, text=self.userBtn.languageMode.get_phrase("Cancel"), width=80,
                                   fg_color='red', hover_color="#CC0000", command=lambda: self.cancle())
        cancel_btn.place(x=350 + 40, y=465)

    def add(self, city, country, from_whom):
        print('przed if')
        if self.photo_path and city != "" and country != "" and from_whom != "":
            # photo = Image.open(self.photo_path)
            bytes_photo = self.pictureService.picture_to_bytes_path(self.photo_path)
            code, json = self.requestService.create_postcard(token=self.token, city=city, country=country,
                                                             date=self.date, from_whom=from_whom, photo=bytes_photo)
            print(code)
            if code == 200:
                ps_json = json['postcard']
                # print(ps_json)
                self.userBtn.view_page(ps_json)
            else:
                print("login")
                self.userBtn.log_out()
        pass

    def cancle(self):
        print("cancel")
        if self.userBtn.last_list_page == 'my':
            self.userBtn.my_postcard()
        else:
            self.userBtn.all_postcard()
