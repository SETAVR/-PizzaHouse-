const labels = {
  created: "Создан",
  paid: "Оплачен",
  cooking: "Готовится",
  baking: "Выпекается",
  delivering: "Передан курьеру",
  completed: "Доставлен",
};

export default function OrderStatus({ status }) {
  const steps = ["created", "paid", "cooking", "baking", "delivering", "completed"];
  const currentIndex = steps.indexOf(status);

  return (
    <div className="status-list">
      {steps.map((step, index) => (
        <span className={index <= currentIndex ? "done" : ""} key={step}>
          {labels[step]}
        </span>
      ))}
    </div>
  );
}

export { labels as orderStatusLabels };
