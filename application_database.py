# This is what we will use to create databases and alter them
import sqlite3
import uuid

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
        self.c.execute("SELECT loggedIn FROM currentStatus")
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

    def login(self, email, passwordAttempt):
        self.c.execute(f"""
        SELECT password FROM tblAccounts 
        WHERE email="{email}" 
        """)
        password = self.c.fetchone()[0]
        if password == passwordAttempt:


    def register(self, email, password, first_name, last_name):
        try:
            randomID = "0" + str(uuid.uuid4())
            print(randomID)

            self.c.execute(f"""
            INSERT INTO tblAccounts
            (userID, email, password, firstName, lastName)
            VALUES 
            ("{randomID}", "{email}", "{password}", "{first_name}", "{last_name}")
            """)
            self.conn.commit()
            return "Success!"
        except:
            return "Failed"

    def end(self):
        self.conn.close()

def main():
    db = database()
    db.login("damiolatunji@gmail.com", "party393")




main()
