import { useState, useEffect } from "react";
import AdminLayout from "../../components/AdminLayout";
import { getFarmers } from "../../services/api";

export default function Farmers() {
    const [farmers, setFarmers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchFarmers = async () => {
            try {
                const res = await getFarmers();
                setFarmers(res.data);
            } catch (err) {
                console.error("Failed to fetch farmers:", err);
            } finally {
                setLoading(false);
            }
        };
        fetchFarmers();
    }, []);

    return (
        <AdminLayout>
            <div style={{ background: "white", borderBottom: "0.5px solid #e8e8e8", padding: "0 28px", height: 56, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <div>
                    <div style={{ fontSize: 15, fontWeight: 500 }}>Registered Farmers</div>
                    <div style={{ fontSize: 12, color: "#888", marginTop: 1 }}>Manage and view all platform users</div>
                </div>
            </div>

            <div style={{ padding: "24px 28px", overflowY: "auto", flex: 1 }}>
                {loading ? (
                    <div style={{ textAlign: "center", padding: 60, color: "#888", fontSize: 14 }}>Loading farmers...</div>
                ) : (
                    <div style={{ background: "white", border: "0.5px solid #e8e8e8", borderRadius: 12, overflow: "hidden" }}>
                        <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "left" }}>
                            <thead style={{ background: "#f8f9fa", borderBottom: "0.5px solid #e8e8e8" }}>
                                <tr>
                                    <th style={{ padding: "14px 20px", fontSize: 11, color: "#666", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.5px" }}>Farmer ID</th>
                                    <th style={{ padding: "14px 20px", fontSize: 11, color: "#666", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.5px" }}>Name</th>
                                    <th style={{ padding: "14px 20px", fontSize: 11, color: "#666", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.5px" }}>Mobile</th>
                                    <th style={{ padding: "14px 20px", fontSize: 11, color: "#666", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.5px" }}>Total Farms</th>
                                    <th style={{ padding: "14px 20px", fontSize: 11, color: "#666", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.5px" }}>Joined</th>
                                </tr>
                            </thead>
                            <tbody>
                                {farmers.map((farmer, idx) => (
                                    <tr key={farmer.id} style={{ borderBottom: idx !== farmers.length - 1 ? "0.5px solid #f0f0f0" : "none" }}>
                                        <td style={{ padding: "14px 20px", fontSize: 13, color: "#888" }}>
                                            <div style={{ display: "inline-block", padding: "2px 8px", background: "#f0f0f0", borderRadius: 4, fontSize: 11, fontFamily: "monospace" }}>
                                                {farmer.id.slice(-6)}
                                            </div>
                                        </td>
                                        <td style={{ padding: "14px 20px", fontSize: 14, fontWeight: 500, color: "#1a1a1a" }}>
                                            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                                                <div style={{ width: 28, height: 28, borderRadius: "50%", background: "#EAF3DE", color: "#3B6D11", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 11, fontWeight: 600 }}>
                                                    {farmer.name ? farmer.name.charAt(0).toUpperCase() : "?"}
                                                </div>
                                                {farmer.name || "Unknown"}
                                            </div>
                                        </td>
                                        <td style={{ padding: "14px 20px", fontSize: 13, color: "#555" }}>+91 {farmer.mobile}</td>
                                        <td style={{ padding: "14px 20px", fontSize: 13, color: "#555" }}>
                                            <span style={{ fontWeight: 500, color: "#2a7de1" }}>{farmer.farms_count}</span> actively registered
                                        </td>
                                        <td style={{ padding: "14px 20px", fontSize: 12, color: "#888" }}>{new Date(farmer.created_at).toLocaleDateString()}</td>
                                    </tr>
                                ))}
                                {farmers.length === 0 && (
                                    <tr>
                                        <td colSpan="5" style={{ padding: "32px", textAlign: "center", color: "#888", fontSize: 13 }}>No farmers found</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </AdminLayout>
    );
}
