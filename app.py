# This is the module that will be used to create the UI
import sqlite3
import tkinter

import customtkinter as ct

import database as db
import ui_creation as tui
import scripts
from ui_creation import btn

# This module will allow us to read and write to the settings file
import csv

# This decides what colours will be picked for the application
ct.set_appearance_mode("System")
ct.set_default_color_theme("dark-blue")

# ct.CTk initialises an application window
class Application(ct.CTk):

    # This defines the width and height of the app
    WIDTH = 800
    HEIGHT = 800

    # Creating the constructor method
    def __init__(self):
        super().__init__()

        # This is how we will get the chosen colour scheme for the file to send into the class
        with open("design.txt", "r") as readFile:
            reader = csv.reader(readFile)
            # This is where all the colors for the app will be temporarily held
            colors = []

            # This is where all the sizes for the app will be temporarily held
            sizes = []
            for row in reader:
                for field in row:
                    if "#" in field:
                        start = field.find("#")
                        color = field[start:]
                        colors.append(color)
                    if "*" in field:
                        start = field.find("*")
                        start = start + 1
                        size = field[start:]
                        sizes.append(size)

        # This defines the colours that will be used in the GUI
        self.main = colors[0]
        self.highlight = colors[1]
        self.accent = colors[2]
        self.background = colors[3]
        self.font_color = colors[4]
        self.left_frame_color = colors[5]

        #This defines the font sizes for the labels in the GUI
        self.title_size = sizes[0]
        self.subtitle_size = sizes[1]
        self.normal_size = sizes[2]

        # This defines the font used for the application
        self.font = "Nunito"
        self.font_bold = "Nunito Bold"

        # This sets the title and dimensions of the application as well as what occurs when the app is closed
        self.title("C.A.R.I Control Centre")
        self.geometry(f"{Application.WIDTH}x{Application.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.close)

        # ==== Here we are creating the frames which the app will be in ==== #

        # This defines the background colour of the entire application
        self.configure(bg=self.background)

        # Configuring a 2x1 grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # This is where the left and right sections of the frame are defined
        self.frame_left = ct.CTkFrame(master=self, width=200, corner_radius=0, fg_color=self.left_frame_color)
        self.frame_right = ct.CTkFrame(master=self, corner_radius=15, fg_color=self.main)

        self.frame_left.grid(row=0, column=0, sticky="nsew")
        self.frame_right.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure(0, weight=1)

        self.frame_info = ct.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # == This is where the left frame will be configured == #
        self.left_title = ct.CTkLabel(master=self.frame_left,
                                      text="C.A.R.I. Control Centre",
                                      text_font=(self.font_bold, self.title_size),
                              text_color=self.font_color)
        self.left_title.grid(row=1, column=0, padx=10, pady=10)

        # This creates the 3 buttons and the
        self.home_btn = tui.btn(self.frame_left,
                                self.home_page,
                                self.accent,
                                "Home", 2, 0, 10, 10,
                                self.font_color)
        self.settings_btn = tui.btn(self.frame_left,
                                    self.settings_page,
                                    self.accent,
                                    "Settings", 3, 0, 10, 10,
                                    self.font_color)
        self.home_btn = tui.btn(self.frame_left,
                                self.close, self.accent,
                                "Exit", 4, 0, 10, 10,
                                self.font_color)

        # This makes sure that the home page is the first thing that is shown
        self.home_page()

    # === This is where the contents of all the pages will be designed === #

    # This is where the home page will be defined
    def home_page(self):
        # This for loop allows for us to completely change the page which we are looking at
        for i in self.frame_right.winfo_children():
            i.destroy()

        # This creates the title for the software
        self.home_title = ct.CTkLabel(master=self.frame_right,
                                      text="Home",
                                      text_font=(self.font_bold, self.title_size),
                              text_color=self.font_color)
        self.home_title.grid(row=0, column=0, padx=5, pady=10)
        self.home_title.configure()

        # This creates the title for the software
        self.s1 = ct.CTkLabel(master=self.frame_right,
                              text="scripts.subtitle_p1",
                              text_font=(self.font, self.subtitle_size),
                              text_color=self.font_color)
        self.s1.grid(row=1, column=0, padx=5, pady=1)

        # This creates the title for the software
        self.p1 = ct.CTkLabel(master=self.frame_right,
                                      text="scripts.home_page_p1",
                                      text_font=(self.font, self.normal_size),
                              text_color=self.font_color)
        self.p1.grid(row=2, column=0, padx=5, pady=1)

    def settings_page(self):
        # This for loop allows for us to completely change the page which we are looking at
        for i in self.frame_right.winfo_children():
            i.destroy()

        # These are the variables for all the settings that can be changed
        self.radio_var = tkinter.IntVar(value=0)

        self.settings_title = ct.CTkLabel(master=self.frame_right,
                                      text="Settings",
                                      text_font=(self.font_bold, self.title_size),
                              text_color=self.font_color)
        self.settings_title.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        # === These will be all the different settings === #

        time_format = str(database.get_date_format())[1:3]

        self.format = (time_format) + "-Hour Format"


        self.format_switch = ct.CTkSwitch(master=self.frame_right,
                                          text=self.format,
                                          command=self.sel_format_event,
                                          text_font=self.font,
                                          text_color=self.font_color,
                                          onvalue="24",
                                          offvalue="12")
        self.format_switch.grid(row=2, column=0, padx=10, pady=20)

        # This means the switch will be on the right setting when the settings page opens it
        if time_format == "24":
            self.format_switch.toggle()

        # === This is the name setting === #

        # This creates the title for the software
        self.name_title = ct.CTkLabel(master=self.frame_right,
                              text="Name",
                              text_font=(self.font, self.normal_size),
                              text_color=self.font_color)
        self.name_title.grid(row=3, column=0, padx=5, pady=0)

        # This gets the name from the database
        name = str(database.get_name())[2:-3]

        self.name_entry = ct.CTkEntry(master=self.frame_right,
                                    placeholder_text=name,
                                    text_font=self.font,
                                    text_color=self.font_color,)
        self.name_entry.grid(row=4, column=0, padx=10, pady=5)



        # This button will be used to save all the settings chosen to the database
        self.save_btn =  btn(self.frame_right,
                                    self.save_format,
                                    self.accent,
                                    "Save Settings", 20, 0, 10, 10,
                                    self.font_color)

    def sel_format_event(self):
        current = self.format_switch.get()
        if current == "12":
            self.format_switch.configure(text="12-Hour Format")
        elif current == "24":
            self.format_switch.configure(text="24-Hour Format")

    # === This is where the button functions will be defined === #

    # This will define what happens when the save button is pressed in the exit menu
    def save_format(self):
        time_format = self.format_switch.get()
        database.set_date_format(time_format)

        name = self.name_entry.get()
        database.set_name(name)

        print(database.get_all())

    # This will define what happens when the exit button is pressed
    def close(self, event=0):
        self.destroy()

if __name__ == "__main__":
    database = db.database()
    app = Application()
    app.mainloop()
