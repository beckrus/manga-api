import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { Eye, Bookmark } from 'lucide-react';

const slugify = (text) =>
  text.toLowerCase().replace(/[^a-zа-я0-9]+/gi, "-").replace(/^-+|-+$/g, "");

function MangaPage() {
  const { idAndSlug } = useParams();
  const navigate = useNavigate();
  const [manga, setManga] = useState(null);
  const [chapters, setChapters] = useState([]);
  const id = idAndSlug.split("-")[0];

  useEffect(() => {
    async function fetchManga() {
      const res = await fetch(`api/manga/${id}`);
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

  // Загрузка списка глав
  useEffect(() => {
    async function fetchChapters() {
      const res = await fetch(`api/manga/${id}/chapters`);
      if (res.ok) {
        const data = await res.json();
        setChapters(data.reverse());
      }
    }
    fetchChapters();
  }, [id]);

  if (!manga) return <div>Загрузка...</div>;

  return (
    <div className="m-6">
        <div className="flex flex-col md:flex-row gap-6">
          <img id="image" src={`api${manga.image}`} alt={manga.main_name} className="w-70 rounded shadow-lg rounded-lg"/>
          <div className="gap-2 flex flex-col mt-3">
            <h1 className="text-2xl font-bold text-gray-800"> {manga.main_name} | {manga.secondary_name}</h1>
            <div className="flex items-center space-x-6 text-gray-600 mb-2">
              <div className="flex items-center space-x-2">
                <Eye className="w-5 h-5" />
                <span>Просмотров: {manga.count_views}</span>
              </div>
              <div className="flex items-center space-x-2">
                <Bookmark className="w-5 h-5" />
                <span>Закладок: {manga.count_bookmarks}</span>
              </div>
            </div>
            <p><strong>Описание:</strong> {manga.description}</p>
            {manga.current_reading_chapter?
            `<a href="api/reader?manga_id=${mangaId}&chapter_id=${manga.current_reading_chapter}" class="mt-8 inline-block bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition shadow m-auto">Продолжить</a>`
            :''}
          </div>
        </div>

        <div className="chapters">
          <h2 className="text-xl font-semibold mt-6 mb-3">Главы</h2>
          <ul id="chapter-list" className="list-disc pl-5">
           {chapters.map((chapter) => (
              <li key={chapter.id} className="mb-2">
                <a href={`/manga/${idAndSlug}/reader/${chapter.id}`}>
                  Глава {chapter.number}
                </a>
              </li>
            ))}
          </ul>
        </div>
    </div>
  );
}

export default MangaPage