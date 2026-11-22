import React from "react";

export function ReviewList({ reviews }) {
  return (
    <ul>
      {reviews.map((r) => (
        <li key={r.id} dangerouslySetInnerHTML={{ __html: r.body }} />
      ))}
    </ul>
  );
}

export function showSearchTerm() {
  const term = new URLSearchParams(window.location.search).get("q");
  document.getElementById("search-title").innerHTML = "Results for " + term;
}

export function showSearchHeading() {
  const term = new URLSearchParams(window.location.search).get("q");
  document.getElementById("search-title").textContent = "Results for " + term;
}

export function runUserScript(source) {
  return new Function("return " + source)();
}
