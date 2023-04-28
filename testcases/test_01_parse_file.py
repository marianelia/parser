import pytest
import sys
import pathlib
sys.path.append(str(pathlib.Path(sys.path[0]).resolve().parent / "src"))
from parser_tree import Parser
from data import Data
from classes_for_tree import Access, DataFromParam, DataFromVariable, DataFromFunc, DataFromMethod, DataFromStruct


def test1_serialize_func():
    path_to_verification_file = "/home/maria/diploma/parser/tests/test1_bin"
    path_to_test_file = "/home/maria/diploma/parser/testcases/tmp_test1"
    path_to_source_file = "/home/maria/diploma/parser/tests/test1_func.hpp"
    data = Data(file_name=path_to_source_file)
    data_func = DataFromFunc(name = "test1_func", output_param = "void")
    data_func.set_inp_params("long long", "param1")
    data_func.set_inp_params("double", "param2")
    data_func.set_inp_params("int", "param3")
    data.add_data_from_func(data_func)

    serializing = Parser()
    serializing.add_data_to_list(data)
    serializing.serialize_data_to_binary_file(path_to_test_file)

    with open(path_to_verification_file, mode="rb") as file:
            serializing_string = file.read()
    with open(path_to_test_file, mode="rb") as file:
            test_string = file.read()
    
    assert test_string == serializing_string, '{0} != {1}'.format(test_string, serializing_string)


# def test2_serialize_func():
#     path_to_verification_file = "/home/maria/diploma/parser/tests/test2_bin"
#     path_to_test_file = "/home/maria/diploma/parser/testcases/tmp_test2"
#     path_to_source_file = "/home/maria/diploma/parser/tests/test2_func.hpp"
#     data = Data(file_name=path_to_source_file)
#     data_func = DataFromFunc(namespaces = ["namespace1", "namespace2", "namespace3"], 
#                              name = "test2_func_with_param", output_param = "int")
#     data_func.set_inp_params("const int", "param")
#     data.add_data_from_func(data_func)

#     data_func = DataFromFunc(namespaces = ["namespace1"], 
#                              name = "test2_func_without_param", output_param = "long long")
#     data.add_data_from_func(data_func)

#     serializing = Parser()
#     serializing.add_data_to_list(data)
#     serializing.serialize_data_to_binary_file(path_to_test_file)

#     with open(path_to_verification_file, mode="rb") as file:
#             serializing_string = file.read()
#     with open(path_to_test_file, mode="rb") as file:
#             test_string = file.read()
    
#     assert test_string == serializing_string, '{0} != {1}'.format(test_string, serializing_string)

def get_data_from_func() -> DataFromFunc:
    inp_param1 = DataFromParam("long long", "p1")
    inp_param2 = DataFromParam("bool", "p2")
    inp_param3 = DataFromParam("int", "p3")
    inp_param4 = DataFromParam("double", "p4")
      
    data_func = DataFromFunc(["namespace1", "namespace2", "namespace3"], "tes3_func", 
                             "void", [inp_param1, inp_param2, inp_param3, inp_param4])
    return data_func

def get_data_from_struct() -> DataFromStruct:

    return  DataFromStruct(["namespace1", "namespace2"], "tes4_struct", Access.PUBLIC)


def test3_get_data_from_func():
    data_func = get_data_from_func()
    data_func.print_for_tests()
# !!!

def test4_arrange_namespaces_for_func():
      data_func = get_data_from_func()
      data_func.arrange_namespaces()
      assert data_func.namespaces == ["namespace3", "namespace2", "namespace1"]

def test5_arrange_namespaces_for_struct():
      data_struct = get_data_from_struct()
      data_struct.arrange_namespaces()
      assert data_struct.namespaces == ["namespace2", "namespace1"]

def test6_add_to_data():
    data = Data()
    data.add_data_from_func(get_data_from_func())
    data.add_data_from_struct(get_data_from_struct())


if __name__ == '__main__':
    pytest.main(["-q", "-v", "-s", "/home/maria/diploma/parser/testcases/test_01_parse_file.py"])