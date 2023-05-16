import sys
import pathlib
import os
sys.path.append(str(pathlib.Path(sys.path[0]).resolve() / "src"))

from parser_tree import Parser

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
            raise FileNotFoundError('There are no libraries with the *.so extension in the directory')
        elif len(library_name) > 1:
            raise ValueError('Libraries with an extension *.so more than one')


        for name in files:
            if(name.endswith(".hpp")):
                parser_tree.parser_tree_from_file(os.path.join(root, name), ['-nostdinc','-std=c++17'])


    if path_to_project[-1] != '/':
        path_to_project += '/'

    print(path_to_project + library_name[0])
    print(path_to_project)
    print(library_name[0][:-3]+'_proto')
    parser_tree.serialize_data_to_binary_file(path_to_project + library_name[0][:-3]+'_proto') 
    del parser_tree
                