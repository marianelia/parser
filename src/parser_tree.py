import clang.cindex
import typing
from classes_for_tree import *
from data import Data
import code_data_pb2

class Parser:
    def __init__(self, data_from_files = []):
        self.__data_from_files :list[Data] = data_from_files

    @property
    def data_from_files(self) -> list:
        return self.__data_from_files

    def parser_tree_from_file(self, file_name:str, args:list) -> None:
        index = clang.cindex.Index.create()
        translation_unit = index.parse(file_name, args=args,
                                       options=clang.cindex.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES |
                                       clang.cindex.TranslationUnit.PARSE_INCOMPLETE)
        data = Data()
        data.file_name = file_name
        self.__data_from_files.append(data)
        self.__filter_for_start_declarations(translation_unit.cursor.get_children(), file_name)    

    #переделать после переписывания архитектуры
    def serialize_data_to_binary_file(self, path_to_file:str):
        project_obj = code_data_pb2.Project()
        for i in range(len(self.__data_from_files)):
            file_obj = project_obj.files.add()
            self.__data_from_files[i].serialize_data_one_file(file_obj)

        serialize_to_string = project_obj.SerializeToString()
        self.put_data_to_file(path_to_file, serialize_to_string)
        # print(serialize_to_string)
        project_obj.ParseFromString(serialize_to_string)
        print(project_obj)


    def put_data_to_file(self, file_name:str, data:str):
        with open(file_name, mode="wb") as file:
            file.write(data)
        #file.closed

    def add_data_to_list(self, data:Data):
        self.__data_from_files.append(data)

    def __find_namespaces(self, node, el_of_tree):
        del el_of_tree.namespaces
        while node.kind == clang.cindex.CursorKind.NAMESPACE:
            el_of_tree.set_namespace(node.spelling)
            node = node.lexical_parent
        el_of_tree.arrange_namespaces()

    def __get_function(self, node) -> DataFromFunc:
        data_func = DataFromFunc()
        data_func.name = node.spelling
        data_func.set_out_param_from_decl(node.type.spelling)
        self.__find_namespaces(node.lexical_parent, data_func)
        self.__find_input_param(node, data_func)
        data_func.print_for_tests()
        return data_func

    def __get_info_from_function_node(self, node) -> None:
        data_func = self.__get_function(node)
        self.__data_from_files[-1].add_data_from_func(data_func)
        
        # del data_func.namespaces
        del data_func

    def __find_constructor_by_struct(self, node, struct) -> None:
        children_node = node.get_children()
        for child in children_node:
            if (child.kind == clang.cindex.CursorKind.CONSTRUCTOR):
                #print(child.spelling)
                struct.constructor = self.__get_function(child)


    def __get_struct(self, node, defult_access) -> None:
        struct:DataFromStruct = DataFromStruct()
        struct.access = defult_access
        struct.name = node.spelling 
        self.__find_namespaces(node.lexical_parent, struct)
        self.__find_method(node, struct)
        self.__find_variable(node, struct)
        self.__find_constructor_by_struct(node, struct)
        struct.print_for_tests()
        self.__data_from_files[-1].add_data_from_struct(struct)
        #del struct

    def __find_access(self, node) -> Access:
        if node.access_specifier == clang.cindex.AccessSpecifier.PUBLIC:
            return Access.PUBLIC
        elif node.access_specifier == clang.cindex.AccessSpecifier.PROTECTED:
            return Access.PROTECTED
        elif node.access_specifier == clang.cindex.AccessSpecifier.PRIVATE:
            return Access.PRIVATE

    def __find_method(self, node, struct:DataFromStruct) -> None: 
        curr_access = struct.access
        children_node = node.get_children()
        for child in children_node:
            if child.kind == clang.cindex.CursorKind.CXX_ACCESS_SPEC_DECL:
                curr_access = self.__find_access(child)

            if child.kind == clang.cindex.CursorKind.CXX_METHOD:
                func = self.__get_function(child)
                struct.set_method(curr_access, func)
                del func.namespaces
        
    def __find_variable(self, node, struct:DataFromStruct) -> None:
        curr_access = struct.access
        children_node = node.get_children()
        for child in children_node:
            if child.kind == clang.cindex.CursorKind.CXX_ACCESS_SPEC_DECL:
                curr_access = self.__find_access(child)
            if child.kind == clang.cindex.CursorKind.FIELD_DECL:
                variable = DataFromParam(child.spelling, child.type.spelling)
                struct.set_variable(curr_access, variable)
        

    def __find_input_param(self, node, result_func:DataFromFunc) -> None:
        del result_func.inp_params
        input_params = node.get_children()
        for param in input_params: 
            if param.kind == clang.cindex.CursorKind.PARM_DECL:
                result_func.set_inp_params(param.type.spelling, param.spelling)
                # возможно нужен будет displayname

    def __find_node_function(self, node) -> None:
        if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            self.__get_info_from_function_node(node)
            return

        if node.kind == clang.cindex.CursorKind.NAMESPACE:
            children_node = node.get_children()
            for child in children_node:
                self.__find_node_function(child)
    
    def __find_node_struct(self, node) -> None:
        if (node.kind == clang.cindex.CursorKind.STRUCT_DECL):
            self.__get_struct(node, Access.PUBLIC)
            return
        if (node.kind == clang.cindex.CursorKind.CLASS_DECL):
            self.__get_struct(node, Access.PRIVATE)
            return

        if node.kind == clang.cindex.CursorKind.NAMESPACE:
            children_node = node.get_children()
            for child in children_node:
                self.__find_node_struct(child)

    def __filter_for_start_declarations(self, nodes: typing.Iterable[clang.cindex.Cursor], file_name):
        for node in nodes:
            if node.location.file.name == file_name:
                self.__find_node_function(node)
                self.__find_node_struct(node)
