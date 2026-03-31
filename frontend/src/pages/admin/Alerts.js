import { useState, useEffect } from "react";
import AdminLayout from "../../components/AdminLayout";
import { getAllAlerts } from "../../services/api";

const severityColors = {
    High: { bg: "#FEF2F2", color: "#B91C1C", border: "#FECACA" },
    Medium: { bg: "#FFFBEB", color: "#B45309", border: "#FDE68A" },
    Low: { bg: "#F0FDF4", color: "#15803D", border: "#BBF7D0" },
};

export default function Alerts() {
    const [alerts, setAlerts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAlerts = async () => {
            try {
                const res = await getAllAlerts();
                setAlerts(res.data);
            } catch (err) {
                console.error("Failed to fetch alerts:", err);
            } finally {
                setLoading(false);
            }
        };
        fetchAlerts();
    }, []);

    return (
        <AdminLayout>
            <div style={{ background: "white", borderBottom: "0.5px solid #e8e8e8", padding: "0 28px", height: 56, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <div>
                    <div style={{ fontSize: 15, fontWeight: 500 }}>Active Platform Alerts</div>
                    <div style={{ fontSize: 12, color: "#888", marginTop: 1 }}>Monitor all system-issued warnings and market notifications</div>
                </div>
            </div>

            <div style={{ padding: "24px 28px", overflowY: "auto", flex: 1 }}>
                {loading ? (
                    <div style={{ textAlign: "center", padding: 60, color: "#888", fontSize: 14 }}>Fetching alerts...</div>
                ) : (
                    <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                        {alerts.map((alert) => {
                            const style = severityColors[alert.severity] || severityColors.Medium;
                            return (
                                <div key={alert.id} style={{ display: "flex", alignItems: "flex-start", gap: 16, background: "white", border: `1px solid ${style.border}`, borderRadius: 12, padding: "16px 20px" }}>
                                    <div style={{ width: 44, height: 44, borderRadius: "50%", background: style.bg, display: "flex", alignItems: "center", justifyContent: "center", color: style.color, flexShrink: 0 }}>
                                        {alert.alert_type === "Weather" ? "⛈️" : "📉"}
                                    </div>
                                    <div style={{ flex: 1 }}>
                                        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
                                            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                                                <span style={{ fontSize: 14, fontWeight: 600, color: "#1a1a1a" }}>{alert.alert_type} Alert</span>
                                                <span style={{ fontSize: 11, background: style.bg, color: style.color, padding: "2px 8px", borderRadius: 12, fontWeight: 500 }}>
                                                    {alert.severity} Severity
                                                </span>
                                            </div>
                                            <div style={{ fontSize: 12, color: "#888" }}>
                                                {new Date(alert.created_at).toLocaleString()}
                                            </div>
                                        </div>
                                        <div style={{ fontSize: 13, color: "#555", lineHeight: "1.5" }}>
                                            {alert.message}
                                        </div>
                                        <div style={{ marginTop: 10, fontSize: 11, color: "#888", display: "flex", alignItems: "center", gap: 12 }}>
                                            <span><strong>Target Farm:</strong> #{String(alert.farm_id).slice(-6)}</span>
                                            <span>•</span>
                                            <span><strong>Dispatched via:</strong> {alert.sent_via}</span>
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                        {alerts.length === 0 && (
                            <div style={{ textAlign: "center", padding: 60, color: "#888", fontSize: 14, background: "white", borderRadius: 12, border: "0.5px solid #e8e8e8" }}>
                                No active alerts at this time.
                            </div>
                        )}
                    </div>
                )}
            </div>
        </AdminLayout>
    );
}
