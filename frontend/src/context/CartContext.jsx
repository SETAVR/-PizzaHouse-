import { createContext, useContext, useEffect, useMemo, useState } from "react";

const CartContext = createContext(null);
const STORAGE_KEY = "pizzahouse_cart";

function readCart() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  } catch {
    return [];
  }
}

export function CartProvider({ children }) {
  const [items, setItems] = useState(readCart);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  }, [items]);

  const addToCart = (pizza) => {
    setItems((current) => {
      const existing = current.find((item) => item.pizza.id === pizza.id);
      if (existing) {
        return current.map((item) =>
          item.pizza.id === pizza.id ? { ...item, quantity: item.quantity + 1 } : item,
        );
      }
      return [...current, { pizza, quantity: 1 }];
    });
  };

  const removeFromCart = (pizzaId) => {
    setItems((current) => current.filter((item) => item.pizza.id !== pizzaId));
  };

  const updateQuantity = (pizzaId, quantity) => {
    const normalizedQuantity = Math.max(1, Number(quantity));
    setItems((current) =>
      current.map((item) => (item.pizza.id === pizzaId ? { ...item, quantity: normalizedQuantity } : item)),
    );
  };

  const clearCart = () => setItems([]);

  const total = items.reduce((sum, item) => sum + Number(item.pizza.price) * item.quantity, 0);
  const count = items.reduce((sum, item) => sum + item.quantity, 0);

  const value = useMemo(
    () => ({ items, total, count, addToCart, removeFromCart, updateQuantity, clearCart }),
    [items, total, count],
  );

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

export function useCart() {
  return useContext(CartContext);
}
