import ast
import re
import astunparse
import unittest
import serve_image
from backend import run_util as sifu

_outFileName = "tmp/test_.json"
_allResults = []
tree = ast.parse(open("serve_image.py", "r").read())
""" FLASK_APP=serve_image.py flask run --port=6000"""#to actually run the app on port 6000, newer 
#version of FLASK, does not support port change from app.run()


def _sifu_method_duplicate_removal(description, PassFail):
    return sifu.genSingleOutputFormat(originTool="unitTest",
                                      priority=10000,
                                      description=description,
                                      lineNumber=-1,
                                      fileName="test_.py",
                                      errorID=35,
                                      PassFail="PASS" if PassFail == True else "FAIL")


class TestApp(unittest.TestCase):

    def setUp(self) -> None:
        # setup of app client
        self.app = serve_image.app.test_client()

    def test_var_app_exist(self) -> bool:
        PassFail = hasattr(serve_image, 'app')
        self.assertTrue(hasattr(serve_image, 'app'))
        finding = _sifu_method_duplicate_removal("Do not alter the appCLient name 'app'", PassFail)

        _allResults.append(finding)
        sifu.saveJSONFile(_outFileName, _allResults)
        self.assertTrue(PassFail)

        return PassFail

    def test_method_exist_serve_image(self) -> bool:
        PassFail = hasattr(serve_image, '_serve_image') and \
                   callable(getattr(serve_image, '_serve_image'))
        finding = _sifu_method_duplicate_removal("Do not alter the Signature of serve_image()", PassFail)
        _allResults.append(finding)
        sifu.saveJSONFile(_outFileName, _allResults)
        self.assertTrue(PassFail)
        return PassFail

    def test_404(self) -> bool:
        response = self.app.get("/image")
        ##################################
        PassFail = (response.status_code == 404)
        finding = _sifu_method_duplicate_removal("HTTP 404", PassFail)
        _allResults.append(finding)
        sifu.saveJSONFile(_outFileName, _allResults)
        ###################################
        self.assertEqual(response.status_code, 404)
        return PassFail

    def test_image_endpoint_unauthorized(self) -> bool:
        filename = '../.../../etc/passwd'
        response = self.app.get(f'/image?filename={filename}')
        ##################################
        PassFail = (response.status_code == 401)
        finding = _sifu_method_duplicate_removal("HTTP 401 - Un-authorized access", PassFail)
        _allResults.append(finding)
        sifu.saveJSONFile(_outFileName, _allResults)
        ###################################
        self.assertEqual(response.status_code, 401)
        return PassFail


                         #######################################
       #################       MOCK TESTING, AST             ##################
                        #######################################



    def test_main(self) -> bool:
        """
        Testing if main method exist
        """
        with open('serve_image.py') as f:
            module = ast.parse(f.read())
            print(astunparse.dump(module))
        has_main = False
        for node in module.body:
            if isinstance(node, ast.If) and isinstance(node.test, ast.Compare):
                if isinstance(node.test.left, ast.Name) and node.test.left.id == '__name__':
                    if len(node.test.ops) == 1 and isinstance(node.test.ops[0], ast.Eq):
                        if isinstance(node.test.comparators[0], ast.Str) and node.test.comparators[0].s == '__main__':
                            has_main = True
        ###################################
        PassFail = has_main
        finding = _sifu_method_duplicate_removal("Provided Imports shall not be altered", PassFail)
        _allResults.append(finding)
        sifu.saveJSONFile(_outFileName, _allResults)
        ###################################

        self.assertTrue( has_main, "The module does not contain an unaltered `if __name__ == '__main__':` block")
        return has_main

    def test_imports(self):
        list_imports = ['os', 'Flask', 'send_file', 'request']
        list_result = []
        for node in ast.walk(tree):
            if isinstance(node, ast.alias):
                node_id = node
                list_result.append(astunparse.unparse(node_id)[:-1])
        print(list_result)
        ###################################
        PassFail = set(list_imports).issubset(set(list_result))
        finding = _sifu_method_duplicate_removal("Provided Imports shall not be altered", PassFail)
        _allResults.append(finding)
        sifu.saveJSONFile(_outFileName, _allResults)
        ###################################
        self.assertTrue(PassFail)

    def test_arr_run_port_6000(self) -> bool:
        """
        Test that  app.run(debug=False, port=6000) exists with its parameters un-altered.
        spaces are tolerated inside the brackest and around "=", as showin in re
        """
        found = False
        pattern = r'app\.run\(\s*debug\s*=\s*False\s*,\s*port\s*=\s*6000\s*\)'
        for node in ast.walk(tree):
            if isinstance(node, ast.Expr):
                found_match = re.search(pattern, astunparse.unparse(node).strip())
                if found_match:
                    found = True
                else:
                    pass
        PassFail = found
        finding = _sifu_method_duplicate_removal("Dont alter the  app.run(debug=False, port=6000) function", PassFail)
        _allResults.append(finding)
        sifu.saveJSONFile(_outFileName, _allResults)
        self.assertTrue(found)
        return PassFail

    def test_complex_decorations(self) -> bool:
        """
        test the parameters of the annotaions of _serve_image
        """
        pattern = r"app\.route\(\s*'\/image'\s*\)"
        found = False
        result = [astunparse.unparse(node)[:-1] for node in ast.walk(tree) if isinstance(node, ast.Call)]

        for s in result:
            if re.search(pattern, s):
                found = True
                break
        PassFail = found
        finding = _sifu_method_duplicate_removal(
            "Decorators/Annotations should be left unchanged ", PassFail)
        _allResults.append(finding)
        sifu.saveJSONFile(_outFileName, _allResults)
        self.assertTrue(found, msg=f"Pattern {pattern} not found in list {result}")
        return PassFail
