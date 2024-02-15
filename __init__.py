dependencies = {'pip': {},
                'pyvista': {"url": "https://github.com/pyvista/pyvista"},}

for dependency in dependencies:
    if dependency != 'pip':
        try:
            __import__(dependency)
        except ImportError:
            import sys
            import subprocess
            subprocess.call([sys.executable, "-m", "pip", "install", dependency])


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
