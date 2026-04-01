import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { sendOtp, verifyOtp } from '../../services/api';

function FarmerLogin() {
  const [mobile, setMobile] = useState('');
  const [otp, setOtp] = useState('');
  const [step, setStep] = useState(1); // 1 = mobile, 2 = otp
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const { loginFarmer } = useAuth();
  const navigate = useNavigate();

  const handleSendOtp = async (e) => {
    e.preventDefault();
    if (mobile.length < 10) {
      setError("Please enter a valid mobile number.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      await sendOtp(mobile);
      setStep(2);
    } catch (err) {
      setError(err.response?.data?.error || "Failed to send OTP. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOtp = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await verifyOtp(mobile, otp);
      // Simulate generic name if backend doesn't provide
      const { token, name, user_id } = res.data;
      loginFarmer(token, name || "Farmer User", user_id);
      navigate("/farmer/dashboard");
    } catch (err) {
      setError(err.response?.data?.error || "Invalid OTP. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-logo">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"></path>
            <path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"></path>
          </svg>
          FarmaSense
        </div>
        <h2 style={{ marginBottom: "20px", color: "var(--dark)" }}>Farmer Portal</h2>
        
        {error && <div className="alert-card danger" style={{ textAlign: "left" }}>{error}</div>}

        {step === 1 ? (
          <form onSubmit={handleSendOtp}>
            <div className="form-group">
              <label>Mobile Number</label>
              <input 
                type="tel" 
                className="form-control" 
                placeholder="Enter 10-digit number"
                value={mobile}
                onChange={(e) => setMobile(e.target.value)}
                required
              />
            </div>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Sending...' : 'Get OTP'}
            </button>
          </form>
        ) : (
          <form onSubmit={handleVerifyOtp}>
            <div className="form-group">
              <label>Enter OTP</label>
              <input 
                type="text" 
                className="form-control" 
                placeholder="6-digit OTP"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                required
              />
              <small style={{ display: 'block', marginTop: 8, color: "var(--gray)" }}>
                Sent to {mobile}. <span style={{ color: "var(--primary)", cursor: "pointer" }} onClick={() => setStep(1)}>Change</span>
              </small>
            </div>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Verifying...' : 'Login'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

export default FarmerLogin;
