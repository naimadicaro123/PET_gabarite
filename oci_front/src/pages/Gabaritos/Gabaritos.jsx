import "../../assets/gabaritos.css";
import { useState } from "react";
import api from "../../config/config.js";


export default function Gabaritos() {
    const [gabarito, setGabarito] = useState("");
    const [modalidade, setModalidade] = useState("");

    const sendForm = async e => {
        e.preventDefault();
        console.log("Envio dos dados");

        const regex = /^[a-e]{20}$/
        // ^ inicio da string | [a-e] apenas a letras minusculas a,b,c,d,e são aceitas | {20} deve conter exatamente 20 caracteres| $ representa o fim da string

        // se o gabarito passado for diferente do formato de regex ele não envia os dados para a api
        if(!regex.test(gabarito)) {
            alert("O gabarito deve conter 20 letras entre 'a' e 'e'")
            return;
        }

        const data = {
            gabarito,
            modalidade,
        };

        console.log(data)
        const headers = {   
            'headers': {
                'Content-Type': 'application/json'
            },
        }

        await api.post("/gabaritos", data, headers).then((response) => {
            console.log(response);
            alert("Gabarito enviado com sucesso!");
            setGabarito("");
            setModalidade("");
        }).catch((err) => {
            if(err.response) {
                console.log(err.response);
                alert("erro ao enviar o gabarito")
            } else {
                console.log("Erro: Tente mais tarde");
                alert("Erro de conexão com o servidor.");
            }
        })
    }


    return (
        <div className="form">
            <form onSubmit={sendForm}>
                <h1>Cadastro de Gabaritos</h1>
                <input type="text" name="gabarito" placeholder="" value={gabarito}  maxLength={20} onChange={e => setGabarito(e.target.value)} required/>
                <select name="modalidade" value={modalidade} onChange={e => setModalidade(e.target.value)} required>
                    <option value="" disabled hidden>Selecione uma modalidade</option>
                    <option value="iniciacao-A">Iniciação A</option>
                    <option value="iniciacao-B">Iniciação B</option>
                    <option value="programacao">Programação</option>
                </select>
                <button type="submit">Enviar</button>
            </form>
        </div>
    );
}
