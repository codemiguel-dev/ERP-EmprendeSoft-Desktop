import os
import sys

from cx_Freeze import Executable, setup

# Aumentar límite de recursión si es necesario
sys.setrecursionlimit(5000)


# Función para incluir carpetas y archivos adicionales
def include_files():
    base_path = os.path.abspath(os.getcwd())
    files = []
    for folder in [
        "database",
        "configuration",
        "design",
        "view",
        "controller",
        "models",
        "doc",
        "excel",
        "img",
    ]:
        folder_path = os.path.join(base_path, folder)
        if os.path.exists(folder_path):
            # Incluir todos los archivos dentro de la carpeta
            for root, _, filenames in os.walk(folder_path):
                for filename in filenames:
                    full_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(full_path, base_path)
                    files.append((full_path, relative_path))
    return files


# Configuración básica de cx_Freeze
setup(
    name="EmprendeSoft",
    version="1.0",
    description="Descripción de tu aplicación",
    options={
        "build_exe": {
            "include_files": include_files(),  # Incluir carpetas y recursos
            "packages": ["os", "PyQt5", "passlib", "pymupdf"],  # fitz es pymupdf
            "includes": [
                "PyQt5.uic.widget-plugins.qtquickwidgets",
                "PyQt5.uic.widget-plugins.qtwebenginewidgets",
                "PyQt5.uic.widget-plugins.qtwebkit",
                "passlib.handlers.bcrypt",
                "pymupdf",
            ],
            "include_msvcr": True,  # Incluir Microsoft Visual C++ Redistributable
        }
    },
    executables=[
        Executable(
            script="main.py",  # Archivo principal
            base=(
                "Win32GUI" if sys.platform == "win32" else None
            ),  # "Win32GUI" oculta la consola en Windows
            icon="img/icon.ico",  # Ícono opcional
        )
    ],
)
