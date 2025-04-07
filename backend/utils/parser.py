import re
import PyPDF2
import docx

def extract_text(file):
    if file.filename.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text() or ''
        return text

    elif file.filename.endswith('.docx'):
        doc = docx.Document(file)
        return '\n'.join([para.text for para in doc.paragraphs])
    
    return "Unsupported file format"

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

def extract_name(text):
    # Simple heuristic: first line or name after "Name:"
    lines = text.strip().split('\n')
    for line in lines:
        if 'name' in line.lower():
            return line.split(':')[-1].strip()
    return lines[0].strip() if lines else "Candidate"

def extract_role(jd_text):
    patterns = [
        r"(?i)(?:Position|Job Title|Role)\s*[:\-]\s*(.+)",         
        r"(?i)we are looking for a[n]?\s+([^\n.]+)",                
        r"(?i)hiring\s+for\s+([^\n.]+)",                            
    ]
    
    for pattern in patterns:
        match = re.search(pattern, jd_text)
        if match:
            raw_role = match.group(1).strip()
            
            # Clean extra details like skills or company names
            cleaned_role = re.sub(r" with .*", "", raw_role, flags=re.IGNORECASE)  # remove "with ..."
            cleaned_role = re.sub(r" at .*", "", cleaned_role, flags=re.IGNORECASE) # remove "at ..."
            cleaned_role = re.sub(r"[^a-zA-Z ]", "", cleaned_role)                 # remove unwanted symbols
            
            return cleaned_role.strip()

    return "a position"
