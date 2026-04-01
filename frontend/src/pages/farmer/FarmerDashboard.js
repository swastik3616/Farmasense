import React, { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { getUserFarms } from '../../services/api';
import { useNavigate } from 'react-router-dom';

function FarmerDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [farms, setFarms] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFarms();
  }, []);

  const fetchFarms = async () => {
    try {
      const res = await getUserFarms();
      setFarms(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Welcome back!</h1>
          <p style={{ color: 'var(--gray)', margin: 0 }}>Here is your farm overview.</p>
        </div>
      </div>

      <div className="summary-cards">
        <div className="stat-card">
          <div className="icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="3" y1="9" x2="21" y2="9"></line>
              <line x1="9" y1="21" x2="9" y2="9"></line>
            </svg>
          </div>
          <div className="stat-value">{loading ? '-' : farms.length}</div>
          <div className="stat-label">Active Farms</div>
        </div>
        
        <div className="stat-card">
          <div className="icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
              <line x1="12" y1="9" x2="12" y2="13"></line>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
          </div>
          <div className="stat-value">0</div>
          <div className="stat-label">New Alerts</div>
        </div>
      </div>

      <h3>Recent Alerts</h3>
      {loading ? (
        <p>Loading alerts...</p>
      ) : (
        farms.length > 0 ? (
          <div>
             <div className="alert-card warning">
                <p style={{ margin: 0, fontWeight: 600 }}>Weather Update</p>
                <div className="error-text" style={{ color: 'var(--dark)' }}>Expected rain tomorrow. Consider delaying irrigation.</div>
             </div>
             <button className="btn btn-primary" onClick={() => navigate('/farmer/farms')} style={{ marginTop: '20px' }}>
                View My Farms
             </button>
          </div>
        ) : (
          <div className="alert-card" style={{ textAlign: 'center', padding: '40px 20px' }}>
            <p>You haven't added any farms yet.</p>
            <button className="btn btn-primary" onClick={() => navigate('/farmer/add-farm')} style={{ width: 'auto', marginTop: '10px' }}>
              Add Your First Farm
            </button>
          </div>
        )
      )}
    </div>
  );
}

export default FarmerDashboard;
