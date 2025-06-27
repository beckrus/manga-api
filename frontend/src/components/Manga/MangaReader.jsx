import { useState, useEffect, useRef } from 'react';
import { useParams } from "react-router-dom";
import { ChevronLeft, Bookmark } from 'lucide-react';

function MangaReader() {
    const { idAndSlug, chapterId } = useParams();
    const mangaId = idAndSlug.split("-")[0];
    const [manga, setManga] = useState(null);
    const [currentChapterId, setCurrentChapterId] = useState(null);
    const [loading, setLoading] = useState(false);
    const [pages, setPages] = useState([]);
    const [error, setError] = useState(null);
    const [hasNextChapter, setHasNextChapter] = useState(true);
    const [nextChapterLoading, setNextChapterLoading] = useState(false);

    const loadingRef = useRef(false);
    const nextChapterLoadingRef = useRef(false);

    useEffect(() => {
        async function fetchManga() {
            const res = await fetch(`api/manga/${mangaId}`);
            const data = await res.json();
            setManga(data);
        }
        fetchManga();
    }, [idAndSlug, mangaId]);

    useEffect(() => {
        setCurrentChapterId(chapterId);
        loadChapter(mangaId, chapterId);
    }, []);

    // Infinity scroll effect
    useEffect(() => {
        const handleScroll = () => {
            if (nextChapterLoadingRef.current || !hasNextChapter) return;

            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const windowHeight = window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight;
            
            if (scrollTop + windowHeight >= documentHeight - 800) {
                loadNextChapter();
            }
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, [currentChapterId, hasNextChapter]);

    const loadChapter = async (mangaId, chapterId, append = false) => {
        if (loadingRef.current) return;
        
        setLoading(true);
        loadingRef.current = true;
        setError(null);

        try {
            const newPages = await fetchPages(mangaId, chapterId);
            if (append) {
                setPages(prevPages => [...prevPages, ...newPages]);
            } else {
                setPages(newPages);
            }
            setCurrentChapterId(chapterId);
        } catch (err) {
            console.warn(err.message)
            setError(`Ошибка загрузки главы: ${err.message}`);
        } finally {
            setLoading(false);
            loadingRef.current = false;
        }
    };

    const loadNextChapter = async () => {
        if (nextChapterLoadingRef.current || !hasNextChapter || !currentChapterId) return;
        
        setNextChapterLoading(true);
        nextChapterLoadingRef.current = true;

        try {
            const nextChapterData = await fetchNextChapterPages(mangaId, currentChapterId);
            
            if (nextChapterData && nextChapterData.pages) {
                setPages(prevPages => [...prevPages, ...nextChapterData.pages]);
                setCurrentChapterId(nextChapterData.id);
                updateUrl(nextChapterData.id);
            } else {
                setHasNextChapter(false);
            }
        } catch (err) {
            console.warn('Error loading next chapter:', err);
            setHasNextChapter(false);
        } finally {
            setNextChapterLoading(false);
            nextChapterLoadingRef.current = false;
        }
    };

    const fetchPages = async (mangaId, chapterId) => {
        try {
            const response = await fetch(`api/manga/${mangaId}/chapters/${chapterId}/pages`, {
                headers: {
                    'accept': 'application/json'
                }
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            return data || [];
        } catch (error) {
            console.warn('API error:', error);
            throw error;
        }
    };

    const fetchNextChapterPages = async (mangaId, chapterId) => {
        try {
            const response = await fetch(`api/manga/${mangaId}/chapters/${chapterId}/next`, {
                headers: {
                    'accept': 'application/json'
                }
            });
            
            if (!response.ok) {
                if (response.status === 404) {
                    return null;
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            return data;

        } catch (error) {
            console.warn('API error:', error);
            throw error;
        }
    };

    const updateUrl = (newChapterId) => {
        const newUrl = `/manga/${idAndSlug}/${newChapterId}`;
        window.history.replaceState(null, '', newUrl);
    };

    return (
        <div className="min-h-screen" style={{ backgroundColor: "hsl(240 10% 95%)" }}>
            {/* Header */}
            <div className="sticky top-0 z-50 bg-black bg-opacity-90 backdrop-blur-sm text-white">
                <div className="flex items-center justify-between px-4 py-3">
                    <div className="flex items-center space-x-4">
                        <button 
                            className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
                            onClick={() => window.history.back()}
                        >
                            <ChevronLeft className="w-5 h-5" />
                        </button>
                        <div>
                            <h1 className="font-bold">{manga?.main_name || '...'}</h1>
                            <p className="text-sm text-gray-300">Глава {currentChapterId || '...'}</p>
                        </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                        <button className="p-2 hover:bg-gray-700 rounded-lg transition-colors">
                            <Bookmark className="w-5 h-5" />
                        </button>
                    </div>
                </div>
            </div>

            {/* Error Message */}
            {error && (
                <div className="bg-red-600 text-white p-4 mx-4 mt-4 rounded-lg">
                    {error}
                    <button 
                        onClick={() => {
                            if (mangaId && currentChapterId) {
                                loadChapter(mangaId, currentChapterId);
                            }
                        }}
                        className="ml-4 underline hover:no-underline"
                    >
                        Повторить
                    </button>
                </div>
            )}

            {/* Pages Container */}
            <div className="flex flex-col items-center">
                {pages.map((page, index) => {
                    return (
                        <div
                            key={`${page.id}-${index}`}
                            className="relative"
                            style={{width: 'auto'}}
                        >
                            <img
                                src={`api${page.url}`}
                                alt={`Page ${page.page_number}`}
                                className="w-full h-auto block"
                                loading="lazy"
                            />
                        </div>
                    );
                })}

                {/* Loading Indicator for initial chapter */}
                {loading && (
                    <div className="flex items-center justify-center py-8">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-600"></div>
                        <span className="ml-3 text-gray-600">Загрузка главы...</span>
                    </div>
                )}

                {/* Loading Indicator for next chapter */}
                {nextChapterLoading && (
                    <div className="flex items-center justify-center py-8">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                        <span className="ml-3 text-gray-600">Загрузка следующей главы...</span>
                    </div>
                )}

                {/* End of Content */}
                {!hasNextChapter && !loading && !nextChapterLoading && pages.length > 0 && (
                    <div className="text-center py-8 text-gray-600">
                        <p className="text-lg font-semibold">Конец манги</p>
                        <p className="text-gray-500 mt-2">Больше глав нет</p>
                    </div>
                )}
            </div> 
        </div>
    );
}

export default MangaReader;