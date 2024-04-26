"""This module contains the definition of the ArrivalDate attribute"""
from uc3m_logistics.attributes import Attribute
from uc3m_travel import hotel_management_exception


class CreditCard(Attribute):
    def __init__(self, attr_value):
        self._validation_pattern = r"^[0-9]{16}"
        self._error_message = "Invalid credit card format"
        self.attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        super()._validate(attr_value)
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(attr_value)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        if not checksum % 10 == 0:
            raise hotel_management_exception.HotelManagementException("Invalid credit card number (not luhn)")
        return attr_value