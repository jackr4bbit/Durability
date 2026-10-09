import os
from pathlib import Path

if os.geteuid() == 0:
    path = Path("/var/lib")
else:
    path = Path.home() / ".config"

standard = t"{"default"}-durability"