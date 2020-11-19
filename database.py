import sqlite3, constants
from constants import DATABASE_PATH

def prepare_database():
    databaseConnection = False
    # Attempt to connect to the database file.
    try:
        databaseConnection = sqlite3.connect(DATABASE_PATH)
        print(sqlite3.version)
    # Report an error if one appears.
    except sqlite3.Error as e:
        print(e)
    # Close the file if it has been opened.
    finally:
        if databaseConnection != None:
            databaseConnection.close()
    return databaseConnection

def create_highscore_table(connection):
    execute_sql(connection, "CREATE TABLE IF NOT EXISTS highscores (name text PRIMARY KEY, discs integer NOT NULL);")

def add_new_highscore(connection, name, discs):
    execute_sql(connection, "INSERT INTO highscores VALUES (?, ?)", (name, discs))

def update_highscore(connection, name, discs):
    execute_sql(connection, "UPDATE highscores SET name = ? , discs = ? ;", (name, discs))

def execute_sql(connection, sql, placeholderValues = None):
    try:
        # Create a cursor object which will run SQL commands.
        cursor = connection.cursor()
        # Execute the SQL command. If "placeholderValues" is set, then the values will be inserted in the placeholders. Otherwise, plain SQl will be run.
        # That is, where there are placeholdes (character "?") values from "placeholderValues" will be inserted.
        cursor.execute(sql, placeholderValues) if placeholderValues is not None else cursor.execute(sql)
        # Save the changes to the database file.
        connection.commit()
    except sqlite3.Error as e:
        print(e)
