from uc3m_logistics.attributes import Attribute
from uc3m_travel import hotel_management_exception


class NumDays(Attribute):
    def __init__(self, attr_value):
        self._validation_pattern = r""
        self._error_message = ""
        self.attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        try:
            days = int(attr_value)
        except ValueError as ex:
            raise hotel_management_exception.HotelManagementException("Invalid num_days datatype") from ex
        if (days < 1 or days > 10):
            raise hotel_management_exception.HotelManagementException("Numdays should be in the range 1-10")
        return attr_value