#!/usr/bin/python3
"""
User Class of Models Module
"""

from models.base_model import BaseModel
import hashlib

class User(BaseModel):
    """
    User class inherits from BaseModel
    """

    email = ''
    password = ''
    first_name = ''
    last_name = ''

    def __init__(self, *args, **kwargs):
        """Instantiation of new User class"""
        super().__init__(*args, **kwargs)
        if 'password' in kwargs:
            self.password = hashlib.md5(kwargs['password'].encode()).hexdigest()

    @property
    def password(self):
        """Getter method for password"""
        return self.__password

    @password.setter
    def password(self, value):
        """Setter method for password"""
        self.__password = hashlib.md5(value.encode()).hexdigest()

    def to_dict(self, save_to_file=False):
        """Return dictionary representation of User"""
        data = super().to_dict(save_to_file)
        if not save_to_file and 'password' in data:
            del data['password']
        return data

