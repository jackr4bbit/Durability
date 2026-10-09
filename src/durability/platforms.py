import sys
from pathlib import Path
from string.templatelib import Template

match sys.platform:
    case "darwin": from ._mac import path, standard
    case "win32": from ._win import path, standard
    case os if os.startswith("linux"): from ._linux import path, standard
    case _: raise OSError(f"Unsupported operating system: {sys.platform}")

path: Path = path
standard: Template = standard