import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { adminLogin } from "../../services/api";

export default function AdminLogin() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const { loginAdmin } = useAuth();
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        try {
            const res = await adminLogin({ email, password });
            loginAdmin(res.data.token, res.data.name, res.data.email);
            navigate("/admin/dashboard");
        } catch (err) {
            setError(err.response?.data?.error || "Login failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ minHeight: "100vh", background: "#f4f6f9", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <div style={{ width: 400 }}>
                {/* Logo */}
                <div style={{ textAlign: "center", marginBottom: 32 }}>
                    <div style={{ width: 48, height: 48, background: "#0f2d52", borderRadius: 12, display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 12px" }}>
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <path d="M12 2C7 2 3 6 3 11C3 14 4.5 16.7 6.8 18.3V20H17.2V18.3C19.5 16.7 21 14 21 11C21 6 17 2 12 2Z" fill="white" />
                        </svg>
                    </div>
                    <div style={{ fontSize: 22, fontWeight: 500, color: "#0f2d52" }}>FarmSense</div>
                    <div style={{ fontSize: 13, color: "#888", marginTop: 4 }}>Admin Portal</div>
                </div>

                {/* Card */}
                <div style={{ background: "white", borderRadius: 12, border: "0.5px solid #e0e0e0", padding: "32px 28px" }}>
                    <div style={{ fontSize: 16, fontWeight: 500, color: "#1a1a1a", marginBottom: 24 }}>Sign in to continue</div>

                    {error && (
                        <div style={{ background: "#FCEBEB", border: "0.5px solid #F7C1C1", borderRadius: 8, padding: "10px 14px", fontSize: 13, color: "#A32D2D", marginBottom: 16 }}>
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleLogin}>
                        <div style={{ marginBottom: 16 }}>
                            <div style={{ fontSize: 12, color: "#555", marginBottom: 6, fontWeight: 500 }}>Email address</div>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="admin@farmsense.com"
                                required
                                style={{ width: "100%", padding: "10px 12px", border: "0.5px solid #ddd", borderRadius: 8, fontSize: 14, outline: "none", boxSizing: "border-box" }}
                            />
                        </div>
                        <div style={{ marginBottom: 24 }}>
                            <div style={{ fontSize: 12, color: "#555", marginBottom: 6, fontWeight: 500 }}>Password</div>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="••••••••"
                                required
                                style={{ width: "100%", padding: "10px 12px", border: "0.5px solid #ddd", borderRadius: 8, fontSize: 14, outline: "none", boxSizing: "border-box" }}
                            />
                        </div>
                        <button
                            type="submit"
                            disabled={loading}
                            style={{ width: "100%", padding: "11px", background: "#0f2d52", color: "white", border: "none", borderRadius: 8, fontSize: 14, fontWeight: 500, cursor: loading ? "not-allowed" : "pointer", opacity: loading ? 0.7 : 1 }}
                        >
                            {loading ? "Signing in..." : "Sign in"}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}