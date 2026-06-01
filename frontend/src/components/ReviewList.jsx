export default function ReviewList({ reviews }) {
  if (!reviews.length) {
    return <p>Отзывов пока нет.</p>;
  }

  return (
    <div className="reviews">
      {reviews.map((review) => (
        <article className="review" key={review.id}>
          <strong>{review.author_username}</strong>
          <span>{review.rating}/5</span>
          <p>{review.text}</p>
        </article>
      ))}
    </div>
  );
}
