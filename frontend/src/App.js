import React, { useState } from "react";
import "./App.css";
import { FaFileUpload, FaEnvelope } from "react-icons/fa";
import UploadCard from "./components/UploadCard";
import MatchModal from "./components/MatchModal";
import axios from "axios";
import logo from "./assets/logo.png";

function App() {
  const [showMatchModal, setShowMatchModal] = useState(false);
  const [matchScore, setMatchScore] = useState(null);
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [role, setRole] = useState("");

  const handleScheduleInterview = async () => {
    if (matchScore && matchScore >= 50) {
      try {
        const response = await axios.post("http://localhost:5000/send-interview-email", {
          email,
          match_score: matchScore,
          name,
          role
        });
        alert(response.data.message);
      } catch (error) {
        alert("❌ Failed to send interview email.");
        console.error(error);
      }
    } else {
      alert("Match score is below 50%. No interview scheduled.");
    }
  };

  return (
    <div className="app-container">
      <div className="header">
        <img src={logo} alt="AI Logo" className="logo" />
        <h1>AI Job Screening System</h1>
        <p>Match CVs with JDs + Schedule Real Interviews!</p>
      </div>

      <div className="upload-section">
        <UploadCard
          title="Upload Job Description (.pdf/.docx)"
          icon={<FaFileUpload />}
          uploadEndpoint="http://localhost:5000/upload-jd"
          onSuccess={(data) => {
            if (data.role) {
              setRole(data.role); // ✅ save role
            }
          }}
        />
        <UploadCard
          title="Upload Candidate CV (.pdf/.docx)"
          icon={<FaFileUpload />}
          uploadEndpoint="http://localhost:5000/upload-cv"
          onSuccess={(data) => {
            setMatchScore(data.match_score);
            setEmail(data.email);
            setName(data.name); // ✅ save name
            setShowMatchModal(true); // ✅ show modal on successful upload
          }}
        />
      </div>

      <div className="action-buttons">
        {matchScore !== null && (
          <button className="btn btn-success" onClick={handleScheduleInterview}>
            <FaEnvelope /> Schedule Interview
          </button>
        )}
      </div>

      <MatchModal
        show={showMatchModal}
        onClose={() => setShowMatchModal(false)}
        matchScore={matchScore}
      />
    </div>
  );
}

export default App;
