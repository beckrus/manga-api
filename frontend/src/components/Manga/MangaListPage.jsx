import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const API_BASE_URL = '/api';

const slugify = (text) =>
  text.toLowerCase().replace(/[^a-zа-я0-9]+/gi, "-").replace(/^-+|-+$/g, "");

function MangaListPage() {
  const [mangaList, setMangaList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    const fetchManga = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/manga?page=1&per_page=10&sort=ASC`);
        const data = await response.json();
        setMangaList(data);
      } catch (error) {
        console.error('Ошибка при загрузке манги:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchManga();
  }, [search]);

  const handleSearch = (e) => {
    if (e.key === 'Enter') {
      setSearch(e.target.value);
    }
  };

  if (loading) return <p>Загрузка...</p>;

  return (
    <div className="p-4">
      <input
        type="text"
        placeholder="Поиск по названию"
        onKeyDown={handleSearch}
        className="border p-2 w-full mb-4 rounded"
      />

      <div className="flex gap-4">
        {mangaList.map((manga) => (
            <div key={manga.id} className="w-60 bg-white rounded-xl shadow overflow-hidden cursor-pointer ">
              <Link to={`/manga/${manga.id}-${slugify(manga.secondary_name)}`} className="flex flex-col h-full">
                <img 
                    src={`api${manga.image}`}
                    alt={manga.main_name}
                    className="w-full object-cover"/>
                <h3 className="mt-2 font-semibold text-center">{manga.main_name}</h3>
                <p className="text-center">{manga.secondary_name}</p>
                <div className="flex items-center justify-evenly mt-auto pb-2">
                    <div className="flex mt-2 text-center">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                            <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                        </svg>
                        <span className='ms-1'>{manga.count_views}</span>
                    </div>
                    

                    <div className="flex mt-2 text-center">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M17.593 3.322c1.1.128 1.907 1.077 1.907 2.185V21L12 17.25 4.5 21V5.507c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0 1 11.186 0Z" />
                        </svg>
                        <span className='ms-1'>{manga.count_bookmarks}</span>
                    </div>
                </div>
              </Link>
            </div>
        ))}
      </div>
    </div>
  );
}

export default MangaListPage;