from ..utils import ast_helpers


def has_no_star_imports(project_folder, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files():
        if ast_helpers.is_tree_has_star_imports(parsed_file.ast_tree):
            return 'has_star_import', parsed_file.name


def has_no_local_imports(project_folder, local_imports_paths_to_ignore, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files(whitelist=local_imports_paths_to_ignore):
        if ast_helpers.is_has_local_imports(parsed_file.ast_tree):
            return 'has_local_import', parsed_file.name


def has_no_pdb_breakpoints(project_folder, *args, **kwargs):
    for parsed_file in project_folder.get_parsed_py_files():
        if 'pdb' in ast_helpers.get_all_import_names_mentioned_in_import(parsed_file.ast_tree):
            return 'has_pdb_breakpoint', parsed_file.name


def has_no_multiple_imports_on_same_line(project_folder, *args, **kwargs):
    """Protects against the case
        import foo, bar
    """
    for parsed_file in project_folder.get_parsed_py_files():
        imports = ast_helpers.get_all_imports(parsed_file.ast_tree)
        for import_node in imports:
            if ast_helpers.is_multiple_imports_on_one_line(import_node):
                return 'has_multiple_imports_on_same_line', parsed_file.get_name_with_line(import_node.lineno)
