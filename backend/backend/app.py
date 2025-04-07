from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.parser import extract_text, extract_email
from utils.matcher import get_match_score
from utils.emailer import send_interview_email
import smtplib
from email.message import EmailMessage

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
    return jsonify({"message": "JD uploaded and stored successfully"})

# ---------------------- CV Upload + Match -----------------------
@app.route("/upload-cv", methods=["POST"])
def upload_cv():
    global stored_jd_text
    if not stored_jd_text:
        return jsonify({"error": "No JD found. Please upload JD first."}), 400

    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No CV file uploaded"}), 400

    try:
        cv_text = extract_text(file)
        match_score = get_match_score(cv_text, stored_jd_text)

        email = extract_email(cv_text)
        print(f"Extracted email: {email}")

        return jsonify({"match_score": round(match_score * 100, 2), "email": email})
    
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Failed to process the CV file."}), 500

# ---------------------- Interview Email Sender -----------------------
@app.route("/send-interview-email", methods=["POST"])
def send_interview_email_api():
    data = request.json
    email = data.get("email")
    match_score = data.get("match_score")

    if not email or match_score is None:
        return jsonify({"error": "Email and match score are required."}), 400

    if match_score < 50:
        return jsonify({"message": "Match score is below 50%, no interview scheduled."}), 200

    # Send the interview email
    role = "Job Position"  # Customize this based on your system
    try:
        send_interview_email("Candidate Name", email, role)
        return jsonify({"message": f"Interview email sent to {email}"}), 200
    except Exception as e:
        print("Error sending email:", e)
        return jsonify({"error": "Failed to send interview email."}), 500

# ---------------------- Run App -----------------------
if __name__ == "__main__":
    app.run(debug=True)
