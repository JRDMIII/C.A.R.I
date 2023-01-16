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
        self.c.execute("SELECT loggedIn FROM tblCurrentStatus")
        return self.c.fetchone()

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
        FROM tblSettings
        """)
        return self.c.fetchall()

    ### These are all the database subroutines which need to be created ###

    def login(self, email, passwordAttempt):
        try:
            self.c.execute(f"""
            SELECT email, password FROM tblAccounts
            WHERE email="{email}" 
            """)

            result = self.c.fetchone()

            email, password = result[0], result[1]

            if password == passwordAttempt:
                self.c.execute(f"""
                SELECT userID FROM tblAccounts
                WHERE email="{email}"
                """)

                userID = str(self.c.fetchone()[0])

                self.c.execute(f"""
                INSERT INTO tblCurrentStatus(userID, loggedIn)
                VALUES ("{userID}", "Yes")
                """)
                self.conn.commit()

                return True, "001"
            else:
                return False, "002"
        except:
            return False, "003"

    def logout(self, uid):
        try:
            # This changes the loggedIn boolean value to "No" so when the
            # application sees it on startup it will show the login screen
            self.c.execute(f"""
            UPDATE tblCurrentStatus
            SET loggedIn="No"
            WHERE userID="{uid}";
            """)
            self.conn.commit()

            # This changes the userID to a dummy variable to show there is currently no user logged in
            self.c.execute(f"""
            UPDATE tblCurrentStatus
            SET userID="deleted"
            WHERE userID="{uid}";
            """)
            self.conn.commit()

            return True, "011"
        except:
            return False, "012"

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

            self.login(email, password)

            return "Success!"
        except:
            return "Failed"

    def getUserID(self):
        self.c.execute("SELECT userID FROM tblCurrentStatus")
        return self.c.fetchone()

    def end(self):
        self.conn.close()

def main():
    db = database()
    print(db.login("damiolatunji@gmail.com", "party393")[1])
    print(db.logout("01b7e4198-d3ca-4d65-a98a-6f2e17d613ae")[1])




main()
