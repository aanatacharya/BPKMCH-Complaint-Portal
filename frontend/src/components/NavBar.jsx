import { Link, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function NavBar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <header className="site-header">
      <nav className="nav-shell" aria-label="Main navigation">
        <Link className="brand" to="/" aria-label="Careline home">
          <span className="brand-mark" aria-hidden="true">+</span>
          <span><span className="brand-name">Careline</span><span className="brand-caption">Hospital concerns portal</span></span>
        </Link>
        <div className="nav-links">
          <NavLink className={({ isActive }) => `nav-link${isActive ? " active" : ""}`} to="/">Community</NavLink>
          {user ? (
            <>
              <NavLink className={({ isActive }) => `nav-link${isActive ? " active" : ""}`} to="/dashboard">Dashboard</NavLink>
              {user.role === "superadmin" && <NavLink className={({ isActive }) => `nav-link${isActive ? " active" : ""}`} to="/superadmin-tools">Management</NavLink>}
              <span className="user-chip">{user.role === "superadmin" ? "Superadmin" : user.role === "admin" ? "Department admin" : "Patient"}</span>
              <button className="nav-action" onClick={handleLogout}>Sign out</button>
            </>
          ) : (
            <>
              <NavLink className={({ isActive }) => `nav-link${isActive ? " active" : ""}`} to="/login">Sign in</NavLink>
              <Link className="nav-action" to="/register">Create account</Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}

export default NavBar;