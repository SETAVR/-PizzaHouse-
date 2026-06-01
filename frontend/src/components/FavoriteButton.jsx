import { useState } from "react";
import api from "../api/client";
import { useAuth } from "../context/AuthContext";

export default function FavoriteButton({ pizzaId, initial = false, onToggle }) {
  const { isAuthenticated } = useAuth();
  const [isFavorite, setIsFavorite] = useState(initial);
  const [error, setError] = useState("");

  const toggleFavorite = async () => {
    if (!isAuthenticated) {
      setError("Войдите, чтобы добавлять в избранное.");
      return;
    }
    const response = await api.post("/favorites/toggle/", { pizza_id: pizzaId });
    setIsFavorite(response.data.is_favorite);
    onToggle?.(response.data.is_favorite);
  };

  return (
    <div>
      <button className="secondary" onClick={toggleFavorite}>
        {isFavorite ? "Убрать из избранного" : "В избранное"}
      </button>
      {error && <p className="form-error">{error}</p>}
    </div>
  );
}
