import { useState, useEffect } from "react";
import api from "../api/axios";

function SuperadminTools() {
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");

  const [adminUsername, setAdminUsername] = useState("");
  const [adminMobile, setAdminMobile] = useState("");
  const [adminPassword, setAdminPassword] = useState("");
  const [adminEmail, setAdminEmail] = useState("");
  const [adminDepartmentId, setAdminDepartmentId] = useState("");
  const [registerFeedback, setRegisterFeedback] = useState(null);

  const [newDepartmentName, setNewDepartmentName] = useState("");
  const [departmentFeedback, setDepartmentFeedback] = useState(null);

  useEffect(() => {
    const fetchDepartments = async () => {
      try {
        const res = await api.get("/departments");
        setDepartments(res.data);
      } catch {
        setLoadError("Departments could not be loaded. Please refresh and try again.");
      } finally {
        setLoading(false);
      }
    };
    fetchDepartments();
  }, []);

  const handleRegisterAdmin = async (e) => {
    e.preventDefault();
    setRegisterFeedback(null);
    if (!adminDepartmentId) {
      setRegisterFeedback("Choose a department for this admin account.");
      return;
    }
    try {
      await api.post("/superadmin/register-admin", {
        username: adminUsername,
        mobile_number: adminMobile,
        password: adminPassword,
        email: adminEmail,
        unique_id: null,
        department_id: Number(adminDepartmentId),
      });
      setRegisterFeedback("Admin registered successfully.");
      setAdminUsername("");
      setAdminMobile("");
      setAdminPassword("");
      setAdminEmail("");
      setAdminDepartmentId("");
    } catch (error) {
      setRegisterFeedback(error.response?.data?.detail || "Failed to register admin.");
    }
  };

  const handleCreateDepartment = async (e) => {
    e.preventDefault();
    setDepartmentFeedback(null);
    try {
      const res = await api.post("/departments", { name: newDepartmentName });
      setDepartments((current) => [...current, res.data]);
      setDepartmentFeedback("Department created.");
      setNewDepartmentName("");
    } catch (error) {
      setDepartmentFeedback(error.response?.data?.detail || "Failed to create department.");
    }
  };

  return (
    <main className="page-shell management-shell">
      <section className="dashboard-heading">
        <div><p className="eyebrow">Portal administration</p><h1>Management</h1><p className="dashboard-subtitle">Set up the departments and people who keep care moving.</p></div>
        <div className="dashboard-count"><span>{departments.length}</span><small>departments</small></div>
      </section>
      {loadError && <p className="form-feedback form-feedback-error" role="alert">{loadError}</p>}
      <div className="management-grid">
        <section className="management-section">
          <div className="section-heading"><div><p className="eyebrow">Team access</p><h2>Register an admin</h2></div><span className="section-number">01</span></div>
          <p className="section-description">Create a department account for a care team lead.</p>
          <form className="form-stack" onSubmit={handleRegisterAdmin}>
            <div className="field-grid">
              <div className="field"><label htmlFor="admin-username">Username</label><input id="admin-username" autoComplete="off" maxLength={50} required value={adminUsername} onChange={(e) => setAdminUsername(e.target.value)} /></div>
              <div className="field"><label htmlFor="admin-mobile">Mobile number</label><input id="admin-mobile" type="tel" required value={adminMobile} onChange={(e) => setAdminMobile(e.target.value)} /></div>
              <div className="field field-span"><label htmlFor="admin-email">Email</label><input id="admin-email" type="email" value={adminEmail} onChange={(e) => setAdminEmail(e.target.value)} /></div>
              <div className="field field-span"><label htmlFor="admin-department">Department</label><select id="admin-department" required value={adminDepartmentId} onChange={(e) => setAdminDepartmentId(e.target.value)}><option value="">Choose a department</option>{departments.map((dept) => <option key={dept.id} value={dept.id}>{dept.name}</option>)}</select></div>
              <div className="field field-span"><label htmlFor="admin-password">Temporary password</label><input id="admin-password" type="password" autoComplete="new-password" required value={adminPassword} onChange={(e) => setAdminPassword(e.target.value)} /></div>
            </div>
            {registerFeedback && <p className={`form-feedback ${registerFeedback.includes("successfully") ? "form-feedback-success" : "form-feedback-error"}`} role="status">{registerFeedback}</p>}
            <button className="button-primary" type="submit" disabled={loading || departments.length === 0}>Register admin<span aria-hidden="true">→</span></button>
          </form>
        </section>

        <div className="management-side">
          <section className="management-section department-create-section">
            <div className="section-heading"><div><p className="eyebrow">Care structure</p><h2>Add a department</h2></div><span className="section-number">02</span></div>
            <form className="department-create-form" onSubmit={handleCreateDepartment}>
              <div className="field"><label htmlFor="department-name">Department name</label><input id="department-name" maxLength={100} required value={newDepartmentName} onChange={(e) => setNewDepartmentName(e.target.value)} placeholder="e.g. Patient Relations" /></div>
              {departmentFeedback && <p className={`form-feedback ${departmentFeedback === "Department created." ? "form-feedback-success" : "form-feedback-error"}`} role="status">{departmentFeedback}</p>}
              <button className="button-primary" type="submit">Add department<span aria-hidden="true">+</span></button>
            </form>
          </section>
          <section className="department-list-section">
            <div className="department-list-heading"><h2>Departments</h2><span>{loading ? "Loading…" : departments.length}</span></div>
            {loading ? <p className="loading-state">Loading departments…</p> : departments.length === 0 ? <p className="department-empty">No departments created yet.</p> : (
              <ul className="department-list">{departments.map((dept, index) => <li key={dept.id}><span className="department-index">{String(index + 1).padStart(2, "0")}</span><span>{dept.name}</span></li>)}</ul>
            )}
          </section>
        </div>
      </div>
    </main>
  );
}

export default SuperadminTools;