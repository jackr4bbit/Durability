# Durability
## A tiny Python persistence library.

---

![PyPI Version](https://img.shields.io/pypi/v/durability?style=for-the-badge)


## Installation

```bash
pip install durability
```


## Why
I don't want to have to mess with state/data files. You have to read and write to them whenever you make a change, worry about different locations for them across platforms, and troubleshoot the system. This autosaves and uses the OS's existing dir for application data.

## How to use
Durability provides a `DataStore` object that may be passed the name of your project (so that files don't conflict). It will automatically use your script/lib's name if you don't provide one.  
In "normal mode" each key of a `DataStore` is another file, but in "simple mode" (which you can use by setting the parameter `simple` to `True`) to get an interface where each key corresponds to a value in the same file. 

Here's an example of using it in simple mode:
```python
from durability import DataStore

store = DataStore("durability-example", simple = True)

#If no existing count, set it to 0
if "count" not in store:
    store["count"] = 0

#Increment and display it
store["count"] += 1
print(store["count"])

#Automatically saves! No hassle necessary.
```
vs in normal mode:
```python
from durability import DataStore

store = DataStore("durability-example")

store["config"] = {"threads": 3, "username": "abc"}
store["currentConnections"] = ["192.168.1.13", "100.90.116.124"]
```