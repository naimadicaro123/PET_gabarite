import './App.css'
import Home from './pages/Home';
import Gabaritos from "./pages/Gabaritos/Gabaritos.jsx";
import Participantes from "./pages/Participantes/Participantes.jsx";
import List from "./pages/List_gabaritos/List_gabaritos.jsx"
import Navbar from './components/Navbar.jsx';
import { BrowserRouter as Router, Routes, Route} from "react-router-dom";

function App() {

  return (
    <>
      <Router>
        <Navbar/> {/*A navbar aparece em todas as paginas*/}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/participantes" element={<Participantes />} />
          <Route path="gabaritos" element={<Gabaritos /> }/>
          <Route path="/resultados" element={<List/>}></Route>
        </Routes>
      </Router>
    </>
  )
}

export default App

