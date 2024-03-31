#!/usr/bin/python3
"""
User Class of Models Module
"""

import os
import json
import models
from uuid import uuid4, UUID
from datetime import datetime
from hashlib import md5
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

storage_type = os.environ.get('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    Base = declarative_base()
else:
    class Base:
        pass

class BaseModel:
    """
    attributes and functions for BaseModel class
    """

    if storage_type == 'db':
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """instantiation of new BaseModel Class"""
        self.id = str(uuid4())
        self.created_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
        if 'password' in kwargs:
            self.password = kwargs['password']

    @property
    def password(self):
        """Getter method for password"""
        return self.__password

    @password.setter
    def password(self, value):
        """Setter method for password"""
        self.__password = md5(value.encode()).hexdigest()

    def to_dict(self, save_to_file=False):
        """returns json representation of self"""
        data = self.__dict__.copy()
        if not save_to_file and 'password' in data:
            del data['password']
        data['__class__'] = type(self).__name__
        if '_sa_instance_state' in data:
            data.pop('_sa_instance_state')
        return data

    def __str__(self):
        """returns string type representation of object instance"""
        class_name = type(self).__name__
        return '[{}] ({}) {}'.format(class_name, self.id, self.__dict__)

    def delete(self):
        """
        deletes current instance from storage
        """
        models.storage.delete(self)


