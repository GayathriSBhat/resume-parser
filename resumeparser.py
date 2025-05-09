import re
import json

def ats_extractor(text):
    data = {}

    # 1. Full Name (assumed to be first line or near top)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    data["Full Name"] = lines[0] if lines else "Not Found"

    # 2. Email
    email = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    data["Email ID"] = email.group(0) if email else "Not Found"

    # 3. GitHub
    github = re.search(r"https?://(www\.)?github\.com/[^\s)]+", text)
    data["GitHub Portfolio"] = github.group(0) if github else "Not Found"

    # 4. LinkedIn
    linkedin = re.search(r"https?://(www\.)?linkedin\.com/in/[^\s)]+", text)
    data["LinkedIn ID"] = linkedin.group(0) if linkedin else "Not Found"

    # 5. Work Experience: look for keywords
    work_exp_matches = re.findall(r".{0,50}(experience|worked at|employment|internship).{0,100}", text, re.IGNORECASE)
    data["Work Experience"] = list(set(work_exp_matches)) if work_exp_matches else ["Not Found"]

    # 6. Skillset
    skill_section = re.search(r"(skills|technologies|tools)\s*[:\-]?\s*(.+?)(\n\n|\Z)", text, re.IGNORECASE | re.DOTALL)
    if skill_section:
        skills_text = skill_section.group(2)
        skills = re.split(r",|\n|•|-", skills_text)
        data["Skillset"] = [s.strip() for s in skills if s.strip()]
    else:
        data["Skillset"] = ["Not Found"]

    # 7. Projects: naive match
    projects = re.findall(r"(?i)project[:\-]?\s*(.+)", text)
    if not projects:
        # Try to match "Projects" section
        project_section = re.search(r"(projects)\s*[:\-]?\s*(.+?)(\n\n|\Z)", text, re.IGNORECASE | re.DOTALL)
        if project_section:
            project_lines = re.split(r"\n|•|-", project_section.group(2))
            projects = [p.strip() for p in project_lines if p.strip()]
    data["Projects"] = projects if projects else ["Not Found"]

    return json.dumps(data, indent=2)