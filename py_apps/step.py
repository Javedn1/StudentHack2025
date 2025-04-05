"""
The class for <step>
"""


class Step:

    # ----------------------------------------------------------------------------------

    def __init__(self, access_by: str, key: str, value: str) -> None:
        """
        How the field is accessed by: id, name, class, xpath
        """
        self.__access_by = access_by.lower()

        """
        The id/name/class/xpath of the field to be operated on
        """
        self.__key = key

        """
        The value to be inputted to the element
        """
        self.__value = value

    @property
    def access_by(self):
        """
        Get __access_by
        :param: None
        :return: __access_by
        """
        return self.__access_by

    @access_by.setter
    def access_by(self, access_by):
        """
        Set __access_by
        :param: access_by: id/name/class/xpath
        :return: None
        """
        self.__access_by = access_by.lower()

    @property
    def key(self):
        """
        Get __key
        :param: None
        :return: __key
        """
        return self.__key

    @key.setter
    def key(self, key):
        """
        Set __key
        :param: key: The new key
        :return: None
        """
        self.__key = key

    @property
    def value(self):
        """
        Get __value
        :param: None
        :return: __value
        """
        return self.__value

    @value.setter
    def value(self, value):
        """
        Set __value
        :param: value
        :return: None
        """
        self.__value = value
