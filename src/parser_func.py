import clang.cindex
import typing
from serialize_func import DataFromFunc
from data_to_proto_format import Data
import string

class Parser:
    def __init__(self) -> None:
        self.__data = Data()
        pass

    def parserTreeFromFile(self, file_name:string, args:list) -> None:
        index = clang.cindex.Index.create()
        translation_unit = index.parse(file_name, args=args)
        self.__filterForStartDeclarations(translation_unit.cursor.get_children())    

    def __getFunction(self, node) -> None:
        result_func:DataFromFunc = DataFromFunc()
        result_func.setName(node.spelling)
        result_func.setOutParamFromDecl(node.type.spelling)
        parent_node = node.lexical_parent

        while parent_node.kind == clang.cindex.CursorKind.NAMESPACE:
            result_func.setNamespace(parent_node.spelling)
            parent_node = parent_node.lexical_parent

        self.__findInputParam(node, result_func)
        result_func.printForTests()
        self.__data.addDataFromFunc(result_func)

    def __findInputParam(self, node, result_func:DataFromFunc) -> None:
        input_params = node.get_children()
        for param in input_params:
            result_func.setInpParam(param.type.spelling, param.spelling) # возможно нужен будет displayname

    def __findNodeFunction(self, node) -> None:
        if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            self.__getFunction(node)
            return

        if node.kind == clang.cindex.CursorKind.NAMESPACE:
            children_node = node.get_children()
            for child in children_node:
                self.__findNodeFunction(child)
    

    def __filterForStartDeclarations(self, nodes: typing.Iterable[clang.cindex.Cursor]):
        for node in nodes:
            self.__findNodeFunction(node)


    def serializeDataToBinaryFile(self, path_to_file:string):
        self.__data.serializeData()
