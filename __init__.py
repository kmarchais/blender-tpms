def install_dependencies():
    import sys, subprocess
    for dependency in dependencies.keys():
        if dependency != 'pip':
            subprocess.call([sys.executable, "-m", "pip", "install", *dependencies])

dependencies = {'pip': {},
                'pyvista': {"url": "https://github.com/pyvista/pyvista"},}
install_dependencies()

from . import ui

bl_info = {
    "name": "TPMS",
    "author": "kmarchais",
    "version": (0, 1),
    "blender": (3, 0, 0),
    "location": "Add > TPMS",
    "description": "Create a TPMS mesh",
    "warning": "",
    "doc_url": "https://github.com/kmarchais/blender-tpms",
    "category": "Add Mesh",
}


def register():
    ui.register()

def unregister():
    ui.unregister()
