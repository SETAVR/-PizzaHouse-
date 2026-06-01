import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/client";
import CartButton from "../components/CartButton";
import FavoriteButton from "../components/FavoriteButton";
import ReviewForm from "../components/ReviewForm";
import ReviewList from "../components/ReviewList";
import { getPizzaImageUrl } from "../utils/pizzaImages";

export default function PizzaDetailPage() {
  const { id } = useParams();
  const [pizza, setPizza] = useState(null);
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    api.get(`/pizzas/${id}/`).then((response) => setPizza(response.data));
    api.get(`/pizzas/${id}/reviews/`).then((response) => setReviews(response.data));
  }, [id]);

  if (!pizza) {
    return <main className="container">Загрузка...</main>;
  }

  return (
    <main className="container detail">
      <img src={getPizzaImageUrl(pizza)} alt={pizza.title} />
      <section>
        <p className="category">{pizza.category_title}</p>
        <h1>{pizza.title}</h1>
        <p>{pizza.description}</p>
        <strong className="price">{Number(pizza.price).toFixed(0)} ₽</strong>
        <div className="actions">
          <CartButton pizza={pizza} />
          <FavoriteButton pizzaId={pizza.id} />
        </div>
        <ReviewForm pizzaId={pizza.id} onCreated={(review) => setReviews((current) => [review, ...current])} />
        <h2>Отзывы</h2>
        <ReviewList reviews={reviews} />
      </section>
    </main>
  );
}
