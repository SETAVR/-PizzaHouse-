import { useState } from "react";
import api from "../api/client";
import { useAuth } from "../context/AuthContext";

export default function ProfilePage() {
  const { user, setUser } = useAuth();
  const [form, setForm] = useState({ email: user?.email || "", phone: user?.phone || "", address: user?.address || "", bio: user?.bio || "" });
  const [message, setMessage] = useState("");

  const updateForm = (field, value) => setForm((current) => ({ ...current, [field]: value }));

  const submitProfile = async (event) => {
    event.preventDefault();
    const response = await api.patch("/auth/profile/", form);
    setUser(response.data);
    setMessage("Профиль обновлен.");
  };

  return (
    <main className="container narrow">
      <h1>Профиль</h1>
      <form className="form" onSubmit={submitProfile}>
        {message && <p className="success">{message}</p>}
        <label>Email<input value={form.email} onChange={(event) => updateForm("email", event.target.value)} /></label>
        <label>Телефон<input value={form.phone} onChange={(event) => updateForm("phone", event.target.value)} /></label>
        <label>Адрес<input value={form.address} onChange={(event) => updateForm("address", event.target.value)} /></label>
        <label>О себе<textarea value={form.bio} onChange={(event) => updateForm("bio", event.target.value)} /></label>
        <button type="submit">Сохранить</button>
      </form>
    </main>
  );
}
