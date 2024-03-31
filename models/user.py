#!/usr/bin/python3
"""
User Class from Models Module
"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float
from hashlib import md5
storage_type = os.environ.get('HBNB_TYPE_STORAGE')


class User(BaseModel, Base):
    """User class handles all application users"""
    if storage_type == "db":
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column("password", String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)

        places = relationship('Place', backref='user', cascade='delete')
        reviews = relationship('Review', backref='user', cascade='delete')
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''

    def __init__(self, *args, **kwargs):
        """
        initialize User Model, inherits from BaseModel
        """
        super().__init__(*args, **kwargs)
        if 'password' in kwargs:
            self.password = kwargs['password']

    @property
    def password(self):
        """
        getter for password
        :return: password (hashed)
        """
        return self.__dict__.get("password")

    @password.setter
    def password(self, password):
        """
        Password setter, with md5 hashing
        :param password: password
        :return: nothing
        """
        self.__dict__["password"] = md5(password.encode('utf-8')).hexdigest()

    def to_dict(self, save_to_file=False):
        """Return dictionary representation of User"""
        data = super().to_dict(save_to_file)
        if not save_to_file and 'password' in data:
            del data['password']
        return data

