import { useState } from "react";
import api from "../api/axios";

function AdminComplaintRow({ complaint, departmentName, onStatusUpdated }) {
  const [status, setStatus] = useState(complaint.current_status);
  const [note, setNote] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState(null);

  const handleUpdate = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setFeedback(null);

    try {
      await api.post(`/admin/complaints/${complaint.id}/status`, { status, note });
      setFeedback("Status updated.");
      setNote("");
      onStatusUpdated();
    } catch (error) {
      setFeedback(error.response?.data?.detail || "Failed to update status.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <li className="complaint-card admin-complaint-card">
      <div className="complaint-card-head">
        <div className="complaint-meta"><span className="department-label">{departmentName || `Department ${complaint.department_id}`}</span><span className="meta-separator" aria-hidden="true">·</span><span className="meta-small">Concern #{complaint.id}</span></div>
        <span className={`status-pill status-${complaint.current_status}`}>{complaint.current_status.replace("_", " ")}</span>
      </div>
      <p className="complaint-description">{complaint.description}</p>
      <div className="complaint-card-foot admin-complaint-meta"><span className="complaint-author">Filed by {complaint.filer_username || "Anonymous"}</span><span className="visibility-pill">{complaint.visibility === "public" ? "Public" : "Private"}</span></div>
      <form className="status-update-form" onSubmit={handleUpdate}>
        <div className="field">
          <label htmlFor={`status-${complaint.id}`}>Update status</label>
          <select id={`status-${complaint.id}`} value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="pending">Pending</option>
          <option value="under_review">Under Review</option>
          <option value="resolved">Resolved</option>
          <option value="rejected">Rejected</option>
          </select>
        </div>
        <div className="field status-note-field">
          <label htmlFor={`note-${complaint.id}`}>Update note <span className="field-optional">Optional</span></label>
          <input id={`note-${complaint.id}`} type="text" maxLength={1000} placeholder="Add context for the filer" value={note} onChange={(e) => setNote(e.target.value)} />
        </div>
        <button className="button-secondary" type="submit" disabled={submitting}>{submitting ? "Saving…" : "Save update"}</button>
      </form>

      {feedback && <p className={`form-feedback ${feedback === "Status updated." ? "form-feedback-success" : "form-feedback-error"}`} role="status">{feedback}</p>}
    </li>
  );
}

export default AdminComplaintRow;