import customtkinter as ct
import csv

# This file will be used to make all the different UI components that will go into the application so
# they can be found and edited easily

font = "Nunito"

# This is the procedure that will create
def btn(smaster, scommand, scolor=None, stext="No Text", srow="0", scolumn="0", spadx=5, spady=5, stxt_color="white"):
    settings_btn = ct.CTkButton(master=smaster,
                                text=stext,
                                command=scommand,
                                fg_color=scolor,
                                text_color=stxt_color, text_font=font)
    settings_btn.grid(row=srow,
                      column=scolumn,
                      padx=spadx,
                      pady=spady)