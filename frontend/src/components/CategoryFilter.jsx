export default function CategoryFilter({ categories, value, onChange }) {
  return (
    <label className="filter">
      <span>Категория</span>
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        <option value="">Все категории</option>
        {categories.map((category) => (
          <option key={category.id} value={category.id}>{category.title}</option>
        ))}
      </select>
    </label>
  );
}
