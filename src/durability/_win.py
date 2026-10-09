import ctypes
from pathlib import Path

if ctypes.windll.shell32.IsUserAnAdmin() != 0:
    path = Path.cwd().anchor / "ProgramData"
else:
    path = Path.home() / "AppData" / "Roaming"

standard = t"durability/{"default"}"