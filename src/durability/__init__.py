from .utils import useVar, toStr
from . import platforms
import inspect
import json
import tempfile
import os
from pathlib import Path

#Get the name of the file/module that imported this
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

        #Make dir/file path
        self.__path = (platforms.path / toStr(useVar(platforms.standard, name))).resolve()

        #Ensure path is safe
        if self.__path.parent != platforms.path:
            raise ValueError(f"Name \"{name}\" is unsafe")

        #If dir, make sure it exists
        if not simple:
            self.__path.mkdir(parents=False, exist_ok=True)

        #Initialize data
        self.__data = {}
        self.__simple = simple

    def __setitem__(self, key: str, value: JSON):
        #Store new data
        self.__data[key] = value

        #Make path for this key
        path = self.__path if self.__simple else self.__path / f"{key}.json"

        #Get data to write
        data = self.__data if self.__simple else value

        #Convert data to JSON
        data = json.dumps(data)

        #Get a temporary file
        with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False) as tmpFile:
            #Write the data
            tmpFile.write(data)

            #Ensure the data was written
            tmpFile.flush()
            os.fsync(tmpFile.fileno())

            #Find where it was written to
            tmpPath = Path(tmpFile.name)

        #Move it to the intended destination
        tmpPath.replace(path)

        #Make sure the temporary file and the destination file were written to
        descriptor = os.open(str(path.parent), os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    def __contains__(self, key: str) -> bool:
        #Make sure the data is loaded from the file
        self.__getitem__(key)

        #Check if the target key exists
        return key in self.__data

    def __getitem__(self, key: str):
        path = self.__path if self.__simple else self.__path / f"{key}.json"

        #Read data from file if not already loaded
        if key not in self.__data:
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except FileNotFoundError:
                return None

            #Store data
            if self.__simple:
                self.__data = data
            else:
                self.__data[key] = data

        #Return requested data
        return self.__data.get(key)