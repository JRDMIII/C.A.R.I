# This is the module that will be used to create the UI
import sqlite3
import tkinter
from PIL import Image, ImageTk
import time

import ui_creation as tui
from ui_creation import btn
import customtkinter as ct

import application_database

# import database as db

# This module will allow us to read and write to the settings file
import csv

# This decides what colours will be picked for the application
import application_database as db

ct.set_appearance_mode("System")
ct.set_default_color_theme("dark-blue")

# This is what we will use to create databases and alter them
import traceback
import uuid
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

class Application(ct.CTk):

    # This defines the width and height of the app
    WIDTH = 800
    HEIGHT = 800

    # Creating the constructor method
    def __init__(self):
        super().__init__()

        self.cred = credentials.Certificate("firebaseAuth/cari-a5744-firebase-adminsdk-v83yb-6d2209d2fc.json")
        self.app = firebase_admin.initialize_app(self.cred)
        self.fs = firestore.client()
        self.auth = firebase_admin.auth

        self.db = application_database.database()

        self.loggedIn = self.db.get_loggedInStatus()
        print(self.loggedIn)

        # self.db = database.database()
        self.uid = ""

        # Defining certain app dimensions
        self.frame_left_width = 200

        # This defines the font used for the application
        self.title_font = ("Roboto Medium", -16)
        self.normal_font = ("Roboto Light", -16)

        # This sets the title and dimensions of the application as well as what occurs when the app is closed
        self.geometry(f'{Application.WIDTH}x{Application.HEIGHT}')
        self.resizable(False, False)
        self.title("C.A.R.I")
        self.protocol("WM_DELETE_WINDOW", self.close)

        if 0 in self.loggedIn:
            self.create_login_screen()
        else:
            email = self.db.get_email()

            self.user = self.auth.get_user_by_email(email)
            self.uid = self.user.uid
            self.create_main_screen()

    # === This is where the contents of all the pages will be designed === #

    def create_main_screen(self):
        self.db.set_loggedInStatus(1)
        self.db.set_email(self.user.email)
        # ==== Here we are creating the frames which the app will be in ==== #
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=0)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = ct.CTkFrame(master=self, width=200, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")
        self.frame_right = ct.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ==== frame_left design ==== #
        self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = ct.CTkLabel(master=self.frame_left,
                                   text="C.A.R.I",
                                   font=self.title_font)  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)
        # These are all the buttons
        self.button_height = 34
        self.home_button = ct.CTkButton(master=self.frame_left,
                                        text="Home",
                                        font=self.title_font,
                                        fg_color="gray",
                                        corner_radius=0,
                                        width=self.frame_left_width,
                                        height=self.button_height,
                                        command=self.home_screen)
        self.home_button.grid(row=2, column=0)
        self.workouttracker_button = ct.CTkButton(master=self.frame_left,
                                                  text="Workout Tracker",
                                                  font=self.title_font,
                                                  fg_color="gray",
                                                  corner_radius=0,
                                                  width=self.frame_left_width,
                                                  height=self.button_height)
        self.workouttracker_button.grid(row=3, column=0)
        self.settings_button = ct.CTkButton(master=self.frame_left,
                                               text="Settings",
                                               font=self.title_font,
                                               fg_color="gray",
                                               corner_radius=0,
                                               width=self.frame_left_width,
                                               height=self.button_height,
                                               command=self.settings_screen)
        self.settings_button.grid(row=4, column=0)
        # This makes sure that the home page is the first thing that is shown
        self.home_screen()

    def create_login_screen(self):
        # ==== Here we are creating the frames which the app will be in ==== #
        self.grid_columnconfigure(0, weight=5)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ct.CTkFrame(master=self, corner_radius=0)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.main_frame.rowconfigure(8, weight=10)
        self.main_frame.rowconfigure(1, weight=5)
        self.main_frame.columnconfigure(0, weight=1)

        self.login_screen()

    # This is where the home page will be defined
    def home_screen(self):
        for child in self.frame_right.winfo_children():
            child.destroy()

        # This creates the title for the software
        self.home_title = ct.CTkLabel(master=self.frame_right,
                                      text="Welcome, {0}".format(self.user.display_name),
                                      font=self.title_font,
                                      text_color="white")
        self.home_title.grid(row=0, column=0, padx=20, pady=15)
        self.home_title.configure()

    # This is where the home page will be defined
    def login_screen(self):
        for child in self.main_frame.winfo_children():
            child.destroy()

        # This creates the title for the software
        self.login_title = ct.CTkLabel(master=self.main_frame,
                                      text="Login",
                                      font=self.title_font,
                                      text_color="white")
        self.login_title.grid(column=0, row=4, padx=5, pady=30)
        self.login_title.configure()

        self.email_entry = ct.CTkEntry(
            master=self.main_frame,
            placeholder_text="Email",
            width=180,
            corner_radius=10
        )
        self.email_entry.grid(
            column=0,
            row=5,
            padx=10,
            pady=10
        )

        self.login_btn = ct.CTkButton(
            master=self.main_frame,
            text="Log In",
            width=120,
            corner_radius=10,
            command=self.login
        )
        self.login_btn.grid(
            column=0,
            row=6,
            padx=10,
            pady=10
        )

        self.register_btn = ct.CTkButton(
            master=self.main_frame,
            text="Register",
            width=120,
            corner_radius=10,
            command=self.register_screen
        )
        self.register_btn.grid(
            column=0,
            row=7,
            padx=10,
        )

    def register_screen(self):
        for child in self.main_frame.winfo_children():
            child.destroy()

        # This creates the title for the software
        self.register_title = ct.CTkLabel(master=self.main_frame,
                                      text="Register",
                                      font=self.title_font,
                                      text_color="white")
        self.register_title.grid(column=0, row=2, padx=5, pady=30)
        self.register_title.configure()

        self.username_entry = ct.CTkEntry(
            master=self.main_frame,
            placeholder_text="Username",
            width=180,
            corner_radius=10
        )
        self.username_entry.grid(
            column=0,
            row=3,
            padx=10,
            pady=10
        )

        self.first_name_entry = ct.CTkEntry(
            master=self.main_frame,
            placeholder_text="First Name",
            width=180,
            corner_radius=10
        )
        self.first_name_entry.grid(
            column=0,
            row=4,
            padx=10,
            pady=10
        )

        self.last_name_entry = ct.CTkEntry(
            master=self.main_frame,
            placeholder_text="Last Name",
            width=180,
            corner_radius=10
        )
        self.last_name_entry.grid(
            column=0,
            row=5,
            padx=10,
            pady=10
        )

        self.email_entry = ct.CTkEntry(
            master=self.main_frame,
            placeholder_text="Email",
            width=180,
            corner_radius=10
        )
        self.email_entry.grid(
            column=0,
            row=6,
            padx=10,
            pady=10
        )

        self.register_btn = ct.CTkButton(
            master=self.main_frame,
            text="Register",
            width=120,
            corner_radius=10,
            command=self.create_account
        )
        self.register_btn.grid(
            column=0,
            row=7,
            padx=10,
            pady=10
        )

    def settings_screen(self):
        for child in self.frame_right.winfo_children():
            child.destroy()

        self.frame_right.grid_columnconfigure(1, weight=1)
        self.frame_right.grid_columnconfigure(0, weight=1)

        self.frame_va_settings = ct.CTkFrame(master=self.frame_right, corner_radius=0)
        self.frame_va_settings.grid(row=1, column=0, sticky="nswe", padx=20, pady=20)

        self.frame_app_settings = ct.CTkFrame(master=self.frame_right, corner_radius=0)
        self.frame_app_settings.grid(row=1, column=1, sticky="nswe", padx=20, pady=20)

        self.settings_title = ct.CTkLabel(master=self.frame_right,
                                      text="Settings",
                                      font=self.title_font)
        self.settings_title.grid(row=0, column=0, columnspan=2, padx=15, pady=10, sticky="w")

        # === These are all the settings which can be changed === #
        self.voice_assistant_title = ct.CTkLabel(master=self.frame_va_settings,
                                          text="Voice Assistant Settings",
                                          font=self.title_font)
        self.voice_assistant_title.grid(row=1, column=0, columnspan=1, padx=15, pady=10, sticky="w")

        # === These are all the settings which can be changed === #
        self.app_settings_title = ct.CTkLabel(master=self.frame_app_settings,
                                                 text="App + Other Settings",
                                                 font=self.title_font)
        self.app_settings_title.grid(row=1, column=0, columnspan=1, padx=15, pady=10)

        # Creating the time format setting

        time_format = str(self.db.get_date_format())[1:3]
        self.format = time_format + "-Hour Format"

        self.format_switch = ct.CTkSwitch(master=self.frame_va_settings,
                                          text=self.format,
                                          command=self.sel_format_event,
                                          font=self.normal_font,
                                          onvalue="24",
                                          offvalue="12"
                                          )
        self.format_switch.grid(row=2, column=0, padx=10, pady=20, sticky="w")

        if time_format == "24":
            self.format_switch.toggle()

        # Creating the name setting
        self.name_title = ct.CTkLabel(master=self.frame_va_settings,
                                      text="Name",
                                      font=self.normal_font)
        self.name_title.grid(row=4, column=0, padx=15, pady=0, sticky="w")

        name = str(self.db.get_name())[2:-3]

        self.name_entry = ct.CTkEntry(master=self.frame_va_settings,
                                      placeholder_text=name,
                                      font=self.normal_font)
        self.name_entry.grid(row=5, column=0, padx=15, pady=15, sticky="we")

        # This button will be used to save all the settings chosen to the database
        self.save_btn = CTkButton

    def history(self):
        for child in self.frame_right.winfo_children():
            child.destroy()


    def create_account(self):
        name = self.first_name_entry.get()
        surname = self.last_name_entry.get()
        email = self.email_entry.get()
        username = self.username_entry.get()

        try:
            user = self.auth.create_user(
                email=email,
                display_name=username,
            )

            data = {
                u'uid': user.uid,
                u'name': name,
                u'surname': surname,
                u'email': email,
            }
            user_id = str(user.uid)
            newDoc = self.fs.collection(u'users').document(u'{}'.format(user_id))
            newDoc.set(data)

            self.user = self.auth.get_user(user.uid)
            self.uid = self.user.uid
            print(self.user.display_name)
            self.create_main_screen()
        except:
            error = traceback.print_exc()
            print(error)
            print("Error occurred while creating an account")

    def login(self):
        try:
            self.user = self.auth.get_user_by_email(self.email_entry.get())
            self.uid = self.user.uid
            self.create_main_screen()
        except:
            print("Retry")

    def get_user_info(self, user_id):
        docRef = self.fs.collection(u'users').document(u'{}'.format(user_id))
        doc = docRef.get()
        if doc.exists:
            self.user_info = doc
        else:
            self.user_info = None

    # This will define what happens when the exit button is pressed
    def close(self, event=0):
        self.destroy()

    def sel_format_event(self):
        current = self.format_switch.get()
        if current == "12":
            self.format_switch.configure(text="12-Hour Format")
        elif current == "24":
            self.format_switch.configure(text="24-Hour Format")

    # This will define what happens when the save button is pressed in the exit menu
    def save_format(self):
        time_format = self.format_switch.get()
        self.db.set_date_format(time_format)

        name = self.name_entry.get()
        self.db.set_name(name)

        print(self.db.get_all_settings())

if __name__ == "__main__":
    application = Application()
    application.mainloop()