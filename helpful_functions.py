import logging
import pymysql.cursors
import os
# This will be a universal page, for use across multiple projects


def create_logger_error(file_name='temp', name='temp'):
    # ---------------------------------------------------------------------------
    # This will create a logger object that will display errors
    # ---------------------------------------------------------------------------

    logger = logging.getLogger(name)

    logs_dir = "../utils/logs"
    os.makedirs(logs_dir, exist_ok=True)  # Create the "logs" folder if it doesn't exist

    log_dir = os.path.join(logs_dir, os.path.splitext(os.path.basename(str(file_name) + '.py'))[0])
    os.makedirs(log_dir, exist_ok=True)  # Create the subfolder if it doesn't exist

    log_file = os.path.join(log_dir, f"{name}.log")
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


# logging.basicConfig(level=logging.INFO, filename='log.log', filemode='w',
#                         format="%(asctime)s - %(levelname)s - %(message)s")


def create_logger_all(file_name, name):
    # ---------------------------------------------------------------------------
    # This will create a logger object that will display everything
    # ---------------------------------------------------------------------------

    logger = logging.getLogger(name)

    caller_dir = os.path.dirname(os.path.abspath(file_name))
    logs_dir = os.path.join(caller_dir, "../utils/logs")
    os.makedirs(logs_dir, exist_ok=True)  # Create the "logs" folder if it doesn't exist

    log_file = os.path.join(logs_dir, f"{name}.log")
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


class CustomError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

# this class will give us an instance of a connection to our database
class MySQLConnection:
    def __init__(self, db):
        # change the user and password as needed
        connection = pymysql.connect(host='localhost',
                                     port=8889,
                                     user='root',
                                     password='root',
                                     db=db,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor,
                                     autocommit=True)
        # establish the connection to the database
        self.connection = connection

    # the method to query the database
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                # On off SQL Text buttton
                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    # INSERT queries will return the ID NUMBER of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                    result = cursor.fetchall()
                    return result
                else:
                    # UPDATE and DELETE queries will return nothing
                    self.connection.commit()
            except Exception as e:
                # if the query fails the method will return FALSE
                return False
            finally:
                # close the connection
                self.connection.close()
            # connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection


def connecttomysql(db):
    return MySQLConnection(db)


def count_lines_of_code(directory):
    # Enter in exact directory
    total_lines = 0

    for root, dirs, files in os.walk(directory):
        # Exclude the "venv" folder
        if "venv" in dirs:
            dirs.remove("venv")

        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    total_lines += len(lines)

    return total_lines