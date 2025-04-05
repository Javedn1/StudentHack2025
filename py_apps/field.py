"""
The class for <field>
We use field_attribute instead of attribute to field_name variables to avofield_id common field_names, e.g. class, which are both keywords in Python and HTML

@TODO Perhaps add function log(), which prints out/returns the details of <field>, e.g. id, name, class, xpath etc. 
"""


class Field:

    # ----------------------------------------------------------------------------------

    def __init__(self, field_id: str, field_name: str, field_class: str, field_xpath: str, field_type: str, value: str, default_index: str, default_value: str, text: str) -> None:
        """
        id of field
        """
        self.__field_id = field_id

        """
        The name of the field
        """
        self.__field_name = field_name

        """
        The class of the field
        """
        self.__field_class = field_class

        """
        The xpath of the field
        """
        self.__field_xpath = field_xpath

        """
        The type of the field: 
        1. text
        2. number
        3. text-area
        4. password
        5. radio
        6. select-one
        7. select-multiple
        8. check-box
        9. button
        10. submit
        11. html-div
        12. hidden
        """
        self.__field_type = field_type.lower()

        """
        The attribute value of the field
        """
        self.__value = value

        """
        The index(es) of the default field(s)
        For select-box, check-box and radio buttons only
        """
        self.__default_index = default_index.split(",")

        """
        The value(s) of the default field(s)
        For select-box, check-box and radio buttons only
        """
        self.__default_value = default_value.split(",")

        """
        The display text of the field
        """
        self.__text = text

    @property
    def field_id(self):
        """
        Get __field_id
        :param: None
        :return: __field_id
        """
        return self.__field_id

    @field_id.setter
    def field_id(self, field_id):
        """
        Set __field_id
        :param: field_id: The new field_id
        :return: None
        """
        self.__field_id = field_id

    @property
    def field_name(self):
        """
        Get __field_name
        :param: None
        :return: __field_name
        """
        return self.__field_name

    @field_name.setter
    def field_name(self, field_name):
        """
        Set __field_name
        :param: field_name: The new field_name
        :return: None
        """
        self.__field_name = field_name

    @property
    def field_class(self):
        """
        Get __field_class
        :param: None
        :return: __field_class
        """
        return self.__field_class

    @field_class.setter
    def field_class(self, field_class):
        """
        Set __field_class
        :param: field_class: The new field_class
        :return: None
        """
        self.__field_class = field_class

    @property
    def field_xpath(self):
        """
        Get __field_xpath
        :param: None
        :return: __field_xpath
        """
        return self.__field_xpath

    @field_xpath.setter
    def field_xpath(self, field_xpath):
        """
        Set __field_xpath
        :param: field_xpath: The new field_xpath
        :return: None
        """
        self.__field_xpath = field_xpath

    @property
    def field_type(self):
        """
        Get __field_type
        :param: None
        :return: __field_type
        """
        return self.__field_type

    @field_type.setter
    def field_type(self, field_type):
        """
        Set __field_type
        :param: field_type: The new field_type
        :return: None
        """
        self.__field_type = field_type

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
        :param: value: The new value
        :return: None
        """
        self.__value = value

    @property
    def default_index(self):
        """
        Get __default_index
        :param: None
        :return: __default_index
        """
        return self.__default_index

    @default_index.setter
    def default_index(self, default_index):
        """
        Set __default_index
        :param: default_index: The new default_index
        :return: None
        """
        self.__default_index = default_index

    @property
    def default_value(self):
        """
        Get __default_value
        :param: None
        :return: __default_value
        """
        return self.__default_value

    @default_value.setter
    def default_value(self, default_value):
        """
        Set __default_value
        :param: default_value: The new default_value
        :return: None
        """
        self.__default_value = default_value

    @property
    def text(self):
        """
        Get __text
        :param: None
        :return: __text
        """
        return self.__text

    @text.setter
    def text(self, text):
        """
        Set __text
        :param: text: The new text
        :return: None
        """
        self.__text = text.lower()
