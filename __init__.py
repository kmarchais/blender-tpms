"""Blender TPMS addon to generate TPMS meshes."""

try:
    import blender_tpms
except ImportError:
    import importlib
    import site
    import subprocess
    import sys
    from pathlib import Path

    # install the blender_tpms package in blender's python environment
    cmd = [
        sys.executable,
        "-m",
        "pip",
        "install",
        str(Path(__file__).parent),
    ]
    subprocess.check_call(cmd)

    user_site = site.getusersitepackages()
    if user_site not in sys.path:
        sys.path.append(user_site)

    importlib.import_module("blender_tpms")

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

import blender_tpms


def register() -> None:
    """Register the addon."""
    blender_tpms.register()


def unregister() -> None:
    """Unregister the addon."""
    blender_tpms.unregister()
