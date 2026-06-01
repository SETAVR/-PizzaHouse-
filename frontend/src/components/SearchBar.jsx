export default function SearchBar({ value, onChange }) {
  return (
    <label className="search">
      <span>Поиск по названию</span>
      <input value={value} onChange={(event) => onChange(event.target.value)} placeholder="Например, Пепперони" />
    </label>
  );
}
