#!/usr/bin/python3
"""
Handles I/O, writing and reading, of JSON for storage of all class instances
"""

import json
from models import base_model, amenity, city, place, review, state, user
from datetime import datetime


class FileStorage:
    """Handles long term storage of all class instances"""

    CNC = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }

    def __init__(self):
        self.__file_path = './dev/file.json'
        self.__objects = {}

    def all(self, cls=None):
        """Returns private attribute: __objects"""
        if cls:
            return {k: v for k, v in self.__objects.items() if
                    isinstance(v, cls)}
        return self.__objects

    def new(self, obj):
        """Sets / updates in __objects the obj with key <obj class name>.id"""
        bm_id = f"{type(obj).__name__}.{obj.id}"
        self.__objects[bm_id] = obj

    def get(self, cls, id):
        """Gets specific object"""
        for obj in self.all(cls).values():
            if str(obj.id) == id:
                return obj
        return None

    def count(self, cls=None):
        """Count of instances"""
        return len(self.all(cls))

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        with open(self.__file_path, mode='w', encoding='utf-8') as f_io:
            json.dump({k: v.to_json() for k,
                       v in self.__objects.items()}, f_io)

    def reload(self):
        """Deserializes JSON file to __objects"""
        try:
            with open(self.__file_path, mode='r', encoding='utf-8') as f_io:
                data = json.load(f_io)
                self.__objects = {k: FileStorage.CNC[v["__class__"]](**v)
                                  for k, v in data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def delete(self, obj=None):
        """Deletes obj"""
        if obj:
            key_to_delete = f"{type(obj).__name__}.{obj.id}"
            self.__objects.pop(key_to_delete, None)
            self.save()

    def close(self):
        """Closes the storage"""
        self.reload()
