import os
from pathlib import Path

root = os.geteuid() == 0
path = (Path("/") if root else Path.home()) / "Library" / "Application Support"
standard = t"py.durability.{"default"}"