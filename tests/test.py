import sys
import pathlib
sys.path.append(str(pathlib.Path(sys.path[0]).resolve().parent / "src"))

from parser_tree import Parser

root = str(pathlib.Path(sys.path[0]).resolve())
fn1 = root + '/test1.cpp'
fn2 = root +'/test2.cpp'
file_names = [
    #fn1, 
    fn2
    ]


if __name__ == '__main__':
    for fn in file_names:
        print(fn)
        parser_tree = Parser()
        parser_tree.parser_tree_from_file(fn, ['-std=c++17'])
        parser_tree.serialize_data_to_binary_file("/home/maria/diploma/generator/tests/")
        del parser_tree