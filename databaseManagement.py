import pymysql
import pymysql.cursors
import os


class DB:
    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.conn = pymysql.connect(
                host="localhost",
                user=os.environ["user"],
                password=os.environ["DBPASSWORD"],
                db=os.environ["database"],
                cursorclass=pymysql.cursors.DictCursor,
            )
        except pymysql.Error as e:
            print("Error connecting to the database:", e)

    def query(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            result = cursor.fetchall()
            cursor.close()
            return result
        except (pymysql.Error, AttributeError) as e:
            print("Error executing query:", e)
            try:
                self.connect()  # Attempt to reconnect
                cursor = self.conn.cursor()
                cursor.execute(sql)
                self.conn.commit()
                result = cursor.fetchall()
                cursor.close()
                return result
            except pymysql.Error as e:
                print("Error reconnecting to the database:", e)
                return None
