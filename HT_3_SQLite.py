import os
import sqlite3

from faker import Faker
from flask import Flask, render_template

app = Flask(__name__)
fake = Faker("ru_RU")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/names")
def names():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    res_all = cur.execute('SELECT FirstName FROM customers')
    list_all_first_name = len(res_all.fetchall())
    res_set = cur.execute('SELECT DISTINCT FirstName FROM customers')
    list_set_first_name = len(res_set.fetchall())
    print(list_all_first_name)
    print(list_set_first_name)
    con.close()
    return render_template("names.html",
                           list_all_first_name=list_all_first_name, list_set_first_name=list_set_first_name)


@app.route("/tracks")
def tracks():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    res = cur.execute('SELECT COUNT(ID) FROM tracks')
    result = res.fetchone()[0]
    print(result)
    con.close()
    return render_template("tracks.html", result=result)


@app.route("/tracks-sec")
def tracks_sec():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    res = cur.execute('SELECT * FROM tracks')
    result = res.fetchall()
    con.close()
    return render_template("tracks-sec.html", result=result)


@app.route("/adding_clients")
def adding_clients():
    populate_table_customers()
    return render_template("adding_clients.html")


@app.route("/adding_tracks")
def adding_tracks():
    populate_table_tracks()
    return render_template("adding_tracks.html")


def create_table_customers():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    try:
        cur.execute('''
            -- dialect: sqlite
            CREATE TABLE customers
            (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                LastName varchar(255),
                FirstName varchar(255),
                Profession varchar(255),
                PhoneNumber varchar(255)
            )
        ''')
        con.commit()
    except sqlite3.Error as ex:
        print("Таблица уже создана: ", ex)
    finally:
        con.close()


def create_table_tracks():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    try:
        cur.execute('''
            CREATE TABLE tracks
            (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                LastName varchar(255),
                TrackLength varchar(50),
                ReleaseDate varchar(50)
            )
        ''')
        con.commit()
    except sqlite3.Error as ex:
        print("Таблица уже создана: ", ex)
    finally:
        con.close()


def populate_table_customers():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    try:
        for i in range(100):
            cur.execute("INSERT INTO customers (LastName, FirstName, Profession, PhoneNumber) VALUES (?, ?, ?, ?)",
                        (fake.last_name(), fake.first_name(), fake.job(), fake.phone_number()))
        con.commit()
    except sqlite3.Error as ex:
        print("Ошибка при добавлении данных: ", ex)
    finally:
        con.close()


def populate_table_tracks():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    try:
        for i in range(100):
            cur.execute("INSERT INTO tracks (LastName, TrackLength, ReleaseDate) VALUES ( ?, ?, ?)",
                        (fake.last_name(), fake.random_int(min=120, max=360), fake.date(pattern='%d-%m-%Y')))
        con.commit()
    except sqlite3.Error as ex:
        print("Ошибка при добавлении данных: ", ex)
    finally:
        con.close()


if __name__ == "__main__":
    if not os.path.isfile("data.db"):
        create_table_customers()
        create_table_tracks()
        populate_table_customers()
        populate_table_tracks()
    app.run()
