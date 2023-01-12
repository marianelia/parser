import clang.cindex
import typing
from serialize_func import DataFromFunc

def getFunction(node) -> None:
    result_func:DataFromFunc = DataFromFunc()
    result_func.setName(node.spelling)
    result_func.setOutParamFromDecl(node.type.spelling)
    parent_node = node.lexical_parent

    while parent_node.kind == clang.cindex.CursorKind.NAMESPACE:
        result_func.setNamespace(parent_node.spelling)
        parent_node = parent_node.lexical_parent

    findInputParam(node, result_func)
    result_func.printForTests()     #откуда-то в структуре появляется none
    

def findInputParam(node, result_func:DataFromFunc) -> None:
    input_params = node.get_children()
    for param in input_params:
        result_func.setInpParam(param.type.spelling, param.spelling) # возможно нужен будет displayname

def findNodeFunction(node):
    if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
        getFunction(node)
        return

    if node.kind == clang.cindex.CursorKind.NAMESPACE:
        children_node = node.get_children()
        for child in children_node:
            findNodeFunction(child)
    

def filterByNodeFunctionsDecl(
        nodes: typing.Iterable[clang.cindex.Cursor],
        kinds: list
    ):
    for node in nodes:
        findNodeFunction(node)
                    
    #return result
