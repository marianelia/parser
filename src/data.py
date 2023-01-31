from classes_for_tree import *
import code_data_pb2
import string

class Data:
    def __init__(self) -> None:
        self.__list_data_func :list[DataFromFunc] = []
        self.__list_data_struct :list[DataFromStruct] = []
        #...

    def addDataFromFunc(self, data:DataFromFunc):
        self.__list_data_func.append(data)
    
    def addDataFromStruct(self, data:DataFromStruct):
        self.__list_data_struct.append(data)

    def serializeData(self):
        file_obj = code_data_pb2.File()
        #file.file_name = ..  
        for num_data_func in range(len(self.__list_data_func)):
            func_obj = file_obj.function_list.add()
            self.serializeFunc(func_obj, self.__list_data_func[num_data_func])

        for num_data_struct in range(len(self.__list_data_struct)):
            struct_obj = file_obj.struct_list.add()
            self.serializeStruct(struct_obj, self.__list_data_struct[num_data_struct])

        serializeToString = file_obj.SerializeToString()
        self.serializeDataToFile("test", serializeToString)
        print(serializeToString)
        file_obj.ParseFromString(serializeToString)
        print(file_obj)

    def serializeDataToFile(self, file_name:string, data:string):
        file = open(file_name, 'wb')
        file.write(data)
        file.close()

    def serializeStruct(self, struct_proto_format, struct:DataFromStruct):
        struct_proto_format.namespace.extend(struct.getNamespaces())
        struct_proto_format.name = struct.getName()

        for num_method in range(len(struct.getMethods())):
            method_obj = struct_proto_format.methods.add()
            self.serializeMethod(method_obj, struct.getMethodByIndex(num_method))


    def serializeMethod(self, method_proto_format, method:DataFromMethod):
        method_proto_format.access = method.getAccess()
        # func_proto_format = method_proto_format.function.add()
        self.serializeFunc(method_proto_format.function, method.getFunction())

        

    def serializeFunc(self, func_proto_format, func:DataFromFunc):
        func_proto_format.namespace.extend(func.getNamespaces())
        func_proto_format.name = func.getName()
        func_proto_format.output_param = func.getOutParam()
        for num_inp_param in range(len(func.getInpParams())):
            inp_param_obj = func_proto_format.input_params.add()
            self.serializeInputParams(inp_param_obj, func.getInpParam(num_inp_param))

    def serializeInputParams(self, param_proto_format, inp_param:DataFromParam):
        param_proto_format.name = inp_param.getName()
        param_proto_format.type = inp_param.getType()
