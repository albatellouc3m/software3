"""
created by Alba Tello in abr 2024
Universidad Carlos III de Madrid
"""
from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.hotel_management_config import JSON_FILES_PATH

class CheckoutJsonStore(JsonStore):
    """checkout json store class"""
    def __init__(self):
        super().__init__()
        self.file_path = JSON_FILES_PATH + "store_check_out.json"

    def find_it(self, key, value):
        """finds a checkout in the store"""
        super().load()
        return super().find(key, value)
