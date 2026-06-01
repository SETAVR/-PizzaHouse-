export default function CartItem({ item, onQuantityChange, onRemove }) {
  return (
    <div className="cart-item">
      <div>
        <h3>{item.pizza.title}</h3>
        <p>{Number(item.pizza.price).toFixed(0)} ₽ за шт.</p>
      </div>
      <input
        type="number"
        min="1"
        value={item.quantity}
        onChange={(event) => onQuantityChange(item.pizza.id, event.target.value)}
      />
      <strong>{(Number(item.pizza.price) * item.quantity).toFixed(0)} ₽</strong>
      <button className="danger" onClick={() => onRemove(item.pizza.id)}>Удалить</button>
    </div>
  );
}
