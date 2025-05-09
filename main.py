import os, sys
from flask import Flask, request, render_template
from pypdf import PdfReader 
import json
from resumeparser import ats_extractor

sys.path.insert(0, os.path.abspath(os.getcwd()))


UPLOAD_PATH = r"__DATA__"
os.makedirs(UPLOAD_PATH, exist_ok=True)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/process", methods=["POST"])
def ats():
    if 'pdf_doc' not in request.files:
        return "No file part in request", 400

    doc = request.files['pdf_doc']

    if doc.filename == '':
        return "No file selected", 400

    if not doc.filename.lower().endswith(".pdf"):
        return "Invalid file format. Please upload a PDF.", 400

    save_path = os.path.join(UPLOAD_PATH, "file.pdf")
    doc.save(save_path)

    # Check if file was actually saved and is not empty
    if os.path.getsize(save_path) == 0:
        return "Uploaded file is empty", 400

    try:
        data = _read_file_from_path(save_path)
        data = ats_extractor(data)
        return render_template('index.html', data=json.loads(data))
    except Exception as e:
        return f"An error occurred while processing the PDF: {str(e)}", 500
 
def _read_file_from_path(path):
    reader = PdfReader(path) 
    data = ""

    for page_no in range(len(reader.pages)):
        page = reader.pages[page_no] 
        data += page.extract_text()

    return data 


if __name__ == "__main__":
    app.run(port=8000, debug=True)
