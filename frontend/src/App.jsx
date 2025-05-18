import { Route, Routes, BrowserRouter } from "react-router-dom";
import MangaListPage from './components/Manga/MangaListPage';
import MangaPage from './components/Manga/MangaDetailPage';

function App() {

  return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<MangaListPage />} />
          <Route path="/manga/:idAndSlug" element={<MangaPage />} />
        </Routes>
      </BrowserRouter>
  );
}

export default App;

