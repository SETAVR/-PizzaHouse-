import { Link } from "react-router-dom";
import CartButton from "./CartButton";
import FavoriteButton from "./FavoriteButton";
import { getPizzaImageUrl } from "../utils/pizzaImages";

export default function PizzaCard({ pizza, favoriteInitial = false, onFavoriteToggle }) {
  return (
    <article className="pizza-card">
      <img src={getPizzaImageUrl(pizza)} alt={pizza.title} />
      <div className="pizza-card-body">
        <p className="category">{pizza.category_title}</p>
        <h2>{pizza.title}</h2>
        <p>{pizza.description}</p>
        <strong>{Number(pizza.price).toFixed(0)} ₽</strong>
        <div className="actions">
          <CartButton pizza={pizza} />
          <FavoriteButton pizzaId={pizza.id} initial={favoriteInitial} onToggle={onFavoriteToggle} />
          <Link className="secondary button-link" to={`/pizzas/${pizza.id}`}>Подробнее</Link>
        </div>
      </div>
    </article>
  );
}
