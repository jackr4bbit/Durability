from .utils import useVar, toStr
from . import platforms
import inspect
import json
from pathlib import Path

for frameInfo in inspect.stack():
    module = frameInfo.frame.f_globals.get("__name__")
    if module and module != __name__ and not module.startswith("importlib"):
        if module == "__main__":
            importing = Path(frameInfo.filename).stem
        elif module.endswith(".__main__"):
            importing = module[:-9]
        else:
            importing = str(module)
        break
else:
    importing = ""

type JSON = dict[str, JSON] | list[JSON] | str | int | float | bool | None

class DataStore:
    def __init__(self, name: str = importing, simple: bool = False):
        if name == "":
            raise ValueError("The name of your script/lib could not be detected. Please specify one.")
        self.name = name

        self.__path = (platforms.path / toStr(useVar(platforms.standard, name))).resolve()
        if self.__path.parent != platforms.path:
            raise ValueError(f"Name \"{name}\" is unsafe")
        if not simple:
            self.__path.mkdir(parents=False, exist_ok=True)

        self.__data = {}
        self.__simple = simple

    def __setitem__(self, key: str, value: JSON):
        self.__data[key] = value

        if self.__simple: self.__path.write_text(json.dumps(self.__data))
        else: (self.__path / f"{key}.json").write_text(json.dumps(value))

    def __contains__(self, key: str) -> bool:
        self.__getitem__(key)
        return key in self.__data

    def __getitem__(self, key: str):
        path = self.__path if self.__simple else self.__path / f"{key}.json"

        if key not in self.__data:
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except FileNotFoundError:
                return None

            if self.__simple:
                self.__data = data
            else:
                self.__data[key] = data

        return self.__data.get(key)