import { useState, useEffect } from "react";

import { useAuth } from "../context/AuthContext";
import api from "../api/axios";
import AdminComplaintRow from "../components/AdminComplaintRow";

function Dashboard(){
    const { user } = useAuth();
    const [complaints, setComplaints] = useState([]);
    const [loading, setLoading] = useState(true);
    const [loadError, setLoadError] = useState("");

    const [departments, setDepartments] = useState([]);
    const [departmentId, setDepartmentId] = useState("");
    const [description, setDescription] = useState("");
    const [visibility, setVisibility] = useState("private");
    const [identityDisplay, setIdentityDisplay] = useState("named");
    const [formFeedback, setFormFeedback] = useState(null);
    const [submitting, setSubmitting] = useState(false);

    const [searchTerm, setSearchTerm] = useState("");
    const [searchResults, setSearchResults] = useState(null);
    const [searchError, setSearchError] = useState("");

    const fetchDashboard = async () => {
        setLoading(true);
        setLoadError("");
        try {
            let response;
            if (user.role === "user") {
                response = await api.get("/complaints/me");
            } else if (user.role === "admin") {
                response = await api.get("/admin/dashboard");
            } else if (user.role === "superadmin") {
                response = await api.get("/superadmin/dashboard");
            }
            setComplaints(response.data);
        } catch {
            setLoadError("Your dashboard could not be loaded. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDashboard();
    }, [user.role]);

    useEffect(() => {
        const fetchDepartments = async () => {
            try {
                const res = await api.get("/departments");
                setDepartments(res.data);
            } catch {
                setDepartments([]);
            }
        };
        fetchDepartments();
    }, [user.role]);

    const handleFileComplaint = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        setFormFeedback(null);

        if (!departmentId || !description.trim()) {
            setFormFeedback("Choose a department and describe your concern before submitting.");
            setSubmitting(false);
            return;
        }

        try {
            await api.post("/complaints", {
                department_id: Number(departmentId),
                description,
                visibility,
                identity_display: identityDisplay,
            });

            setFormFeedback("Complaint filed successfully.");
            setDescription("");
            setDepartmentId("");
            await fetchDashboard();
        } catch (error) {
            setFormFeedback(error.response?.data?.detail || "Failed to file complaint.");
        } finally {
            setSubmitting(false);
        }
    };

    const handleSearch = async (e) => {
        e.preventDefault();
        setSearchError("");
        try {
            const res = await api.get("/admin/complaints/search", {
                params: { filer_name: searchTerm }
            });
            setSearchResults(res.data);
        } catch {
            setSearchError("Search could not be completed. Please try again.");
        }
    };

    const clearSearch = () => {
        setSearchTerm("");
        setSearchResults(null);
        setSearchError("");
    };

    const departmentName = (departmentId) =>
        departments.find((department) => department.id === departmentId)?.name || `Department ${departmentId}`;
    const visibleComplaints = searchResults ?? complaints;
    const pageTitle = user.role === "user" ? "Your concerns" : user.role === "admin" ? "Department inbox" : "All concerns";

    return (
        <main className="page-shell dashboard-shell">
            <section className="dashboard-heading">
                <div>
                    <p className="eyebrow">{user.role === "user" ? "Your care, in view" : "Care team workspace"}</p>
                    <h1>{pageTitle}</h1>
                    <p className="dashboard-subtitle">{user.role === "user" ? "Submit a concern or follow progress on reports you have shared." : "Review reports, keep status updates current, and help concerns reach resolution."}</p>
                </div>
                <div className="dashboard-count"><span>{complaints.length}</span><small>{user.role === "user" ? "reports filed" : "reports in view"}</small></div>
            </section>

            {user.role === "user" && (
                <form className="report-form" onSubmit={handleFileComplaint}>
                    <div className="section-heading">
                        <div><p className="eyebrow">New report</p><h2>Tell us what happened</h2></div>
                        <span className="section-aside">Your report is handled with care.</span>
                    </div>
                    <div className="field-grid report-fields">
                        <div className="field">
                            <label htmlFor="complaint-department">Department</label>
                            <select id="complaint-department" required value={departmentId} onChange={(e) => setDepartmentId(e.target.value)}>
                                <option value="">Choose a department</option>
                                {departments.map((dept) => <option key={dept.id} value={dept.id}>{dept.name}</option>)}
                            </select>
                        </div>
                        <div className="field">
                            <label htmlFor="complaint-visibility">Who can see this report?</label>
                            <select id="complaint-visibility" value={visibility} onChange={(e) => setVisibility(e.target.value)}>
                                <option value="private">Private · care team only</option>
                                <option value="public">Public · community feed</option>
                            </select>
                        </div>
                        <div className="field field-span">
                            <label htmlFor="complaint-description">Your concern</label>
                            <textarea id="complaint-description" value={description} onChange={(e) => setDescription(e.target.value)} maxLength={6000} required placeholder="Describe your experience, including any details that may help the team respond." />
                            <span className="field-hint">{description.length} / 6000 characters</span>
                        </div>
                        <div className="field">
                            <label htmlFor="complaint-identity">Name display</label>
                            <select id="complaint-identity" value={identityDisplay} onChange={(e) => setIdentityDisplay(e.target.value)}>
                                <option value="named">Show my name</option>
                                <option value="anonymous">Keep me anonymous</option>
                            </select>
                        </div>
                    </div>
                    {formFeedback && <p className={`form-feedback ${formFeedback.includes("successfully") ? "form-feedback-success" : "form-feedback-error"}`} role="status">{formFeedback}</p>}
                    <div className="report-form-actions"><span className="field-hint">You can choose public or private visibility.</span><button className="button-primary" type="submit" disabled={submitting}>{submitting ? "Submitting…" : "Submit concern"}<span aria-hidden="true">→</span></button></div>
                </form>
            )}

            {user.role === "admin" && (
                <form className="search-toolbar" onSubmit={handleSearch}>
                    <label className="sr-only" htmlFor="complaint-search">Search by filer username</label>
                    <input id="complaint-search" type="search" placeholder="Search by filer username" value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} />
                    <button className="button-primary" type="submit">Search</button>
                    {searchResults !== null && (
                        <button className="button-secondary" type="button" onClick={clearSearch}>Clear search</button>
                    )}
                </form>
            )}

            {(user.role === "admin" || user.role === "superadmin") && user.role === "superadmin" && (
                <div className="dashboard-list-heading"><h2>Reports</h2><span>Update a status to notify the record.</span></div>
            )}
            {searchError && <p className="form-feedback form-feedback-error" role="alert">{searchError}</p>}
            {loadError && <div className="error-state" role="alert"><h2>Dashboard unavailable</h2><p>{loadError}</p><button className="button-secondary" type="button" onClick={fetchDashboard}>Try again</button></div>}
            {loading && <p className="loading-state" role="status">Loading your dashboard…</p>}
            {!loading && !loadError && (
                <section aria-label={user.role === "user" ? "Your filed concerns" : "Complaint reports"}>
                    {(user.role === "admin" || user.role === "superadmin") && user.role === "admin" && <div className="dashboard-list-heading"><h2>{searchResults !== null ? "Search results" : "Reports"}</h2><span>{visibleComplaints.length} {visibleComplaints.length === 1 ? "report" : "reports"}</span></div>}
                    {visibleComplaints.length === 0 ? (
                        <div className="empty-state"><h2>{searchResults !== null ? "No matching reports" : user.role === "user" ? "Nothing filed yet" : "No reports to review"}</h2><p>{searchResults !== null ? "Try another username or clear your search." : user.role === "user" ? "When you share a concern, its progress will appear here." : "New reports for your team will appear here."}</p></div>
                    ) : (
                        <ul className="complaint-list">
                            {user.role === "user" ? complaints.map((complaint) => (
                                <li className="complaint-card" key={complaint.id}>
                                    <div className="complaint-card-head"><div className="complaint-meta"><span className="department-label">{departmentName(complaint.department_id)}</span><span className="meta-separator" aria-hidden="true">·</span><span className="meta-small">Concern #{complaint.id}</span></div><span className={`status-pill status-${complaint.current_status}`}>{complaint.current_status.replace("_", " ")}</span></div>
                                    <p className="complaint-description">{complaint.description}</p>
                                    <div className="complaint-card-foot"><span className="visibility-pill">{complaint.visibility === "public" ? "Public report" : "Private report"}</span><span className="meta-small">Name {complaint.identity_display === "anonymous" ? "hidden" : "visible"}</span></div>
                                </li>
                            )) : visibleComplaints.map((complaint) => (
                                <AdminComplaintRow key={complaint.id} complaint={complaint} departmentName={departmentName(complaint.department_id)} onStatusUpdated={fetchDashboard} />
                            ))}
                        </ul>
                    )}
                </section>
            )}
        </main>
    )
}

export default Dashboard;