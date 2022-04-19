#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
import os

if (os.getenv('DBStorage')) == 'db':
    from models.engine.db_storage.py import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
