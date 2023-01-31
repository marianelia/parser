import clang.cindex
import typing
from classes_for_tree import DataFromFunc, DataFromStruct, DataFromMethod, DataFromParam
from data import Data
import string

class Parser:
    def __init__(self) -> None:
        self.__data = Data()

    def parserTreeFromFile(self, file_name:string, args:list) -> None:
        index = clang.cindex.Index.create()
        translation_unit = index.parse(file_name, args=args)
        self.__filterForStartDeclarations(translation_unit.cursor.get_children())    

    #переделать после переписывания архитектуры
    def serializeDataToBinaryFile(self, path_to_file:string):
        self.__data.serializeData()

    def __getNamespaces(self, node, el_of_tree):
        while node.kind == clang.cindex.CursorKind.NAMESPACE:
            el_of_tree.setNamespace(node.spelling)
            node = node.lexical_parent

    def __getFunction(self, node) -> DataFromFunc:
        data_func = DataFromFunc()
        data_func.setName(node.spelling)
        data_func.setOutParamFromDecl(node.type.spelling)
        self.__getNamespaces(node.lexical_parent, data_func)
        self.__findInputParam(node, data_func)
        data_func.printForTests()
        return data_func

    def __getInfoFromFunctionNode(self, node) -> None:
        data_func = self.__getFunction(node)
        self.__data.addDataFromFunc(data_func)

    # def __getInfoFromMethodNode(self, node) -> None:
    #     data_func = self.__getFunction(node)

    def __getStruct(self, node) -> None:
        struct:DataFromStruct = DataFromStruct()
        struct.setName(node.spelling)
        self.__getNamespaces(node.lexical_parent, struct)
        self.__findMethod(node, struct)
        self.__findVariable(node, struct)
        struct.printForTests()
        self.__data.addDataFromStruct(struct)

    def __findMethod(self, node, struct:DataFromStruct) -> None: 
        children_node = node.get_children()
        for child in children_node:
            if child.kind == clang.cindex.CursorKind.CXX_METHOD:
                #пока без доступа
                struct.setMethod("", self.__getFunction(child))
        
    def __findVariable(self, node, struct:DataFromStruct) -> None:
        children_node = node.get_children()
        for child in children_node:
            if child.kind == clang.cindex.CursorKind.FIELD_DECL:
                #пока без доступа
                variable = DataFromParam()
                variable.setName(child.spelling)
                variable.setType(child.type.spelling)
                struct.setVariable("", variable)
        pass

    def __findInputParam(self, node, result_func:DataFromFunc) -> None:
        input_params = node.get_children()
        for param in input_params:
            result_func.setInpParam(param.type.spelling, param.spelling) 
            # возможно нужен будет displayname

    def __findNodeFunction(self, node) -> None:
        if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            self.__getInfoFromFunctionNode(node)
            return

        if node.kind == clang.cindex.CursorKind.NAMESPACE:
            children_node = node.get_children()
            for child in children_node:
                self.__findNodeFunction(child)
    
    def __findNodeStruct(self, node) -> None:
        if (node.kind == clang.cindex.CursorKind.STRUCT_DECL 
                or node.kind == clang.cindex.CursorKind.CLASS_DECL):
            self.__getStruct(node)
            return

        if node.kind == clang.cindex.CursorKind.NAMESPACE:
            children_node = node.get_children()
            for child in children_node:
                self.__findNodeStruct(child)

    def __filterForStartDeclarations(self, nodes: typing.Iterable[clang.cindex.Cursor]):
        for node in nodes:
            self.__findNodeFunction(node)
            self.__findNodeStruct(node)
