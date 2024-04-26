"""
created by Alba Tello in abr 2024
Universidad Carlos III de Madrid
"""
import json
import hashlib
from uc3m_travel.hotel_management_exception import HotelManagementException

class JsonStore:
    """Json store class"""
    def __init__(self):
        self.file_path = ""
        self._data_l = []

    def load(self):
        """loads the data from the json file"""
        try:
            with open(self.file_path, 'r', encoding="utf-8") as file:
                self._data_l = json.load(file)
        except FileNotFoundError as ex:
            self._data_l = []
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return self._data_l

    def save(self):
        """saves the data to a json file"""
        try:
            with open(self.file_path, 'w', encoding="utf-8") as file:
                json.dump(self._data_l, file, indent=2)
        except FileNotFoundError as ex:
            raise HotelManagementException("Wrong file  or file path") from ex


    def add(self, item):
        """adds an item to the store and saves the list to the file"""
        if isinstance(item, dict):
            self._data_l.append(item)
        else:
            self._data_l.append(item.__dict__)
        self.save()

    def find(self, key, value):
        for item in self._data_l:
            if key in item and item[key] == value:
                return item
        return None

    @property
    def data_l(self):
        return self._data_l

    @property
    def hash(self):
        return hashlib.md5(json.dumps(self._data_l).encode()).hexdigest()