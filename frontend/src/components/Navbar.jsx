import { Link, NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useCart } from "../context/CartContext";

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuth();
  const { count } = useCart();

  return (
    <header className="topbar">
      <Link className="brand" to="/">PizzaHouse</Link>
      <nav className="nav">
        <NavLink to="/">Каталог</NavLink>
        <NavLink to="/cart">Корзина ({count})</NavLink>
        {isAuthenticated && <NavLink to="/favorites">Избранное</NavLink>}
        {isAuthenticated && <NavLink to="/orders">Мои заказы</NavLink>}
        {isAuthenticated && <NavLink to="/profile">{user?.username}</NavLink>}
        {!isAuthenticated && <NavLink to="/login">Вход</NavLink>}
        {!isAuthenticated && <NavLink to="/register">Регистрация</NavLink>}
        {isAuthenticated && <button className="link-button" onClick={logout}>Выйти</button>}
      </nav>
    </header>
  );
}
