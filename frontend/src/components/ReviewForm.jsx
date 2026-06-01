import { useState } from "react";
import api from "../api/client";
import { useAuth } from "../context/AuthContext";

export default function ReviewForm({ pizzaId, onCreated }) {
  const { isAuthenticated } = useAuth();
  const [text, setText] = useState("");
  const [rating, setRating] = useState(5);
  const [error, setError] = useState("");

  const submitReview = async (event) => {
    event.preventDefault();
    if (!text.trim()) {
      setError("Введите текст отзыва.");
      return;
    }
    if (rating < 1 || rating > 5) {
      setError("Рейтинг должен быть от 1 до 5.");
      return;
    }
    const response = await api.post(`/pizzas/${pizzaId}/reviews/`, { text, rating });
    setText("");
    setRating(5);
    setError("");
    onCreated(response.data);
  };

  if (!isAuthenticated) {
    return <p>Войдите, чтобы оставить отзыв.</p>;
  }

  return (
    <form className="form" onSubmit={submitReview}>
      <h3>Оставить отзыв</h3>
      {error && <p className="form-error">{error}</p>}
      <textarea value={text} onChange={(event) => setText(event.target.value)} placeholder="Ваш отзыв" />
      <label>
        Рейтинг
        <input type="number" min="1" max="5" value={rating} onChange={(event) => setRating(Number(event.target.value))} />
      </label>
      <button type="submit">Отправить</button>
    </form>
  );
}
