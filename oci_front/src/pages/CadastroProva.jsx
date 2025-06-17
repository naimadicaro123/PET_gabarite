// src/pages/CadastroProva.jsx

import React from 'react';
import { Link } from 'react-router-dom';
import "../styles/style.css"; // Importa o CSS corretamente

function CadastroProva() {
  return (
    <>
      <header>
        <div className="image_container">
          {/* Usa o caminho direto da imagem na pasta public */}
          <img src="/oci-logo-horizontal-color.svg" alt="Logo OCI" />
        </div>
      </header>
      <main>
        <form>
          <div className="itens">
            <h2>Cadastro das Provas</h2>
            <select required defaultValue="">
              <option value="" disabled hidden>Selecione uma modalidade</option>
              <option value="1">Iniciante</option>
              <option value="2">Intermediário</option>
              <option value="3">Avançado</option>
            </select>
          </div>

          <div className="the_buttons">
            <Link to="/" className="link-btn">
              <button type="button">VOLTAR</button>
            </Link>

            <Link to="/page3" className="link-btn">
              <button type="button">AVANÇAR</button>
            </Link>
          </div>
        </form>
      </main>

      <footer>
        <div>
          <p>© 2025 - Todos os direitos reservados</p>
          <p className="nomes">Desenvolvido por: Francisco Iram, Ícaro Damian, Felipe e Daniel Ítalo</p>
        </div>
      </footer>
    </>
  );
}

export default CadastroProva;
