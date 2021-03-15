import sqlite3, classes, pathlib
from constants import DATABASE_PATH

def prepare_database():
    pathlib.Path("./db").mkdir(parents=True, exist_ok=True)
    databaseConnection = None
    # Attempt to connect to the database file.
    try:
        databaseConnection = sqlite3.connect(DATABASE_PATH)
    # Report an error if one appears.
    except sqlite3.Error as e:
        print(e)
    # Close the file if it has been opened.
    finally:
        if databaseConnection != None:
            databaseConnection.close()
    return databaseConnection

def drop_highscore_table():
    execute_sql("DROP TABLE highscores;")

def create_highscore_table():
    execute_sql("CREATE TABLE IF NOT EXISTS highscores (name text PRIMARY KEY, discs integer NOT NULL);")

def add_new_highscore(name, discs):
    execute_sql("INSERT INTO highscores VALUES (?, ?);", (name, discs))

def update_highscore(name, discs):
    execute_sql("UPDATE highscores SET name = ? , discs = ? ;", (name, discs))

def execute_sql(sql, placeholderValues = None):
    databaseConnection = None
    try:
        databaseConnection = sqlite3.connect(DATABASE_PATH)
        # Create a cursor object which will run SQL commands.
        cursor = databaseConnection.cursor()
        # Execute the SQL command. If "placeholderValues" is set, then the values will be inserted in the placeholders. Otherwise, plain SQl will be run.
        # That is, where there are placeholdes (character "?") values from "placeholderValues" will be inserted.
        cursor.execute(sql, placeholderValues) if placeholderValues is not None else cursor.execute(sql)
        # Save the changes to the database file.
        databaseConnection.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        if databaseConnection != None:
            databaseConnection.close()

def get_highscores():
    databaseConnection = None
    scores = []
    try:
        databaseConnection = sqlite3.connect(DATABASE_PATH)
        # Create a cursor object which will run SQL commands.
        cursor = databaseConnection.cursor()
        # Execute the SQL command. If "placeholderValues" is set, then the values will be inserted in the placeholders. Otherwise, plain SQl will be run.
        # That is, where there are placeholdes (character "?") values from "placeholderValues" will be inserted.
        cursor.execute("SELECT name, discs FROM highscores;")
        records = cursor.fetchall()
        for record in records:
            scores.append(classes.ScoreRecord(record[0], record[1]))
    except sqlite3.Error as e:
        print(e)
    finally:
        if databaseConnection != None:
            databaseConnection.close()
        return scores
