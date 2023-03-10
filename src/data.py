from classes_for_tree import *
import code_data_pb2

class Data:
    def __init__(self) -> None:
        self.__list_data_func :list[DataFromFunc] = []
        self.__list_data_struct :list[DataFromStruct] = []
        #...

    def add_data_from_func(self, data:DataFromFunc) -> None:
        self.__list_data_func.append(data)
    
    def add_data_from_struct(self, data:DataFromStruct) -> None:
        self.__list_data_struct.append(data)

    def serialize_data(self, path_to_output_file:str):
        file_obj = code_data_pb2.File()
        #file.file_name = ..  
        for num_data_func in range(len(self.__list_data_func)):
            func_obj = file_obj.function_list.add()
            self.serialize_func(func_obj, self.__list_data_func[num_data_func])

        for num_data_struct in range(len(self.__list_data_struct)):
            struct_obj = file_obj.struct_list.add()
            self.serialize_struct(struct_obj, self.__list_data_struct[num_data_struct])

        serialize_to_string = file_obj.SerializeToString()
        self.serialize_data_to_file(path_to_output_file + "test", serialize_to_string)
        print(serialize_to_string)
        file_obj.ParseFromString(serialize_to_string)
        print(file_obj)

    def serialize_data_to_file(self, file_name:str, data:str):
        with open(file_name, mode="wb") as file:
            file.write(data)
        #file.closed

    def serialize_struct(self, struct_proto_format, struct:DataFromStruct):
        #struct.print_for_tests()
        struct_proto_format.namespace.extend(struct.get_namespaces())
        struct_proto_format.name = struct.get_name()

        for num_method in range(len(struct.get_methods())):
            method_obj = struct_proto_format.methods.add()
            self.serialize_method(method_obj, struct.get_method_by_index(num_method))

        for num_var in range(len(struct.get_variable())):
            var_obj = struct_proto_format.variables.add()
            self.serialize_variable(var_obj, struct.get_variable_by_index(num_var))


    def enum_access_to_protobuf(self, access:Access):
        if (access == Access.PUBLIC):
            return code_data_pb2.PUBLIC

        if (access == Access.PRIVATE):
            return code_data_pb2.PRIVATE

        if (access == Access.PROTECTED):
            return code_data_pb2.PROTECTED
        return None

    def serialize_variable(self, var_proto_format, var:DataFromVariable):
        var_proto_format.access = self.enum_access_to_protobuf(var.access)
        self.serialize_input_params(var_proto_format.variable, var.variable)
    
    def serialize_method(self, method_proto_format, method:DataFromMethod):
        method_proto_format.access = self.enum_access_to_protobuf(method.get_access())
        self.serialize_func(method_proto_format.function, method.get_function())        

    def serialize_func(self, func_proto_format, func:DataFromFunc):
        func_proto_format.namespace.extend(func.namespaces)
        func_proto_format.name = func.name
        func_proto_format.output_param = func.get_out_param()
        for num_inp_param in range(len(func.get_inp_params())):
            inp_param_obj = func_proto_format.input_params.add()
            self.serialize_input_params(inp_param_obj, func.get_inp_param(num_inp_param))

    def serialize_input_params(self, param_proto_format, inp_param:DataFromParam):
        param_proto_format.name = inp_param.get_name()
        param_proto_format.type = inp_param.get_type()
