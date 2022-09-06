# This is the module that will be used to create the UI
import tkinter

import customtkinter as ct
import ui_creation as tui
import tkinter as t

# This module will allow us to read and write to the settings file
import csv

# This decides what colours will be picked for the application
ct.set_appearance_mode("System")
ct.set_default_color_theme("dark-blue")


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
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = ct.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # == This is where the left frame will be configured == #
        self.left_title = ct.CTkLabel(master=self.frame_left,
                                      text="C.A.R.I. Control Centre",
                                      text_font=(self.font_bold, self.title_size))
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
                                      text_font=(self.font_bold, self.title_size))
        self.home_title.grid(row=0, column=0, padx=5, pady=10)
        self.home_title.configure()

        # This creates the title for the software
        self.p1 = ct.CTkLabel(master=self.frame_right,
                                      text="Welcome to the C.A.R.I Control Centre",
                                      text_font=(self.font, self.normal_size))
        self.p1.grid(row=1, column=0, padx=5, pady=10)


    def settings_page(self):
        # This for loop allows for us to completely change the page which we are looking at
        for i in self.frame_right.winfo_children():
            i.destroy()

        self.settings_title = ct.CTkLabel(master=self.frame_right,
                                      text="Settings",
                                      text_font=(self.font_bold, self.title_size))
        self.settings_title.grid(row=0, column=0, padx=5, pady=20)

    # === This is where the button functions will be defined === #

    # This will define what happens when the exit button is pressed
    def close(self, event=0):
        self.destroy()


if __name__ == "__main__":

    app = Application()
    app.mainloop()
