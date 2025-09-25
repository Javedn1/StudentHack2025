from flask import Flask, render_template, request, send_file
from py_apps.main import read_xml_file_paths
from py_apps.web_tester import WebTester
import os
from openai import OpenAI
from dotenv import load_dotenv
import base64
import google.generativeai as genai


load_dotenv()

GEMINI_API_KEY = os.getenv('AI_KEY')

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
    
    # Fetch advice from AI
    # Cannot be done on demo
    client = genai.Client(
        api_key=GEMINI_API_KEY,
    )

    model = "gemini-2.0-flash-thinking-exp-01-21"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"With the given json output from a testing, provide a short feedback: {web_tester_json_outputs}"),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    ai_response = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        ai_response += chunk.text  # It is similar to buffer where each chunk has a limited size and when combined, these chunks form a sentence

    return render_template("./test_result/index.html", test_data=web_tester_json_outputs, ai_message=ai_response)

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
