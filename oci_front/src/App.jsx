import './App.css';
import CadastroAluno from './pages/cadastro.jsx';       // sua página cadastro
import CadastroProva from './pages/CadastroProva.jsx';  // página cadastro de provas

import Home from './pages/Home';
import Gabaritos from "./pages/Gabaritos/Gabaritos.jsx";
import Participantes from "./pages/Participantes/Participantes.jsx";
import List from "./pages/List_gabaritos/List_gabaritos.jsx";
import Navbar from './components/Navbar.jsx';

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
  return (
    <Router>
      <Navbar /> 
      <Routes>
        {/* Rota raiz abre cadastro.jsx */}
        <Route path="/" element={<CadastroAluno />} />

        {/* Segunda rota importante */}
        <Route path="/cadastro-prova" element={<CadastroProva />} />

        {/* Rotas restantes */}
        <Route path="/home" element={<Home />} />
        <Route path="/participantes" element={<Participantes />} />
        <Route path="/gabaritos" element={<Gabaritos />} />
        <Route path="/resultados" element={<List />} />

        {/* Você pode adicionar rota para cadastro se quiser */}
        <Route path="/cadastro" element={<CadastroAluno />} />
      </Routes>
    </Router>
  );
}

export default App;
