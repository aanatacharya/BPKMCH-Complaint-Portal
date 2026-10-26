import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

function Login(){
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [submitting, setSubmitting] = useState(false);

    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        setErrorMessage("");
        const result = await login(username, password);

        if (result.success)
        {
            navigate("/");
        } else {
            setErrorMessage(result.message);
        }
        setSubmitting(false);
    };

    return (
        <main className="auth-shell">
            <section className="auth-layout" aria-labelledby="login-title">
                <aside className="auth-aside">
                    <p className="eyebrow">A better way to be heard</p>
                    <p className="auth-aside-quote">Your experience can help care move forward.</p>
                    <p className="auth-aside-note">Sign in to follow your concerns and hear from the teams reviewing them.</p>
                    <span className="auth-aside-index">PATIENT VOICE <span>·</span> CARE IN ACTION</span>
                </aside>
                <div className="auth-form-panel">
                    <p className="eyebrow">Welcome back</p>
                    <h1 id="login-title">Sign in</h1>
                    <p className="auth-intro">Access your reports and updates from your care team.</p>
                    <form className="form-stack" onSubmit={handleSubmit}>
                        <div className="field">
                            <label htmlFor="login-username">Username</label>
                            <input id="login-username" autoComplete="username" required value={username} onChange={(e) => setUsername(e.target.value)} />
                        </div>
                        <div className="field">
                            <label htmlFor="login-password">Password</label>
                            <input id="login-password" type="password" autoComplete="current-password" required value={password} onChange={(e) => setPassword(e.target.value)} />
                        </div>
                        {errorMessage && <p className="form-feedback form-feedback-error" role="alert">{errorMessage}</p>}
                        <button className="button-primary form-submit" type="submit" disabled={submitting}>
                            {submitting ? "Signing in…" : "Sign in"}<span aria-hidden="true">→</span>
                        </button>
                    </form>
                    <p className="auth-switch">New to the portal? <Link to="/register">Create an account</Link></p>
                </div>
            </section>
        </main>
    )
}

export default Login;