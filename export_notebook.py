#### THIS FILE WAS AUTOMATICALLY GENERATED - DO NOT EDIT ####
#### Edit source notebook instead: ./export_notebook.ipynb
import json
import os
import ast

def line_contains_import(line):
    try:
        parsed = ast.parse(line.strip())
        for node in ast.walk(parsed):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                return True
    except SyntaxError:
        pass
    return False


def export_notebook(notebook_path:str, 
                    out_dir_path:str = '', 
                    out_file_name:str = '',
                    put_imports_on_top:bool = True) -> None:
    """
    Given a notebook file path, exports only code cells whose first line
    is: #_CELL_TO_EXPORT_#
    
    - The output directory path is optional, if none is chose it defaults
    to the same directory.
    - The output file name is optional, if none is chose it defaults to the
    same name of the notebook (but with .py extension).
    - Put imports on top set to true if you want all the imports to be placed
    at the top of the script file.

    Example use: export_notebook(notebook_path='./this_notebook.ipynb',
                        output_dir_path='../folder/',
                        output_file_name='python_script.py')
    """

    # message colors
    GREEN = lambda x: '\033[92m' + x + '\033[0m'
    BOLD = lambda x: '\033[1m'  + x + '\033[0m'
    RED = lambda x: '\033[91m' + x + '\033[0m'

    print('[[[[', GREEN(BOLD('EXPORT NOTEBOOK TO PY')), ']]]]')

    # if notebook path does not exist
    if not os.path.exists(notebook_path):
        raise Exception('Notebook path does not exist.')
    
    # if no filename is given:
    if not out_file_name:
        # remove folder path
        out_file_name = os.path.split(notebook_path)[-1]
        # remove .ipynb extension
        out_file_name = os.path.splitext(out_file_name)[0]
        # add .py extension
        out_file_name = out_file_name + '.py'

    # if no output directory path is given:
    if not os.path.exists(out_dir_path):
        out_dir_path = os.path.dirname(notebook_path)

    out_file_path = os.path.join(out_dir_path, out_file_name)

    confirm_export = input('Are you sure you want to export' +
                        f'the notebook [{notebook_path}]' + 
                        f'to [{out_file_path}] ? (y/N) \n')
    if confirm_export.lower() not in ['y', 'yes']:
        print(RED('Export aborted.'))
        return

    print('Notebook path:', notebook_path)
    print('Output file path:', out_file_path)
    
    # output file buffer
    buffer = []
    # place a warning message at the top of the file
    buffer.append( '#### THIS FILE WAS AUTOMATICALLY GENERATED - DO NOT EDIT ####\n')
    buffer.append(f'#### Edit source notebook instead: {notebook_path}\n')

    # keep track of the number of imports in the file
    # to place them in order at the top
    num_of_imports = len([c for c in buffer if '\n' in c])

    with open(notebook_path, 'r') as f:
        data = json.load(f)
        for cell in data['cells']:
            # skip non-code cells
            if cell['cell_type'] != 'code':
                continue
            # skip empty cells
            if not cell['source']:
                continue
            # skip non marked cells
            if '#_CELL_TO_EXPORT_#' not in cell['source'][0]:
                continue
            # -- Cell to be exported -- read line by line:
            # skip the first line (which contains #_CELL_TO_EXPORT_#)
            for line in cell['source'][1:]:
                # if line contains import statement
                if line_contains_import(line) and put_imports_on_top:
                    buffer.insert(num_of_imports, line)
                    num_of_imports = num_of_imports + 1
                    continue
                # normal lines are appended at the end
                buffer.append(line)
            # put a new line at the end of cells
            buffer.append('\n')

    # write buffer to output file
    with open(out_file_path, 'w') as out_file:
        for line in buffer:
            out_file.write(line)
    
    # process ended
    print('[-----', GREEN('Export  completed') ,'-----]')

