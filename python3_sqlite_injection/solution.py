import db_initialise as db
import pprint

####################################################
#                 SOLUTION                         #
#               **  QMARK **                       #
####################################################
def select_student_solution(studentNr: str) -> None:
    pprint.pprint(db.cur.execute("""
    SELECT * 
    FROM student
    WHERE studNr = ?
    """, (studentNr,))
                  .fetchall())
### santiy checks
#pprint.pprint(select_student_solution("' OR TRUE; --"))


####################################################
#                 EXPLANATION                      #
####################################################

def select_student_print_query(studentNr: str) -> None:
    print("""
    SELECT * 
    FROM student
    WHERE studNr = '{0}'
    """.format(studentNr))

def select_student_solution_print_query(studentNr: str) -> None:
    print("""
    SELECT * 
    FROM student
    WHERE studNr = ?
    """, (studentNr,))


### Sanity checks
select_student_print_query("' OR TRUE; --")
select_student_solution_print_query("' OR TRUE; --")


####################################################
#                 Question                         #
#                                                  #
####################################################
def select_student(studentNr: str) -> None:
    pprint.pprint(db.cur.execute("""
    SELECT * 
    FROM student
    WHERE studNr = '{0}'
    """.format(studentNr)).fetchall())