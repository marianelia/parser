import clang.cindex
import typing
from serialize_func import DataFromFunc

def getFunction(node, result_func:DataFromFunc) -> DataFromFunc:
    result_func.setName(node.spelling)
    #result_func.name = node.spelling
    parent_node = node.lexical_parent

    while parent_node.kind == clang.cindex.CursorKind.NAMESPACE:
        result_func.setNamespace(parent_node.spelling)
        #result_func.namespace.append(parent_node.spelling)
        parent_node = parent_node.lexical_parent

    children_node = node.get_children()
    #getParam(children_node)
    
    return result_func

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



# def getNameNode(node):
#     kind = str(node.kind)[str(node.kind).index('.')+1:]
#     text_name = node.spelling or node.displayname 
#     return kind, text_name

# def getTypeInputArgs(node):
#     kind = str(node.kind)[str(node.kind).index('.')+1:]
#     text_type = node.type.spelling
#     return kind, text_type

# def printInfoNode(node):
#     if node.kind == clang.cindex.CursorKind.FUNCTION_DECL or node.kind == clang.cindex.CursorKind.PARM_DECL:
#         kind_name, text_name = getNameNode(node)
#         print('{} {}'.format(kind_name, text_name))
#         kind_type, text_type = getTypeInputArgs(node)
#         print('{} {}'.format(kind_type, text_type))
#         #print('lex perent {}'.format(node.lexical_parent.kind))
#     else:
#         kind, text = getNameNode(node)
#         print('{} {}'.format(kind, text))


# def filterByNodeFunctionsDecl(
#         nodes: typing.Iterable[clang.cindex.Cursor],
#         kinds: list
#     ):
#     #-> typing.Iterable[clang.cindex.Cursor]:
#     #result = []
#     for i in nodes:

#         if i.kind == clang.cindex.CursorKind.FUNCTION_DECL:
#             printInfoNode(i)
            
#         namespaces_children = i.get_children() 
#         for ns_child in namespaces_children:
#             printInfoNode(ns_child)

#             func_children = ns_child.get_children()

#             for f_child in func_children:
#                 printInfoNode(f_child)

#                 args__children = f_child.get_children()
#                 for arg_child in args__children:
#                     printInfoNode(arg_child)
                    
#     #return result