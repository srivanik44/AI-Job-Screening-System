import React, { useRef } from "react";
import axios from "axios";

const UploadCard = ({ title, icon, uploadEndpoint, onSuccess }) => {
  const fileInputRef = useRef();

  const handleUpload = async () => {
    const file = fileInputRef.current.files[0];
    if (!file) {
      alert("Please select a file to upload.");
      return;
    }

    // ✅ File type validation
    const allowedTypes = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];
    if (!allowedTypes.includes(file.type)) {
      alert("Only PDF and DOCX files are allowed.");
      return;
    }

    // ✅ File size validation (5MB max)
    const maxSize = 5 * 1024 * 1024;
    if (file.size > maxSize) {
      alert("File size exceeds 5MB limit.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post(uploadEndpoint, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      alert("✅ File uploaded successfully!");
      if (onSuccess) {
        onSuccess(response.data);
      }
    } catch (err) {
      alert("❌ Upload failed. Try again.");
      console.error("Upload error:", err);
    }
  };

  return (
    <div className="upload-card">
      <h5>{icon} {title}</h5>
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,.docx"
        className="form-control my-2"
      />
      <button className="btn btn-primary" onClick={handleUpload}>Upload</button>
    </div>
  );
};

export default UploadCard;
