import sys
import pathlib
sys.path.append(str(pathlib.Path(sys.path[0]).resolve().parent / "src"))

from parser_func import Parser
from serialize_func import DataFromFunc

if __name__ == '__main__':
    file_name = '/home/maria/parser/tests/ns_func.cpp'
    parser_tree = Parser()
    parser_tree.parserTreeFromFile(file_name, ['-std=c++17'])
    parser_tree.serializeDataToBinaryFile("z")
