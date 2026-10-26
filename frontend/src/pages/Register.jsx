import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api/axios";

function Register(){
    const [email, setEmail] = useState("");
    const [mobileNum, setMobileNum] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [feedback, setFeedback] = useState(null);
    const [waiting, setWaiting] = useState(false);

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (password !== confirmPassword)
        {
            setFeedback("Passwords do not match.")
            return;
        }

        setWaiting(true);
        setFeedback(null);

        try {
            await api.post("/auth/register", {
                username,
                mobile_number: mobileNum,
                password,
                email,
                unique_id: null
            });

            navigate("/login");
        }
        catch(err){
            setFeedback(err.response?.data?.detail || "Registration failed. Please try again.");
        }
        finally{
            setWaiting(false);
        }
    }

    return (
        <main className="auth-shell">
            <section className="auth-layout auth-layout-register" aria-labelledby="register-title">
                <aside className="auth-aside">
                    <p className="eyebrow">Care works better together</p>
                    <p className="auth-aside-quote">Make room for the conversation that matters.</p>
                    <p className="auth-aside-note">Create an account to submit concerns and keep track of every update.</p>
                    <span className="auth-aside-index">YOUR VOICE <span>·</span> YOUR CARE</span>
                </aside>
                <div className="auth-form-panel">
                    <p className="eyebrow">Get started</p>
                    <h1 id="register-title">Create your account</h1>
                    <p className="auth-intro">A few details are all you need to join the conversation.</p>
                    <form className="form-stack" onSubmit={handleSubmit}>
                        <div className="field-grid">
                            <div className="field">
                                <label htmlFor="register-username">Username</label>
                                <input id="register-username" autoComplete="username" maxLength={50} required value={username} onChange={(e) => setUsername(e.target.value)} />
                            </div>
                            <div className="field">
                                <label htmlFor="register-mobile">Mobile number</label>
                                <input id="register-mobile" type="tel" autoComplete="tel" required value={mobileNum} onChange={(e) => setMobileNum(e.target.value)} />
                            </div>
                            <div className="field field-span">
                                <label htmlFor="register-email">Email <span className="field-optional">Optional</span></label>
                                <input id="register-email" type="email" autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                            </div>
                            <div className="field">
                                <label htmlFor="register-password">Password</label>
                                <input id="register-password" type="password" autoComplete="new-password" required value={password} onChange={(e) => setPassword(e.target.value)} />
                            </div>
                            <div className="field">
                                <label htmlFor="register-confirm">Confirm password</label>
                                <input id="register-confirm" type="password" autoComplete="new-password" required value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} />
                            </div>
                        </div>
                        {feedback && <p className="form-feedback form-feedback-error" role="alert">{feedback}</p>}
                        <button className="button-primary form-submit" type="submit" disabled={waiting}>
                            {waiting ? "Creating account…" : "Create account"}<span aria-hidden="true">→</span>
                        </button>
                    </form>
                    <p className="auth-switch">Already registered? <Link to="/login">Sign in</Link></p>
                </div>
            </section>
        </main>
    )
}

export default Register;