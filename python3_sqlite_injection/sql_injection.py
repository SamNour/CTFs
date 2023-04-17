import pprint

import db_initialise as db


def select_student(studentNr: str) -> None:
    pprint.pprint(db.cur.execute("""
    SELECT * 
    FROM student
    WHERE studNr = ?
    """, (studentNr,))
                  .fetchall())




select_student("' OR TRUE; --")




