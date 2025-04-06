"""
The class for web tester
"""
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import lxml
from .field import Field
from .test import Test
from .step import Step
from .expectation import Expectation
from .webform import Webform
from .message import Message
import time


class WebTester:

    # ===========================================================================
    def __init__(self, file_path: str, timeout=60, submission_timeout=20) -> None:
        """
        The file path of the xml file to be read
        """
        self.__file_path = file_path

        """
        The webdriver
        """
        self.__web_driver = None

        """
        The list containing <webform>
        """
        self.__webforms = []

        """
        The url of the last <webform>
        If the url of the current webform is the same as last_url, we do not need to close the browser
        """
        self.__last_url = ""

        """
        The browser of the last <webform>
        If the browser of the webform changes, even if there is only 1 url, we still need to init_webdriver()
        """
        self.__last_browser = ""

        """
        The browsers for this testing
        Also know as useragents in <webforms>
        """
        self.__browsers = []

        """
        The time at which run() is invoked
        """
        self.__start_time = 0

        self.__json_output = {
            "xml_config": {}, 
            "errors": [], 
            "test_result": {
                "webform": {}
            }, 
            "stats": {
                "test_num": -1, 
                "test_failure_num": -1, 
                "test_error_num": -1, 
                "test_skipped_num": -1
            }, 
            "total_time": -1, 
            "finished_at": -1
        }

    @staticmethod
    def log(mode=1, message="", enabled=False):
        """
        Log/Print out the message with the corresponding mode
        Mode: 
        0 - [ERROR]
        1 - [INFO]
        2 - [TEST]
        3 - [EXPECTATION]
        """
        if not enabled:
            return

        # The final message to be printed
        log_message = ""
        if mode == 0:
            # [ERROR]
            log_message += "[ERROR] "
        elif mode == 1:
            # [INFO]
            log_message += "[INFO] "
        elif mode == 2:
            # [TEST]
            log_message += "[TEST] "
        else:
            # [EXPECTATION]
            log_message += "[EXPECT] "

        log_message += str(message)
        print(log_message)

    def run(self):
        """
        Invoke read_xml_config() and fill_web()
        :param: None
        :return: None
        """
        self.__start_time = datetime.datetime.now()

        self.read_xml_config()
        self.print_xml_config()
        self.fill_web()
        self.conclude()

    def read_xml_config(self):
        """
        Read the xml file with file path stored in __file_path
        :param: None
        :return: None
        """
        try:
            WebTester.log(1, "Scanning for projects ...")
            WebTester.log()
            WebTester.log(
                1, "-----------------< web_tester:web_tester >-----------------")
            WebTester.log(1, f"xml file path: {self.__file_path}")
            WebTester.log()
            self.__json_output["xml_file_path"] = self.__file_path

            with open(self.__file_path, "r") as f:
                file = f.read()  # Read the file

            xml_reader = BeautifulSoup(file, "xml")
        except Exception as e:
            WebTester.log(0, f"Error in reading file: {e}")
            self.__json_output["errors"].append(f"Error in reading file: {e}")

        self.__browsers = WebTester.extract_from_tag(
            xml_reader.find("webforms"), "useragents").split(",")  # Ensure self.__browsers is a list rather than a String

        # Read <webform>
        webforms = xml_reader.find_all("webform")

        # try-catch is to surround <test> rather than <webform> as we want the testings continue if 1 test fails
        for w in webforms:
            # print("webform = ", webform)
            # print(type(webform))

            try:
                # Instantiate Webform
                webform = Webform(url=WebTester.extract_from_tag(w, "url"), form_id=WebTester.extract_from_tag(w, "formid"), timeout=WebTester.extract_from_tag(
                    w, "timeout"), submission_timeout=WebTester.extract_from_tag(w, "submissiontimeout"), browsers=self.__browsers)
                webform_children = w.findChildren()

                for webform_child in webform_children:
                    # print("child = ", webform_child)
                    # Look for <field>, <test>

                    if webform_child.name == "fieldset":
                        # Read <field>
                        fields = webform_child.findChildren()
                        for f in fields:
                            field = Field(field_id=WebTester.extract_from_tag(f, "id"), field_name=WebTester.extract_from_tag(f, "name"), field_class=WebTester.extract_from_tag(f, "class"), field_xpath=WebTester.extract_from_tag(f, "xpath"), field_type=WebTester.extract_from_tag(
                                f, "type"), value=WebTester.extract_from_tag(f, "value"), default_index=WebTester.extract_from_tag(f, "defaultindex"), default_value=WebTester.extract_from_tag(f, "defaultvalue"), text=f.text)
                            webform.add_field(field)
                    elif webform_child.name == "tests":
                        # Read <test>
                        tests = webform_child.findChildren()
                        for t in tests:
                            if t.name != "test":
                                # Prevent xml_reader from scanning <step> now
                                continue

                            test = Test(test_id=WebTester.extract_from_tag(t, "id"), description=WebTester.extract_from_tag(
                                t, "description"), run=WebTester.extract_from_tag(t, "run"), language=WebTester.extract_from_tag(t, "language"))
                            test_children = t.findChildren()
                            for test_child in test_children:
                                # print("test_child = ", test_child)
                                if test_child.name == "step":
                                    # Read <step>
                                    step = Step(access_by=WebTester.extract_from_tag(test_child, "accessby"), key=WebTester.extract_from_tag(
                                        test_child, "key"), value=WebTester.extract_from_tag(test_child, "value"))
                                    test.add_step(step)
                                elif test_child.name == "expectation":
                                    # Read <expectation>
                                    expectation = Expectation(
                                        WebTester.extract_from_tag(test_child, "formsubmission"))

                                    messages = test_child.findChildren()

                                    for m in messages:
                                        message = Message(access_by=WebTester.extract_from_tag(m, "accessby"), key=WebTester.extract_from_tag(
                                            m, "key"), language=WebTester.extract_from_tag(m, "language"), message_type=WebTester.extract_from_tag(m, "type"), value=m.text)
                                        expectation.add_message(message)

                                    test.add_expectation(expectation)
                            webform.add_test(test)
                self.__webforms.append(webform)
            except Exception as e:
                WebTester.log(0, f"Error in read_xml_config(): {e}")
                self.__json_output["errors"].append(f"Error in read_xml_config(): {e}")

    def fill_web(self):
        """
        With the filled data, use selenium to fill in the webpage
        :param: None
        :return: None
        """
        WebTester.log(1)
        WebTester.log(1)
        WebTester.log(
            1, "------------------------------------------------------------")
        WebTester.log(1, " T E S T S")
        WebTester.log(
            1, "------------------------------------------------------------")
        WebTester.log(
            1, "Running comp10120_selenium_test.py-apps.web_tester.py")

        # Attribute "form_submission" of last <expectation>
        # If last_form_submission == True, then we need to init_web_driver() cause we are not at the same webpage
        last_form_submission = True

        for browser in self.__browsers:
            # 1 - browser
            # 2 - webform
            for webform in self.__webforms:
                # Number of tests run for this <webform>
                test_num = 0

                # Number of test failures
                test_failure_num = 0

                # Number of test errors
                test_error_num = 0

                # Number of test skipped
                test_skipped_num = 0

                if webform.url != self.__last_url or browser != self.__last_browser:
                    # Create the web driver

                    # Close the current web_driver if there is
                    self.close_webdriver()
                    # No need to init_webdriver if webform.url = __last_url
                    self.init_webdriver(
                        browser, webform.url, webform.timeout)

                    # Set last_url
                    self.__last_url = self.__web_driver.current_url

                    # Set last_browser
                    self.__last_browser = browser

                for test in webform.tests:
                    try:
                        test_num += 1
                        if not last_form_submission:
                            # Reset webform
                            self.reset_webform(webform.fields)

                        # Fill HTML elements with selenium
                        for step in test.steps:
                            # Run <step>
                            if step.access_by == "id":
                                # Find element by id
                                by = By.ID
                            elif step.access_by == "name":
                                # Find element by name
                                by = By.NAME
                            elif step.access_by == "class":
                                # Find element by class (not recommended)
                                by = By.CLASS_NAME
                            elif step.access_by == "xpath":
                                # Find element by xpath
                                by = By.XPATH
                            else:
                                # Invalid access_by for this stage
                                # might update this as the programme improves and adds more identifier
                                WebTester.log(
                                    0, f"Invalid <step> access_by: {step.access_by}")
                                self.__json_output["errors"].append(f"Invalid <step> access_by: {step.access_by}")
                                test_error_num += 1

                            element = self.__web_driver.find_element(
                                by, step.key)
                            # print(
                            # f"After getting element in <step>, web_driver.url = {self.__web_driver.current_url}")
                            field = webform.find_field(
                                step.access_by, step.key)

                            # Determine the action to be taken on the element
                            # We do not care about the element if its type = html-div or type = hidden
                            action = ""
                            if field.field_type == "text" or field.field_type == "number" or field.field_type == "password":
                                action = "type"
                            elif field.field_type == "radio" or field.field_type == "check-box" or field.field_type == "button" or field.field_type == "submit":
                                action = "click"
                            elif field.field_type == "select-one" or field.field_type == "select-multiple":
                                action = "select"

                            # print(
                            # f"step: action = {step.action}; value = {step.value}")
                            if action == "type":
                                # Type by sending keys
                                element.send_keys(step.value)
                            elif action == "click":
                                # Click by click(). Could be use to control buttons
                                element.click()
                            elif action == "select":
                                # Select select box by select_by_value()
                                element = Select(element)
                                element.select_by_value(step.value)
                            else:
                                # Skip the test
                                raise Exception(
                                    f"Invalid <step> action, field_type: {field.field_type}")

                        # Wait for a few seconds to allow the browser to go to next page
                        time.sleep(1)

                        # Check <expectation>
                        # print("expectations = ", test.expectations)
                        for expectation in test.expectations:
                            # Check <expectation>
                            # There should be 1 <expectation> for each test right now
                            for message in expectation.messages:
                                # Check <message>

                                if message.access_by == "id":
                                    # Find element by id
                                    by = By.ID
                                elif message.access_by == "name":
                                    # Find element by name
                                    by = By.NAME
                                elif message.access_by == "xpath":
                                    # Find element by xpath
                                    by = By.XPATH
                                elif message.access_by == "class":
                                    # Find element by class (not recommended)
                                    by = By.CLASS_NAME
                                else:
                                    # Invalid access_by for this stage
                                    # might update this as the programme improves and adds more identifier
                                    pass

                                if expectation.form_submission:
                                    # form_submission = True so need to wait the webpage to get element
                                    element = WebDriverWait(self.__web_driver, webform.submission_timeout).until(
                                        expected_conditions.presence_of_element_located((by, message.key)))
                                else:
                                    # form_submission = False so get element in the normal way
                                    element = self.__web_driver.find_element(
                                        by, message.key)

                                # Check whether the value in <message> matches that in HTML element
                                WebTester.log(1)
                                WebTester.log(
                                    1, "=================== [Test Result] ===================")
                                WebTester.log(2, f"webform.url: {webform.url}")
                                self.__json_output["test_result"]["webform"]["url"] = webform.url
                                WebTester.log(
                                    2, f"webform.form_id: {webform.form_id}")
                                self.__json_output["test_result"]["webform"]["form_id"] = webform.form_id
                                WebTester.log(2, f"webform.browser: {browser}")
                                self.__json_output["test_result"]["webform"]["browser"] = browser
                                WebTester.log(2, f"test_id = {test.test_id}")
                                self.__json_output["test_result"]["test_id"] = test.test_id

                                if message.message_type == "text":
                                    WebTester.log(
                                        2, f"Test passed: {message.value == element.text}")
                                    self.__json_output["test_result"]["message_type"] = "text"
                                    self.__json_output["test_result"]["test_passed"] = message.value == element.text
                                    self.__json_output["test_result"]["expected_value"] = element.text
                                    self.__json_output["test_result"]["actual_value"] = message.value
                                    self.__json_output["test_result"]["error_message"] = ""

                                    if message.value != element.text:
                                        # Test failure
                                        test_failure_num += 1
                                        # Show HTML element display
                                        WebTester.log(
                                            2, f"element.text: {element.text}")
                                        WebTester.log(
                                            2, f"message.value: {message.value}")

                                elif message.message_type == "attribute":
                                    WebTester.log(
                                        2, f"Test passed: {message.value == element.get_attribute('value')}")
                                    self.__json_output["test_result"]["message_type"] = "attribute"
                                    self.__json_output["test_result"]["test_passed"] = message.value == element.get_attribute('value')
                                    self.__json_output["test_result"]["expected_value"] = element.get_attribute('value')
                                    self.__json_output["test_result"]["actual_value"] = message.value
                                    self.__json_output["test_result"]["error_message"] = ""

                                    if message.value != element.get_attribute("value"):
                                        # Test failure
                                        test_failure_num += 1
                                        # Show HTML element attribute "value"
                                        WebTester.log(
                                            2, f"element.value: {element.get_attribute('value')}")
                                        WebTester.log(
                                            2, f"message.value: {message.value}")

                                else:
                                    WebTester.log(2, "Test passed: False")
                                    WebTester.log(
                                        0, f"Invalid message type: {message.message_type}")
                                    self.__json_output["test_result"]["message_type"] = message.message_type
                                    self.__json_output["test_result"]["test_passed"] = False
                                    self.__json_output["test_result"]["expected_value"] = ""
                                    self.__json_output["test_result"]["actual_value"] = ""
                                    self.__json_output["test_result"]["error_message"] = f"Invalid message type: {message.message_type}"
                                    test_error_num += 1
                                WebTester.log(
                                    1, "=====================================================")
                                WebTester.log(1)

                            # Set last_form_submission
                            last_form_submission = expectation.form_submission

                    except Exception as e:
                        test_error_num += 1
                        WebTester.log(
                            0, f"Error in running <test>. test_id: {test.test_id}")
                        WebTester.log(0, f"Error: {e}")
                        self.__json_output["errors"].append(f"Error: {e}")
                        continue  # Continue running other <test>

                WebTester.log(
                    2, f"Tests run: {test_num}, Failures: {test_failure_num}, Errors: {test_error_num}, Skipped: {test_skipped_num} - in comp10120_selenium_test.py-apps.web_tester.py")
                self.__json_output["stats"]["test_num"] = test_num
                self.__json_output["stats"]["test_failure_num"] = test_failure_num
                self.__json_output["stats"]["test_error_num"] = test_error_num
                self.__json_output["stats"]["test_skipped_num"] = test_skipped_num

        # The above logic does not close the last web_driver. Thus, we need to close it manually at the end of this function
        self.close_webdriver()

        # Just in case
        # Quit all things, including web_driver
        if self.__web_driver != None:
            WebTester.log(1)
            WebTester.log(
                1, "-----------------------------------------------------")
            WebTester.log(1, "Quitting web driver")
            self.__web_driver.quit()
            self.__web_driver = None
            WebTester.log(
                1, "-----------------------------------------------------")
            WebTester.log(1)

    def print_xml_config(self):
        """
        Print the xml content read
        :param: None
        :return: None
        """
        WebTester.log(1, f"Reading SNAPSHOT from {self.__file_path}")
        WebTester.log(
            1, "===================== <xml> =====================")
        self.__json_output["xml_config"] = {}
        self.__json_output["xml_config"]["file_path"] = self.__file_path
        self.__json_output["xml_config"]["webforms"] = []
        for webform in self.__webforms:
            # Print out the <webform> read
            WebTester.log(1)
            WebTester.log(
                1, "===================== <webform> =====================")
            webform_json = {}  # For self.__json_output
            WebTester.log(1, f"url = {webform.url}")
            webform_json["url"] = webform.url
            WebTester.log(1, f"form_id = {webform.form_id}")
            webform_json["form_id"] = webform.form_id
            WebTester.log(1, f"timeout = {webform.timeout}")
            webform_json["timeout"] = webform.timeout
            WebTester.log(
                1, f"submission_timeout = {webform.submission_timeout}")
            webform_json["submission_timeout"] = webform.submission_timeout
            WebTester.log(1, f"browsers = {webform.browsers}")
            webform_json["browsers"] = webform.browsers

            webform_json["fields"] = []
            for field in webform.fields:
                # Print out the <field> read
                WebTester.log(1)
                WebTester.log(
                    1, "===================== <field> =====================")
                field_json = {}
                WebTester.log(1, f"id = {field.field_id}")
                field_json["id"] = field.field_id
                WebTester.log(1, f"name = {field.field_name}")
                field_json["name"] = field.field_name
                WebTester.log(1, f"class = {field.field_class}")
                field_json["class"] = field.field_class
                WebTester.log(1, f"xpath = {field.field_xpath}")
                field_json["xpath"] = field.field_xpath
                WebTester.log(1, f"type = {field.field_type}")
                field_json["type"] = field.field_type
                WebTester.log(1, f"value = {field.value}")
                field_json["value"] = field.value
                if field.field_type == "radio" or field.field_type == "select-multiple" or field.field_type == "select-one" or field.field_type == "check-box":
                    WebTester.log(
                        1, f"default_index = {field.default_index}")
                    field_json["default_index"] = field.default_index
                    WebTester.log(
                        1, f"default_value = {field.default_value}")
                    field_json["default_value"] = field.default_value
                else:
                    field_json["default_index"] = ""
                    field_json["default_value"] = ""
                WebTester.log(1, f"text = {field.text}")
                field_json["text"] = field.text
                WebTester.log(
                    1, "=====================================================")
                webform_json["fields"].append(field_json)

            webform_json["tests"] = []
            for test in webform.tests:
                # Print out the <test> read
                WebTester.log(1)
                WebTester.log(
                    1, "===================== <test> =====================")
                test_json = {}
                WebTester.log(1, f"id = {test.test_id}")
                test_json["id"] = test.test_id
                WebTester.log(1, f"description = {test.description}")
                test_json["description"] = test.description
                WebTester.log(1, f"run = {test.run}")
                test_json["run"] = test.run
                WebTester.log(1, f"language = {test.language}")
                test_json["language"] = test.language

                test_json["steps"] = []
                for step in test.steps:
                    # Print out the <step> read
                    WebTester.log(1)
                    WebTester.log(
                        1, "===================== <step> =====================")
                    step_json = {}
                    WebTester.log(1, f"access_by = {step.access_by}")
                    step_json["access_by"] = step.access_by
                    WebTester.log(1, f"key = {step.key}")
                    step_json["key"] = step.key
                    WebTester.log(1, f"value = {step.value}")
                    step_json["value"] = step.value
                    WebTester.log(
                        1, "=====================================================")
                    test_json["steps"].append(step_json)

                test_json["expectations"] = []
                for expectation in test.expectations:
                    # Print out the <expectation> read
                    WebTester.log(1)
                    WebTester.log(
                        1, "===================== <expectation> =====================")
                    expectation_json = {}
                    WebTester.log(1,
                                  f"form_submission = {expectation.form_submission}")
                    expectation_json["form_submission"] = expectation.form_submission

                    expectation_json["messages"] = []
                    for message in expectation.messages:
                        # Print out the <message> read
                        WebTester.log(1)
                        WebTester.log(
                            1, "===================== <message> =====================")
                        message_json = {}
                        WebTester.log(
                            1, f"access_by = {message.access_by}")
                        message_json["access_by"] = message.access_by
                        WebTester.log(1, f"key = {message.key}")
                        message_json["key"] = message.key
                        WebTester.log(
                            1, f"language = {message.language}")
                        message_json["language"] = message.language
                        WebTester.log(1,
                                      f"type = {message.message_type}")
                        message_json["type"] = message.message_type
                        WebTester.log(1, f"value = {message.value}")
                        message_json["value"] = message.value

                        WebTester.log(
                            1, "=====================================================")
                        expectation_json["messages"].append(message_json)

                WebTester.log(
                    1, "=====================================================")
                test_json["expectations"].append(expectation_json)

            WebTester.log(
                1, "=====================================================")
            webform_json["tests"].append(test_json)
        self.__json_output["xml_config"]["webforms"].append(webform_json)

    @staticmethod
    def extract_from_tag(tag, attribute: str) -> str:
        """
        Given a tag, extract the data of the designated attribute and return it
        :param: tag: The tag to be extracted; Type: <class 'bs4.element.Tag'>
        :param: attribute: The attribute of the tag to be extracted
        :return: value: The value of the attribute in the tag
        """
        try:
            return tag[attribute]
        except Exception as e:
            return ""

    def reset_webform(self, fields: list) -> None:
        """
        We do not use fields as sometimes, a <step> will affect more than 1 control and using fields does not ensure the form is reseted completely. 
        After non-submission testing, reset the fields so that the browser does not need to be closed, saving a lot of time
        :param: fields: test.fields
        :return: None
        """

        # Skip this function if null is passed
        if len(fields) == 0:
            return

        for field in fields:
            try:
                # Reset every element to its default value
                key = ""  # id/name/class (not recommended)/xpath
                if field.field_id != "":
                    # Find element by ID
                    by = By.ID
                    key = field.field_id
                elif field.field_name != "":
                    # Find element by name
                    by = By.NAME
                    key = field.field_name
                elif field.field_xpath != "":
                    # FInd element by xpath
                    by = By.XPATH
                    key = field.field_xpath
                elif field.field_class != "":
                    # Find element by class (not recommended)
                    by = By.CLASS_NAME
                    key = field.field_class
                else:
                    # Invalid attribute
                    # print(
                    #     f"[ERROR] No available identifier of <field>: {field}")
                    # continue
                    raise Exception(
                        f"No available identifier of <field>: {field}")

                # Locate the element
                element = self.__web_driver.find_element(by, key)

                # Check the type of element as different types of element have different actions and default value(s)
                """
                4 Categories: 
                1. Send keys (text, number, text-area, password, hidden)
                2. Select item(s) (select-multiple, select-one, check-box)
                3. Click button by values (radio)
                4. Those who cannot be set (button, html-div, submit)
                Note: 
                - To change the attribute "value" of an element, one cannot do element.value = ... directly. 
                This is becaseSelenium imitates a user, who cannot change the value of attributes
                - To change the value(s) of attribute(s), one can do: 
                    1. self.__web_driver.execute_script("arguments[0].value = ...", element)
                    2. self.__web_driver.execute_script("document.getElementById() ...")
                """
                if field.field_type == "text" or field.field_type == "number" or field.field_type == "text-area" or field.field_type == "password" or field.field_type == "hidden":
                    # Reset attribute "value", e.g. for userSession, i.e. input
                    if field.value == "":
                        # Set value to null
                        self.__web_driver.execute_script(
                            "arguments[0].value = '';", element)
                    else:
                        # Set value to default value
                        self.__web_driver.execute_script(
                            "arguments[0].value = '" + str(field.value) + "';", element)

                    # Reset text
                    # First set text to null
                    element.clear()

                    if field.text != "":
                        # Send keys
                        # Set text to default value
                        element.send_keys(field.text)

                elif field.field_type == "select-multiple" or field.field_type == "select-one" or field.field_type == "check-box":
                    # Deselect all items
                    # Does not matter whether there are default items to be selected
                    element = Select(element)
                    element.deselect_all()

                    # Select default options
                    if len(field.default_index) > 0:
                        # We use default index
                        for index in field.default_index:
                            # Select each item
                            element.select_by_index(index)
                    elif len(field.default_value) > 0:
                        # We use default value
                        for value in field.default_value:
                            # Select each item
                            element.select_by_value(value)
                    # TODO: Add select_by_visible_by_text?
                    else:
                        # Both default_index and default_value = ""
                        pass
                elif field.field_type == "radio":
                    # Deselct radio button
                    self.__web_driver.execute_script(
                        "arguments[0].checked = false;", element)

                    # Click by value
                    if field.value != "":
                        # Click item
                        element.click()
                    else:
                        # Invalid value for radio
                        raise Exception(
                            f"Invalid null value for radio button, field_id: {field.field_id}")
                else:
                    # Invalid field_type but as expected so no need to raise Exception
                    # raise Exception(
                    #     print(f"Invalid field_type: {field.field_type}"))
                    # WebTester.log(1)
                    # WebTester.log(
                    #     1, "=====================================================")
                    # WebTester.log(
                    #     3, f"Expected invalid field_type: {field.field_type}")
                    # WebTester.log(
                    #     1, "=====================================================")
                    # WebTester.log(1)
                    continue

            except Exception as e:
                # Could be a real error or not
                # There might be a chance that the element to be found is only generated after a specific action, e.g. the error message after entering invalid login password, and cannot be found in most situations
                #TODO: Might need to update self.__output_json here
                WebTester.log(
                    1, "=====================================================")
                WebTester.log(
                    1, "=========== [Skip resetting HTML element] ===========")
                WebTester.log(3, f"id = {field.field_id}")
                WebTester.log(3, f"name = {field.field_name}")
                WebTester.log(3, f"class = {field.field_class}")
                WebTester.log(3, f"xpath = {field.field_xpath}")
                WebTester.log(3, f"type = {field.field_type}")
                WebTester.log(
                    1, "=====================================================")
                # WebTester.log(
                #     1, "=====================================================")
                # WebTester.log(0, f"Error in reset_webform(): {e}")
                # WebTester.log(
                #     1, "=====================================================")
                continue

    def init_webdriver(self, browser: str, url: str, timeout: int) -> None:
        """
        Initialise a web_driver depending on the browser required
        :param: browser: A String that indicates what browser to be initialised
        :return: None
        """
        try:
            # Set web driver type
            if browser.lower() == "firefox":
                self.__web_driver = webdriver.Firefox()
            elif browser.lower() == "edge":
                self.__web_driver = webdriver.Edge()
            elif browser.lower() == "safari":
                self.__web_driver = webdriver.Safari()
            else:
                # Default: Chrome
                self.__web_driver = webdriver.Chrome()

            # Set the timeout if the page is not available
            self.__web_driver.set_page_load_timeout(timeout)

            # Visit the required url
            self.__web_driver.get(url)
        except Exception as e:
            WebTester.log(0, f"Error in init_webdriver(): {e}")
            WebTester.log(
                1, "=====================================================")
            self.__json_output["errors"].append(f"Error in init_webdriver(): {e}")

    def close_webdriver(self) -> None:
        """
        This closes the web_driver
        :param: None
        :return: None
        """
        if self.__web_driver != None:
            # Close the current browser window
            # Did not use quit() which closes all browser windows and ends driver's session
            WebTester.log(1)
            WebTester.log(
                1, "-----------------------------------------------------")
            WebTester.log(1, f"Closing web driver")
            self.__web_driver.close()
            WebTester.log(
                1, "-----------------------------------------------------")
            WebTester.log(1)

    def conclude(self) -> None:
        """
        Print out the conclusion, e.g. Total time and time at which programme is finished
        :param: None
        :return: None
        """
        WebTester.log(
            1, "-----------------------------------------------------")
        WebTester.log(
            1, f"Total time: {(datetime.datetime.now() - self.__start_time).seconds} s")
        self.__json_output["total_time"] = (datetime.datetime.now() - self.__start_time).seconds
        WebTester.log(1, f"Finished at: {datetime.datetime.now()}")
        self.__json_output["finished_at"] = datetime.datetime.now()
        WebTester.log(
            1, "-----------------------------------------------------")
    
    def get_json(self) -> dict:
        """
        Get the json format of the data logged

        :return: The dict object containing the console output
        """
        return self.__json_output
