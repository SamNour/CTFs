import inspect
import os
import re
import unittest
import sql_injection
import db_initialise as db
from backend import run_util as sifu

_outFileName = "tmp/test_.json"
_allResults = []


def _sifu_method_duplicate_removal(description, PassFail):
    return sifu.genSingleOutputFormat(originTool="unitTest",
                                      priority=10000,
                                      description=description,
                                      lineNumber=-1,
                                      fileName="test_.py",
                                      errorID=35,
                                      PassFail="PASS" if PassFail == True else "FAIL")


class TestSelectStudentSolution(unittest.TestCase):



    def test_select_student_solution(self) -> bool:
        method_code = inspect.getsource(sql_injection)

        ##################################
        PassFail = bool(re.compile(r"\s*WHERE\s* studNr\s* =\s* \?\s*").search(method_code)) and bool(re.compile(
            r"\(\s*studentNr\s*,\s*\)").search(method_code))
        finding = _sifu_method_duplicate_removal("sqlite injection is still possible... Sanitize your code ", PassFail)
        _allResults.append(finding)
        sifu.saveJSONFile(_outFileName, _allResults)
        ###################################

        self.assertTrue(PassFail)
        return PassFail
    def test_dbfile_exists(self):
        ###################################
        PassFail = os.path.exists("./school.db")
        finding = _sifu_method_duplicate_removal("Data base is corrupt!!, Donot perform any Transactions", PassFail)
        _allResults.append(finding)
        sifu.saveJSONFile(_outFileName, _allResults)
        ###################################
        self.assertTrue(PassFail)
        return PassFail

    def test_student_rows(self):
        count = db.cur.execute("""SELECT COUNT(*) FROM student""").fetchone()[0]
        ###################################
        PassFail = count == 14
        finding = _sifu_method_duplicate_removal("Do not alter the student table", PassFail)
        _allResults.append(finding)
        sifu.saveJSONFile(_outFileName, _allResults)
        ###################################
        self.assertEqual(count, 14)
        return PassFail

    def test_imports(self):
        PassFail = False
        db_module = inspect.getmembers(sql_injection)
        for mem in db_module:
            if "db_initialise" and "pprint" in mem:
                PassFail = True
        ###################################
        finding = _sifu_method_duplicate_removal("Do not remove the already given imports", PassFail)
        _allResults.append(finding)
        sifu.saveJSONFile(_outFileName, _allResults)
        ###################################
        self.assertTrue(PassFail)




    def test_method_exist_serve_image(self) -> bool:
        PassFail = hasattr(sql_injection, 'select_student') and \
                   callable(getattr(sql_injection, 'select_student'))
        finding = _sifu_method_duplicate_removal("Do not alter the Signature of select_student()", PassFail)
        _allResults.append(finding)
        sifu.saveJSONFile(_outFileName, _allResults)
        self.assertTrue(PassFail)
        return PassFail