"""
The class for <webform>
"""


class Webform:
    def __init__(self, url: str, form_id: str, timeout: int, submission_timeout: int, browsers: str) -> None:
        self.__url = url
        self.__form_id = form_id  # The id attribute of <form>, not the id of <webform>
        self.__timeout = timeout
        self.__submission_timeout = submission_timeout

        if isinstance(browsers, str):
            # browsers = "A,B,C,D"
            # Not supposed to happen
            self.__browsers = browsers.split(",")
        else:
            # browsers = ["A", "B". "C", "D"]
            self.__browsers = browsers

        """
        The list containing all the fields
        """
        self.__fields = []

        """
        The list containing all the tests
        """
        self.__tests = []

    @property
    def url(self):
        """
        Get the url of the webform
        :param: None
        :return: url: url of the website
        """
        return self.__url

    @url.setter
    def url(self, url):
        """
        Set the url of the webform
        :param: url: url of the website
        :return: None
        """
        self.__url = url

    @property
    def form_id(self):
        """
        Get the form_id of the webform
        :param: None
        :return: form_id: id attribute of the form of the website
        """
        return self.__form_id

    @form_id.setter
    def form_id(self, form_id):
        """
        Set the form_id of the webform
        :param: form_id: id attribute of the form of the website
        :return: None
        """
        self.__form_id = form_id

    @property
    def timeout(self):
        """
        Get the timeout of the webform
        :param: None
        :return: timeout: timeout of the website
        """
        return self.__timeout

    @timeout.setter
    def timeout(self, timeout):
        """
        Set the timeout of the webform
        :param: timeout: timeout of the website
        :return: None
        """
        self.__timeout = timeout

    @property
    def submission_timeout(self):
        """
        Get the submission_timeout of the webform
        :param: None
        :return: submission_timeout: submission_timeout of the website
        """
        return self.__submission_timeout

    @submission_timeout.setter
    def submission_timeout(self, submission_timeout):
        """
        Set the submission_timeout of the webform
        :param: submission_timeout: submission_timeout of the website
        :return: None
        """
        self.__submission_timeout = submission_timeout

    @property
    def browsers(self):
        """
        Get the browsers of the webform
        :param: None
        :return: browsers: browsers of the website
        """
        return self.__browsers

    @browsers.setter
    def browsers(self, browsers):
        """
        Set the browsers of the webform
        :param: browsers: browsers of the website
        :return: None
        """
        self.__browsers = browsers

    def add_field(self, field):
        """
        Add field to self.fields
        :param: field: field to be added
        :return: None
        """
        self.__fields.append(field)

    @property
    def fields(self):
        """
        Return self.fields
        :param: None
        :return: fields: self.__fields
        """
        return self.__fields

    def find_field(self, access_by, key):
        """
        With the given information, find the instance of field from fields which matches the requirements
        :param: access_by: by id/name/class(not recommended)/xpath
        :param: key: id/name/class(not recommended)/xpath of the field
        """
        for field in self.fields:
            field_key = ""

            if access_by == "id":
                field_key = field.field_id
            elif access_by == "name":
                field_key = field.field_name
            elif access_by == "class":
                # Not recommended
                field_key = field.field_class
            elif access_by == "xpath":
                field_key = field.field_xpath
            else:
                # Invalid access_by
                raise Exception(f"Invalid <step> access_by: {access_by}")

            if field_key == key:
                return field

        raise Exception(
            f"Cannot locate <field> with access_by = {access_by} and key = {key}")

    def add_test(self, test):
        """
        Add test to self.tests
        :param: test: test to be added
        :return: None
        """
        self.__tests.append(test)

    @property
    def tests(self):
        """
        Return self.tests
        :param: None
        :return: tests: self.__tests
        """
        return self.__tests
