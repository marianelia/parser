import code_data_pb2
import string

class DataFromFunc:
    def __init__(self) -> None:
        self.namespace :list = []
        self.name :string
        self.output_param :string
        self.list_input_params :list[DataFromParam] = []
        pass

    def setNamespace(self, ns:string) -> None:
        self.namespace.append(ns)

    def setName(self, name:string) -> None:
        self.name = name

    def setOutParam(self, out_param:string) -> None:
        self.output_param = out_param

    def setOutParamFromDecl(self, out_param:string) -> None:
        self.output_param = out_param.partition('(')[0] #DELETE space after type???

    def setInpParam(self, inp_type:string, inp_name:string) -> None:
        input_params :DataFromParam = DataFromParam()
        input_params.setType(inp_type)
        input_params.setName(inp_name)
        self.list_input_params.append(input_params)

    def printForTests(self) -> None:
        print(self.namespace)
        print(self.name)
        print(self.output_param)
        for num_inp_param in range(len(self.list_input_params)):
            self.list_input_params[num_inp_param].printForTests()


class DataFromParam:
    def __init__(self) -> None:
        self.name :string
        self.type :string
        pass

    def setName(self, name:string) -> None:
        self.name = name
    
    def setType(self, type:string) -> None:
        self.type = type

    def printForTests(self)-> None:
        print(self.name)
        print(self.type)



if __name__ == '__main__':
    function_decl = code_data_pb2.Function()
    function_decl.file_name = "a.h"
    ns = function_decl.namespace.extend(["std", "std1"])
    function_decl.name = "func"
    function_decl.output_param = "int"

    serializeToString = function_decl.SerializeToString()
    print(serializeToString,type(serializeToString))
    # to file
    function_decl.ParseFromString(serializeToString)
    print(function_decl)