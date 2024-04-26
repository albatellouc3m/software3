from uc3m_logistics.attributes import Attribute
class PhoneNumber(Attribute):
    """Definition of attribute PhoneNumber"""
    def __init__(self, attr_value):
        """Definition of attribute PhoneNumber init"""
        self._validation_pattern = r"^(\+)[0-9]{9}"
        self._error_message = "Invalid phone number format"
        self.attr_value = self._validate(attr_value)