"""
The class for <test>
"""
from step import Step
from expectation import Expectation


class Test:

    # ----------------------------------------------------------------------------------

    def __init__(self, test_id: int, description: str, run: str, language="en") -> None:
        """
        id of the test
        """
        self.__test_id = test_id

        """
        The description of the test: compulsory, general, submission
        For reporting. Have no use in testing
        """
        self.__description = description

        """
        Whether this test is to be run or skipped
        Default: True
        """
        if run.lower() == "true":
            self.__run = True
        else:
            self.__run = False

        """
        What language this test uses: en
        """
        self.__language = language

        """
        The list containing instances of Step
        """
        self.__steps = []

        """
        The list containing instances of Expectation
        """
        self.__expectations = []

    @property
    def test_id(self):
        """
        Get __test_id
        :param: None
        :return: __test_id
        """
        return self.__test_id

    @test_id.setter
    def test_id(self, test_id):
        """
        Set __test_id
        :param: test_id: The new test_id
        :return: None
        """
        self.__test_id = test_id

    @property
    def description(self):
        """
        Get __description
        :param: None
        :return: __description
        """
        return self.__description

    @description.setter
    def description(self, description):
        """
        Set __description
        :param: description: The new description
        :return: None
        """
        self.__description = description

    @property
    def run(self):
        """
        Get __run
        :param: None
        :return: __run
        """
        return self.__run

    @run.setter
    def run(self, run):
        """
        Set __run
        :param: run: The new run
        :return: None
        """
        self.__run = run

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

    def add_step(self, step: Step):
        """
        Add the instance of Step to __steps
        :param: step: The instance of Step to be added to list
        :return: None
        """
        self.__steps.append(step)

    def add_expectation(self, expectation: Expectation):
        """
        Add the instance of Expectation to __expectations
        :param: expectation: The instance of Expectation to be added to list
        :return: None
        """
        self.__expectations.append(expectation)

    @property
    def steps(self):
        """
        Get __steps
        :param: None
        :return: __steps
        """
        return self.__steps

    @property
    def expectations(self):
        """
        Get __expectations
        :param: None
        :return: __expectations
        """
        return self.__expectations
