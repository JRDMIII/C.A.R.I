# This is the module that will be used to create the UI
import sqlite3
import threading
import tkinter
import time
import re

from tkinter import colorchooser
import colorsys as csys

import hardware
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

class Application(ct.CTk):

    # This defines the width and height of the app
    WIDTH = 800
    HEIGHT = 800

    # Creating the constructor method
    def __init__(self):
        super().__init__()

        # This initialises the database class to access the SQL database
        self.db = application_database.database()

        self.colour_code = ""
        self.hardware = hardware.Hardware(self.db.get_plug1IP(), self.db.get_plug2IP(), self.db.get_bulbIP(), "damiolatunji4tj@gmail.com", "party39ta3")

        # This uses the database to get the value of loggedIn in tblCurrentStatus
        self.loggedIn = self.db.get_loggedInStatus()[0]

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

        try:
            ct.set_default_color_theme(self.db.get_theme()[1])
        except:
            ct.set_default_color_theme("dark-blue")

        # This checks to see if the user has logged in and goes
        # to the appropriate screen depending on the result of the check
        if "No" in self.loggedIn:
            self.create_login_screen()
        else:
            self.uid = self.db.getUserID()
            self.create_main_screen()

    # === This is where the contents of all the pages will be designed === #

    def create_main_screen(self):
        # ==== Here we are creating the frames which the app will be in ==== #
        for child in self.winfo_children():
            child.destroy()

        # Re-initialising the hardware object using the information of the newly logged in user
        self.hardware = hardware.Hardware(self.db.get_plug1IP(), self.db.get_plug2IP(), self.db.get_bulbIP(),
                                          "damiolatunji4tj@gmail.com", "party39ta3")

        # Debug statement to make sure the correct person has logged in
        print("Logged in as {0}".format(self.db.getUserID()[0]))

        # Setting the colour theme to the user's desired colour scheme in the settings menu
        ct.set_default_color_theme(self.db.get_theme()[1])

        # Configuring the rows and columns of the application for the frames to be added
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Creating the frame which will include all the objects
        self.application_frame = ct.CTkTabview(master=self, corner_radius=0)
        self.application_frame.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

        # Creating the two tabs that wil be included in the main application screen
        self.devices_tab = self.application_frame.add("Devices")
        self.settings_tab = self.application_frame.add("Settings")

        # This is what creates the settings tab
        # Configuring the columns and rows of the settings tab to match the design
        self.settings_tab.grid_columnconfigure(1, weight=1)
        self.settings_tab.grid_columnconfigure(0, weight=1)
        self.settings_tab.grid_rowconfigure(1, weight=1)

        # This sets up both of the frames which are included in the settings tab
        self.frame_va_settings = ct.CTkFrame(master=self.settings_tab, corner_radius=10)
        self.frame_va_settings.grid(row=1, column=0, sticky="nswe", padx=10, pady=20)
        self.frame_va_settings.grid_columnconfigure(0, weight=0)

        # Creating the column for all settings relating to the application
        self.frame_app_settings = ct.CTkFrame(master=self.settings_tab, corner_radius=10)
        self.frame_app_settings.grid(row=1, column=1, sticky="nswe", padx=10, pady=20)

        self.settings_title = ct.CTkLabel(master=self.settings_tab,
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
        # Getting the user's current time format from the database
        time_format = str(self.db.get_time_format()[0])
        self.format = time_format + "-Hour Format"

        self.format_switch = ct.CTkSwitch(master=self.frame_va_settings,
                                          text=self.format,
                                          command=self.sel_format_event,
                                          font=self.normal_font,
                                          onvalue="24",
                                          offvalue="12"
                                          )
        self.format_switch.grid(row=2, column=0, padx=10, pady=20, sticky="w")
         # Checks what the time format currently is in settings and switches the switch on if it's 24
        if time_format == "24":
            self.format_switch.toggle()

        # Creating the name setting
        self.name_title = ct.CTkLabel(master=self.frame_va_settings,
                                      text="Name",
                                      font=self.normal_font)
        self.name_title.grid(row=4, column=0, padx=15, pady=0, sticky="w")

        # Getting the users name from the database
        name = str(self.db.get_name())

        # Creating an entry box with the users name as placeholder text
        self.name_entry = ct.CTkEntry(master=self.frame_va_settings,
                                      placeholder_text=name,
                                      font=self.normal_font)
        self.name_entry.grid(row=5, column=0, padx=15, pady=15, sticky="we")

        # Creating the plug1IP setting
        # Adding and placing the title for the IP address
        self.plug1IP_title = ct.CTkLabel(master=self.frame_app_settings,
                                         text="Plug 1's IP Address",
                                         font=self.normal_font)
        self.plug1IP_title.grid(row=2, column=0, padx=15, pady=0, sticky="w")

        # Getting the current IP address for the plug held in the settings database
        plug1IP = self.db.get_plug1IP()
        self.plug1IP_entry = ct.CTkEntry(master=self.frame_app_settings,
                                         placeholder_text=plug1IP,
                                         font=self.normal_font)
        self.plug1IP_entry.grid(row=3, column=0, padx=15, pady=15, sticky="we")

        # Creating the second plug IP setting
        # Adding and placing the title for the IP address
        self.plug2IP_title = ct.CTkLabel(master=self.frame_app_settings,
                                         text="Plug 2's IP Address",
                                         font=self.normal_font)
        self.plug2IP_title.grid(row=4, column=0, padx=15, pady=0, sticky="w")

        # Getting the current IP address for the plug held in the settings database
        plug2IP = self.db.get_plug2IP()
        self.plug2IP_entry = ct.CTkEntry(master=self.frame_app_settings,
                                         placeholder_text=plug2IP,
                                         font=self.normal_font)
        self.plug2IP_entry.grid(row=5, column=0, padx=15, pady=15, sticky="we")

        # Creating the bulb IP setting
        self.bulbIP_title = ct.CTkLabel(master=self.frame_app_settings,
                                        text="Bulb's IP Address",
                                        font=self.normal_font)
        self.bulbIP_title.grid(row=6, column=0, padx=15, pady=0, sticky="w")
        bulbIP = self.db.get_bulbIP()
        self.bulbIP_entry = ct.CTkEntry(master=self.frame_app_settings,
                                        placeholder_text=bulbIP,
                                        font=self.normal_font)
        self.bulbIP_entry.grid(row=7, column=0, padx=15, pady=15, sticky="we")

        # Creating the colour theme drop down
        self.colour_theme_title = ct.CTkLabel(master=self.frame_app_settings,
                                              text="App Colour Theme",
                                              font=self.normal_font)
        self.colour_theme_title.grid(row=8, column=0, padx=15, pady=0, sticky="w")

        # Creating a variable which will be used to store the current colour theme
        self.colour_theme_var = ct.StringVar(value=(self.db.get_theme()[1]).replace("-", " "))
        self.colour_theme_entry = ct.CTkComboBox(master=self.frame_app_settings,
                                                 values=["dark blue", "green", "blue"],
                                                 command=self.colourThemeCallback,
                                                 variable=self.colour_theme_var,
                                                 font=self.normal_font)
        self.colour_theme_entry.grid(row=9, column=0, padx=15, pady=15, sticky="we")

        # This button allows users to logout through the settings menu
        self.logout_button = ct.CTkButton(master=self.frame_app_settings,
                                          text="Logout",
                                          font=self.title_font,
                                          corner_radius=10,
                                          width=self.frame_left_width,
                                          height=35,
                                          command=self.logout)
        self.logout_button.grid(row=10, column=0, padx=40, pady=10, sticky="we")

        # Creating a button which will activate the save function when pressed
        self.save_btn = ct.CTkButton(
            master=self.settings_tab,
            text="Save",
            width=120,
            corner_radius=10,
            command=self.save_format
        )
        self.save_btn.grid(
            column=0,
            columnspan=2,
            row=2,
            padx=10,
            pady=10,
            sticky="we"
        )


        # A try except statement is used to show users without valid devices a different screen
        try:
            # This defines what the devices tab will look like
            self.devices_tab.grid_columnconfigure(0, weight=1)
            self.devices_tab.grid_columnconfigure(1, weight=1)
            self.devices_tab.grid_rowconfigure(0, weight=1)
            self.devices_tab.grid_rowconfigure(1, weight=1)
            self.devices_tab.grid_rowconfigure(2, weight=10)
            self.devices_tab.grid_rowconfigure(3, weight=10)

            # This creates the title for the software
            self.devices_title = ct.CTkLabel(master=self.devices_tab,
                                          text="Devices",
                                          font=self.title_font,
                                          text_color="white")
            self.devices_title.grid(row=0, column=0, padx=20, pady=5, sticky="wn")

            # Creating and configuring a frame for the first plug
            self.plug1_frame = ct.CTkFrame(master=self.devices_tab)
            self.plug1_frame.grid(row=1, column=0, padx=10, pady=10, sticky="sewn")
            self.plug1_frame.grid_rowconfigure(0, weight=1)
            self.plug1_frame.grid_rowconfigure(1, weight=1)
            self.plug1_frame.grid_columnconfigure(0, weight=1)

            # Creating and configuring a frame for the second plug
            self.plug2_frame = ct.CTkFrame(master=self.devices_tab)
            self.plug2_frame.grid(row=1, column=1, padx=10, pady=10, sticky="sewn")
            self.plug2_frame.grid_rowconfigure(0, weight=1)
            self.plug2_frame.grid_rowconfigure(1, weight=1)
            self.plug2_frame.grid_columnconfigure(0, weight=1)

            # Creating and configuring a frame for the light bulb
            self.bulb_frame = ct.CTkFrame(master=self.devices_tab)
            self.bulb_frame.grid(row=2, rowspan=2, column=0, columnspan=2, padx=10, pady=10, sticky="sewn")

            # Creating a title to say what the first plug controls
            self.plug1_title = ct.CTkLabel(master=self.plug1_frame, text="Plug 1 - Fan", font=self.normal_font)
            self.plug1_title.grid(row=0, column=0, padx=10, pady=10, sticky="swn")

            # Gets the state of the plug so that the switch can be toggled to show the correct state
            self.plug1State = self.hardware.getDeviceStatus("p1")

            self.plug1_switch = ct.CTkSwitch(master=self.plug1_frame, text="", onvalue=1, offvalue=0,
                                             command=self.togglePlug1)
            self.plug1_switch.grid(row=1, column=0, padx=20, pady=10, sticky="swn")

            # Changing the switch text and the state dependent on the value of plug1State
            if self.plug1State == True:
                self.plug1_switch.configure(text="On")
                self.plug1_switch.select()
            else:
                self.plug1_switch.configure(text="Off")
                self.plug1_switch.deselect()

            # Creating a title to say what the second plug controls
            self.plug2_title = ct.CTkLabel(master=self.plug2_frame, text="Plug 2 - Desk", font=self.normal_font)
            self.plug2_title.grid(row=0, column=0, padx=10, pady=10, sticky="swn")

            # Gets the state of the plug so that the switch can be toggled to show the correct state
            self.plug2State = self.hardware.getDeviceStatus("p2")

            self.plug2_switch = ct.CTkSwitch(master=self.plug2_frame, text="", onvalue=1, offvalue=0,
                                             command=self.togglePlug2)
            self.plug2_switch.grid(row=1, column=0, padx=10, pady=10, sticky="swn")

            # Changing the switch text and the state dependent on the value of plug1State
            if self.plug2State == True:
                self.plug2_switch.configure(text="On")
                self.plug2_switch.select()
            else:
                self.plug2_switch.configure(text="Off")
                self.plug2_switch.deselect()

            self.bulb_frame.grid_columnconfigure(0, weight=1)

            # Same is then done for the bulb as the other plugs
            # The title is created
            # The current state of the lightbulb is retrieved and the switch is set to show that state
            self.bulb_title = ct.CTkLabel(master=self.bulb_frame, text="Bulb", font=self.normal_font)
            self.bulb_title.grid(row=0, column=0, padx=20, pady=12, sticky="swn")

            self.bulbState = self.hardware.getDeviceStatus("b")

            self.bulb_switch = ct.CTkSwitch(master=self.bulb_frame, text="", onvalue=1, offvalue=0,
                                            command=self.toggleBulb)
            self.bulb_switch.grid(row=0, column=1, padx=10, pady=(15, 5), sticky="wn")

            if self.bulbState == True:
                self.bulb_switch.configure(text="On")
                self.bulb_switch.select()
            else:
                self.bulb_switch.configure(text="Off")
                self.bulb_switch.deselect()


            # Creating a title for the colour temperature entry
            # Title includes the range of values which are allowed for the colour temperature
            self.colourTemperature_title = ct.CTkLabel(master=self.bulb_frame,
                                                       text="Colour Temperature (From 2500-6000K)",
                                                       font=self.normal_font)
            self.colourTemperature_title.grid(row=1, column=0, padx=20, pady=12, sticky="swn")

            # Creating the colour temperature entry
            self.colourTemperature_entry = ct.CTkEntry(master=self.bulb_frame,
                                            placeholder_text="e.g. 2356",
                                            font=self.normal_font)
            self.colourTemperature_entry.grid(row=2, column=0, columnspan=2, padx=15, pady=15, sticky="we")

            # Creating the button that will open the colour picker window
            self.selectColour_button = ct.CTkButton(master=self.bulb_frame, text="Select Bulb Colour",
                                                    command=self.chooseColour)
            self.selectColour_button.grid(row=3, column=0, columnspan=2, padx=20, pady=5)

            # This creates the button which will execute the light colour change asked for by the user

            self.setColour_button = ct.CTkButton(master=self.bulb_frame, text="Save All settings",
                                                    command=self.executeLightChange)
            self.setColour_button.grid(row=5, column=0, columnspan=2, padx=20, pady=5)

            # Creating the button that will open the colour picker window
            self.rgb_button = ct.CTkButton(master=self.bulb_frame, text="RGB!",
                                                    command=self.hardware.start_rgb)
            self.rgb_button.grid(row=7, column=0, columnspan=2, padx=20, pady=5)

        except Exception as e:
            # If the user hasn't entered IP addresses for all of their devices then it will show this instead

            for child in self.devices_tab.winfo_children():
                child.destroy()

            self.devices_tab.grid_columnconfigure(0, weight=1)
            self.devices_tab.grid_columnconfigure(1, weight=0)
            self.devices_tab.grid_rowconfigure(0, weight=1)
            self.devices_tab.grid_rowconfigure(1, weight=0)
            self.devices_tab.grid_rowconfigure(2, weight=0)
            self.devices_tab.grid_rowconfigure(3, weight=0)

            # Creating a frame with text in it to say that devices are unavailable until the IP addresses have been
            # added to the settings and the application has been restarted
            self.unavailable_frame = ct.CTkFrame(master=self.devices_tab, corner_radius=5)
            self.unavailable_frame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

            self.unavailable_frame.grid_columnconfigure(0, weight=1)

            self.unavailable_title = ct.CTkLabel(master=self.unavailable_frame,
                                                 text="Devices Unavailable",
                                                 font=self.title_font)
            self.unavailable_title.grid(row=0, column=0, sticky="nswe", pady=5)
            self.unavailable_text = ct.CTkLabel(master=self.unavailable_frame,
                                                 text="Please Input All Device IPs into the settings tab then restart the application",
                                                 font=self.normal_font)
            self.unavailable_text.grid(row=1, column=0, sticky="nswe")

    def toggleBulb(self):
        # Used to toggle the text for the switch in the devices tab
        # Also toggles the state of the bulb
        value = self.bulb_switch.get()
        if value == 1:
            self.bulb_switch.configure(text="On")
            self.hardware.deviceToggle("b", True)
        if value == 0:
            self.bulb_switch.configure(text="Off")
            self.hardware.deviceToggle("b", False)

    def togglePlug1(self):
        # Used to toggle the text for the switch in the devices tab
        # Also toggles the state of the plug
        value = self.plug1_switch.get()
        if value == 1:
            self.plug1_switch.configure(text="On")
            self.hardware.deviceToggle("p1", True)
        if value == 0:
            self.plug1_switch.configure(text="Off")
            self.hardware.deviceToggle("p1", False)

    def togglePlug2(self):
        # Used to toggle the text for the switch in the devices tab
        # Also toggles the state of the plug
        value = self.plug2_switch.get()
        if value == 1:
            self.plug2_switch.configure(text="On")
            self.hardware.deviceToggle("p2", True)
        if value == 0:
            self.plug2_switch.configure(text="Off")
            self.hardware.deviceToggle("p2", False)


    def chooseColour(self):
        # Opens the colour picker window
        # When a colour is chosen in the colour picker window the value for it is saved into the colour_code attribute
        self.colour_code = colorchooser.askcolor(title="Select Colour")

        # Each value within the code needs to be divided by 225
        # They can then be saved into red, green and blue variables
        r, g, b = [x/255.0 for x in self.colour_code[0]]

        # Converting the RGB values to hue, saturation, brightness as that is
        # what the method to change the lighting takes in as an input
        self.colour_hsv = csys.rgb_to_hsv(r, g, b)

        # Putting all values in colour_hsv in the correct range
        self.colour_hsv = [self.colour_hsv[0]*360, self.colour_hsv[1]*100, self.colour_hsv[2]*100]

        # Creating a frame witch shows the colour which the user has chosen in the colour picker window
        self.colour_preview = ct.CTkFrame(master=self.bulb_frame, width=300, height=250, fg_color=self.colour_code[1])
        self.colour_preview.grid(row=4, column=0, columnspan=2, padx=20, pady=5)

    def executeLightChange(self):
        try:
            # Attempting to get the hsv values from the chooseColour() subroutine
            hue, saturation, brightness = int(self.colour_hsv[0]), int(self.colour_hsv[1]), int(self.colour_hsv[2])
        except:
            # If that doesnt work it means the user has not chosen a colour so an error message is shown
            retry_thread = threading.Thread(target=self.show_light_error_msg)
            retry_thread.start()

        try:
            # This also attempts to get the colour temperature that was inputted
            colour_temperature = int(self.colourTemperature_entry.get())

            # If there is a colour temperature it checks if it is in the correct range
            if colour_temperature <= 6000 and colour_temperature >= 2500:
                # If so the colour change is executed
                self.hardware.changeLightSettings(hue, brightness, saturation, colour_temperature)
            else:
                # Otherwise the error messasge is shown using
                # threading to show it while the user is using the application
                retry_thread = threading.Thread(target=self.show_light_error_msg)
                retry_thread.start()
        except:
            # This is if no value is in the colour temperature entry box
            # It will instead perform the colour change without giving in a colour temperature value
            self.hardware.changeLightSettings(hue, brightness, saturation, "invalid")

    def show_light_error_msg(self):
        # Creates a label at the bottom of the devices tab which
        # will show that there is an error with the users entries
        self.error_message = ct.CTkLabel(master=self.bulb_frame,
                                         text="Invalid entry / Not all fields have been filled")
        self.error_message.grid(row=6, column=0, pady=5, sticky="we", columnspan=2)
        time.sleep(3)
        self.error_message.destroy()

    def create_login_screen(self):
        # ==== Here we are creating the frames which the app will be in ==== #
        for child in self.winfo_children():
            child.destroy()

        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=0)

        self.grid_columnconfigure(0, weight=5)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ct.CTkFrame(master=self, corner_radius=0)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.main_frame.rowconfigure(9, weight=10)
        self.main_frame.rowconfigure(1, weight=5)
        self.main_frame.columnconfigure(0, weight=1)

        self.login_screen()

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

        self.password_entry = ct.CTkEntry(
            master=self.main_frame,
            placeholder_text="Password",
            width=180,
            corner_radius=10
        )
        self.password_entry.grid(
            column=0,
            row=6,
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
            row=7,
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
            row=8,
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

        self.first_name_entry = ct.CTkEntry(
            master=self.main_frame,
            placeholder_text="First Name",
            width=180,
            corner_radius=10
        )
        self.first_name_entry.grid(
            column=0,
            row=3,
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
            row=4,
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
            row=5,
            padx=10,
            pady=10
        )

        self.password_entry = ct.CTkEntry(
            master=self.main_frame,
            placeholder_text="Password",
            width=180,
            corner_radius=10
        )
        self.password_entry.grid(
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

        self.back_btn = ct.CTkButton(
            master=self.main_frame,
            text="Back",
            width=120,
            corner_radius=10,
            command=self.login_screen
        )
        self.back_btn.grid(
            column=0,
            row=0,
            padx=10,
            pady=10,
            sticky="w"
        )

    def colourThemeCallback(self, choice):
        # Simple function to change the value of the colour_theme_var to the current choice of the combobox
        self.colour_theme_var.set(choice)

    def create_account(self):
        # Getting all the values within the entry boxes
        firstname = self.first_name_entry.get()
        lastname = self.last_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Checking if any of the variables are empty and showing an error message if so
        if firstname == "" or lastname == "" or email == "" or password == "":
            self.retry_msg = "All fields must be filled"
            retry_thread = threading.Thread(target=self.show_register_error_msg)
            retry_thread.start()

        # Checking if the email is a valid email
        elif "@" not in email or ".com" not in email:
            self.retry_msg = "Invalid Email"
            retry_thread = threading.Thread(target=self.show_register_error_msg)
            retry_thread.start()

        # Checking if the account already exists
        elif self.db.check_email(email) == False:
            self.retry_msg = "Account already exists"
            retry_thread = threading.Thread(target=self.show_register_error_msg)
            retry_thread.start()

        # Performing checks on the password validity
        elif (len(password) < 6 or len(password) > 20):
            self.retry_msg = "Your password must be between 6 and 20 letters"
            retry_thread = threading.Thread(target=self.show_register_error_msg)
            retry_thread.start()

        elif not re.search("[a-z]", password):
            self.retry_msg = "Your password must have at least one lower case letter"
            retry_thread = threading.Thread(target=self.show_register_error_msg)
            retry_thread.start()

        elif not re.search("[0-9]", password):
            self.retry_msg = "Your password must have at least one number"
            retry_thread = threading.Thread(target=self.show_register_error_msg)
            retry_thread.start()

        elif not re.search("[A-Z]", password):
            self.retry_msg = "Your password must have at least 1 uppercase letter"
            retry_thread = threading.Thread(target=self.show_register_error_msg)
            retry_thread.start()

        elif not re.search("[$#@]", password):
            self.retry_msg = "Your password must have at least 1 special character"
            retry_thread = threading.Thread(target=self.show_register_error_msg)
            retry_thread.start()

        else:
            self.db.register(email, password, firstname, lastname)
            self.create_main_screen()

    def show_register_error_msg(self):
        self.error_message = ct.CTkLabel(master=self.main_frame,
                                         text=self.retry_msg)
        self.error_message.grid(row=9, column=0)
        time.sleep(1.5)
        self.error_message.destroy()

    def logout(self):
        self.db.logout()
        self.create_login_screen()

    def login(self):
        # Getting the value of the email and password
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Attempting to log into the application through the database function
        return_code = self.db.login(email, password)

        # If successful, the application's main screen is generated
        if return_code[0] == True:
            self.create_main_screen()
        else:
            if return_code[1] == "002":
                # Otherwise, if the error message is "002" it will show that
                # the password didnt match the one in the database
                self.msg = "Incorrect password"
                retry_thread = threading.Thread(target=self.show_login_error_msg)
                retry_thread.start()
            else:
                # If it isn't the password, it means that the account doesn't exist
                # Error message is shown to show that error message
                self.msg = "Account doesn't exist"
                retry_thread = threading.Thread(target=self.show_login_error_msg)
                retry_thread.start()

    def show_login_error_msg(self):
        # Creating text on the screen to show the label
        self.error_message = ct.CTkLabel(master=self.main_frame,
                                         text=self.msg)
        self.error_message.grid(row=9, column=0)
        time.sleep(3)
        self.error_message.destroy()

    # This defines what happens when the exit button is pressed
    def close(self, event=0):
        self.destroy()

    def sel_format_event(self):
        # Checking the value of the format switch
        current = self.format_switch.get()

        # Changing the text of the switch to match the current value of the switch
        if current == "12":
            self.format_switch.configure(text="12-Hour Format")
        elif current == "24":
            self.format_switch.configure(text="24-Hour Format")

    # This will define what happens when the save button is pressed in the exit menu
    def save_format(self):
        # Getting all of the values of the entry boxes
        time_format = self.format_switch.get()
        self.db.set_time_format(time_format)

        name = self.name_entry.get()

        # Checking the entry boxes to see if they are empty
        # If they aren't, it is a valid entry and the value can be saved
        if name != "":
            self.db.set_name(name)

        plug1IP = self.plug1IP_entry.get()
        if plug1IP != "":
            self.db.set_plug1IP(plug1IP)
        else:
            pass

        plug2IP = self.plug2IP_entry.get()
        if plug2IP != "":
            self.db.set_plug2IP(plug2IP)
        else:
            pass

        # This checks what colour theme is currently selected
        # and saves the corresponding ID into the settings table
        colourTheme = self.colour_theme_var.get()
        if colourTheme == "dark blue":
            self.db.set_theme("001")
        if colourTheme == "blue":
            self.db.set_theme("002")
        if colourTheme == "green":
            self.db.set_theme("003")

        # Debugging statement to check what is saved into the database now
        # Note: no longer needed as DB Browser can be used something
        # print(self.db.get_all_settings())

if __name__ == "__main__":
    application = Application()
    application.mainloop()