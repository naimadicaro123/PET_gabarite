from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import random 
import string

from .models import Participante, Prova, Resultado
from .serializers import UploadProvaSerializer, ResultadoSerializer

# Simulação da "Biblioteca C" ou função de processamento de imagem

def processar_imagem_gabarito(image_path):
    """
    Simula o processamento da imagem do gabarito por uma "biblioteca C".
    Retorna os dados extraídos.
    """
    print(f"Simulando processamento da imagem: {image_path}")
    
    simulated_id_aluno = random.randint(1000, 9999)
    simulated_id_prova = random.randint(1, 10)
    simulated_erro = random.randint(0, 5)
    simulated_gabarito_res = ''.join(random.choices(string.ascii_uppercase, k=10)) 
    simulated_acertos = ''.join(random.choices(string.ascii_uppercase, k=10)) 
    simulated_nota = round(random.uniform(0.0, 10.0), 2)


    participante, created_p = Participante.objects.get_or_create(
        id_aluno=simulated_id_aluno,
        defaults={
            'nome': f'Aluno {simulated_id_aluno}',
            'escola': 'Escola Teste',
            'cpf': f'{simulated_id_aluno:04d}.{random.randint(100,999):03d}.{random.randint(100,999):03d}-{random.randint(10,99):02d}',
            'data': '2000-01-01' 
        }
    )
    prova, created_pr = Prova.objects.get_or_create(
        id_prova=simulated_id_prova,
        defaults={
            'gabarito': 'GABARITODUMMY',
            'modalidade': 1
        }
    )

    return {
        'erro': simulated_erro,
        'id_aluno': participante, 
        'id_prova': prova, 
        'gabarito_res': simulated_gabarito_res,
        'acertos': simulated_acertos,
        'nota': simulated_nota,
    }


class UploadProvaAPIView(APIView):
    serializer_class = UploadProvaSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True) 

        
        imagem_upload = serializer.validated_data['arquivo_prova']

        
        file_name = default_storage.save(imagem_upload.name, ContentFile(imagem_upload.read()))
        
        full_image_path = os.path.join(default_storage.location, file_name) 

    
        try:
            
            processed_data = processar_imagem_gabarito(full_image_path)
        except Exception as e:
            
            default_storage.delete(file_name)
            return Response({'error': f'Erro ao processar imagem: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

       
        resultado_data = {
            'erro': processed_data['erro'],
            'gabarito_res': processed_data['gabarito_res'],
            'acertos': processed_data['acertos'],
            'nota': processed_data['nota'],
            'id_prova': processed_data['id_prova'], 
            'id_aluno': processed_data['id_aluno'], 
            'arquivo': file_name, 
        }

        resultado_serializer = ResultadoSerializer(data=resultado_data)
        if resultado_serializer.is_valid():
            resultado_serializer.save() 

            return Response(resultado_serializer.data, status=status.HTTP_201_CREATED)
        else:
            default_storage.delete(file_name) 
            return Response(resultado_serializer.errors, status=status.HTTP_400_BAD_REQUEST)