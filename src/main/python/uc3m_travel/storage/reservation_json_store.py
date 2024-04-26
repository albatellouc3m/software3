"""
created by Alba Tello in abr 2024
Universidad Carlos III de Madrid
"""

from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.hotel_management_exception import HotelManagementException

class ReservationJsonStore(JsonStore):
    """Json store class for reservations"""
    def __init__(self):
        super().__init__()
        self.file_path = JSON_FILES_PATH + "store_reservation.json"

    def add_reservation(self, reservation):
        """finds a reservation"""
        reservation_find = self.find("_HotelReservation__localizer", reservation.localizer)
        if reservation_find:
            raise HotelManagementException("Reservation already exists")
        super().add(reservation)

    def find_reservation(self, key, value):
        """finds a reservation in the store"""
        self.load()
        return self.find(key, value)

    @property
    def data_l(self):
        return self._data_l