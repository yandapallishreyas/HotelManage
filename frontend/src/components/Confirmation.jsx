import React from 'react';
import { FaCheckCircle, FaDownload } from 'react-icons/fa'; // Ensure react-icons is installed

export default function Confirmation({ details }) {
  const handleDownload = () => {
    window.open(`http://localhost:5000/download/${details.pdf}`, '_blank');
  };

  return (
    <div className="d-flex justify-content-center align-items-center vh-100 bg-light">
      <div className="card shadow-lg p-4" style={{ maxWidth: '500px', width: '100%' }}>
        <div className="text-center">
          <FaCheckCircle size={60} color="green" className="mb-3" />
          <h3 className="text-success mb-3">Booking Confirmed!</h3>
          <p className="lead">Thank you, <strong>{details.name}</strong>.<br />
          Your <strong>{details.roomType}</strong> has been booked from <strong>{details.checkIn}</strong> to <strong>{details.checkOut}</strong>.</p>
          <button className="btn btn-primary mt-3" onClick={handleDownload}>
            <FaDownload className="me-2" /> Download Confirmation PDF
          </button>
        </div>
      </div>
    </div>
  );
}
