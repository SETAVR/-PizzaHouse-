import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", email: "", password: "", repeatPassword: "", phone: "", address: "" });
  const [error, setError] = useState("");

  const updateForm = (field, value) => setForm((current) => ({ ...current, [field]: value }));

  const submitRegister = async (event) => {
    event.preventDefault();
    if (!form.username || !form.email || !form.password) {
      setError("Заполните обязательные поля.");
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
      setError("Введите корректный email.");
      return;
    }
    if (form.password !== form.repeatPassword) {
      setError("Пароли не совпадают.");
      return;
    }
    try {
      await register({
        username: form.username,
        email: form.email,
        password: form.password,
        phone: form.phone,
        address: form.address,
      });
      navigate("/");
    } catch {
      setError("Не удалось зарегистрироваться.");
    }
  };

  return (
    <main className="container narrow">
      <h1>Регистрация</h1>
      <form className="form" onSubmit={submitRegister}>
        {error && <p className="form-error">{error}</p>}
        <label>Логин<input value={form.username} onChange={(event) => updateForm("username", event.target.value)} /></label>
        <label>Email<input value={form.email} onChange={(event) => updateForm("email", event.target.value)} /></label>
        <label>Пароль<input type="password" value={form.password} onChange={(event) => updateForm("password", event.target.value)} /></label>
        <label>Повтор пароля<input type="password" value={form.repeatPassword} onChange={(event) => updateForm("repeatPassword", event.target.value)} /></label>
        <label>Телефон<input value={form.phone} onChange={(event) => updateForm("phone", event.target.value)} /></label>
        <label>Адрес<input value={form.address} onChange={(event) => updateForm("address", event.target.value)} /></label>
        <button type="submit">Зарегистрироваться</button>
      </form>
    </main>
  );
}
