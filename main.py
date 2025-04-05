import os

def tree(directory, exclude_dirs, prefix=''):
    """
    Imprime la estructura de directorios de forma recursiva, excluyendo las carpetas especificadas.
    :param directory: El directorio raíz desde donde comenzar.
    :param exclude_dirs: Lista de carpetas a excluir.
    :param prefix: Prefijo para la impresión (usado para la recursión).
    """
    if not os.path.isdir(directory):
        print(f"{directory} no es un directorio válido.")
        return

    items = sorted(os.listdir(directory))
    for index, item in enumerate(items):
        path = os.path.join(directory, item)
        if item in exclude_dirs:
            continue
        connector = '└── ' if index == len(items) - 1 else '├── '
        print(f"{prefix}{connector}{item}")
        if os.path.isdir(path):
            extension = '    ' if index == len(items) - 1 else '│   '
            tree(path, exclude_dirs, prefix + extension)

# Directorio raíz desde donde comenzar
root_directory = '.'

# Lista de carpetas a excluir
exclude_directories = ['__pycache__', '.venv', '.git']

# Llamada a la función tree
tree(root_directory, exclude_directories)