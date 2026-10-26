import {useState, createContext, useContext, useEffect} from "react";
import {jwtDecode} from "jwt-decode";

import api from "../api/axios";

const AuthContext = createContext();

export function AuthProvider({ children }){
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem("access_token");
        if (token) {
            try {
                const decoded = jwtDecode(token);
                setUser({ id: decoded.sub, role: decoded.role });
            } catch {
                localStorage.removeItem("access_token");
                localStorage.removeItem("refresh_token");
            }
        }
        setLoading(false);
    }, []);

    const login = async (username, password) => {
        try {
            const response = await api.post("/auth/login", { username, password });

            localStorage.setItem("access_token", response.data.access_token);
            localStorage.setItem("refresh_token", response.data.refresh_token);

            const decoded = jwtDecode(response.data.access_token);
            setUser({ id: decoded.sub, role: decoded.role });

            return { success: true };
        } catch (error) {
            return {
                success: false,
                message: error.response?.data?.detail || "Login failed. Please try again."
            };
        }
    }

    const logout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        setUser(null);
    }

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth(){
    return useContext(AuthContext);
}