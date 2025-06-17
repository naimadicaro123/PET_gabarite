// src/pages/Cadastro.jsx

import React from 'react';
import { Link } from 'react-router-dom';
import '../the_css/style.css'; // ajuste o caminho se necessário
import logo from '../img/oci-logo-horizontal-color.svg'; // mova a imagem para src/img

function Cadastro() {
  return (
    <>
      <header>
        <div className="image_container">
          <img src={logo} alt="Logo OCI" />
        </div>
      </header>

      <main>
        <div className="cadastre_div">
          <h2>Cadastro de Alunos</h2>
          <div className="dates">
            <label htmlFor="nome">Nome do aluno:</label>
            <input type="text" name="nome" />

            <label htmlFor="escola">Nome da escola:</label>
            <input type="text" name="escola" />

            <label htmlFor="cpf">CPF do aluno:</label>
            <input type="text" name="cpf" />

            <div className="the_buttons">
              <Link to="/page2" className="link-btn" id="avanced">
                <button type="button">AVANÇAR</button>
              </Link>
            </div>
          </div>
        </div>
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

export default Cadastro;
