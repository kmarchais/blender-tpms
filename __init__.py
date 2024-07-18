import bpy

dependencies = {
    "pip": {},
    "pyvista": {"url": "https://github.com/pyvista/pyvista"},
}

for dependency in dependencies:
    if dependency != "pip":
        try:
            __import__(dependency)
        except ImportError:
            import importlib
            import subprocess
            import sys

            cmd = [sys.executable, "-m", "pip", "install", "--user", dependency]
            subprocess.check_call(cmd)

            from site import getusersitepackages

            user_site = getusersitepackages()
            if user_site not in sys.path:
                sys.path.append(user_site)

            importlib.import_module(dependency)


from . import ui

bl_info = {
    "name": "TPMS",
    "author": "kmarchais",
    "version": (0, 1),
    "blender": (3, 6, 0),
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
