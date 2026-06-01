import { MEDIA_URL } from "../api/client";

const demoPizzaImages = {
  margherita: "/pizzas/margherita.png",
  meat: "/pizzas/meat.png",
  pepperoni: "/pizzas/pepperoni.png",
  "four-cheese": "/pizzas/four-cheese.png",
  vegetarian: "/pizzas/vegetarian.png",
};

export function getPizzaImageUrl(pizza) {
  if (pizza.image) {
    return pizza.image.startsWith("http") ? pizza.image : `${MEDIA_URL}${pizza.image}`;
  }
  return demoPizzaImages[pizza.slug] || "/pizza-placeholder.svg";
}
