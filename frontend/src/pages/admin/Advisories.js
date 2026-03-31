import { useState, useEffect } from "react";
import AdminLayout from "../../components/AdminLayout";
import { getAdvisories } from "../../services/api";

const cropColors = {
    Cotton: { bg: "#FEF3C7", color: "#92400E" },
    Rice: { bg: "#EAF3DE", color: "#3B6D11" },
    Maize: { bg: "#EEEDFE", color: "#3C3489" },
    Wheat: { bg: "#FAECE7", color: "#993C1D" },
};

export default function Advisories() {
    const [advisories, setAdvisories] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAdvisories = async () => {
            try {
                const res = await getAdvisories();
                setAdvisories(res.data);
            } catch (err) {
                console.error("Failed to fetch advisories:", err);
            } finally {
                setLoading(false);
            }
        };
        fetchAdvisories();
    }, []);

    return (
        <AdminLayout>
            <div style={{ background: "white", borderBottom: "0.5px solid #e8e8e8", padding: "0 28px", height: 56, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <div>
                    <div style={{ fontSize: 15, fontWeight: 500 }}>Global Advisories</div>
                    <div style={{ fontSize: 12, color: "#888", marginTop: 1 }}>Monitor all issued AI crop recommendations</div>
                </div>
            </div>

            <div style={{ padding: "24px 28px", overflowY: "auto", flex: 1 }}>
                {loading ? (
                    <div style={{ textAlign: "center", padding: 60, color: "#888", fontSize: 14 }}>Loading advisories...</div>
                ) : (
                    <div style={{ display: "grid", gridTemplateColumns: "repeat(2, minmax(0,1fr))", gap: 16 }}>
                        {advisories.map((advisory) => {
                            const cropStyle = cropColors[advisory.recommended_crop] || { bg: "#f0f0f0", color: "#555" };
                            return (
                                <div key={advisory.id} style={{ background: "white", border: "0.5px solid #e8e8e8", borderRadius: 12, padding: "20px" }}>
                                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16 }}>
                                        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                                            <div style={{ width: 40, height: 40, borderRadius: "50%", background: "#EBF2FD", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 600, color: "#185FA5", flexShrink: 0 }}>
                                                #{String(advisory.farm_id).slice(-4)}
                                            </div>
                                            <div>
                                                <div style={{ fontSize: 13, fontWeight: 500, color: "#1a1a1a" }}>Target Farm: #{String(advisory.farm_id).slice(-6)}</div>
                                                <div style={{ fontSize: 11, color: "#888", marginTop: 2 }}>Analysis issued on {new Date(advisory.created_at).toLocaleString()}</div>
                                            </div>
                                        </div>
                                        {advisory.recommended_crop && (
                                            <div style={{ fontSize: 12, padding: "4px 12px", borderRadius: 20, background: cropStyle.bg, color: cropStyle.color, fontWeight: 500 }}>
                                                {advisory.recommended_crop}
                                            </div>
                                        )}
                                    </div>
                                    <div style={{ fontSize: 13, color: "#555", background: "#f9f9f9", padding: "12px", borderRadius: 8, border: "0.5px dashed #ccc" }}>
                                        <div style={{ marginBottom: 6 }}><strong style={{ color: "#333", fontWeight: 500 }}>Season Protocol:</strong> {advisory.season} Crop Cycle</div>
                                        <div>Our AI agents recommended planting <span style={{ fontWeight: 600 }}>{advisory.recommended_crop}</span> based on cross-analyzed soil & weather dynamics for this specific farm's district coordinates.</div>
                                    </div>
                                </div>
                            );
                        })}
                        {advisories.length === 0 && (
                            <div style={{ gridColumn: "span 2", textAlign: "center", padding: 60, color: "#888", fontSize: 14 }}>
                                No advisories have been issued yet
                            </div>
                        )}
                    </div>
                )}
            </div>
        </AdminLayout>
    );
}
