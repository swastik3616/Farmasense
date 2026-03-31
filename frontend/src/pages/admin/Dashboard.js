import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import AdminLayout from "../../components/AdminLayout";
import { getAnalytics, getAdvisories } from "../../services/api";

export default function Dashboard() {
    const [analytics, setAnalytics] = useState(null);
    const [advisories, setAdvisories] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [aRes, advRes] = await Promise.all([getAnalytics(), getAdvisories()]);
                setAnalytics(aRes.data);
                setAdvisories(advRes.data.slice(0, 5));
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    const metrics = [
        { label: "Total Farmers", value: analytics?.total_farmers ?? "—", color: "#EBF2FD", icon: "👨‍🌾" },
        { label: "Total Farms", value: analytics?.total_farms ?? "—", color: "#EAF3DE", icon: "🌾" },
        { label: "Total Advisories", value: analytics?.total_advisories ?? "—", color: "#EEEDFE", icon: "📋" },
        { label: "Total Alerts", value: analytics?.total_alerts ?? "—", color: "#FAEEDA", icon: "🚨" },
    ];

    const cropColors = {
        Cotton: { bg: "#FEF3C7", color: "#92400E" },
        Rice: { bg: "#EAF3DE", color: "#3B6D11" },
        Maize: { bg: "#EEEDFE", color: "#3C3489" },
        Wheat: { bg: "#FAECE7", color: "#993C1D" },
    };

    return (
        <AdminLayout>
            {/* Topbar */}
            <div style={{ background: "white", borderBottom: "0.5px solid #e8e8e8", padding: "0 28px", height: 56, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <div>
                    <div style={{ fontSize: 15, fontWeight: 500 }}>Overview</div>
                    <div style={{ fontSize: 12, color: "#888", marginTop: 1 }}>FarmSense Admin Dashboard</div>
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                    <div style={{ width: 7, height: 7, borderRadius: "50%", background: "#22c55e" }}></div>
                    <div style={{ fontSize: 12, color: "#888" }}>All agents running</div>
                </div>
            </div>

            {/* Content */}
            <div style={{ padding: "24px 28px", overflowY: "auto" }}>
                {loading ? (
                    <div style={{ textAlign: "center", padding: 60, color: "#888", fontSize: 14 }}>Loading dashboard...</div>
                ) : (
                    <>
                        {/* Metric Cards */}
                        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, minmax(0,1fr))", gap: 12, marginBottom: 24 }}>
                            {metrics.map((m) => (
                                <div key={m.label} style={{ background: "white", border: "0.5px solid #e8e8e8", borderRadius: 12, padding: "16px 18px" }}>
                                    <div style={{ width: 36, height: 36, background: m.color, borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16, marginBottom: 12 }}>{m.icon}</div>
                                    <div style={{ fontSize: 11, color: "#888", textTransform: "uppercase", letterSpacing: "0.5px", marginBottom: 6 }}>{m.label}</div>
                                    <div style={{ fontSize: 26, fontWeight: 500, color: "#1a1a1a" }}>{m.value}</div>
                                </div>
                            ))}
                        </div>

                        {/* Recent Advisories */}
                        <div style={{ background: "white", border: "0.5px solid #e8e8e8", borderRadius: 12, padding: "18px 20px" }}>
                            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16 }}>
                                <div style={{ fontSize: 13, fontWeight: 500 }}>Recent advisories</div>
                                <div
                                    onClick={() => navigate("/admin/advisories")}
                                    style={{ fontSize: 12, color: "#2a7de1", cursor: "pointer" }}
                                >
                                    View all →
                                </div>
                            </div>

                            {advisories.length === 0 ? (
                                <div style={{ textAlign: "center", padding: 32, color: "#888", fontSize: 13 }}>No advisories yet</div>
                            ) : (
                                <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                                    {advisories.map((a) => {
                                        const cropStyle = cropColors[a.recommended_crop] || { bg: "#f0f0f0", color: "#555" };
                                        return (
                                            <div key={a.id} style={{ display: "flex", alignItems: "center", gap: 12, padding: "10px 12px", border: "0.5px solid #f0f0f0", borderRadius: 8 }}>
                                                <div style={{ width: 32, height: 32, borderRadius: "50%", background: "#EBF2FD", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 500, color: "#185FA5", flexShrink: 0 }}>
                                                    #{String(a.farm_id).slice(-4)}
                                                </div>
                                                <div style={{ flex: 1 }}>
                                                    <div style={{ fontSize: 12, fontWeight: 500, color: "#1a1a1a" }}>Farm #{String(a.farm_id).slice(-4)}</div>
                                                    <div style={{ fontSize: 11, color: "#888", marginTop: 1 }}>{a.season} season · {new Date(a.created_at).toLocaleString()}</div>
                                                </div>
                                                {a.recommended_crop && (
                                                    <div style={{ fontSize: 11, padding: "2px 10px", borderRadius: 20, background: cropStyle.bg, color: cropStyle.color }}>
                                                        {a.recommended_crop}
                                                    </div>
                                                )}
                                            </div>
                                        );
                                    })}
                                </div>
                            )}
                        </div>
                    </>
                )}
            </div>
        </AdminLayout>
    );
}