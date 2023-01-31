# import code_data_pb2
import string

class DataFromParam:
    def __init__(self) -> None:
        self.__name :string
        self.__type :string

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

class DataFromVariable:
    def __init__(self, access: string, param : DataFromParam) -> None:
        self.__access :string = access
        self.__variable :DataFromParam = param

    def printForTests(self)-> None:
        print(self.__access)
        self.__variable.printForTests()

class DataFromFunc:
    def __init__(self) -> None:
        self.__namespaces :list = []
        self.__name :string
        self.__output_param :string
        self.__list_input_params :list[DataFromParam] = []

    def setNamespace(self, ns:string) -> None:
        self.__namespaces.append(ns)

    def setName(self, name:string) -> None:
        self.__name = name

    def setOutParam(self, out_param:string) -> None:
        self.__output_param = out_param

    def setOutParamFromDecl(self, out_param:string) -> None:
        self.__output_param = out_param.partition(' (')[0]

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


class DataFromMethod:
    def __init__(self, access: string, func : DataFromFunc) -> None:
        self.__access :string = access
        self.__function :DataFromFunc = func

    def getAccess(self) -> string:
        return self.__access

    def getFunction(self) -> DataFromFunc:
        return self.__function
        
    def printForTests(self)-> None:
        print(self.__access)
        self.__function.printForTests()


class DataFromStruct:
    def __init__(self) -> None:
        self.__namespaces :list = []
        self.__name :string
        self.__list_methods :list[DataFromMethod] = []
        self.__list_variable :list[DataFromVariable] = []
    
    def setNamespace(self, ns:string) -> None:
        self.__namespaces.append(ns)

    def setName(self, name:string) -> None:
        self.__name = name

    def getName(self) -> string:
        return self.__name
    
    def getNamespaces(self) -> list:
        return self.__namespaces

    def setMethod(self, access:string, func:DataFromFunc) -> None:
        method :DataFromMethod = DataFromMethod(access, func)
        self.__list_methods.append(method)

    def getMethods(self) -> list:
        return self.__list_methods

    def getMethodByIndex(self, index:int) -> DataFromMethod:
        return self.__list_methods[index]


    def setVariable(self, access:string, var:DataFromVariable) -> None:
        variable :DataFromVariable = DataFromVariable(access, var)
        self.__list_variable.append(variable)

    def getVariable(self) -> list:
        return self.__list_variable

    def getVariableByIndex(self, index:int) -> DataFromVariable:
        return self.__list_variable[index]

    def printForTests(self)-> None:
        print(self.__namespaces)
        print(self.__name)
        
        for num_method in range(len(self.__list_methods)):
            self.__list_methods[num_method].printForTests()

        for num_var in range(len(self.__list_variable)):
            self.__list_variable[num_var].printForTests()