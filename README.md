# jsonDB
A simple yet powerful json wrapper module for python3 and micropython


### Example 1
```python
from jsonDB import jsonDB as DB

# DB("path/to/db_folder", "db_file.json")
db = DB("./DB", "numbers.json")

# Write to db dictionary
for i in range(20):
    db.write(i, i**i)

# Write existing db buffer into the db_file
db.flush()

# Read value by key
db.read(771)

# Get key list by value
db.read(value=27)

# Get evaluated key list by value
db.read(value=27, ev=True)
```

### Example 2
```python

from jsonDB import jsonDB as DB

db = DB("./DB", "products.json")

products = [
    {
        "cat": "fruit",
        "name": "apple",
        "qty": 30
    },
    {
        "cat": "chocolate",
        "name": "kitkat",
        "qty": 5
    }   
]

db.write("products", products)
db.flush()

# Get list of product dictionaries
products = db.read("products")
```
