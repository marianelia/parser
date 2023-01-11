import code_data_pb2
import string

class DataFromFunc:
    def __init__(self) -> None:
        self.namespace :list = []
        self.name :string
        self.output_param :string
        self.input_params :DataFromParam
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
        self.input_params.setType(inp_type)
        self.input_params.setName(inp_name)

    def printForTests(self):
        print(self.namespace)
        print(self.name)
        print(self.output_param)
        print(self.input_params.printForTests())


class DataFromParam:
    def __init__(self) -> None:
        self.name :string
        self.type :string
        pass

    def setName(self, name:string) -> None:
        self.name = name
    
    def setType(self, type:string) -> None:
        self.type = type

    def printForTests(self):
        print(self.name)
        print(self.type)




# function_decl = code_data_pb2.Function()
# function_decl.file_name = "a.h"
# #ns = function_decl.namespace.add()
# #ns = "std"
# #ns1 = function_decl.namespace.add()
# #ns1 = "std1"
# function_decl.name = "func"
# function_decl.output_param = "int"

# serializeToString = function_decl.SerializeToString()
# print(serializeToString,type(serializeToString))
# # to file
# function_decl.ParseFromString(serializeToString)
