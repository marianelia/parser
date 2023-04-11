import pytest
import sys
import pathlib
sys.path.append(str(pathlib.Path(sys.path[0]).resolve().parent / "src"))
from parser_tree import Parser
from data import Data
from classes_for_tree import Access, DataFromParam, DataFromVariable, DataFromFunc, DataFromMethod, DataFromStruct


def test1_serialize_func():
    path_to_verification_file = "/home/maria/diploma/parser/tests/test1_bin"
    data = Data(file_name=[path_to_verification_file])
    # data.file_names(path_to_verification_file)
    data_func = DataFromFunc(namespaces = ["namespace1", "namespace2", "namespace3"], 
                             name = "test2_func_with_param", output_param = "int")
    data_func.set_inp_params("const int", "param")
    data.add_data_from_func(data_func)

    serializing = Parser()
    serializing.add_data_to_list(data)
    serializing.serialize_data_to_binary_file("./tmp_test1")

    with open(path_to_verification_file, mode="wb") as file:
            serializing_string = file.read()
    with open("/home/maria/diploma/parser/testcases/tmp_test1", mode="wb") as file:
            test_string = file.read()
    
    assert test_string == serializing_string


if __name__ == '__main__':
    pytest.main(["-q", "-s", "/home/maria/diploma/parser/testcases/test_01_parse_file.py"])