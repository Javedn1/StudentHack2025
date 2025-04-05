"""
The class for <message>
"""


class Message:
    def __init__(self, access_by: str, key: str, language: str, message_type: str, value: str) -> None:
        """
        How the field to be expected is accessed by: id, name, class
        """
        self.__access_by = access_by.lower()

        """
        The id/name of the expected element to be checked
        """
        self.__key = key

        """
        The expected language of the expected value of the returned element
        Language: en
        """
        self.__language = language

        """
        The type of the expected value of the HTML element to be compared with the attribute "value" in <message>
        2 types: 
        1. attribute (attribute value of the HTML element)
        2. text (display of the HTML element)
        """
        self.__message_type = message_type

        """
        The expected value of the returned element
        This will be stored in between <message> and </message> in xml files
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
        :param: access_by: id/name
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
    def language(self):
        """
        Get __language
        :param: None
        :return: __language
        """
        return self.__language

    @language.setter
    def language(self, language):
        """
        Set __language
        :param: language
        :return: None
        """
        self.__language = language

    @property
    def message_type(self):
        """
        Return __message_type
        :param: None
        :return: __message_type
        """
        return self.__message_type

    @message_type.setter
    def message_type(self, message_type):
        """
        Set __message_type
        :param: message_type: attribute/text
        :return: None
        """
        self.__message_type = message_type

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
