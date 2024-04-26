from uc3m_logistics.attributes import Attribute
class RoomKey(Attribute):
    """Definition of attribute PhoneNumber"""
    def __init__(self, attr_value):
        """Definition of attribute PhoneNumber init"""
        self._validation_pattern = r'^[a-fA-F0-9]{64}$'
        self._error_message = "Invalid room key format"
        self.attr_value = self._validate(attr_value)