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
    try:
        cursor = connection.cursor()
        # Create a high scores table with the attributes:
        # - "name" type text, primary key,
        # - "discs" type integrer.
        cursor.execute("CREATE TABLE IF NOT EXISTS highscores (name text PRIMARY KEY, discs integer NOT NULL);")
    except sqlite3.Error as e:
        print(e)
