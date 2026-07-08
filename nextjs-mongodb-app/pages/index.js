import React, { useEffect, useState } from 'react';

export default function Home() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetch('/api/items')
      .then((r) => r.json())
      .then((data) => setItems(data))
      .catch(() => setItems([]));
  }, []);

  return (
    <main style={{ padding: 24, fontFamily: 'Arial, sans-serif' }}>
      <h1>Next.js + MongoDB (ejemplo)</h1>
      <p>
        API: <code>/api/items</code>
      </p>
      <section>
        {items.length === 0 ? (
          <p>No hay ítems (conecta tu base de datos y agrega documentos).</p>
        ) : (
          <ul>
            {items.map((it) => (
              <li key={it._id}>{it.nombre || JSON.stringify(it)}</li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
