"""Blender TPMS addon to generate TPMS meshes."""

dependencies = {
    "pip": {},
    "blender_tpms": {},
}

for dependency in dependencies:
    if dependency != "pip":
        try:
            __import__(dependency)
        except (ImportError, ModuleNotFoundError):
            import importlib
            import subprocess
            import sys
            from pathlib import Path

            cmd = [
                sys.executable,
                "-m",
                "pip",
                "install",
                Path(__file__).parent,
            ]
            subprocess.check_call(cmd)

            from site import getusersitepackages

            user_site = getusersitepackages()
            if user_site not in sys.path:
                sys.path.append(user_site)

            importlib.import_module(dependency)


from blender_tpms import ui

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


def register() -> None:
    """Register the addon."""
    ui.register()


def unregister() -> None:
    """Unregister the addon."""
    ui.unregister()
