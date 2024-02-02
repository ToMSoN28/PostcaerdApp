import customtkinter as ctk
import tkinter as tk

from shered import RequestService

class ConfirmationPage:
    main_frame = None
    token = None
    userBtn = None

    requestService = RequestService()

    def __init__(self, main_frame, userBtn):
        self.main_frame = main_frame
        self.token = userBtn.token
        self.userBtn = userBtn
        pass

    def confirmation_delete(self, json):
        frame = ctk.CTkFrame(master=self.main_frame, width=260, height=230, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.userBtn.show_mode_btn(frame, 260)

        info_label = ctk.CTkLabel(master=frame, width=240, text=self.userBtn.languageMode.get_phrase('You are sure\nthat you want to\ndelete the postcard'), font=('Bold', 20),
                                  anchor='center')
        info_label.place(x=15, y=60)

        cancel_btn = ctk.CTkButton(master=frame, width=60, text=self.userBtn.languageMode.get_phrase('Cancel'), command=lambda: self.cancel_ps(json), border_width=2, border_color='#009900')
        cancel_btn.place(x=130-80, y=165)
        delete_btn = ctk.CTkButton(master=frame, width=60, text=self.userBtn.languageMode.get_phrase('Delete'), command=lambda: self.delete_ps(json), border_width=2, border_color='red')
        delete_btn.place(x=130+20, y=165)

    def cancel_ps(self, json):
        print('cancel')
        self.userBtn.view_page(json)

    def delete_ps(self, json):
        print('delete')
        code, json = self.requestService.delete_postcard(self.token, json['id'])
        if code == 200:
            if self.userBtn.last_list_page == 'my':
                self.userBtn.my_postcard()
            else:
                self.userBtn.all_postcard()
        else:
            self.userBtn.log_out()

