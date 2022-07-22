from datetime import datetime
from re import I
import sqlite3


DATABASE_PATH = "/Users/sebastiankaeser/Desktop/Coding/Python/Homeserver/WebInterface/database.db"


def finput(msg):
    return str(input("%s\n>> " % msg))


def getTables(cur):
    t = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [x[0] for x in cur.fetchall()]
    return ("CURRENT TABLES:\t" + str(tables))


def getIDMax(cur, table):
    statement = "SELECT MAX(id) from %s" % table
    try:
        cur.execute(statement)
    except sqlite3.OperationalError:
        print("Error in IDMax occured")
        return None
    return int(cur.fetchall()[0][0])


def dbEasyAdd():
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    getIDMax(cur, "sensor")
    print(getTables(cur))
    table = finput("Which table do you want to add something?")
    if table == 'sensor':
        new_sensor(con)
    elif table == 'unit':
        new_unit(con)
    elif table == 'device':
        new_device(con)
    elif table == 'room':
        new_room(con)
    elif table == 'measurement':
        print("Please dont add measurements manually (use mechanism)!")
    else:
        print("No table named %s" % table)
    con.commit()
    con.close()


def addStatement():
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()

    statement = finput("Bitte SQL-Statement angeben:")
    try:
        cur.execute(statement)
    except sqlite3.OperationalError:
        print("Bad Statement, please try again")
        return

    res = [x[0] for x in cur.fetchall()]
    print("STATEMENT RESULT")
    for idx, e in enumerate(res):
        print("[%s]\t%s" % (idx, e))

    con.commit()
    con.close()


def new_device(cur):
    name = input("Name:\t>> ")
    room = input("Room:\t>> ")
    ip = input("IP:\t>> ")
    port = input("Port:\t>> ")
    statement = "Insert into device values ('%s','%s','%s','%s')" % (
        name, room, ip, port)
    cur.execute(statement)
    select = "Select * from device where device.name ='%s'" % name
    for e in cur.execute(select):
        print(e[0])


def new_user(cur):
    next_id = getIDMax(cur, "user") + 1
    first_name = finput("First Name:")
    email = finput("Name:")
    password = finput("Password:")

    statement = "Insert into user values ('%s','%s','%s','%s')" % (
        next_id, first_name, email, password)
    
    cur.execute(statement)
    select = "Select * from user where user.id = '%s'" % next_id
    for e in cur.excecute(select):
        print(e[0])


def new_unit(cur):
    name = input("Name:\t>> ")
    statement = "Insert into unit (name) values ('%s')" % name
    cur.execute(statement)
    select = "Select * from unit where unit.name = '%s'" % name
    for e in cur.execute(select):
        print(e[0])


def new_sensor(cur):
    next_id = getIDMax(cur, "sensor") + 1
    typ = input("Typ:\t>> ")
    device = input("Device:\t>> ")
    unit = input("Unit:\t>> ")
    statement = "Insert into sensor values ('%s','%s','%s','%s')" % (
        next_id, typ, device, unit)
    cur.execute(statement)
    select = "Select * from sensor where sensor.id = '%s'" % next_id
    for e in cur.execute(select):
        print(e[0])


def new_room(cur):
    name = input("Name:\t>> ")
    statement = "Insert into room values ('%s')" % name
    cur.execute(statement)
    select = "Select * from room where room.name = '%s'" % name
    for e in cur.execute(select):
        print(e[0])


def new_Measure(cur, sensor, value):
    next_id = getIDMax(cur, "measure") + 1
    date = str(datetime.now())
    statement = "Insert into measure values ('%s','%s','%s','%s','%s')" % (
        next_id, sensor, date, value
    )
    cur.execute(statement)
    select = "Select * form measure where measure.id = '%s'" % next_id
    for e in cur.execute(select):
        print(e[0])


def options():
    print("statement\t -> execute SQL Statement")
    print("easyAdd\t -> easy table adding")
    print("quit or q or ^C -> back to mainloop")


def databaseConfigLoop():
    try:
        while 1:
            opt = finput("Which option")
            if opt == "statement":
                addStatement()
            elif opt == "easyAdd":
                dbEasyAdd()
            elif opt == "help" or opt == "h":
                options()
            elif opt == "quit" or opt == "q":
                print("Quit Database Configuration")
                return
    except KeyboardInterrupt:
        print("Quit Database Configuration")
        return
