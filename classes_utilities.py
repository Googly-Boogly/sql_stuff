# from global_code.helpful_functions import connecttomysql, create_logger_error
import pymysql.cursors

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

class timers:

    db = 'iris_v2'

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.end_date = data['end_date']
        self.name = data['name']
        self.added = data['added']
        self.updated = data['updated']
        self.device_id = data['device_id']


    @staticmethod
    def save(data):
        # logger = create_logger_error(__file__, 'timer')

        query = 'INSERT INTO timers (user_id, end_date, name, added, updated) VALUES (%(user_id)s, %(end_date)s, %(name)s, %(added)s, %(updated)s);'
        try:
            x = connecttomysql(timers.db).query_db(query, data)
            return x
        except Exception as e:
            # logger.error(e)
            return None



    @staticmethod
    def select_all():
        # logger = create_logger_error(__file__, 'timer')

        query = 'SELECT * FROM timers'
        try:
            x = connecttomysql(timers.db).query_db(query)
            return x
        except Exception as e:
            # logger.error(e)
            return None