import sqlite3, pprint

new_con = sqlite3.connect("testing.db")
cur = new_con.cursor()

username = ("' OR TRUE; --",)
passwd = 12
arguments = ("' OR TRUE; --", 'Doe',)

fname = "' OR TRUE; --"
lname = 'Doe'
print(len(arguments))
# pprint.pprint(cur.execute('SELECT * FROM sqlite_master').fetchall())
# pprint.pprint(cur.execute( "SELECT * FROM student WHERE fname = '{}' AND lname='{}'".format(fname,lname)).fetchall())

pprint.pprint(cur.executemany("SELECT * FROM student WHERE fname = ? AND l"
                              "name= ?", [arguments]).fetchall())
"""
student(fname,lname,studID,grade)')
[('John', 'Doe', '1234', 'A'),
 ('Jane', 'Smith', '5678', 'B+'),
 ('Alex', 'Johnson', '9012', 'A-')]
"""
