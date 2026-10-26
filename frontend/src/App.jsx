import { BrowserRouter, Routes, Route } from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";
import NavBar from "./components/NavBar";

import Feed from "./pages/Feed";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import ProtectedRoute from "./components/ProtectedRoutes";
import SuperadminTools from "./pages/SuperadminTools";

function App(){
    return (
        <AuthProvider>
            <BrowserRouter>
            <NavBar />
                <Routes>
                    <Route path="/" element={<Feed />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
                    <Route path="/superadmin-tools" element={<ProtectedRoute requiredRole="superadmin"><SuperadminTools /></ProtectedRoute>} />
                </Routes>
            </BrowserRouter>
        </AuthProvider>
    );
}

export default App;