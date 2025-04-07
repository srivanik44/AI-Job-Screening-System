// src/components/MatchModal.js
import React from "react";

const MatchModal = ({ show, onClose }) => {
  if (!show) return null;

  return (
    <div className="modal-backdrop">
      <div className="modal-box">
        <h4>Match Score</h4>
        <p><strong>CV matches 85%</strong> with JD.</p>
        <button className="btn btn-secondary" onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default MatchModal;
