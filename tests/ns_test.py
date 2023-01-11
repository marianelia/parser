import sys
import pathlib
sys.path.append(str(pathlib.Path(sys.path[0]).resolve().parent / "src"))

from parser_func import filterByNodeFunctionsDecl
from serialize_func import DataFromFunc

import clang.cindex

#from parser.src import parser_func
#sys.path.append(os.path.abspath('../src'))

#import filterByNodeFunctionsDecl
#from ..src.parser_func import filterByNodeFunctionsDecl
#import filterByNodeFunctionsDecl
# from ..src import *

# func for test (temp)
def ns_and_func():

    result_func = DataFromFunc()


    file_name = '/home/maria/parser/tests/ns_func.cpp'
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_name, args=['-std=c++17'])
    filterByNodeFunctionsDecl(translation_unit.cursor.get_children(), 
                    [clang.cindex.CursorKind.FUNCTION_DECL, clang.cindex.CursorKind.NAMESPACE], result_func)

    result_func.printForTests()



if __name__ == '__main__':
    ns_and_func()
    #data = DataFromFunc()

