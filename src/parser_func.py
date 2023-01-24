import clang.cindex
import typing
from serialize_func import DataFromFunc, DataFromStruct
from data_to_proto_format import Data
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

    def __getFunction(self, node) -> None:
        result_func:DataFromFunc = DataFromFunc()
        result_func.setName(node.spelling)
        result_func.setOutParamFromDecl(node.type.spelling)

        self.__getNamespaces(node.lexical_parent, result_func)

        self.__findInputParam(node, result_func)
        result_func.printForTests()
        self.__data.addDataFromFunc(result_func)

    def __getStruct(self, node) -> None:
        struct:DataFromStruct = DataFromStruct()
        print(node.spelling)
        
    # def __getClass(self, node) -> None:
    #     #print(node.spelling)
    #     pass

    def __findInputParam(self, node, result_func:DataFromFunc) -> None:
        input_params = node.get_children()
        for param in input_params:
            result_func.setInpParam(param.type.spelling, param.spelling) 
            # возможно нужен будет displayname

    def __findNodeFunction(self, node) -> None:
        if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            self.__getFunction(node)
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

        # if node.kind == clang.cindex.CursorKind.CLASS_DECL:
        #     self.__getClass(node)
        #     return

        if node.kind == clang.cindex.CursorKind.NAMESPACE:
            children_node = node.get_children()
            for child in children_node:
                self.__findNodeStruct(child)

    def __filterForStartDeclarations(self, nodes: typing.Iterable[clang.cindex.Cursor]):
        for node in nodes:
            self.__findNodeFunction(node)
            self.__findNodeStruct(node)
