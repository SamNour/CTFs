import inspect
import os
import re
import unittest
import ast

import astunparse
from backend import run_util as sifu

import tempfile_creation

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


with open("tempfile_creation.py", "r") as f:
    source = f.read()

tree = ast.parse(source)
for node in ast.walk(tree):
    if isinstance(node, ast.keyword):
        print(node)

print(astunparse.dump(tree))


class TestMktempArgs(unittest.TestCase):

    def test_imports(self):
        list_imports = ['tempfile']
        list_result = []
        for node in ast.walk(tree):
            if isinstance(node, ast.alias):
                node_id = node
                list_result.append(astunparse.unparse(node_id)[:-1])
        print(list_result)
        ###################################
        PassFail = set(list_imports).issubset(set(list_result))

        self.assertTrue(PassFail)

    def test_mkstemp_call(self):
        _, file_path = tempfile_creation.create_file()
        PassFail = False
        if os.path.commonprefix((os.path.realpath(file_path), os.getcwd())) == os.getcwd():
            PassFail = True

        ##################################
        finding = _sifu_method_duplicate_removal("You did not use the right method", PassFail)
        _allResults.append(finding)
        sifu.saveJSONFile(_outFileName, _allResults)
        ##################################
        self.assertTrue(PassFail, "The dir argument of mkstemp is incorrect.")

    def test_args_values(self) -> bool:
        PassFail = False
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == 'create_file':
                # Once we find the function definition, we iterate through the nodes in its body
                for stmt in node.body:
                    if isinstance(stmt, ast.Return):
                        # If the statement is a return statement, we extract the keywords and their values
                        keywords = {kw.arg: kw.value for kw in stmt.value.keywords}

                        # Now we can test each keyword's value
                        PassFail = keywords['suffix'].s == '.txt' and \
                                   keywords['prefix'].s == 'random_file' and \
                                   keywords['dir'].s == '.' and \
                                   isinstance(keywords['text'], ast.Constant) and \
                                   keywords['text'].value is True

                        ##################################
                        finding = _sifu_method_duplicate_removal(
                            "The mkstemp args_values are not correct"
                            , PassFail)
                        _allResults.append(finding)
                        sifu.saveJSONFile(_outFileName, _allResults)

                        ##################################
        self.assertTrue(PassFail)

    def test_mkstemp_args(self):
        PassFail = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and getattr(node.func, 'attr', '') == 'mkstemp':
                PassFail = all(kw.arg in ['suffix', 'prefix', 'dir', 'text'] for kw in node.keywords)
        ##################################
        finding = _sifu_method_duplicate_removal(
                                "The mkstemp function call has unexpected keyword arguments."
                                                 , PassFail)
        _allResults.append(finding)
        sifu.saveJSONFile(_outFileName, _allResults)
        ##################################
        self.assertTrue(PassFail)

    def test_number_args_number(self):
        PassFail = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and getattr(node.func, 'attr', '') == 'mkstemp':
                PassFail = len(node.keywords) ==  4
        ##################################
        finding = _sifu_method_duplicate_removal("The mkstemp function call does not have exactly 4 keyword arguments."
                                                 , PassFail)
        _allResults.append(finding)
        sifu.saveJSONFile(_outFileName, _allResults)
        ##################################
        self.assertTrue(PassFail)


if __name__ == '__main__':
    unittest.main()
"""
 def test_args_values(self) -> bool:
        PassFail = False
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == 'create_file':
                # Once we find the function definition, we iterate through the nodes in its body
                for stmt in node.body:
                    if isinstance(stmt, ast.Return):
                        # If the statement is a return statement, we extract the keywords and their values
                        keywords = {kw.arg: kw.value for kw in stmt.value.keywords}

                        # Now we can test each keyword's value
                        PassFail = keywords['suffix'].s == '.txt' and \
                                   keywords['prefix'].s == 'random_file' and \
                                   keywords['dir'].s, '.' and \
                                   isinstance(keywords['text'], ast.Constant) and \
                                   keywords['text'].value is True

                        ##################################
                        finding = _sifu_method_duplicate_removal(
                            "The mkstemp args_values are not correct"
                            , PassFail)
                        _allResults.append(finding)
                        sifu.saveJSONFile(_outFileName, _allResults)

                        ##################################
        print(bool(PassFail[1]))
        self.assertTrue(bool(PassFail[1]))
"""