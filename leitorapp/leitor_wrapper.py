import ctypes
import os
import logging

# Configura o logger para leitor_wrapper
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_DIR = os.path.join(BASE_DIR, 'libs')

# Ajusta LD_LIBRARY_PATH para garantir que as bibliotecas sejam encontradas
ld_path = os.environ.get("LD_LIBRARY_PATH", "")
if LIBS_DIR not in ld_path.split(":"):
    os.environ["LD_LIBRARY_PATH"] = f"{LIBS_DIR}:{ld_path}"

# Carrega as dependências manualmente antes de libleitor.so
try:
    ctypes.CDLL(os.path.join(LIBS_DIR, "libraylib.so.550"))
    ctypes.CDLL(os.path.join(LIBS_DIR, "libZXing.so.3"))
except OSError as e:
    logger.error(f"Erro ao carregar dependência: {e}")

# Ajusta LD_LIBRARY_PATH para garantir que as bibliotecas sejam encontradas
ld_path = os.environ.get("LD_LIBRARY_PATH", "")
if LIBS_DIR not in ld_path.split(":"):
    os.environ["LD_LIBRARY_PATH"] = f"{LIBS_DIR}:{ld_path}"
leitor_lib = None # Inicializa como None
is_lib_loaded = False # Flag para verificar se a biblioteca foi carregada com sucesso

try:
    # Adiciona LIBS_DIR ao LD_LIBRARY_PATH temporariamente para esta sessão
    # Isso pode ser útil em alguns cenários, mas a configuração no shell é mais robusta.
    # No entanto, ctypes.CDLL tenta usar o caminho completo primeiro.
    # A dependência de libleitor.so em libraylib.so.550 precisa que libraylib esteja acessível
    # pelo linker dinâmico do sistema antes mesmo de libleitor.so ser carregado com sucesso.
    # Por isso, o LD_LIBRARY_PATH no shell antes de iniciar o Django é crucial.
    # Exemplo de como ctypes tenta encontrar libs:
    # 1. Path completo dado a CDLL
    # 2. Caminhos em LD_LIBRARY_PATH (Linux/macOS) / PATH (Windows)
    # 3. Caminhos padrão do sistema

    leitor_lib_path = os.path.join(LIBS_DIR, 'libleitor.so')

    # Verifica se o arquivo existe antes de tentar carregar
    if not os.path.exists(leitor_lib_path):
        logger.error(f"Biblioteca libleitor.so não encontrada em: {leitor_lib_path}")
        raise FileNotFoundError(f"Biblioteca libleitor.so não encontrada em: {leitor_lib_path}")

    # Tenta carregar a biblioteca principal
    leitor_lib = ctypes.CDLL(leitor_lib_path)
    logger.info(f"Biblioteca libleitor.so carregada de: {leitor_lib_path}")
    is_lib_loaded = True

    # Define a estrutura Reading conforme leitor.h
    class Reading(ctypes.Structure):
        _fields_ = [
            ("erro", ctypes.c_int),
            ("id_prova", ctypes.c_int),
            ("id_participante", ctypes.c_int),
            ("leitura", ctypes.c_char_p)
        ]

    # Define o protótipo da função free_reading_string, se existir
    # É CRUCIAL que sua biblioteca C tenha uma função para liberar a memória de 'char* leitura'
    # Ex: void free_reading_string(char* s);
    if hasattr(leitor_lib, 'free_reading_string'):
        leitor_lib.free_reading_string.argtypes = [ctypes.c_char_p]
        leitor_lib.free_reading_string.restype = None
        logger.info("Função free_reading_string encontrada e configurada.")
    else:
        logger.warning("Função free_reading_string não encontrada na biblioteca C. Risco de vazamento de memória!")
        # Definir uma função dummy para evitar AttributeError se free_reading_string não existir
        def dummy_free_reading_string(s):
            pass
        leitor_lib.free_reading_string = dummy_free_reading_string


    # Define o protótipo da função read_image_path
    leitor_lib.read_image_path.argtypes = [ctypes.c_char_p]
    leitor_lib.read_image_path.restype = Reading

    # Define o protótipo da função read_image_data
    leitor_lib.read_image_data.argtypes = [
        ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_ubyte),
        ctypes.c_int
    ]
    leitor_lib.read_image_data.restype = Reading

except FileNotFoundError as e:
    logger.error(f"Erro: {e}. Certifique-se de que libleitor.so está em '{LIBS_DIR}'.")
except OSError as e:
    logger.error(f"Erro ao carregar a biblioteca C principal (libleitor.so) ou suas dependências: {e}")
    logger.error("Verifique se as dependências (libraylib.so.550, libZXing.so.3) estão acessíveis")
    logger.error(f"e se a variável de ambiente LD_LIBRARY_PATH inclui o diretório: {LIBS_DIR}")
    logger.error("Ou se elas estão em um local padrão do sistema.")
except Exception as e:
    logger.error(f"Ocorreu um erro inesperado ao configurar a biblioteca C: {e}")

# Funções que serão importadas pelos outros módulos.
# Elas verificarão se a biblioteca foi carregada antes de tentar usá-la.

def read_image_from_path(image_path: str) -> dict:
    """
    Chama a função read_image_path da biblioteca C.

    Args:
        image_path (str): O caminho para a imagem.

    Returns:
        dict: Um dicionário contendo os resultados da leitura.
    """
    if not is_lib_loaded:
        logger.warning("Tentativa de chamar read_image_from_path, mas a biblioteca C não está carregada.")
        return {"erro": -1, "mensagem": "Biblioteca C não carregada ou erro no carregamento inicial."}

    path_bytes = image_path.encode('utf-8')
    result = None
    leitura_str = None
    try:
        result = leitor_lib.read_image_path(path_bytes)
        leitura_str = result.leitura.decode('utf-8') if result.leitura else None
    except Exception as e:
        logger.error(f"Erro ao chamar read_image_path: {e}")
        return {"erro": -3, "mensagem": f"Erro fatal ao processar imagem: {e}"}
    finally:
        # Libera a memória alocada pela biblioteca C, se a função existir
        if result and result.leitura and hasattr(leitor_lib, 'free_reading_string'):
            leitor_lib.free_reading_string(result.leitura)

    return {
        "erro": result.erro,
        "id_prova": result.id_prova,
        "id_participante": result.id_participante,
        "leitura": leitura_str
    }

def read_image_from_data(file_type: str, file_data: bytes) -> dict:
    """
    Chama a função read_image_data da biblioteca C.

    Args:
        file_type (str): A extensão do arquivo (ex: ".png").
        file_data (bytes): Os dados brutos do arquivo da imagem.

    Returns:
        dict: Um dicionário contendo os resultados da leitura.
    """
    if not is_lib_loaded:
        logger.warning("Tentativa de chamar read_image_from_data, mas a biblioteca C não está carregada.")
        return {"erro": -1, "mensagem": "Biblioteca C não carregada ou erro no carregamento inicial."}

    file_type_bytes = file_type.encode('utf-8')
    file_data_array = (ctypes.c_ubyte * len(file_data)).from_buffer_copy(file_data)
    file_data_size = len(file_data)

    result = None
    leitura_str = None
    try:
        result = leitor_lib.read_image_data(
            file_type_bytes,
            file_data_array,
            file_data_size
        )
        leitura_str = result.leitura.decode('utf-8') if result.leitura else None
    except Exception as e:
        logger.error(f"Erro ao chamar read_image_data: {e}")
        return {"erro": -3, "mensagem": f"Erro fatal ao processar imagem: {e}"}
    finally:
        # Libera a memória alocada pela biblioteca C, se a função existir
        if result and result.leitura and hasattr(leitor_lib, 'free_reading_string'):
            leitor_lib.free_reading_string(result.leitura)

    return {
        "erro": result.erro,
        "id_prova": result.id_prova,
        "id_participante": result.id_participante,
        "leitura": leitura_str
    }
