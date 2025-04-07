from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.parser import extract_text, extract_email, extract_name, extract_role
from utils.matcher import get_match_score
from utils.emailer import send_interview_email

app = Flask(__name__)
CORS(app)

stored_jd_text = None  # To temporarily hold JD content

# ---------------------- JD Upload -----------------------
@app.route("/upload-jd", methods=["POST"])

def upload_jd():
    global stored_jd_text
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No JD file uploaded"}), 400

    stored_jd_text = extract_text(file)
    role = extract_role(stored_jd_text)  # ✅ extract role from JD

    return jsonify({"message": "JD uploaded and stored successfully", "role": role})

# ---------------------- CV Upload + Match -----------------------
@app.route("/upload-cv", methods=["POST"])
def upload_cv():
    global stored_jd_text, extracted_name

    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No CV file uploaded"}), 400

    try:
        cv_text = extract_text(file)
        if not cv_text.strip():
            return jsonify({"error": "Could not extract text from CV."}), 400

        match_score = get_match_score(cv_text, stored_jd_text)
        email = extract_email(cv_text)
        name = extract_name(cv_text)

        if not email:
            return jsonify({"error": "Email could not be extracted from CV."}), 400

        return jsonify({
            "match_score": round(match_score * 100, 2),
            "email": email,
            "name": name
        })

    except Exception as e:
        print("❌ Error processing CV:", e)
        return jsonify({"error": "Failed to process the CV file."}), 500

# ---------------------- Interview Email Sender -----------------------
@app.route("/send-interview-email", methods=["POST"])
def schedule_interview():
    data = request.get_json()
    email = data.get("email")
    match_score = data.get("match_score")
    name = data.get("name", "Candidate")
    role = data.get("role", "a position")

    if match_score >= 50:
        result = send_interview_email(name, email, role)
        return jsonify({"message": result})
    else:
        return jsonify({"message": "Match score too low. Interview not scheduled."}), 400

if __name__ == "__main__":
    app.run(debug=True)
