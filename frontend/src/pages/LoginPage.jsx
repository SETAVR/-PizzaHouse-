import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const submitLogin = async (event) => {
    event.preventDefault();
    if (!username.trim() || !password) {
      setError("Логин и пароль обязательны.");
      return;
    }
    try {
      await login(username, password);
      navigate("/");
    } catch {
      setError("Не удалось войти.");
    }
  };

  return (
    <main className="container narrow">
      <h1>Вход</h1>
      <form className="form" onSubmit={submitLogin}>
        {error && <p className="form-error">{error}</p>}
        <label>Логин<input value={username} onChange={(event) => setUsername(event.target.value)} /></label>
        <label>Пароль<input type="password" value={password} onChange={(event) => setPassword(event.target.value)} /></label>
        <button type="submit">Войти</button>
      </form>
      <p><Link to="/register">Создать аккаунт</Link></p>
    </main>
  );
}
