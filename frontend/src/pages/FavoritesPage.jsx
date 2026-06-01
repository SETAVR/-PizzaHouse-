import { useEffect, useState } from "react";
import api from "../api/client";
import PizzaCard from "../components/PizzaCard";

export default function FavoritesPage() {
  const [favorites, setFavorites] = useState([]);

  useEffect(() => {
    api.get("/favorites/my/").then((response) => setFavorites(response.data));
  }, []);

  return (
    <main className="container">
      <h1>Избранное</h1>
      {!favorites.length && <p>В избранном пока пусто.</p>}
      <section className="grid">
        {favorites.map((favorite) => (
          <PizzaCard
            key={favorite.id}
            pizza={favorite.pizza}
            favoriteInitial
            onFavoriteToggle={(isFavorite) => {
              if (!isFavorite) {
                setFavorites((current) => current.filter((item) => item.id !== favorite.id));
              }
            }}
          />
        ))}
      </section>
    </main>
  );
}
