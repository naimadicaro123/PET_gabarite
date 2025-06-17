import './App.css';
import Home from './pages/Home';
import Gabaritos from "./pages/Gabaritos/Gabaritos.jsx";
import Participantes from "./pages/Participantes/Participantes.jsx";
import List from "./pages/List_gabaritos/List_gabaritos.jsx";
import Navbar from './components/Navbar.jsx';

// Importando os HTMLs convertidos para React:
import CadastroAluno from './pages/CadastroAluno.jsx';      // index.html
import CadastroProva from './pages/CadastroProva.jsx';      // page2.html

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
  return (
    <Router>
      <Navbar /> {/* A navbar aparece em todas as páginas */}
      <Routes>
        {/* Rotas já existentes */}
        <Route path="/" element={<Home />} />
        <Route path="/participantes" element={<Participantes />} />
        <Route path="/gabaritos" element={<Gabaritos />} />
        <Route path="/resultados" element={<List />} />

        {/* Rotas para as páginas HTML convertidas */}
        <Route path="/cadastro" element={<CadastroAluno />} />
        <Route path="/cadastro-prova" element={<CadastroProva />} />
      </Routes>
    </Router>
  );
}

export default App;


