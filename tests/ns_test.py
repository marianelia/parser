import sys
import pathlib
sys.path.append(str(pathlib.Path(sys.path[0]).resolve().parent / "src"))

from parser_func import Parser
from serialize_func import DataFromFunc

fn1 = '/home/maria/parser/tests/ns_func.cpp'
fn2 = '/home/maria/parser/tests/struct.cpp'
file_names = [fn1, fn2]


if __name__ == '__main__':
    for fn in file_names:
        print(fn)
        parser_tree = Parser()
        parser_tree.parserTreeFromFile(fn, ['-std=c++17'])
        parser_tree.serializeDataToBinaryFile("")
        del parser_tree