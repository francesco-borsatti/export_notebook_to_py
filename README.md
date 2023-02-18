# Export ipython Notebook to python script file

In a jupyter notebook, if you want to export just some cells, put in their first line `#_CELL_TO_EXPORT_#`.

You can add the function `export_notebook()` to your notebook and just run the cell when you want to export just the code blocks you selected to a python file.

### Parameters:
- `notebook_path` : the path of the notebook of which you want to export marked code cells.
- `out_dir_path` : output directory path, if none is given it defaults to same directory of the selected notebook.
- `out_file_name` : [str] --- output python script file name, if none is given it defaults to the name of the selected notebook.
- `put_imports_on_top` : [bool] --- Whether to put import lines at the top of the python script file. Default value = False.