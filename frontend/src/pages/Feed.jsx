import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

function Feed(){
    const { user } = useAuth();
    const [complaints, setComplaints] = useState([]);
    const [loading, setLoading] = useState(true);
    const [loadingMore, setLoadingMore] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const [departments, setDepartments] = useState([]);
    const [hasMore, setHasMore] = useState(false);
    const pageSize = 20;

    useEffect(() => {
        const fetchComplaints = async () => {
            try {
                const [response, departmentResponse] = await Promise.all([
                    api.get("/complaints/public", { params: { skip: 0, limit: pageSize } }),
                    api.get("/departments"),
                ]);
                setComplaints(response.data);
                setDepartments(departmentResponse.data);
                setHasMore(response.data.length === pageSize);
            } catch {
                setErrorMessage("The public feed could not be loaded. Check your connection and try again.");
            } finally {
                setLoading(false);
            }
        }
        fetchComplaints();
    }, [])

    const loadMore = async () => {
        setLoadingMore(true);
        try {
            const response = await api.get("/complaints/public", {
                params: { skip: complaints.length, limit: pageSize }
            });
            setComplaints((current) => [...current, ...response.data]);
            setHasMore(response.data.length === pageSize);
        } catch {
            setErrorMessage("More complaints could not be loaded. Please try again.");
        } finally {
            setLoadingMore(false);
        }
    };

    const departmentName = (departmentId) =>
        departments.find((department) => department.id === departmentId)?.name || `Department ${departmentId}`;

    const formatDate = (value) => new Intl.DateTimeFormat(undefined, {
        month: "short",
        day: "numeric",
        year: "numeric",
    }).format(new Date(value));

    return (
        <main className="page-shell">
            <section className="feed-intro">
                <div>
                    <p className="eyebrow">Hospital care, heard</p>
                    <h1>Better care starts with listening.</h1>
                    <p className="feed-intro-copy">A shared view of concerns raised by patients and families, with updates from the teams working to resolve them.</p>
                </div>
                <div className="intro-action">
                    {user?.role === "user" ? (
                        <>
                            <Link className="button-primary" to="/dashboard">File a complaint <span aria-hidden="true">→</span></Link>
                            <p>Your report can be private or public.</p>
                        </>
                    ) : !user ? (
                        <>
                            <Link className="button-primary" to="/register">Share a concern <span aria-hidden="true">→</span></Link>
                            <p>Already registered? <Link to="/login">Sign in</Link></p>
                        </>
                    ) : null}
                </div>
            </section>

            <section aria-labelledby="public-feed-title">
                <div className="feed-toolbar">
                    <h2 id="public-feed-title" className="feed-toolbar-title">Community concerns <span>{complaints.length} shown</span></h2>
                    <span className="feed-update">Public reports · Newest first</span>
                </div>

                {errorMessage && (
                    <div className="error-state" role="alert">
                        <h2>We hit a connection issue</h2>
                        <p>{errorMessage}</p>
                        <button className="button-secondary" onClick={() => window.location.reload()}>Try again</button>
                    </div>
                )}

                {loading && <p className="loading-state" role="status">Loading community concerns…</p>}

                {!loading && !errorMessage && complaints.length === 0 && (
                    <div className="empty-state">
                        <h2>No public concerns yet</h2>
                        <p>When a patient chooses to share a concern publicly, it will appear here.</p>
                    </div>
                )}

                <ul className="complaint-list">
                    {complaints.map((complaint, index) => (
                        <li className="complaint-card" key={complaint.id} style={{ animationDelay: `${Math.min(index, 8) * 35}ms` }}>
                            <div className="complaint-card-head">
                                <div className="complaint-meta">
                                    <span className="department-label">{departmentName(complaint.department_id)}</span>
                                    <span className="meta-separator" aria-hidden="true">·</span>
                                    <span className="meta-small">Reported {formatDate(complaint.created_at)}</span>
                                </div>
                                <div className="complaint-tags">
                                    <span className={`status-pill status-${complaint.current_status}`}>{complaint.current_status.replace("_", " ")}</span>
                                    {complaint.identity_display === "anonymous" && <span className="visibility-pill">Anonymous</span>}
                                </div>
                            </div>
                            <p className="complaint-description">{complaint.description}</p>
                            <div className="complaint-card-foot">
                                <span className="complaint-author">Shared by {complaint.filer_username || "Anonymous"}</span>
                                <span className="meta-small">Concern #{complaint.id}</span>
                            </div>
                        </li>
                    ))}
                </ul>

                {hasMore && !loading && (
                    <div className="page-footer">
                        <button className="button-secondary" onClick={loadMore} disabled={loadingMore}>
                            {loadingMore ? "Loading…" : "Load more concerns"}
                        </button>
                    </div>
                )}
            </section>
        </main>
    );
}

export default Feed;