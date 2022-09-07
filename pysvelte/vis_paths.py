
from pathlib import Path

"""
This is the pysvelte subfolder of the repo if cloned, and the site-packages/pysvelte folder
if installed with pip
"""
PYSVELTE_PACKAGE_ROOT = Path(__file__).parent.absolute()

"""
Some supporting infrastructure is in the pysvelte/node folder
"""
NODE_ROOT = PYSVELTE_PACKAGE_ROOT / "node"

"""
Some components are included with PySvelte in the pysvelte/src folder
"""
INTERNAL_COMPONENTS_SRC = PYSVELTE_PACKAGE_ROOT / "src"

"""
All components share the same build folder
"""
COMPONENTS_DIST = PYSVELTE_PACKAGE_ROOT / "dist"
