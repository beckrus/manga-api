import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

const slugify = (text) =>
  text.toLowerCase().replace(/[^a-zа-я0-9]+/gi, "-").replace(/^-+|-+$/g, "");

function MangaPage() {
  const { idAndSlug } = useParams();
  const navigate = useNavigate();
  const [manga, setManga] = useState(null);
  const id = idAndSlug.split("-")[0];

  useEffect(() => {
    async function fetchManga() {
      const res = await fetch(`http://10.10.0.6:8000/manga/${id}`);
      const data = await res.json();
      setManga(data);

      // Проверка slug'а и редирект, если он не совпадает
      const correctSlug = slugify(data.main_name);
      const currentSlug = idAndSlug.split("-").slice(1).join("-");
      if (currentSlug !== correctSlug) {
        navigate(`/manga/${id}-${correctSlug}`, { replace: true });
      }
    }

    fetchManga();
  }, [idAndSlug, id, navigate]);

  if (!manga) return <div>Загрузка...</div>;

  return (
    <div>
        <h1>{manga.main_name}</h1>
        <div class="container">
          <img id="image" src={`http://10.10.0.6:8000${manga.image}`} alt={manga.main_name}/>
          <div id="details">
            <p><strong>Название:</strong> {manga.main_name} | {manga.secondary_name}</p>
            <p><strong>Описание:</strong> {manga.description}</p>
            <p><strong>Просмотры:</strong> {manga.count_views}</p>
            <p><strong>Следят:</strong> {manga.count_bookmarks}</p>
            {manga.current_reading_chapter?
            `<a href="http://10.10.0.6:8000/reader?manga_id=${mangaId}&chapter_id=${manga.current_reading_chapter}" class="mt-8 inline-block bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition shadow">Продолжить</a>`
            :''}
          </div>
        </div>

        <div class="chapters">
          <h2 class="text-xl font-semibold mt-6 mb-3">Главы</h2>
          <ul id="chapter-list" class="list-disc pl-5"></ul>
        </div>
    </div>
  );
}

export default MangaPage