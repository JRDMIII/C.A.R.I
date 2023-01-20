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
        uid = self.getUserID()[0]

        self.c.execute(f"""SELECT email FROM tblAccounts
               WHERE userID="{uid}"
               """)
        result = self.c.fetchone()[0]
        return result

    def set_email(self, email):
        self.c.execute(f"""
        UPDATE tblAccounts
        SET email='{email}';
    """)
        self.conn.commit()

    def get_plug1IP(self):
        uid = self.getUserID()[0]

        self.c.execute(f"""SELECT plugOneIP FROM tblSettings
        WHERE userID="{uid}"
        """)
        try:
            result = self.c.fetchone()[0]
            return result
        except:
            return "*No IP added"

    def set_plug1IP(self, IP):
        uid = self.getUserID()[0]
        

        try:
            self.c.execute(f"""
            UPDATE tblSettings
            SET plugOneIP='{IP}'
            WHERE userID="{uid}"
        """)
            self.conn.commit()
            return "Success"
        except:
            return "Failed"

    def get_plug2IP(self):
        uid = self.getUserID()[0]
        

        self.c.execute(f"""SELECT plugTwoIP FROM tblSettings
        WHERE userID="{uid}"
        """)
        try:
            result = self.c.fetchone()[0]
            return result
        except:
            return "*No IP added"

    def set_plug2IP(self, IP):
        uid = self.getUserID()[0]
        

        try:
            self.c.execute(f"""
            UPDATE tblSettings
            SET plugTwoIP='{IP}'
            WHERE userID="{uid}";
        """)
            self.conn.commit()
            return "Success"
        except:
            return "Failed"

    def get_bulbIP(self):
        uid = self.getUserID()[0]

        self.c.execute(f"""SELECT bulbIP FROM tblSettings
        WHERE userID="{uid}"
        """)
        try:
            result = self.c.fetchone()[0]
            return result
        except:
            return "*No IP added"

    def set_bulbIP(self, IP):
        uid = self.getUserID()[0]
        

        try:
            self.c.execute(f"""
            UPDATE tblSettings
            SET bulbIP='{IP}'
            WHERE userID="{uid};
        """)
            self.conn.commit()
            return "Success"
        except:
            return "Failed"

    def get_theme(self):
        uid = self.getUserID()[0]

        self.c.execute(f"""
        SELECT tblSettings.colourID, tblColourPresets.presetPath
        FROM tblSettings
        INNER JOIN tblColourPresets
        ON tblSettings.colourID=tblColourPresets.colourPresetID
        WHERE userID="{uid}"
        """)
        result = self.c.fetchone()
        return result

    def set_theme(self, ID):
        uid = self.getUserID()[0]
        

        try:
            self.c.execute(f"""
            UPDATE tblSettings
            SET colourID='{ID}'
            WHERE userID="{uid}";
        """)
            self.conn.commit()
            return "Success"
        except:
            return "Failed"

    # === These are the setters and getters for the date format element === #
    def get_loggedInStatus(self):
        self.c.execute("SELECT loggedIn FROM tblCurrentStatus")
        return self.c.fetchone()

    # === These are the setters and getters for the name element === #
    def get_name(self):
        uid = self.getUserID()[0]

        self.c.execute(f"""SELECT firstName FROM tblAccounts
               WHERE userID="{uid}"
               """)
        return self.c.fetchone()[0]

    def set_name(self, name):
        uid = self.getUserID()[0]

        self.c.execute(f"""
        UPDATE tblAccounts
        SET firstName='{name}'
        WHERE userID="{uid}";
    """)
        self.conn.commit()

    # === These are the setters and getters for the date format element === #
    def get_time_format(self):
        self.c.execute("SELECT time_format FROM tblSettings")
        return self.c.fetchone()

    def set_time_format(self, format):
        self.c.execute(f"""
        UPDATE tblSettings
        SET time_format='{format}';
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

    def login(self, emailAttempt, passwordAttempt):
        try:
            self.c.execute(f"""
            SELECT email, password FROM tblAccounts
            WHERE email="{emailAttempt}" 
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
                UPDATE tblCurrentStatus
                SET userID="{userID}"
                WHERE loggedIn="No"
                """)
                self.conn.commit()

                self.c.execute(f"""
                UPDATE tblCurrentStatus
                SET loggedIn="Yes"
                WHERE userID="{userID}"
                """)
                self.conn.commit()

                return True, "001"
            else:
                return False, "002"
        except:
            return False, "003"

    def logout(self):
        try:
            uid = self.getUserID()[0]

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

            self.c.execute(f"""
            INSERT INTO tblAccounts
            (userID, email, password, firstName, lastName)
            VALUES 
            ("{randomID}", "{email}", "{password}", "{first_name}", "{last_name}")
            """)
            self.conn.commit()

            self.c.execute(f"""
                        INSERT INTO tblSettings
                        (userID, colourID, textID, time_format)
                        VALUES 
                        ("{randomID}", "001", "default", "24")
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