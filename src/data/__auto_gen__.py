import ast
import fnmatch
import logging
import os
import sys


def get_data_path(relative_path: str) -> str:
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res


def top_level_functions(body: list) -> list:
    return [f for f in body if isinstance(f, ast.FunctionDef)]


def parse_ast(filename: str) -> ast.Module:
    with open(filename, "rt") as file:
        return ast.parse(file.read(), filename=filename)


def gen_import_lists(data: list) -> str:
    res = ""
    i = 0
    last = ''
    while i < len(data):
        if data[i][0] == '_':
            i += 1
            continue
        else:
            pass
        line = "    "
        if last == data[i][0]:
            while last == data[i][0]:
                line += data[i]
                line += ", "
                i += 1
                if i == len(data):
                    break
                else:
                    pass
            res += line
            res += "\n"
        else:
            last = data[i][0]
    return res[:-3]


def get_all_py_files() -> list:
    data_pkg = get_data_path('.')
    all_files = [f for f in os.listdir(data_pkg) if os.path.isfile(os.path.join(data_pkg, f))]
    all_files.remove('__init__.py')
    all_files.remove(os.path.basename(__file__))

    py_files = []
    for file in all_files:
        if fnmatch.fnmatch(file, '*.py'):
            py_files.append(file)
        else:
            pass
    return py_files


def print_body() -> str:
    py_files = get_all_py_files()
    output = ""
    for filename in py_files:
        tree = parse_ast(get_data_path(os.path.join(".", filename)))
        ast_objs = top_level_functions(tree.body)
        func_names = sorted([i.name for i in ast_objs])
        output += f'from .{filename[:-3]} import (\n'
        output += gen_import_lists(func_names)
        output += '\n)\n'
    return output


def start_generator() -> bool:
    header = '''
"""
DO **NOT** EDIT THIS FILE!

THIS FILE IS AUTO-GENERATED BY src/data/__auto_gen__.py

Note that '_' leading functions are not imported!

If error comes from __init__.py, due largely to asynchronous update,
delete the __init__.py and re-run __auto_gen__.py
"""
    '''
    res = False
    try:
        output_path = get_data_path(os.path.join('.', '__init__.py'))
        with open(output_path, 'w') as f:
            header += "\n"
            header += print_body()
            f.write(header)
            res = True
    except FileNotFoundError as e:
        logging.error(f'DATA - auto_gen failed for {e}')
    return res


if __name__ == "__main__":
    print('Starting __auto_gen__...')
    print(start_generator())
else:
    pass

# End of File
