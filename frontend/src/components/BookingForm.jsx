import React, { useState, useEffect } from 'react';
import { FaHotel, FaCalendarAlt, FaBed } from 'react-icons/fa';
import AOS from 'aos';
import 'aos/dist/aos.css';

export default function BookingForm({ setConfirmed, setDetails }) {
  const [form, setForm] = useState({
    name: '', phone: '', address: '',
    checkIn: '', checkOut: '', roomType: ''
  });

  useEffect(() => {
    AOS.init({ duration: 800 });
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch('http://localhost:5000/book', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    });
    const data = await res.json();
    if (data.status === 'success') {
      setConfirmed(true);
      setDetails({ ...form, pdf: data.pdf });
    } else {
      alert(data.message);
    }
  };

  return (
    <div className="container py-5 d-flex justify-content-center align-items-center vh-100 bg-light">
      <div className="card shadow-lg p-4 w-100" style={{ maxWidth: '600px' }} data-aos="fade-up">
        <h3 className="text-center mb-4 text-primary"><FaHotel className="me-2" />Hotel VNR Room Booking</h3>

        <form onSubmit={handleSubmit}>
          {['name', 'phone', 'address'].map((field, i) => (
            <div className="mb-3" key={i}>
              <label className="form-label">
                {field.charAt(0).toUpperCase() + field.slice(1)}
              </label>
              <input name={field} className="form-control" onChange={handleChange} required />
            </div>
          ))}

          <div className="row">
            {['checkIn', 'checkOut'].map((field, i) => (
              <div className="col-md-6 mb-3" key={i}>
                <label className="form-label">
                  <FaCalendarAlt className="me-1" />
                  {field === 'checkIn' ? 'Check-In' : 'Check-Out'} Date
                </label>
                <input type="date" name={field} className="form-control" onChange={handleChange} required />
              </div>
            ))}
          </div>

          <div className="mb-4">
            <label className="form-label"><FaBed className="me-1" />Room Type</label>
            <select className="form-select" name="roomType" onChange={handleChange} required>
              <option value="">Select Room Type</option>
              <option value="Standard Non-AC">Standard Non-AC - ₹3500</option>
              <option value="Standard AC">Standard AC - ₹4000</option>
              <option value="Suite Non-AC">Suite Non-AC - ₹4500</option>
              <option value="Suite AC">Suite AC - ₹5000</option>
            </select>
          </div>

          <button type="submit" className="btn btn-primary w-100">Book Now</button>
        </form>
      </div>
    </div>
  );
}
