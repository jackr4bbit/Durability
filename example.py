from durability import DataStore

store = DataStore("durability-example", simple = True)

if "count" not in store:
    store["count"] = 0

store["count"] += 1
print(store["count"])