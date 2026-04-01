import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import AdminLogin from "./pages/admin/AdminLogin";
import Dashboard from "./pages/admin/Dashboard";
import Farmers from "./pages/admin/Farmers";
import Advisories from "./pages/admin/Advisories";
import Alerts from "./pages/admin/Alerts";
import Analytics from "./pages/admin/Analytics";

// Farmer
import FarmerLayout from "./components/FarmerLayout";
import FarmerLogin from "./pages/farmer/Login";
import FarmerDashboard from "./pages/farmer/FarmerDashboard";
import MyFarms from "./pages/farmer/MyFarms";
import AddFarm from "./pages/farmer/AddFarm";

function ProtectedRoute({ children, role }) {
  const { user, loading } = useAuth();
  if (loading) return <div style={{ padding: 40, textAlign: "center" }}>Loading...</div>;
  if (!user) return <Navigate to="/admin/login" />;
  if (role && user.role !== role) return <Navigate to="/admin/login" />;
  return children;
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Default Route */}
          <Route path="/" element={<Navigate to="/farmer/login" />} />

          {/* Admin Routes */}
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route path="/admin/dashboard" element={
            <ProtectedRoute role="admin">
              <Dashboard />
            </ProtectedRoute>
          } />
          <Route path="/admin/farmers" element={
            <ProtectedRoute role="admin">
              <Farmers />
            </ProtectedRoute>
          } />
          <Route path="/admin/advisories" element={
            <ProtectedRoute role="admin">
              <Advisories />
            </ProtectedRoute>
          } />
          <Route path="/admin/alerts" element={
            <ProtectedRoute role="admin">
              <Alerts />
            </ProtectedRoute>
          } />
          <Route path="/admin/analytics" element={
            <ProtectedRoute role="admin">
              <Analytics />
            </ProtectedRoute>
          } />

          {/* Farmer Routes */}
          <Route path="/farmer/login" element={<FarmerLogin />} />
          <Route path="/farmer" element={
            <ProtectedRoute role="farmer">
              <FarmerLayout />
            </ProtectedRoute>
          }>
            <Route path="dashboard" element={<FarmerDashboard />} />
            <Route path="farms" element={<MyFarms />} />
            <Route path="add-farm" element={<AddFarm />} />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;