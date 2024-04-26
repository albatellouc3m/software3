
"""Module for the hotel manager"""
import json
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_logistics.attribute_arrival_date import ArrivalDate
from uc3m_logistics.attribute_credit_card import CreditCard
from uc3m_logistics.attribute_idcard import IDCard
from uc3m_logistics.attribute_localizer import Localizer
from uc3m_logistics.attribute_name_surname import NameSurname
from uc3m_logistics.attribute_num_days import NumDays
from uc3m_logistics.attribute_phone_number import PhoneNumber
from uc3m_logistics.attribute_room_type import RoomType
from uc3m_travel.storage.reservation_json_store import ReservationJsonStore
from uc3m_travel.storage.stay_json_store import StayJsonStore
from uc3m_travel.hotel_reservation import HotelReservation
from uc3m_travel.hotel_stay import HotelStay

class HotelManager:
    class __HotelManager:
        """Class with all the methods for managing reservations and stays"""
        _instance = None

        def __new__(cls, *args, **kwargs):
            if not cls._instance:
                cls._instance = super().__new__(cls, *args, **kwargs)
            return cls._instance

        def __init__(self):
            if not hasattr(self, 'initialized'):
                self.initialized = True

        def load_json_store(self, file_path):
            try:
                with open(file_path, "r", encoding="utf-8", newline="") as file:
                    file_contents = json.load(file)
            except FileNotFoundError:
                raise HotelManagementException("Wrong file or file path")
            except json.JSONDecodeError as ex:
                raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex
            return file_contents

        # pylint: disable=too-many-arguments
        def room_reservation(self,
                             credit_card: str,
                             name_surname: str,
                             id_card: str,
                             phone_number: str,
                             room_type: str,
                             arrival_date: str,
                             num_days: int) -> str:

            id_card = IDCard(id_card)
            room_type = RoomType(room_type)
            name_surname = NameSurname(name_surname)
            credit_card = CreditCard(credit_card)
            arrival_date = ArrivalDate(arrival_date)
            num_days = NumDays(num_days)
            phone_number = PhoneNumber(phone_number)
            my_reservation = HotelReservation(id_card=id_card.attr_value,
                                              credit_card_number=credit_card.attr_value,
                                              name_surname=name_surname.attr_value,
                                              phone_number=phone_number.attr_value,
                                              room_type=room_type.attr_value,
                                              arrival=arrival_date.attr_value,
                                              num_days=num_days.attr_value)

            # escribo el fichero Json con todos los datos
            existing_reservations = ReservationJsonStore()

            # compruebo que esta reserva no esta en la lista
            if existing_reservations.find_reservation("_HotelReservation__localizer",my_reservation.localizer):
                raise HotelManagementException("Reservation already exists")
            if existing_reservations.find_reservation("_HotelReservation__id_card", my_reservation.id_card):
                raise HotelManagementException("This ID card has another reservation")
            # añado los datos de mi reserva a la lista , a lo que hubiera
            existing_reservations.add(my_reservation.__dict__)
            return my_reservation.localizer

        def guest_arrival(self, file_input: str) -> str:
            """Manages the arrival of a guest with a reservation."""
            try:
                input_list = self.load_json_store(file_input)
                my_localizer = input_list["Localizer"]
                my_id_card = input_list["IdCard"]
            except KeyError as e:
                raise HotelManagementException(
                    "Error - Invalid Key in JSON")

            my_id_card = IDCard(my_id_card).attr_value
            my_localizer = Localizer(my_localizer).attr_value

            # Generar la room key y verificar el check-in
            new_checkin_record = HotelStay(my_id_card, my_localizer)
            stay_json_store = StayJsonStore()

            if stay_json_store.find_stay("room_key", new_checkin_record.room_key):
                raise HotelManagementException("checkin already exists")

            stay_json_store.add(new_checkin_record.__dict__)
            return new_checkin_record.room_key

        def guest_checkout(self, room_key: str) -> bool:
            """manages the checkout of a guest"""
            HotelStay.get_stay(room_key)
            HotelStay.checkout(room_key)
            return True

        instance = None
        def __new__(cls):
            if not HotelManager.instance:
                HotelManager.instance = HotelManager.__HotelManager()
            return HotelManager.instance

        def __getattr__(self, name):
            return getattr(self.instance, name)

        def __setattr__(self, name, value):
            return setattr(self.instance, name, value)
