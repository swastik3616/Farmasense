import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createFarm } from '../../services/api';

function AddFarm() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [geoLoading, setGeoLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const [formData, setFormData] = useState({
    name: '',
    land_size_acres: '',
    water_source: 'Borewell',
    soil_type: 'Alluvial',
    district: '',
    state: '',
    latitude: '',
    longitude: ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleGetLocation = () => {
    setGeoLoading(true);
    setError(null);
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setFormData(prev => ({
            ...prev,
            latitude: position.coords.latitude.toFixed(6),
            longitude: position.coords.longitude.toFixed(6)
          }));
          setGeoLoading(false);
        },
        (err) => {
          setError("Failed to retrieve location. Please allow location access or map API key.");
          setGeoLoading(false);
        }
      );
    } else {
      setError("Geolocation is not supported by your browser.");
      setGeoLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await createFarm(formData);
      navigate('/farmer/farms');
    } catch (err) {
      setError(err.response?.data?.error || "Failed to add farm");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header" style={{ marginBottom: '16px' }}>
        <h1 className="page-title">Register Farm</h1>
        <button className="btn" style={{ width: 'auto', background: 'var(--gray-light)', padding: '10px 16px' }} onClick={() => navigate(-1)}>
          Cancel
        </button>
      </div>

      <div className="auth-card" style={{ maxWidth: '100%', padding: '24px' }}>
        {error && <div className="alert-card danger">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Farm Name (Optional)</label>
            <input type="text" className="form-control" name="name" value={formData.name} onChange={handleChange} placeholder="e.g. North Field" />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
            <div className="form-group">
              <label>Size (Acres)</label>
              <input type="number" step="0.1" className="form-control" name="land_size_acres" value={formData.land_size_acres} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Water Source</label>
              <select className="form-control" name="water_source" value={formData.water_source} onChange={handleChange}>
                <option value="Borewell">Borewell</option>
                <option value="Canal">Canal</option>
                <option value="Rainfed">Rainfed</option>
                <option value="River">River</option>
              </select>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
            <div className="form-group">
              <label>Soil Type</label>
              <select className="form-control" name="soil_type" value={formData.soil_type} onChange={handleChange}>
                <option value="Alluvial">Alluvial</option>
                <option value="Black Cotton">Black Cotton</option>
                <option value="Red">Red</option>
                <option value="Laterite">Laterite</option>
              </select>
            </div>
            <div className="form-group">
              <label>District</label>
              <input type="text" className="form-control" name="district" value={formData.district} onChange={handleChange} required />
            </div>
          </div>
          
          <div className="form-group">
            <label>State</label>
            <input type="text" className="form-control" name="state" value={formData.state} onChange={handleChange} required />
          </div>

          <div className="alert-card" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <p style={{ margin: 0, fontWeight: 600 }}>Location (Coordinates)</p>
            <p style={{ margin: 0, fontSize: '0.9rem', color: 'var(--gray)' }}>Get accurate weather and advisory data by pinpointing your farm.</p>
            
            <button type="button" className="btn" style={{ background: 'var(--primary-dark)', color: 'white' }} onClick={handleGetLocation} disabled={geoLoading}>
              {geoLoading ? 'Getting Location...' : 'Use My Current Location'}
            </button>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginTop: '8px' }}>
              <input type="text" className="form-control" placeholder="Latitude" name="latitude" value={formData.latitude} onChange={handleChange} required />
              <input type="text" className="form-control" placeholder="Longitude" name="longitude" value={formData.longitude} onChange={handleChange} required />
            </div>
          </div>

          <button type="submit" className="btn btn-primary" style={{ marginTop: '20px' }} disabled={loading}>
            {loading ? 'Saving...' : 'Register Farm'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default AddFarm;
