import clang.cindex
import typing
from serialize_func import DataFromFunc

def getFunction(node, result_func:DataFromFunc) -> DataFromFunc:
    result_func.setName(node.spelling)
    result_func.setOutParamFromDecl(node.type.spelling)
    parent_node = node.lexical_parent

    while parent_node.kind == clang.cindex.CursorKind.NAMESPACE:
        result_func.setNamespace(parent_node.spelling)
        parent_node = parent_node.lexical_parent

    findInputParam(node, result_func)    
    return result_func

def findInputParam(node, result_func:DataFromFunc) -> None:
    input_params = node.get_children()
    for param in input_params:
        result_func.setInpParam(param.type.spelling, param.spelling) # возможно нужен будет displayname

def findNodeFunction(node, result_func:DataFromFunc):
    if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
        getFunction(node, result_func)
        return

    if node.kind == clang.cindex.CursorKind.NAMESPACE:
        children_node = node.get_children()
        for child in children_node:
            findNodeFunction(child, result_func)
    


def filterByNodeFunctionsDecl(
        nodes: typing.Iterable[clang.cindex.Cursor],
        kinds: list,
        result_func:DataFromFunc
    ):
    for node in nodes:
        findNodeFunction(node, result_func)
                    
    #return result
