import { useEffect, useState } from "react";
import api from "../api/client";
import CategoryFilter from "../components/CategoryFilter";
import Pagination from "../components/Pagination";
import PizzaCard from "../components/PizzaCard";
import SearchBar from "../components/SearchBar";

export default function CatalogPage() {
  const [categories, setCategories] = useState([]);
  const [pizzas, setPizzas] = useState([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [page, setPage] = useState(1);
  const [meta, setMeta] = useState({ next: null, previous: null });

  useEffect(() => {
    api.get("/categories/").then((response) => setCategories(response.data.results || response.data));
  }, []);

  useEffect(() => {
    const params = { page };
    if (search) params.search = search;
    if (category) params.category = category;
    api.get("/pizzas/", { params }).then((response) => {
      setPizzas(response.data.results || response.data);
      setMeta({ next: response.data.next, previous: response.data.previous });
    });
  }, [search, category, page]);

  const changeSearch = (value) => {
    setSearch(value);
    setPage(1);
  };

  const changeCategory = (value) => {
    setCategory(value);
    setPage(1);
  };

  return (
    <main className="container">
      <section className="hero">
        <div>
          <p className="eyebrow">Учебная пиццерия</p>
          <h1>PizzaHouse</h1>
          <p>Каталог пицц с корзиной, заказами, отзывами, избранным и real-time статусом заказа.</p>
        </div>
      </section>
      <section className="toolbar">
        <SearchBar value={search} onChange={changeSearch} />
        <CategoryFilter categories={categories} value={category} onChange={changeCategory} />
      </section>
      <section className="grid">
        {pizzas.map((pizza) => <PizzaCard pizza={pizza} key={pizza.id} />)}
      </section>
      <Pagination page={page} hasNext={Boolean(meta.next)} hasPrevious={Boolean(meta.previous)} onChange={setPage} />
    </main>
  );
}
