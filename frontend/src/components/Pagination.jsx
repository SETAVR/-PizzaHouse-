export default function Pagination({ page, hasNext, hasPrevious, onChange }) {
  return (
    <div className="pagination">
      <button disabled={!hasPrevious} onClick={() => onChange(page - 1)}>Назад</button>
      <span>Страница {page}</span>
      <button disabled={!hasNext} onClick={() => onChange(page + 1)}>Вперед</button>
    </div>
  );
}
