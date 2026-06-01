import { useCart } from "../context/CartContext";

export default function CartButton({ pizza }) {
  const { addToCart } = useCart();
  return <button onClick={() => addToCart(pizza)}>В корзину</button>;
}
