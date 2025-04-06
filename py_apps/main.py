"""
The main programme that invokes functions in WebTester
"""
from .web_tester import WebTester
from bs4 import BeautifulSoup

"""
The list containing all the files paths of xml files to be read by web tester
"""
xml_file_paths = []

"""
The file path of the xml file which contains all the testings and details for 1 website
"""
# xml_file_path = "xml-docs/web-testing-epublication.xml"
# xml_file_path = "xml-docs/web-testing-testhtmlform.xml"


def read_xml_file_paths(file_path="xml-docs/web-testing-config.xml", is_multiple_xml_files=True):
    """
    Read the xml configuration file "", which contains all the file path for xml files to be read by web tester
    :param: None
    :return: None
    """
    with open(file_path, "r") as f:
        file = f.read()

    if is_multiple_xml_files:
        xml_reader = BeautifulSoup(file, "xml")
        configuration_files = xml_reader.find_all("configuration-file")

        for cf in configuration_files:
            xml_file_paths.append(cf.text)
        
        return xml_file_paths
    else:
        # Just 1 single configuration file
        return [file_path]


if __name__ == "__main__":
    # Read web-testing-config.xml
    xml_file_paths = read_xml_file_paths()

    # Run the code
    # Multiple case
    for xml_file_path in xml_file_paths:
        web_tester = WebTester(xml_file_path)
        web_tester.run()

    # Single case
    # web_tester = WebTester(xml_file_path)
    # web_tester.run()
