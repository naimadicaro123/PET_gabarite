import { useState } from "react";
import "../assets/file.css";
import { Link } from "react-router-dom";
import api from "../config/config.js";


export default function FileUploader() {
  //Quando carregar essa página ela inicia como vazio
  const [image, setImage] = useState("");

  const uploadImage = async (e) => {
    e.preventDefault(); // usado para que não seja preciso recarregar a página
    console.log("Upload imagem");

    // envio da imagem
    const formData = new FormData();
    formData.append("image", image);

    // envio dos dados em formato json
    const headers = {
      headers: {
        "Content-Type": "application/json",
      },
    };

    //Tratamento de erros
    await api
      .post("/Upload-image", formData, headers)
      .then((response) => {
        // status 200, caso seja feito o upload com sucesso
        console.log(response);
      })
      .catch((err) => {
        // se existir erro
        if (err.response) {
          // status 400
          console.log(err.response);
        } else {
          // caso a aplicação do back não está ativo
          console.log("Erro: Tente mais tarde");
        }
      });
  };
  // onChange identica se o usuário selecionou a imagem
  // e.target.files pega a imagem que o usuário selecionou
  return (
    <div className="Filebox">
      <form onSubmit={uploadImage}>
        <div className="text_label">
          <h1>Selecione gabarito</h1>
        </div>
        <input
          type="file"
          name="image" required
          onChange={(e) => setImage(e.target.files[0])}
        />
        <div>
          <button type="submit" className="button">
            Enviar gabarito
          </button>
          <button type="submit" className="button"> 
            Salvar gabarito
          </button>
        </div>
      </form>
      <Link to="/resultados">Visualizar gabaritos </Link>
    </div>
  );
}
