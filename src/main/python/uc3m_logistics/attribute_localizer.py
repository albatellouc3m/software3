from uc3m_logistics.attributes import Attribute
class Localizer(Attribute):
    """Definition of attribute PhoneNumber"""
    def __init__(self, attr_value):
        """Definition of attribute PhoneNumber init"""
        self._validation_pattern = r'^[a-fA-F0-9]{32}$'
        self._error_message = "Invalid localizer"
        self.attr_value = self._validate(attr_value)