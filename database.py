# This is what we will use to create databases and alter them
import sqlite3

class database():
    def __init__(self):
        try:

            # This connects our program to the appropriate database
            # Or creates it if the file hasn't been created
            self.conn = sqlite3.connect('settings.db')

            # A cursor is used to edit the database
            self.c = self.conn.cursor()

            self.c.execute("""CREATE TABLE settings (
                            name text,
                            date_format integer
                )""")
            self.c.execute(f"INSERT INTO settings VALUES ('User', '12')")
            self.conn.commit()
        except sqlite3.OperationalError:
            print("Database Already Created")

    def insert_name(self, name):
        # This will insert the desired name into the table
        self.c.execute(f"INSERT INTO settings VALUES ('{name}', '12')")
        self.conn.commit()

    # === These are the setters and getters for the name element === #
    def get_name(self):
        self.c.execute("SELECT name FROM settings")
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
    def get_all(self):
        self.c.execute("""
        SELECT *
        FROM settings
        """)
        return self.c.fetchall()
    def end(self):
        self.conn.close()
