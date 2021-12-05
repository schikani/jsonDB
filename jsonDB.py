# ==========================================
# Project:   jsonDB
# Author:    Shivang Chikani
# Date:      05 Dec 2021
# ==========================================

import json
import os
import errno

class jsonDB:
    
    def __init__(self, folder_path, name):
        self.folder_path = folder_path
        self.name = name
        self._db_file_path = "/".join((self.folder_path, self.name))
        self._db = None
        self._stream = None
        self._removed = False

        # Try to make the database folder if it doesn't exist.
        try:
            os.mkdir(self.folder_path)

        except OSError as exc:
            if exc.args[0] == errno.EEXIST:
                pass
        
        # If the database exists, fill the db dictionary with data
        try:
            with open(self._db_file_path, "r") as self._stream:
                self._db = json.load(self._stream)
        
        # Else initialize with an empty dictionary
        except OSError as exc:
            if exc.args[0] == errno.ENOENT:
                self._db = {}

    def _write_to_db_file(self):
        with open (self._db_file_path, "w") as self._stream:
            json.dump(self._db, self._stream)

    # Write to db dictionary
    def write(self, key, value):
        key = str(key)
        self._db[key] = value
    
    # Remove key-value pair by giving key or value as parameter
    def remove(self, key=None, value=None):

        if key is not None:
            del self._db[str(key)]

        elif value is not None:
            for k, v in self._db.items():
                if v == value:
                    del self._db[k]
    
    # Write current dictionary to the stream file
    def flush(self):
        self._write_to_db_file()


    # Get value by key or key list by value
    # Optionally if ev=True, get evaluated keys or values
    def read(self, key=None, value=None, ev=False):

        if key is not None:
            for k, v in self._db.items():
                    if k == str(key):
                        if ev:
                            return eval(v)
                        return v

        elif value is not None:
            keys = []
            for k, v in self._db.items():
                if v == value:
                    if ev:
                        keys.append(eval(k))
                    else:
                        keys.append(k)

            if len(keys) > 0:
                return keys
        
        return None

    # Get key list
    def keys(self):
        return list(self._db.keys())

    # Get value list
    def values(self):
        return list(self._db.values())

    # Get items dictionary
    def items(self):
        return dict(self._db.items())
    
    # Check if a key or value exist
    def exists(self, key = None, value = None):
        if key is not None:
            if self.read(str(key)):
                return True
        
        elif value is not None:
            for v in self._db.values():
                if v == value: 
                    return True

        return False

    # Clear current db dictionary and stream file
    def clear_all(self):
        self._db.clear()
        if not self._removed:
            with open(self._db_file_path, "w") as self._stream:
                json.dump(self._db, self._stream)

    # Remove stream file
    def remove_db(self):
        self._removed = True
        os.remove(self._db_file_path)
