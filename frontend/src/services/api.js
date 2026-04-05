import axios from "axios";

const API = axios.create({ baseURL: "http://localhost:5000/api" });

API.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});

API.interceptors.response.use(
    (res) => res,
    (err) => {
        if (err.response?.status === 401) {
            localStorage.clear();
            window.location.href = "/admin/login";
        }
        return Promise.reject(err);
    }
);

// Admin
export const adminLogin = (data) => API.post("/admin/login", data);
export const getAnalytics = () => API.get("/admin/analytics");
export const getFarmers = () => API.get("/admin/farmers");
export const getAdvisories = () => API.get("/admin/advisories");
export const getAllAlerts = () => API.get("/admin/alerts");

// Farmer Auth
export const sendOtp = (mobile) => API.post("/auth/send-otp", { mobile_number: mobile });
export const verifyOtp = (mobile, otp) => API.post("/auth/verify-otp", { mobile_number: mobile, otp });
export const verifyFirebase = (idToken, name) => API.post("/auth/verify-firebase", { id_token: idToken, name });

// Farm
export const createFarm = (data) => API.post("/farm/create", data);
export const getFarm = (id) => API.get(`/farm/${id}`);
export const getUserFarms = () => API.get("/farm/");
export const getAutoLocation = () => API.get("/farm/location");

// Advisory
export const generateAdvisory = (farmId, language) => API.post("/advisory/generate", { farm_id: farmId, language });
export const getAdvisoryHistory = (farmId) => API.get(`/advisory/history/${farmId}`);
export const chatAdvisory = (farmId, message, language, history) => API.post("/advisory/chat", { farm_id: farmId, message, language, history });

// Market
export const getMandiPrices = (district) => API.get(`/market/prices/${district}`);

// Alerts
export const getAlerts = (farmId) => API.get(`/alerts/${farmId}`);

export default API;