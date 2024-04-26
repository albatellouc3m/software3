''' Class HotelStay (GE2.2) '''
from datetime import datetime
import hashlib
from uc3m_travel.storage.checkout_json_store import CheckoutJsonStore
from uc3m_travel.hotel_reservation import HotelReservation
from uc3m_travel.storage.stay_json_store import StayJsonStore
from uc3m_logistics.attribute_room_key import RoomKey
from uc3m_travel.hotel_management_exception import HotelManagementException
class HotelStay():
    """Class for representing hotel stays"""
    def __init__(self,
                 idcard:str,
                 localizer:str):
        """constructor for HotelStay objects"""
        self.__alg = "SHA-256"
        self.__idcard = idcard
        self.__localizer = localizer
        reservation = HotelReservation.load_from_localizer(self.__localizer)
        if reservation.id_card != self.__idcard:
            raise HotelManagementException("Error: Localizer is not correct for this IdCard")
        self.__type = reservation.room_type
        justnow = datetime.utcnow()
        self.__arrival = datetime.timestamp(justnow)
        date_today = datetime.strptime(reservation.arrival, "%d/%m/%Y")
        if date_today.date() != justnow.date():
            raise HotelManagementException("Error: today is not reservation date")
        #timestamp is represented in seconds.miliseconds
        #to add the number of days we must express num_days in seconds
        self.__departure = self.__arrival + (reservation.num_days * 24 * 60 *
                                             60)
        self.__room_key = hashlib.sha256(self.__signature_string().encode()).hexdigest()

    def __signature_string(self):
        """Composes the string to be used for generating the key for the room"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",localizer:" + \
            self.__localizer + ",arrival:" + str(self.__arrival) + \
            ",departure:" + str(self.__departure) + "}"

    @property
    def id_card(self):
        """Property that represents the product_id of the patient"""
        return self.__idcard

    @id_card.setter
    def id_card(self, value):
        self.__idcard = value

    @property
    def localizer(self):
        """Property that represents the order_id"""
        return self.__localizer

    @localizer.setter
    def localizer(self, value):
        self.__localizer = value

    @property
    def arrival(self):
        """Property that represents the phone number of the client"""
        return self.__arrival
    @arrival.setter
    def arrival(self, value):
        self.__arrival = value

    @property
    def room_key(self):
        """Returns the sha256 signature of the date"""
        return self.__room_key
    @room_key.setter
    def room_key(self, value):
        self.__room_key = value

    @property
    def departure(self):
        """Returns the issued at value"""
        return self.__departure

    @departure.setter
    def departure(self, value):
        """returns the value of the departure date"""
        self.__departure = value


    @classmethod
    def get_stay(cls, room_key: str):
        """instance method for getting a stay"""
        json_checkout = CheckoutJsonStore()
        if json_checkout.find_it("room_key", room_key):
            raise HotelManagementException("Guest is already out")

        stay = StayJsonStore()
        stay_inf = stay.find_checkout("_HotelStay__room_key", RoomKey(room_key).attr_value)

        if not stay_inf:
            raise HotelManagementException("Error: room key not found")
        date_dep = datetime.fromtimestamp(stay_inf["_HotelStay__departure"])
        date_ex = datetime.utcnow().date()
        if date_dep.date() != date_ex:
            raise HotelManagementException("Error: today is not the departure day")
        return HotelStay

    @classmethod
    def checkout(cls, room_key: str):
        """instance method for checking out"""
        json_checkout = CheckoutJsonStore()
        room_checkout = {
            "room_key": room_key,
            "checkout_time": datetime.utcnow().timestamp()}
        json_checkout.add(room_checkout)
