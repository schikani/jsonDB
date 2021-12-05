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
        self._db = {}
        self._db_file_path = "/".join((self.folder_path, self.name))
        self._stream = None
        self._removed = False

        # Try to make the database folder if it doesn't exist.
        try:
            os.mkdir(self.folder_path)

        except OSError as exc:
            if exc.args[0] == errno.EEXIST:
                pass

        self._initialize()

    # This function will try to open the database and add empty dict {}.
    def _initialize(self):
        try:
            self._stream = open(self._db_file_path, "r")
        except OSError:
            self._stream = open(self._db_file_path, "w")
            json.dump(self._db, self._stream)
        self._stream.close()
        self._update_db()
    
    def _update_db(self):
        with open(self._db_file_path, "r") as self._stream:
            self._db = json.load(self._stream)

    def _write_to_db_file(self):
        with open (self._db_file_path, "w") as self._stream:
            json.dump(self._db, self._stream)

    def write(self, key, value):
        key = str(key)
        self._db[key] = value
    
    def remove(self, key=None, value=None):

        if key is not None:
            del self._db[str(key)]

        elif value is not None:
            for k, v in self._db.items():
                if v == value:
                    del self._db[k]
    
    def flush(self):
        self._write_to_db_file()

    def read(self, key=None, value=None, ev=False):

        keys = []

        if key is not None:
            for k, v in self._db.items():
                    if k == str(key):
                        if ev:
                            return eval(v)
                        return v

        elif value is not None:
            for k, v in self._db.items():
                if v == value:
                    if ev:
                        keys.append(eval(k))
                    else:
                        keys.append(k)
        
        if len(keys) > 0:
            return keys
        
        return None

    def keys(self):
        return list(self._db.keys())

    def values(self):
        return list(self._db.values())

    def items(self):
        return dict(self._db.items())

    def clear_all(self):
        self._db.clear()
        if not self._removed:
            with open(self._db_file_path, "w") as self._stream:
                json.dump(self._db, self._stream)

    def remove_db(self):
        self._removed = True
        os.remove(self._db_file_path)
