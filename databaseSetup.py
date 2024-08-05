import pymysql
import pymysql.cursors
from databaseManagement import DB


def connect():
    try:
        db = DB()
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="ofqr2595",
            db="testdb",
            cursorclass=pymysql.cursors.DictCursor,
        )

        cur = conn.cursor()
        # cur.execute(r"drop database test;")
        # cur.execute(r"create database testdb;")
        cur.execute(r"use testdb;")
        # cur.execute(
        #    r"create table User(Username varchar(100),Name varchar(100), Email varchar(100), Password varchar(100));"
        # )
        #print(len(db.query(r"select * from User where ")))
        cur.execute(r"create table Recipe(RecipeId int, Username varchar(100), RecipeName varchar(100), DifficultyLevel int, CookingTime int, Description varchar(100), Recipe varchar(600), Rating int, TotalReviews int);")
        cur.execute(r"desc Recipe;")
        print(cur.fetchall())
        
    except Exception as e:
        print(e)


connect()
