# This is what we will use to create databases and alter them
import sqlite3

class database():
    def __init__(self):
        # This connects our program to the appropriate database
        # Or creates it if the file hasn't been created
        self.conn = sqlite3.connect('settings.db')

        # A cursor is used to edit the database
        self.c = self.conn.cursor()

    # === These are the setters and getters for the name element === #
    def get_email(self):
        self.c.execute("SELECT email FROM tblAccounts")
        result = self.c.fetchone()[0]
        return result

    def set_email(self, email):
        self.c.execute(f"""
        UPDATE tblAccounts
        SET email='{email}';
    """)
        self.conn.commit()

    # === These are the setters and getters for the date format element === #
    def get_loggedInStatus(self):
        self.c.execute("SELECT loggedIn FROM profile")
        return self.c.fetchone()

    def set_loggedInStatus(self, status):
        self.c.execute(f"""
        UPDATE profile
        SET loggedIn='{status}';
    """)
        self.conn.commit()

    # === This will show the entire database - for debugging purposes === #
    def get_all_profile(self):
        self.c.execute("""
        SELECT *
        FROM profile
        """)
        return self.c.fetchall()

    # === These are the setters and getters for the name element === #
    def get_name(self):
        self.c.execute("SELECT name FROM tblAccounts")
        return self.c.fetchone()

    def set_name(self, name):
        self.c.execute(f"""
        UPDATE settings
        SET name='{name}';
    """)
        self.conn.commit()

    # === These are the setters and getters for the date format element === #
    def get_date_format(self):
        self.c.execute("SELECT date_format FROM settings")
        return self.c.fetchone()

    def set_date_format(self, format):
        self.c.execute(f"""
        UPDATE settings
        SET date_format='{format}';
    """)
        self.conn.commit()

    # === This will show the entire database - for debugging purposes === #
    def get_all_settings(self):
        self.c.execute("""
        SELECT *
        FROM settings
        """)
        return self.c.fetchall()

    ### These are all the database subroutines which need to be created ###

    def login(self, email, password):
        return 1

    def register(self, email, password, first_name, last_name):

    def end(self):
        self.conn.close()