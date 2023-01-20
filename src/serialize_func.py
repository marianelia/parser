# import code_data_pb2
import string

class DataFromParam:
    def __init__(self) -> None:
        self.__name :string
        self.__type :string
        pass

    def setName(self, name:string) -> None:
        self.__name = name
    
    def setType(self, type:string) -> None:
        self.__type = type

    def getName(self) -> string:
        return self.__name
    
    def getType(self) -> string:
        return self.__type

    def printForTests(self)-> None:
        print(self.__name)
        print(self.__type)



class DataFromFunc:
    def __init__(self) -> None:
        self.__namespaces :list = []
        self.__name :string
        self.__output_param :string
        self.__list_input_params :list[DataFromParam] = []
        pass

    def setNamespace(self, ns:string) -> None:
        self.__namespaces.append(ns)

    def setName(self, name:string) -> None:
        self.__name = name

    def setOutParam(self, out_param:string) -> None:
        self.__output_param = out_param

    def setOutParamFromDecl(self, out_param:string) -> None:
        self.__output_param = out_param.partition(' (')[0] #DELETE space after type???

    def setInpParam(self, inp_type:string, inp_name:string) -> None:
        input_params :DataFromParam = DataFromParam()
        input_params.setType(inp_type)
        input_params.setName(inp_name)
        self.__list_input_params.append(input_params)

    def getNamespaces(self) -> list:
        return self.__namespaces

    def getName(self) -> string:
        return self.__name

    def getOutParam(self) -> string:
        return self.__output_param

    def getInpParams(self) -> list:
        return self.__list_input_params

    def getInpParam(self, index:int) -> DataFromParam:
        return self.__list_input_params[index]


    def printForTests(self) -> None:
        print(self.__namespaces)
        print(self.__name)
        print(self.__output_param)
        for num_inp_param in range(len(self.__list_input_params)):
            self.__list_input_params[num_inp_param].printForTests()




# if __name__ == '__main__':
#     function_decl = code_data_pb2.Function()
#     print(type(function_decl))

#     ns = function_decl.namespace.extend(["std", "std1"])
#     function_decl.name = "func"
#     function_decl.output_param = "int"

#     serializeToString = function_decl.SerializeToString()
#     print(serializeToString,type(serializeToString))
#     # to file
#     function_decl.ParseFromString(serializeToString)
#     print(function_decl)