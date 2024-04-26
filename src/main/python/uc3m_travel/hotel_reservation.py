"""Hotel reservation class"""
import hashlib
from datetime import datetime
from freezegun import freeze_time
from uc3m_travel.storage.reservation_json_store import ReservationJsonStore
from uc3m_logistics.attribute_arrival_date import ArrivalDate
from uc3m_logistics.attribute_credit_card import CreditCard
from uc3m_logistics.attribute_idcard import IDCard
from uc3m_logistics.attribute_localizer import Localizer
from uc3m_logistics.attribute_name_surname import NameSurname
from uc3m_logistics.attribute_num_days import NumDays
from uc3m_logistics.attribute_phone_number import PhoneNumber
from uc3m_logistics.attribute_room_type import RoomType
from uc3m_travel.hotel_management_exception import HotelManagementException
class HotelReservation:
    """Class for representing hotel reservations"""
    #pylint: disable=too-many-arguments, too-many-instance-uc3m_logistics
    def __init__(self,
                 id_card:str,
                 credit_card_number:str,
                 name_surname:str,
                 phone_number:str,
                 room_type:str,
                 arrival:str,
                 num_days:int):
        """constructor of reservation objects"""
        self.__credit_card_number = CreditCard(credit_card_number).attr_value
        self.__id_card = IDCard(id_card).attr_value
        justnow = datetime.utcnow()
        self.__arrival = ArrivalDate(arrival).attr_value
        self.__reservation_date = datetime.timestamp(justnow)
        self.__name_surname = NameSurname(name_surname).attr_value
        self.__phone_number = PhoneNumber(phone_number).attr_value
        self.__room_type = RoomType(room_type).attr_value
        self.__num_days = NumDays(num_days).attr_value
        self.__localizer =  hashlib.md5(str(self).encode()).hexdigest()

    def __str__(self):
        """return a json string with the elements required to calculate the localizer"""
        #VERY IMPORTANT: JSON KEYS CANNOT BE RENAMED
        json_info = {"id_card": self.__id_card,
                     "name_surname": self.__name_surname,
                     "credit_card": self.__credit_card_number,
                     "phone_number:": self.__phone_number,
                     "reservation_date": self.__reservation_date,
                     "arrival_date": self.__arrival,
                     "num_days": self.__num_days,
                     "room_type": self.__room_type,
                     }
        return "HotelReservation:" + json_info.__str__()
    @property
    def credit_card(self):
        """property for getting and setting the credit_card number"""
        return self.__credit_card_number
    @credit_card.setter
    def credit_card(self, value):
        self.__credit_card_number = value

    @property
    def id_card(self):
        """property for getting and setting the id_card"""
        return self.__id_card
    @id_card.setter
    def id_card(self, value):
        self.__id_card = value

    @property
    def localizer(self):
        """Returns the md5 signature"""
        return self.__localizer
    @property
    def room_type(self):
        """property for getting and setting the room type"""
        return self.__room_type

    @property
    def num_days(self):
        """property for getting and setting the number of days"""
        return self.__num_days

    @property
    def arrival(self):
        """property for getting and setting the arrival date"""
        return self.__arrival
    @arrival.setter
    def arrival(self, value):
        self.__arrival = value

    @classmethod
    def load_from_localizer(cls, localizer):
        """Returns a HotelReservation object from a localizer"""
        reservation = ReservationJsonStore()
        reservation_info = reservation.find_reservation("_HotelReservation__localizer",Localizer(localizer).attr_value)
        if reservation_info is None:
            raise HotelManagementException("Error: localizer not found")
        else:
            reservation_date = datetime.fromtimestamp(reservation_info["_HotelReservation__reservation_date"])

        with freeze_time(reservation_date):
            reservation_new = cls(reservation_info["_HotelReservation__id_card"],
                       reservation_info["_HotelReservation__credit_card_number"],
                       reservation_info["_HotelReservation__name_surname"],
                       reservation_info["_HotelReservation__phone_number"],
                       reservation_info["_HotelReservation__room_type"],
                       reservation_info["_HotelReservation__arrival"],
                       reservation_info["_HotelReservation__num_days"])
            if reservation_new.localizer != localizer:
                raise HotelManagementException("Error: reservation has been "
                                               "manipulated")
            return reservation_new


