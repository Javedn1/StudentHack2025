"""
The class for <expectation>
"""


class Expectation:

    # ----------------------------------------------------------------------------------

    def __init__(self, form_submission: str) -> None:
        """
        Whether the response is triggered by a form submission
        Boolean
        """
        if form_submission.lower() == "true":
            self.__form_submission = True
        else:
            self.__form_submission = False

        """
        The list containing all the messages
        """
        self.__messages = []

    @property
    def form_submission(self):
        """
        Get __form_submission
        :param: None
        :return: __form_submission
        """
        return self.__form_submission

    @form_submission.setter
    def form_submission(self, form_submission):
        """
        Set __form_submission
        :param: form_submission: The new form_submission
        :return: None
        """
        if form_submission.lower() == "true":
            self.__form_submission = True
        elif form_submission.lower() == "false":
            self.__form_submission = False

    def add_message(self, message):
        """
        Add message to self.messages
        :param: message: The message to be added
        :return: None
        """
        self.__messages.append(message)

    @property
    def messages(self):
        """
        Get self.messages
        :param: None
        :return: messages: self.messages
        """
        return self.__messages
