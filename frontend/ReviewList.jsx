import React, { useEffect, useState } from "react";

export function ReviewList({ productId }) {
  const [reviews, setReviews] = useState([]);

  useEffect(() => {
    fetch(`/api/reviews/${productId}`)
      .then((response) => response.json())
      .then(setReviews);
  }, [productId]);

  return (
    <ul>
      {reviews.map((r) => (
        <li key={r.id} dangerouslySetInnerHTML={{ __html: r.body }} />
      ))}
    </ul>
  );
}

export function ReviewCount({ reviews }) {
  return <span>{reviews.length} reviews</span>;
}

export function showSearchTerm() {
  const term = new URLSearchParams(window.location.search).get("q");
  document.getElementById("search-title").innerHTML = "Results for " + term;
}

export function showSearchHeading() {
  const term = new URLSearchParams(window.location.search).get("q");
  document.getElementById("search-title").textContent = "Results for " + term;
}

export function applyPriceRule() {
  const rule = decodeURIComponent(window.location.hash.slice(1));
  return new Function("price", "return " + rule);
}
