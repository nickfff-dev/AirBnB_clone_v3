#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
import os
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
        if kwargs.get('password'):
           self.password = self._hash_password(kwargs['password'])
        
    def _hash_password(self, password):
        """hashes the password for storing."""
        return md5(password.encode()).hexdigest()

    def update(self, **kwargs):
        """updates the user"""
        for key, value in kwargs.items():
            if key == "password":
                value = self._hash_password(value)
            setattr(self, key, value)
        self.save()
