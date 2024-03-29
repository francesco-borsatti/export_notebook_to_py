#### THIS FILE WAS AUTOMATICALLY GENERATED - DO NOT EDIT ####
# Edit source notebook instead: ./export_notebook.ipynb

import ast
import json
import os


# message colors
GREEN = lambda x: '\033[92m' + x + '\033[0m'
BOLD = lambda x: '\033[1m'  + x + '\033[0m'
RED = lambda x: '\033[91m' + x + '\033[0m'

def line_contains_import(line):
    try:
        parsed = ast.parse(line.strip())
        for node in ast.walk(parsed):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                return True
    except SyntaxError:
        pass
    return False


def user_approval(notebook_path:str, out_file_path:str) -> bool:
    """
    Returns true if user wants to perform the notebook export.
    """
    confirm_export = input('Are you sure you want to export' +
                    f'the notebook [{notebook_path}]' + 
                    f'to [{out_file_path}] ? (y/N) \n')
    if confirm_export.lower() not in ['y', 'yes']:
        print('[------', RED('Export canceled'), '------]')
        return False
    return True


def clean_newlines(filepath:str):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Remove consecutive empty lines
    new_file_buffer = []
    empty_count = 0
    for line in lines:

        if line == '\n':
            empty_count += 1
            if empty_count > 2:
                continue
        else:
            empty_count = 0

        new_file_buffer.append(line)
    
    # remove excessive last empty lines
    i = 1
    try:
        while new_file_buffer[-i] == '\n':
            i += 1
    except IndexError:
        pass

    new_file_buffer = new_file_buffer[:-empty_count]    

    # Write the new lines to the file
    with open(filepath, 'w') as f:
        f.writelines(new_file_buffer)


def export_notebook(notebook_path:str, 
                    out_dir_path:str = '', 
                    out_file_name:str = '',
                    put_imports_on_top:bool = False) -> None:
    """
    Given a notebook file path, exports only code cells whose first line
    is: # EXPORT_CELL #
    
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

    # ask the user for if they want to continue
    if not user_approval(notebook_path, out_file_path):
        return

    print('Notebook path:', notebook_path)
    print('Output file path:', out_file_path)
    
    # output file buffer
    buffer = []

    # keep track of the number of imports in the file to place them in order at the top
    import_lines = []

    with open(notebook_path, 'r') as f:
        data = json.load(f)
        for cell in data['cells']:
            # skip non-code cells
            if cell['cell_type'] != 'code':
                continue
            # skip empty cells
            if not cell['source']:
                continue
            # check if marked cell
            # skip first empty lines
            cell_to_export = False
            # keep record of the line in which appears # EXPORT_CELL #
            num_lines_to_skip = 0
            for line_number, line in enumerate(cell['source']):
                if not line.strip():
                    continue
                if '# EXPORT_CELL #' in line:
                    cell_to_export = True
                    num_lines_to_skip = line_number
                    break
            # skip this cell if it's not to export
            if not cell_to_export:
                continue
            # -- Cell to be exported -- read line by line:
            # skip the first 'num_lines_to_skip+1' lines (which contain '' or # EXPORT_CELL #)
            num_lines_to_skip += 1
            for line in cell['source'][num_lines_to_skip:]:
                # if line contains import statement
                if put_imports_on_top and line_contains_import(line):
                    import_lines.append(line.replace('\n',''))
                    continue
                # normal lines are appended at the end
                buffer.append(line)
            # put a new line at the end of cells
            buffer.append('\n\n')

    # place a warning message at the top of the file
    initial_message = ['#### THIS FILE WAS AUTOMATICALLY GENERATED - DO NOT EDIT ####\n',
                       f'# Edit source notebook instead: {notebook_path}\n\n']

    # save final lines to another buffer to output file
    with open(out_file_path, 'w') as out_file:
        for line in initial_message:
            out_file.write(line)
        # nicely place imports
        if put_imports_on_top:
            for line in import_lines:
                out_file.write(line + '\n')
            out_file.write('\n')
        # write the rest of the file
        for line in buffer:
            out_file.write(line)

    # clean file from excessive empty lines
    clean_newlines(out_file_path)
    
    # process ended
    print('[-----', GREEN('Export  completed'), '-----]')
