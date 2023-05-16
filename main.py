import sys
import pathlib
import os
sys.path.append(str(pathlib.Path(sys.path[0]).resolve() / "src"))

from parser_tree import Parser

# root = str(pathlib.Path(sys.path[0]).resolve())
# fn1 = root + '/test1.cpp'
# fn2 = root +'/test2.cpp'
# file_names = [
#     #fn1,
#     fn2
#     ]

#path_to_project = str(pathlib.Path(sys.path[0]).resolve().parent.parent / 'test_lib')
#path_to_project = str(pathlib.Path(sys.path[0]).resolve())

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('The path to the library is not set')
    path_to_project = sys.argv[1]
    extension_dict = {}
    parser_tree = Parser()

    
    for root, _, files in os.walk(path_to_project):
        for name in files:
            extension = os.path.splitext(name)[1]
            if extension in extension_dict:
                extension_dict[extension].append(name)
            else:
                extension_dict[extension] = [name]
        library_name = extension_dict.get('.so', [])
        if len(library_name) == 0:
            raise FileNotFoundError('There are no libraries with the .so extension in the directory')
        elif len(library_name) > 1:
            raise ValueError('Libraries with an extension .so more than one')


        for name in files:
            if(name.endswith(".hpp")):
                parser_tree.parser_tree_from_file(os.path.join(root, name), ['-nostdinc','-std=c++17'])



    #parser_tree.serialize_data_to_binary_file("/home/maria/diploma/parser/tests/test") 
    parser_tree.serialize_data_to_binary_file("/home/maria/diploma/parser/tests/test") 
    del parser_tree
                