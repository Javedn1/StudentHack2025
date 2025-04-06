from flask import Flask, render_template, request, send_file
from py_apps.main import read_xml_file_paths
from py_apps.web_tester import WebTester
import os

xml_file_paths = []

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/build_xml")
def build_xml():
    return render_template("build_xml/index.html")

@app.route("/run_test", methods=["POST"])
def run_test():
    if "files" not in request.files:
        return f"No XML files uploaded"
    
    files = request.files.getlist("files")
    if not files:
        return f"No selected files"
    
    uploaded_files = []
    for file in files:
        if file and file.filename.endswith('.xml'):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            uploaded_files.append(filename)
        else:
            return "Invalid file format. Only XML files are allowed"

    # Read web-testing-config.xml
    xml_file_paths = read_xml_file_paths(file_path=uploaded_files[0], is_multiple_xml_files=False)  # Hardcoded

    web_tester_json_outputs = []

    # Run the code
    # Multiple case
    for xml_file_path in xml_file_paths:
        web_tester = WebTester(xml_file_path)
        web_tester.run()
        web_tester_json_outputs.append(web_tester.get_json())

    return render_template("./test_result/index.html", test_data=web_tester_json_outputs, ai_message="")

@app.route("/template_file", methods=["GET"])
def template_file():
    return send_file("./templates/template_file/template.xml")

#TODO: To be removed
@app.route("/dummy", methods=["GET"])
def dummy():
    # Read web-testing-config.xml
    xml_file_paths = read_xml_file_paths()  # Hardcoded

    web_tester_json_outputs = []

    # Run the code
    # Multiple case
    for xml_file_path in xml_file_paths:
        web_tester = WebTester(xml_file_path)
        web_tester.run()
        web_tester_json_outputs.append(web_tester.get_json())

    return str(web_tester_json_outputs)