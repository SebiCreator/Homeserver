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


def dbEasyAdd():
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
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
    cur.execute(statement)

    res = [x[0] for x in cur.fetchall()]
    print("STATEMENT RESULT")
    for idx,e in enumerate(res):
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
        print(e)


def new_unit(cur):
    name = input("Name:\t>> ")
    statement = "Insert into unit (name) values ('%s')" % name
    cur.execute(statement)
    select = "Select * from unit where unit.name = '%s'" % name
    for e in cur.execute(select):
        print(e)


def new_sensor(cur):
    typ = input("Typ:\t>> ")
    device = input("Device:\t>> ")
    unit = input("Unit:\t>> ")
    statement = "Insert into sensor values ('%s','%s','%s')"


def new_room(cur):
    app = create_app()
    name = input("Name:\t>> ")
    with app.app_context():
        r = Room(name=name)
        db.session.add(r)
        db.session.commit()
        print(r)


def new_Measure(con, sensor, value):
    app = create_app()
    with app.app_context():
        date = str(datetime.now())
        m = Measure(sensor=sensor, date=date, value=value)
        db.session.add(m)
        db.session.commit()
        print(m)

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
            elif opt == "quit" or opt == "q":
                print("Quit Database Configuration")
                return
    except KeyboardInterrupt:
        print("Quit Database Configuration")
        return