import sys
import pathlib
sys.path.append(str(pathlib.Path(sys.path[0]).resolve().parent / "src"))

from parser_func import Parser

root = str(pathlib.Path(sys.path[0]).resolve())
fn1 = root + '/test1.cpp'
fn2 = root +'/test2.cpp'
file_names = [
    # fn1, 
    fn2
    ]


if __name__ == '__main__':
    for fn in file_names:
        print(fn)
        parser_tree = Parser()
        parser_tree.parserTreeFromFile(fn, ['-std=c++17'])
        parser_tree.serializeDataToBinaryFile("")
        del parser_tree