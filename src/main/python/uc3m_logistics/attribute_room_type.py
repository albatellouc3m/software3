from uc3m_logistics.attributes import Attribute
class RoomType(Attribute):
    """Definition of attribute PhoneNumber"""
    def __init__(self, attr_value):
        """Definition of attribute PhoneNumber init"""
        self._validation_pattern = r"(SINGLE|DOUBLE|SUITE)"
        self._error_message = "Invalid roomtype value"
        self.attr_value = self._validate(attr_value)