import json
import os

def export_notebook(notebook_path:str, 
                    out_dir_path:str = '', 
                    out_file_name:str = '') -> None:
    """
    Given a notebook file path, exports only code cells whose first line
    is: #_CELL_TO_EXPORT_#
    
    The output directory path is optional, if none is chose it defaults
    to the same directory.
    The output file name is optional, if none is chose it defaults to the
    same name of the notebook (but with .py extension).

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
                        f'to [{out_file_path}] ? (y/N)')

    if confirm_export.lower() not in ['y', 'yes']:
        print(RED('Export aborted.'))
        return

    print('Notebook path:', notebook_path)
    print('Output file path:', out_file_path)
    
    # output file buffer
    buffer = []

    with open(notebook_path, 'r') as f:
        data = json.load(f)
        for cell in data['cells']:
            if cell['cell_type'] == 'code':
                # if the first line contains the keyword that indicates 
                # the cell needs to be exported
                try:
                    if '#_CELL_TO_EXPORT_#' in cell['source'][0]:
                            # skip the first line
                            for line in cell['source'][1:]:
                                buffer.append(line)
                            buffer.append('\n')
                except IndexError:
                    pass

    with open(out_file_path, 'w') as out_file:
        for line in buffer:
            out_file.write(line)
               # [[[[ EXPORT NOTEBOOK TO PY ]]]]
    print('[-----', GREEN('Export  completed') ,'-----]')
