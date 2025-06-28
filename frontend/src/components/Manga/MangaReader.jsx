import { useState, useEffect, useRef, useCallback } from 'react';
import { useParams } from "react-router-dom";
import { ChevronLeft, Bookmark } from 'lucide-react';

// Константы
const API_BASE_URL = '/api';
const SCROLL_THRESHOLD = 800;

// Кастомные хуки
const useInfiniteScroll = (callback, hasMore, isLoading) => {
  useEffect(() => {
    if (!hasMore || isLoading) return;

    const handleScroll = () => {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      const windowHeight = window.innerHeight;
      const documentHeight = document.documentElement.scrollHeight;
      
      if (scrollTop + windowHeight >= documentHeight - SCROLL_THRESHOLD) {
        callback();
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [callback, hasMore, isLoading]);
};

const useMangaReader = (mangaId, initialChapterId) => {
  const [state, setState] = useState({
    manga: null,
    currentChapterId: initialChapterId,
    currentChapterNumber: null,
    pages: [],
    loading: false,
    nextChapterLoading: false,
    hasNextChapter: true,
    error: null
  });

  const loadingRef = useRef(false);
  const nextChapterLoadingRef = useRef(false);

  // API функции
  const fetchManga = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/manga/${mangaId}`);
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      setState(prev => ({ ...prev, manga: data }));
    } catch (error) {
      console.warn('Error fetching manga:', error);
      setState(prev => ({ ...prev, error: `Ошибка загрузки манги: ${error.message}` }));
    }
  }, [mangaId]);

  const fetchPages = useCallback(async (mangaId, chapterId) => {
    const response = await fetch(`${API_BASE_URL}/manga/${mangaId}/chapters/${chapterId}/pages`, {
      headers: { 'accept': 'application/json' }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json() || [];
  }, []);

  const fetchNextChapterPages = useCallback(async (mangaId, chapterId) => {
    const response = await fetch(`${API_BASE_URL}/manga/${mangaId}/chapters/${chapterId}/next`, {
      headers: { 'accept': 'application/json' }
    });
    
    if (!response.ok) {
      if (response.status === 404) return null;
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  }, []);

  const loadChapter = useCallback(async (chapterId, append = false) => {
    if (loadingRef.current) return;
    
    setState(prev => ({ ...prev, loading: true, error: null }));
    loadingRef.current = true;

    try {
      const newPages = await fetchPages(mangaId, chapterId);
      setState(prev => ({
        ...prev,
        pages: append ? [...prev.pages, ...newPages] : newPages,
        currentChapterId: chapterId,
        loading: false
      }));
    } catch (error) {
      console.warn('Error loading chapter:', error);
      setState(prev => ({
        ...prev,
        error: `Ошибка загрузки главы: ${error.message}`,
        loading: false
      }));
    } finally {
      loadingRef.current = false;
    }
  }, [mangaId, fetchPages]);

  const loadNextChapter = useCallback(async () => {
    if (nextChapterLoadingRef.current || !state.hasNextChapter || !state.currentChapterId) return;
    
    setState(prev => ({ ...prev, nextChapterLoading: true }));
    nextChapterLoadingRef.current = true;

    try {
      const nextChapterData = await fetchNextChapterPages(mangaId, state.currentChapterId);
      
      if (nextChapterData?.pages) {
        setState(prev => ({
          ...prev,
          pages: [...prev.pages, ...nextChapterData.pages],
          currentChapterNumber: nextChapterData.number,
          currentChapterId: nextChapterData.id,
          nextChapterLoading: false
        }));
        
        // Обновляем URL
        const newUrl = `/manga/${mangaId}/reader/${nextChapterData.id}`;
        window.history.replaceState(null, '', newUrl);
      } else {
        setState(prev => ({ ...prev, hasNextChapter: false, nextChapterLoading: false }));
      }
    } catch (error) {
      console.warn('Error loading next chapter:', error);
      setState(prev => ({ ...prev, hasNextChapter: false, nextChapterLoading: false }));
    } finally {
      nextChapterLoadingRef.current = false;
    }
  }, [mangaId, state.currentChapterId, state.hasNextChapter, fetchNextChapterPages]);

  const retryLoadChapter = useCallback(() => {
    if (mangaId && state.currentChapterId) {
      loadChapter(state.currentChapterId);
    }
  }, [mangaId, state.currentChapterId, loadChapter]);

  return {
    ...state,
    loadChapter,
    loadNextChapter,
    retryLoadChapter,
    fetchManga
  };
};

// Компоненты
const Header = ({ manga, currentChapterNumber, onBack }) => (
  <div className="sticky top-0 z-50 bg-black bg-opacity-90 backdrop-blur-sm text-white">
    <div className="flex items-center justify-between px-4 py-3">
      <div className="flex items-center space-x-4">
        <button 
          className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
          onClick={onBack}
          aria-label="Назад"
        >
          <ChevronLeft className="w-5 h-5" />
        </button>
        <div>
          <h1 className="font-bold">{manga?.main_name || '...'}</h1>
          <p className="text-sm text-gray-300">
            Глава {currentChapterNumber || '...'}
          </p>
        </div>
      </div>
      
      <div className="flex items-center space-x-2">
        <button 
          className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
          aria-label="Добавить в закладки"
        >
          <Bookmark className="w-5 h-5" />
        </button>
      </div>
    </div>
  </div>
);

const ErrorMessage = ({ error, onRetry }) => (
  <div className="bg-red-600 text-white p-4 mx-4 mt-4 rounded-lg">
    {error}
    <button 
      onClick={onRetry}
      className="ml-4 underline hover:no-underline"
    >
      Повторить
    </button>
  </div>
);

const LoadingSpinner = ({ message }) => (
  <div className="flex items-center justify-center py-8">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-600"></div>
    <span className="ml-3 text-gray-600">{message}</span>
  </div>
);

const PageImage = ({ page, index }) => (
  <div
    key={`${page.id}-${index}`}
    className="relative"
    style={{ width: 'auto' }}
  >
    <img
      src={`${API_BASE_URL}${page.url}`}
      alt={`Page ${page.page_number}`}
      className="w-full h-auto block"
      loading="lazy"
    />
  </div>
);

const EndMessage = () => (
  <div className="text-center py-8 text-gray-600">
    <p className="text-lg font-semibold">Конец манги</p>
    <p className="text-gray-500 mt-2">Больше глав нет</p>
  </div>
);

// Основной компонент
function MangaReader() {
  const { idAndSlug, chapterId } = useParams();
  const mangaId = idAndSlug?.split("-")[0];
  
  const {
    manga,
    currentChapterId,
    currentChapterNumber,
    pages,
    loading,
    nextChapterLoading,
    hasNextChapter,
    error,
    loadChapter,
    loadNextChapter,
    retryLoadChapter,
    fetchManga
  } = useMangaReader(mangaId, chapterId);

  // Эффекты
  useEffect(() => {
    if (mangaId) {
      fetchManga();
    }
  }, [mangaId, fetchManga]);

  useEffect(() => {
    if (mangaId && chapterId) {
      loadChapter(chapterId);
    }
  }, [mangaId, chapterId, loadChapter]);

  // Бесконечная прокрутка
  useInfiniteScroll(loadNextChapter, hasNextChapter, nextChapterLoading);

  const handleBack = useCallback(() => {
    window.history.back();
  }, []);

  // Обработка ошибок маршрутизации
  if (!mangaId || !chapterId) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center text-red-600">
          <p>Неверные параметры URL</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen" style={{ backgroundColor: "hsl(240 10% 95%)" }}>
      <Header 
        manga={manga} 
        currentChapterNumber={currentChapterNumber}
        onBack={handleBack}
      />

      {error && (
        <ErrorMessage error={error} onRetry={retryLoadChapter} />
      )}

      <div className="flex flex-col items-center">
        {pages.map((page, index) => (
          <PageImage key={`${page.id}-${index}`} page={page} index={index} />
        ))}

        {loading && (
          <LoadingSpinner message="Загрузка главы..." />
        )}

        {nextChapterLoading && (
          <LoadingSpinner message="Загрузка следующей главы..." />
        )}

        {!hasNextChapter && !loading && !nextChapterLoading && pages.length > 0 && (
          <EndMessage />
        )}
      </div> 
    </div>
  );
}

export default MangaReader;