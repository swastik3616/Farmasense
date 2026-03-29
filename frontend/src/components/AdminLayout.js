import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const navItems = [
    { path: "/admin/dashboard", label: "Overview", icon: "grid" },
    { path: "/admin/farmers", label: "Farmers", icon: "users" },
    { path: "/admin/advisories", label: "Advisories", icon: "chart" },
    { path: "/admin/alerts", label: "Alerts", icon: "bell" },
    { path: "/admin/analytics", label: "Analytics", icon: "bar" },
];

const Icon = ({ name }) => {
    const icons = {
        grid: <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><rect x="1" y="1" width="6" height="6" rx="1.5" fill="currentColor" /><rect x="9" y="1" width="6" height="6" rx="1.5" fill="currentColor" opacity="0.5" /><rect x="1" y="9" width="6" height="6" rx="1.5" fill="currentColor" opacity="0.5" /><rect x="9" y="9" width="6" height="6" rx="1.5" fill="currentColor" opacity="0.5" /></svg>,
        users: <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="5" r="3" stroke="currentColor" strokeWidth="1.2" /><path d="M2 13C2 10.8 4.7 9 8 9C11.3 9 14 10.8 14 13" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" /></svg>,
        chart: <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M2 12L5 8L8 10L11 5L14 7" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" /></svg>,
        bell: <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 2C5.8 2 4 3.8 4 6V10L2 12H14L12 10V6C12 3.8 10.2 2 8 2Z" stroke="currentColor" strokeWidth="1.2" /><path d="M6.5 12C6.5 12.8 7.2 13.5 8 13.5C8.8 13.5 9.5 12.8 9.5 12" stroke="currentColor" strokeWidth="1.2" /></svg>,
        bar: <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><rect x="2" y="9" width="3" height="5" rx="0.5" fill="currentColor" /><rect x="6.5" y="6" width="3" height="8" rx="0.5" fill="currentColor" /><rect x="11" y="3" width="3" height="11" rx="0.5" fill="currentColor" /></svg>,
    };
    return icons[name] || null;
};

export default function AdminLayout({ children }) {
    const navigate = useNavigate();
    const location = useLocation();
    const { user, logout } = useAuth();

    return (
        <div style={{ display: "flex", minHeight: "100vh", background: "#f4f6f9" }}>
            {/* Sidebar */}
            <div style={{ width: 220, background: "#0f2d52", display: "flex", flexDirection: "column", flexShrink: 0 }}>
                {/* Logo */}
                <div style={{ padding: "20px 20px 16px", borderBottom: "0.5px solid rgba(255,255,255,0.1)" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                        <div style={{ width: 32, height: 32, background: "#2a7de1", borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center" }}>
                            <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                                <path d="M9 2C5.7 2 3 4.7 3 9C3 11.5 4.2 13.7 6 15V16H12V15C13.8 13.7 15 11.5 15 9C15 4.7 12.3 2 9 2Z" fill="white" />
                            </svg>
                        </div>
                        <div>
                            <div style={{ color: "white", fontSize: 15, fontWeight: 500 }}>FarmSense</div>
                            <div style={{ color: "rgba(255,255,255,0.4)", fontSize: 10 }}>Admin Portal</div>
                        </div>
                    </div>
                </div>

                {/* Nav */}
                <div style={{ flex: 1, padding: "12px 0" }}>
                    <div style={{ padding: "8px 16px 4px", color: "rgba(255,255,255,0.3)", fontSize: 10, letterSpacing: "0.8px", textTransform: "uppercase" }}>Main</div>
                    {navItems.map((item) => {
                        const active = location.pathname === item.path;
                        return (
                            <div
                                key={item.path}
                                onClick={() => navigate(item.path)}
                                style={{
                                    display: "flex", alignItems: "center", gap: 10,
                                    padding: "9px 20px", cursor: "pointer",
                                    color: active ? "white" : "rgba(255,255,255,0.65)",
                                    background: active ? "rgba(42,125,225,0.2)" : "transparent",
                                    borderLeft: active ? "3px solid #2a7de1" : "3px solid transparent",
                                    fontSize: 13, transition: "all 0.15s",
                                }}
                            >
                                <Icon name={item.icon} />
                                {item.label}
                            </div>
                        );
                    })}
                </div>

                {/* Footer */}
                <div style={{ padding: "16px 20px", borderTop: "0.5px solid rgba(255,255,255,0.1)" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                        <div style={{ width: 30, height: 30, borderRadius: "50%", background: "#2a7de1", display: "flex", alignItems: "center", justifyContent: "center", color: "white", fontSize: 11, fontWeight: 500 }}>
                            {user?.name?.charAt(0) || "A"}
                        </div>
                        <div style={{ flex: 1 }}>
                            <div style={{ color: "white", fontSize: 12, fontWeight: 500 }}>{user?.name || "Admin"}</div>
                            <div style={{ color: "rgba(255,255,255,0.4)", fontSize: 10 }}>Super Admin</div>
                        </div>
                        <div onClick={logout} style={{ color: "rgba(255,255,255,0.4)", cursor: "pointer", fontSize: 11 }}>Exit</div>
                    </div>
                </div>
            </div>

            {/* Main content */}
            <div style={{ flex: 1, display: "flex", flexDirection: "column", minWidth: 0 }}>
                {children}
            </div>
        </div>
    );
}