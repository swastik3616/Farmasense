import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getUserFarms } from '../../services/api';

function MyFarms() {
  const [farms, setFarms] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchFarms();
  }, []);

  const fetchFarms = async () => {
    try {
      const res = await getUserFarms();
      setFarms(res.data);
    } catch (err) {
      console.error("Error fetching farms:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header" style={{ marginBottom: '16px' }}>
        <h1 className="page-title">My Farms</h1>
        <button className="btn btn-primary" onClick={() => navigate('/farmer/add-farm')} style={{ width: 'auto', padding: '10px 16px' }}>
          + Add New
        </button>
      </div>

      {loading ? (
        <div style={{ textAlign: "center", padding: 40 }}>Loading...</div>
      ) : (
        <div className="farm-list">
          {farms.length === 0 ? (
            <div className="alert-card warning">
              <p>You haven't registered any farms yet.</p>
            </div>
          ) : (
            farms.map(farm => (
              <div key={farm.id} className="farm-card">
                <div className="farm-info">
                  <h3>{farm.name || "Unnamed Farm"}</h3>
                  <p>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                      <polyline points="2 17 12 22 22 17"></polyline>
                      <polyline points="2 12 12 17 22 12"></polyline>
                    </svg>
                    {farm.land_size_acres} Acres • {farm.district}, {farm.state}
                  </p>
                  <p>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path>
                    </svg>
                    {farm.water_source} • {farm.soil_type}
                  </p>
                </div>
                <div>
                  <button className="btn" style={{ background: 'var(--gray-light)', padding: '8px 16px' }} onClick={() => navigate(`/farmer/farm/${farm.id}`)}>
                    View
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default MyFarms;
