import { createContext, useContext, useState, useEffect } from "react";

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem("token");
        const role = localStorage.getItem("role");
        const name = localStorage.getItem("name");
        if (token) setUser({ token, role, name });
        setLoading(false);
    }, []);

    const loginAdmin = (token, name, email) => {
        localStorage.setItem("token", token);
        localStorage.setItem("role", "admin");
        localStorage.setItem("name", name);
        localStorage.setItem("email", email);
        setUser({ token, role: "admin", name });
    };

    const loginFarmer = (token, name, userId) => {
        localStorage.setItem("token", token);
        localStorage.setItem("role", "farmer");
        localStorage.setItem("name", name);
        localStorage.setItem("user_id", userId);
        setUser({ token, role: "farmer", name });
    };

    const logout = () => {
        localStorage.clear();
        setUser(null);
        window.location.href = "/";
    };

    return (
        <AuthContext.Provider value={{ user, loading, loginAdmin, loginFarmer, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => useContext(AuthContext);