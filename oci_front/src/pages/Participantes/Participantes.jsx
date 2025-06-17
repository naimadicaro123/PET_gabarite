import { useState } from "react";
import api from "../../config/config.js"

export default function Participantes() {

    const [nome, setNome] = useState("");
    const [escola, setEscola] = useState("");
    const [inscricao, setInscricao] = useState("");

    const sendForm = async e => {
        e.preventDefault();
        console.log("Processando");

        if(inscricao.length > 10) {
            alert("O numero da inscricao deve ter no máximo 10 digitos");
        }

        const dataForm = {
            nome, 
            escola,
            inscricao,
        };

        const headers = {   
            'headers': {
                'Content-Type': 'application/json'
            },
        }

        console.log(dataForm);


        await api.post("/participantes", dataForm, headers).then((response) => {
            console.log(response);
            alert("Participante cadastrado com sucesso");
            setNome("");
            setEscola("");
            setInscricao("");
        }).catch((err) => {
            if(err.response) {
                console.log(err.response);
                alert("erro ao enviar ao fazer o cadastro");
            } else {
                console.log("Erro: Tente mais tarde");
                alert("Erro de conexão com o servidor.");
            }
        })
    }

    return (
        <div>
            <form onSubmit={sendForm}>
                <h1>Cadastro de Participantes</h1>
                    <input type="text" name="" id="" value={nome} placeholder="Nome" onChange={e => setNome(e.target.value)} required/>
                    <input type="text" name="" id="" value={escola} placeholder="Escola" onChange={e => setEscola(e.target.value)} required/>
                    <input type="number" name="" id="" value={inscricao} placeholder="Numero de inscrição" onChange={e => setInscricao(e.target.value)} required/>
                    <button type="submit">Enviar</button>
            </form>
        </div>
    );
}
