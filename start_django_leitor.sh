#!/bin/bash

# --- Configurações Iniciais ---
# Obtém o diretório raiz do projeto (onde manage.py está)
PROJECT_ROOT=$(dirname "$(realpath "$0")")
LIBS_DIR="$PROJECT_ROOT/leitorapp/libs"
MANAGE_PY="$PROJECT_ROOT/manage.py"

# --- Funções Auxiliares ---

# Função para codificar URLs (handle spaces and special characters)
urlencode() {
    local string="$1"
    local length="${#string}"
    local i
    for (( i = 0; i < length; i++ )); do
        local c="${string:i:1}"
        case "$c" in
            [a-zA-Z0-9.~_-]) printf "%s" "$c" ;;
            *) printf "%%%02X" "'$c" ;;
        esac
    done
}

# Função para abrir o navegador de forma multiplataforma
open_browser() {
    local url="$1"
    if command -v xdg-open > /dev/null; then
        xdg-open "$url" &
    elif command -v open > /dev/null; then
        open "$url" &
    elif command -v cygstart > /dev/null; then
        cygstart "$url" & # For Cygwin on Windows
    else
        echo "Não foi possível encontrar um comando para abrir o navegador (xdg-open, open, cygstart)."
        echo "Por favor, abra esta URL manualmente: $url"
    fi
}

# --- Verificações ---
if [ ! -f "$MANAGE_PY" ]; then
    echo "Erro: 'manage.py' não encontrado em $PROJECT_ROOT."
    echo "Por favor, execute este script a partir do diretório raiz do seu projeto Django ('meuprojeto/')."
    exit 1
fi

if [ ! -d "$LIBS_DIR" ]; then
    echo "Erro: O diretório de bibliotecas C não foi encontrado em $LIBS_DIR."
    echo "Certifique-se de que suas libs estejam em 'leitorapp/libs' dentro do seu projeto."
    exit 1
fi

# --- 1. Exporta a biblioteca LD_LIBRARY_PATH ---
echo "Configurando LD_LIBRARY_PATH para: $LIBS_DIR"
export LD_LIBRARY_PATH="$LIBS_DIR:$LD_LIBRARY_PATH"

# Verifica se a exportação funcionou (opcional, para depuração)
# echo "LD_LIBRARY_PATH atual: $LD_LIBRARY_PATH"

# --- 2. Pede o endereço da imagem ---
read -p "Por favor, digite o caminho ABSOLUTO para a imagem (ex: /home/frnc/Downloads/0012.png): " image_path

if [ -z "$image_path" ]; then
    echo "Caminho da imagem não fornecido. Abortando."
    exit 1
fi

if [ ! -f "$image_path" ]; then
    echo "Aviso: A imagem '$image_path' não parece existir. O servidor pode retornar um erro."
    read -p "Deseja continuar mesmo assim? (s/N) " continue_choice
    if [[ ! "$continue_choice" =~ ^[Ss]$ ]]; then
        echo "Operação cancelada."
        exit 1
    fi
fi

# --- 3. Inicia o servidor Django em segundo plano ---
echo "Iniciando o servidor Django em segundo plano (http://127.0.0.1:8000/)..."
# O 'nohup' garante que o processo continue rodando mesmo se o terminal for fechado
# O '>/dev/null 2>&1' redireciona a saída do servidor para /dev/null (silencia)
nohup python "$MANAGE_PY" runserver > /dev/null 2>&1 &
SERVER_PID=$! # Captura o PID do processo do servidor

echo "Servidor Django iniciado com PID: $SERVER_PID"
echo "Aguardando 5 segundos para o servidor iniciar..."
sleep 5

# --- 4. Abre o navegador com a URL de teste ---
ENCODED_IMAGE_PATH=$(urlencode "$image_path")
TEST_URL="http://127.0.0.1:8000/leitor/read-path/?image_path=$ENCODED_IMAGE_PATH"

echo "Abrindo o navegador para a URL de teste:"
echo "$TEST_URL"
open_browser "$TEST_URL"

echo ""
echo "--- Teste Concluído ---"
echo "O navegador deve exibir a resposta JSON da leitura da imagem."
echo ""
echo "Para parar o servidor Django que está rodando em segundo plano, execute o seguinte comando:"
echo "kill $SERVER_PID"
echo "Se o servidor não parar, você pode precisar usar 'kill -9 $SERVER_PID'"
echo "Ou, para encontrar o PID manualmente: 'ps aux | grep \"python manage.py runserver\"'"
