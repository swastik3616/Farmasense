import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

// Simple SVG Icons
const HomeIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
    <polyline points="9 22 9 12 15 12 15 22"></polyline>
  </svg>
);

const LeafIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"></path>
    <path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"></path>
  </svg>
);

const UserIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
    <circle cx="12" cy="7" r="4"></circle>
  </svg>
);

const LogOutIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
    <polyline points="16 17 21 12 16 7"></polyline>
    <line x1="21" y1="12" x2="9" y2="12"></line>
  </svg>
);


function FarmerLayout() {
  const { user, logout } = useAuth();

  return (
    <div className="farmer-layout">
      {/* Mobile Top Bar */}
      <div className="top-bar" style={{ display: window.innerWidth > 768 ? 'none' : 'flex' }}>
        <div className="logo">FarmaSense</div>
        <div className="user-profile">
          <UserIcon /> {user?.name}
        </div>
      </div>

      {/* Navigation (Sidebar Desktop / Bottom Mobile) */}
      <nav className="bottom-nav">
        {window.innerWidth > 768 && (
          <div className="logo" style={{ padding: '0 16px', fontSize: '1.5rem', fontWeight: 800, color: 'var(--primary-dark)', marginBottom: '40px' }}>
            FarmaSense
          </div>
        )}
        
        <NavLink to="/farmer/dashboard" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <HomeIcon /> <span>Home</span>
        </NavLink>
        
        <NavLink to="/farmer/farms" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <LeafIcon /> <span>My Farms</span>
        </NavLink>
        
        <NavLink to="/farmer/profile" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <UserIcon /> <span>Profile</span>
        </NavLink>

        <div className="nav-item" onClick={logout} style={{ cursor: 'pointer', marginTop: window.innerWidth > 768 ? 'auto' : 0 }}>
          <LogOutIcon /> <span>Logout</span>
        </div>
      </nav>

      <div className="page-container">
        <Outlet />
      </div>
    </div>
  );
}

export default FarmerLayout;
