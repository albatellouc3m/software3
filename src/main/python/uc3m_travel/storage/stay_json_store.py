"""
created by Alba Tello in abr 2024
Universidad Carlos III de Madrid
"""

import json
from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException

class StayJsonStore(JsonStore):
    """reservation json store class"""
    def __init__(self):
        super().__init__()
        self.file_path = JSON_FILES_PATH + "store_check_in.json"

    def find_stay(self, key, value):
        """finds a stay in the store"""
        super().load()
        return super().find(key, value)

    def find_checkout(self, key, value):
        """finds a stay in the store"""
        try:
            with open(self.file_path, 'r', encoding="utf-8") as file:
                self._data_l = json.load(file)
        except FileNotFoundError as ex:
            raise HotelManagementException("Error: store checkin not found") from ex
        except json.JSONDecodeError as ex:
            raise HotelManagementException("Error: JSON Decode Error - Wrong JSON Format") from ex
        return self.find(key, value)