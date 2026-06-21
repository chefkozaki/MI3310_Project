import os
import file_io
from data_structures import LinkedList

class Database:
    def __init__(self, db_folder="."):
        self.db_folder = db_folder
        
    def _get_path(self, filename):
        return os.path.join(self.db_folder, filename)
        
    def save_list(self, filename, linked_list):
        path = self._get_path(filename)
        file_io.save_objects_to_file(path, linked_list)

    def load_list(self, filename, factory_func):
        path = self._get_path(filename)
        return file_io.load_objects_from_file(path, factory_func)
