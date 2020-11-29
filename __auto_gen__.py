# NOT WORKING, tried to implement a script to auto import for data/__init__.py
# trapped by ModuleNotFoundError
# use if __name__ == "..." to bypass relative imoprt for data/*.py
import ast
import fnmatch
import os
import sys
import inspect
from importlib import import_module


def gen_import_lists(data):
    # this works
    unwanted = ['os', 'json', 'QSettings', 'qdarkstyle']
    res = ""
    i = 0
    last = ''
    while i < len(data):
        if (data[i][0] == '_') or (data[i] in unwanted) or (data[i][:3] == 'wgv'):
            i += 1
            continue
        else:
            pass
        line = "    "
        if last == data[i][0]:
            while last == data[i][0]:
                line += data[i]
                line += ","
                i += 1
                if i == len(data):
                    break
                else:
                    pass
            res += line
            res += "\n"
        else:
            last = data[i][0]
    return res[:-2]

def get_data_path(relative_path):
    # This needs to be in current file
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    res = os.path.join(bundle_dir, relative_path)
    return relative_path if not os.path.exists(res) else res

def top_level_functions(body):
    return (f for f in body if isinstance(f, ast.FunctionDef))

def parse_ast(filename):
    with open(filename, "rt") as file:
        return ast.parse(file.read(), filename=filename)

# if __name__ == "__main__":
#     for filename in sys.argv[1:]:
#         print(filename)
#         tree = parse_ast(filename)
#         for func in top_level_functions(tree.body):
#             print("  %s" % func.name)


data_pkg = get_data_path('./src/data')
all_files = [f for f in os.listdir(data_pkg) if os.path.isfile(os.path.join(data_pkg, f))]
all_files.remove('__init__.py')

py_files = []
for file in all_files:
    if fnmatch.fnmatch(file, '*.py'):
        py_files.append(file)
    else:
        pass

for filename in py_files:
    print(filename)
    # print(inspect(filename))

    # import inspect
    functions = inspect.getmembers(import_module('src.data'), inspect.isfunction)
    # print(functions.name)
    for f in functions:
        print(f[0])
    print('\n')
    # print(filename)
    # tree = parse_ast(os.path.join("./src/data", filename))
    # for func in top_level_functions(tree.body):
        # print("  %s" % func.name)
    # output = f'from .{filename} import (\n'
    # temp = import_module('src.data')
    # output += gen_import_lists(dir(temp))
    # output += '\n)'
    # print(output)
    # print("\n")