from serialize_func import *
import code_data_pb2
import string

class Data:
    def __init__(self) -> None:
        self.__list_data_func :list[DataFromFunc] = []
        #...
        pass

    def addDataFromFunc(self, data:DataFromFunc):
        self.__list_data_func.append(data)
    
    def serializeData(self):
        file = code_data_pb2.File()
        #file.file_name = ..  
        for num_data_func in range(len(self.__list_data_func)):
            func_obj = file.function_list.add()
            self.serializeFunc(func_obj, self.__list_data_func[num_data_func])

        serializeToString = file.SerializeToString()
        print(serializeToString,type(serializeToString))
        file.ParseFromString(serializeToString)
        print(file)
        
            
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