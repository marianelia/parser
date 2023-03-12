import sys
import pathlib
import os
sys.path.append(str(pathlib.Path(sys.path[0]).resolve().parent / "src"))

from parser_tree import Parser

# root = str(pathlib.Path(sys.path[0]).resolve())
# fn1 = root + '/test1.cpp'
# fn2 = root +'/test2.cpp'
# file_names = [
#     #fn1,
#     fn2
#     ]

path_to_project = str(pathlib.Path(sys.path[0]).resolve())

if __name__ == '__main__':
    for root, dirs, files in os.walk(path_to_project):
        for name in files:
            if(name.endswith(".cpp")):
                # print(os.path.join(root, name))
                parser_tree = Parser()
                parser_tree.parser_tree_from_file(os.path.join(root, name), ['-std=c++17'])
                parser_tree.serialize_data_to_binary_file("/home/maria/diploma/generator/tests/")
                del parser_tree
                