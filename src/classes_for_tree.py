# import code_data_pb2
import string
from enum import Enum 


class Access(Enum):
    PUBLIC = 1
    PROTECTED = 2
    PRIVATE = 3
    NONE = 4


class DataFromParam:
    def __init__(self) -> None:
        self.__name :string
        self.__type :string

    def set_name(self, name:string) -> None:
        self.__name = name
    
    def set_type(self, type:string) -> None:
        self.__type = type

    def get_name(self) -> string:
        return self.__name
    
    def get_type(self) -> string:
        return self.__type

    def print_for_tests(self)-> None:
        print(self.__name)
        print(self.__type)

class DataFromVariable:
    def __init__(self, access: Access, param : DataFromParam) -> None:
        self.__access :Access = access
        self.__variable :DataFromParam = param

    def get_access(self) -> Access:
        return self.__access

    def get_variable(self) -> DataFromParam:
        return self.__variable

    def print_for_tests(self)-> None:
        print(self.__access)
        self.__variable.print_for_tests()

class DataFromFunc:
    def __init__(self) -> None:
        self.__namespaces :list = []
        self.__name :string
        self.__output_param :string
        self.__list_input_params :list[DataFromParam] = []

    def set_namespace(self, ns:string) -> None:
        self.__namespaces.append(ns)

    def set_name(self, name:string) -> None:
        self.__name = name

    def set_out_param(self, out_param:string) -> None:
        self.__output_param = out_param

    def set_out_param_from_decl(self, out_param:string) -> None:
        self.__output_param = out_param.partition(' (')[0]

    def set_inp_param(self, inp_type:string, inp_name:string) -> None:
        input_params :DataFromParam = DataFromParam()
        input_params.set_type(inp_type)
        input_params.set_name(inp_name)
        self.__list_input_params.append(input_params)

    def get_namespaces(self) -> list:
        return self.__namespaces

    def get_name(self) -> string:
        return self.__name

    def get_out_param(self) -> string:
        return self.__output_param

    def get_inp_params(self) -> list:
        return self.__list_input_params

    def get_inp_param(self, index:int) -> DataFromParam:
        return self.__list_input_params[index]

    def print_for_tests(self) -> None:
        print(self.__namespaces)
        print(self.__name)
        print(self.__output_param)
        for num_inp_param in range(len(self.__list_input_params)):
            self.__list_input_params[num_inp_param].print_for_tests()


class DataFromMethod:
    def __init__(self, access: Access, func : DataFromFunc) -> None:
        self.__access :Access = access
        self.__function :DataFromFunc = func

    def get_access(self) -> Access:
        return self.__access

    def get_function(self) -> DataFromFunc:
        return self.__function
        
    def print_for_tests(self)-> None:
        print(self.__access)
        self.__function.print_for_tests()


class DataFromStruct:
    def __init__(self) -> None:
        self.__namespaces :list = []
        self.__name :string
        self.__default_access :Access = Access.NONE
        self.__list_methods :list[DataFromMethod] = []
        self.__list_variable :list[DataFromVariable] = []

    def set_access(self,access:Access) -> None:
        self.__default_access = access

    def get_access(self) -> Access:
        return self.__default_access
    
    def set_namespace(self, ns:string) -> None:
        self.__namespaces.append(ns)

    def set_name(self, name:string) -> None:
        self.__name = name

    def get_name(self) -> string:
        return self.__name
    
    def get_namespaces(self) -> list:
        return self.__namespaces

    def set_method(self, access:string, func:DataFromFunc) -> None:
        method :DataFromMethod = DataFromMethod(access, func)
        self.__list_methods.append(method)

    def get_methods(self) -> list:
        return self.__list_methods

    def get_method_by_index(self, index:int) -> DataFromMethod:
        return self.__list_methods[index]


    def set_variable(self, access:string, var:DataFromParam) -> None:
        variable :DataFromVariable = DataFromVariable(access, var)
        self.__list_variable.append(variable)

    def get_variable(self) -> list:
        return self.__list_variable

    def get_variable_by_index(self, index:int) -> DataFromVariable:
        return self.__list_variable[index]

    def print_for_tests(self)-> None:
        print(self.__namespaces)
        print(self.__name)
        
        for num_method in range(len(self.__list_methods)):
            self.__list_methods[num_method].print_for_tests()

        for num_var in range(len(self.__list_variable)):
            self.__list_variable[num_var].print_for_tests()