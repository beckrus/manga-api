import { Route, Routes, BrowserRouter } from "react-router-dom";
import MangaListPage from './components/Manga/MangaListPage';
import MangaPage from './components/Manga/MangaDetailPage';
import MangaReader from './components/Manga/MangaReader';

function App() {

  return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<MangaListPage />} />
          <Route path="/manga/:idAndSlug" element={<MangaPage />} />
          <Route path="/manga/:idAndSlug/reader/:chapterId" element={<MangaReader />} />
        </Routes>
      </BrowserRouter>
  );
}

export default App;

