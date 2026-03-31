import { useState, useEffect } from "react";
import AdminLayout from "../../components/AdminLayout";
import { getAnalytics } from "../../services/api";

export default function Analytics() {
    const [analytics, setAnalytics] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAnalytics = async () => {
            try {
                const res = await getAnalytics();
                setAnalytics(res.data);
            } catch (err) {
                console.error("Failed to fetch analytics:", err);
            } finally {
                setLoading(false);
            }
        };
        fetchAnalytics();
    }, []);

    const insights = [
        { title: "Registered Farmers", val: analytics?.total_farmers ?? 0, highlight: "#2a7de1", diff: "+12%" },
        { title: "Active Farm Sites", val: analytics?.total_farms ?? 0, highlight: "#22c55e", diff: "+15%" },
        { title: "AI Advisories Granted", val: analytics?.total_advisories ?? 0, highlight: "#9333ea", diff: "+4%" },
        { title: "Weather/Market Alerts", val: analytics?.total_alerts ?? 0, highlight: "#eab308", diff: "-2%" }
    ];

    return (
        <AdminLayout>
            <div style={{ background: "white", borderBottom: "0.5px solid #e8e8e8", padding: "0 28px", height: 56, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <div>
                    <div style={{ fontSize: 15, fontWeight: 500 }}>System Analytics</div>
                    <div style={{ fontSize: 12, color: "#888", marginTop: 1 }}>Deep Dive into Global Metric Aggregation</div>
                </div>
            </div>

            <div style={{ padding: "24px 28px", overflowY: "auto", flex: 1 }}>
                {loading ? (
                    <div style={{ textAlign: "center", padding: 60, color: "#888", fontSize: 14 }}>Aggregating global metrics...</div>
                ) : (
                    <div>
                        <div style={{ fontSize: 13, fontWeight: 600, color: "#1a1a1a", marginBottom: 16, textTransform: "uppercase", letterSpacing: "0.8px" }}>
                            KPI Breakdown
                        </div>
                        <div style={{ display: "grid", gridTemplateColumns: "repeat(2, minmax(0,1fr))", gap: 20 }}>
                            {insights.map((kpi, idx) => (
                                <div key={idx} style={{ background: "white", border: "0.5px solid #e8e8e8", borderRadius: 12, padding: "24px", position: "relative", overflow: "hidden" }}>
                                    <div style={{ position: "absolute", top: 0, left: 0, width: 4, height: "100%", background: kpi.highlight }} />
                                    <div style={{ color: "#888", fontSize: 12, fontWeight: 500, letterSpacing: "0.5px", textTransform: "uppercase" }}>
                                        {kpi.title}
                                    </div>
                                    <div style={{ display: "flex", alignItems: "baseline", gap: 12, marginTop: 12 }}>
                                        <div style={{ fontSize: 40, fontWeight: 600, color: "#1a1a1a", letterSpacing: "-1px" }}>
                                            {kpi.val}
                                        </div>
                                        <div style={{ fontSize: 13, fontWeight: 500, color: kpi.diff.includes("-") ? "#ef4444" : "#22c55e" }}>
                                            {kpi.diff} month
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </AdminLayout>
    );
}
