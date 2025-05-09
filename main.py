import re
import pdfplumber
#import spacy
from typing import List, Optional
from pydantic import BaseModel
import json



# Load spaCy NLP model
#nlp = spacy.load("en_core_web_sm")

# --- Define a Pydantic model for the extracted data (for validation + standards) ---
class ResumeData(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    skills: List[str]
    education: List[str]
    experience: List[str]

# --- File Readers ---
def read_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def read_file(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return read_pdf(file_path)
    else:
        raise ValueError("Unsupported file format")

<<<<<<< HEAD
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
=======
# --- Extractors ---

def extract_name(text: str) -> Optional[str]:
    # Get the first 5 lines to find the name
    lines = text.strip().split("\n")
    for line in lines[:5]:
        line = line.strip()
        # Ignore lines that are clearly email, phone, links, etc.
        if re.search(r'\b[\w.-]+@[\w.-]+\.\w+\b', line):
            continue
        if re.search(r'\+?\d[\d\s-]+\d', line):
            continue
        if "linkedin.com" in line.lower() or "github.com" in line.lower():
            continue
        # Assume first clean line is the name
        if line:
            return line
    return None
>>>>>>> parent of 6652a63 (Frontend made with Flask)

def extract_email(text: str) -> Optional[str]:
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

def extract_phone(text: str) -> Optional[str]:
    match = re.search(r'(\+?\d{1,3}[\s-]?)?\(?\d{2,4}\)?[\s-]?\d{3,4}[\s-]?\d{3,4}', text)
    return match.group(0) if match else None

# def extract_name(text: str) -> Optional[str]:
#     doc = nlp(text)
#     for ent in doc.ents:
#         if ent.label_ == "PERSON":
#             return ent.text
#     return None

def extract_skills(text: str, skills_list: List[str]) -> List[str]:
    text = text.lower()
    skills_found = []
    for skill in skills_list:
        if skill.lower() in text:
            skills_found.append(skill)
    return skills_found

def extract_education(text: str) -> List[str]:
    education_keywords = [
        "bachelor", "master", "b.sc", "m.sc", "b.tech", "m.tech",
        "phd", "mba", "b.e", "m.e", "bachelor's degree", "master's degree", "university", "college"
    ]
    found = []
    for line in text.split("\n"):
        for keyword in education_keywords:
            if keyword.lower() in line.lower():
                found.append(line.strip())
                break
    return found

def extract_experience(text: str) -> List[str]:
    experience_sections = []
    exp_keywords = ["experience", "work history", "employment"]
    lines = text.lower().split("\n")
    start = False
    for line in lines:
        if any(kw in line for kw in exp_keywords):
            start = True
            continue
        if start:
            if line.strip() == "":
                break
            experience_sections.append(line.strip())
    return experience_sections

# --- Master Parser ---
def parse_resume(file_path: str, skills_list: List[str]) -> ResumeData:
    text = read_file(file_path)
    
    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text, skills_list)
    education = extract_education(text)
    experience = extract_experience(text)

    return ResumeData(
        name=name,
        email=email,
        phone=phone,
        skills=skills,
        education=education,
        experience=experience
    )


def save_json(data: ResumeData, filename: str):
    """ Save the parsed resume data as a JSON file. """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data.dict(), f, ensure_ascii=False, indent=4)

def main():
    skills_list = ["Python", "Java", "Machine Learning", "SQL", "AWS", "Docker", "Kubernetes", "JavaScript", "React"]

    file_path = "sample_resume\GayathriBhat.pdf"
    print("Starting resume parsing...")

    try:
        parsed_data = parse_resume(file_path, skills_list)
        print("Parsed Resume:")
        print(parsed_data.model_dump_json(indent=4))

        save_json(parsed_data, "parsed_resume.json")
    except Exception as e:
        print("Error:", e)

if __name__=="__main__":
    main()