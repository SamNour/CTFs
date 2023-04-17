import pprint
import sqlite3


con = sqlite3.connect("school.db")
cur = con.cursor()

def _commit():
    print("committing...")
    con.commit()


def _db_initialise():
    cur.execute("""
    CREATE TABLE student(fname CHAR, lname CHAR , studNr CHAR PRIMARY KEY, avg_grade CHAR)
    """)


def _insert_students():#studNr must be unique as it is the Primary Key
    entries = [
        ('John', 'Doe', '123456789', 'B'),
        ('Jane', 'Doe', '987654321', 'A'),
        ('Bob', 'Smith', '456789123', 'C'),
        ('Alice', 'Jones', '789123456', 'A'),
        ('Tom', 'Williams', '321654987', 'B'),
        ('Sara', 'Brown', '159753468', 'C'),
        ('Mike', 'Johnson', '357159246', 'B'),
        ('Emily', 'Davis', '246813579', 'A'),
        ('Jack', 'Taylor', '468135792', 'C'),
        ('Linda', 'Wilson', '852369741', 'B'),
        ('David', 'Martin', '741852963', 'A'),
        ('Karen', 'Clark', '963852741', 'B'),
        ('Peter', 'Walker', '654321987', 'C'),
        ('Sarah', 'Moore', '369852147', 'A')
    ]

    cur.executemany('INSERT INTO student VALUES (?,?,?,?)', entries)
def close():
    print("db closed...")
    cur.close()

#### sanity checks

# pprint.pprint(cur.execute("""SELECT * FROM student """).fetchall())





