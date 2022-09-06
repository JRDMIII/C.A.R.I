# This is the module that will be used to create the UI
import customtkinter as ct

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

        # This sets the title and dimensions of the application as well as what occurs when the app is closed
        self.title("C.A.R.I Control Centre")
        self.geometry(f"{Application.WIDTH}x{Application.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.close)

        # Here we are creating the frames which the app will be in

        # Configuring a 2x1 grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # This is where the left and right sections of the frame are defined
        self.frame_left = ct.CTkFrame(master=self, width=200, height=800, corner_radius=0)
        self.frame_right = ct.CTkFrame(master=self, corner_radius=15, fg_color="dark-blue")

        self.frame_left.grid(row=0, column=0, sticky="nswe")
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

    # This will define what happens when the exit button is pressed
    def close(self, event=0):
        self.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
