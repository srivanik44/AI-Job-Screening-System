import React from "react";

const MatchModal = ({ show, onClose, matchScore }) => {
  if (!show) return null;  // If modal is not shown, return nothing

  return (
    <div className="modal-backdrop">
      <div className="modal-box">
        <h4>Match Score</h4>
        <p><strong>CV matches {matchScore ? `${matchScore}%` : "0"} with JD.</strong></p>
        <button className="btn btn-secondary" onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default MatchModal;
