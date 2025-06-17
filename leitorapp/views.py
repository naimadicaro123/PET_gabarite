from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import UploadProvaSerializer, ParticipanteSerializer, ProvaSerialiazer, ResultadoSerializer
from . import serializers
from . import models
from .models import Participante, Prova, Resultado
from .compare import comparar_leitura
import os

from .leitor_wrapper import read_image_from_data
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser


class ResultadoViewSet(viewsets.ModelViewSet):
    queryset = Resultado.objects.all()
    serializer_class = ResultadoSerializer
    parser_classes = [MultiPartParser]

    @action(detail=False, methods=['post'], url_path='resultados')
    def avaliar_resposta(self, request):
        leitura = request.data.get('gabarito_res')
        id_prova = request.data.get('id_prova')
        id_aluno = request.data.get('id_aluno')
        arquivo = request.FILES.get('arquivo')

        erro_raw = request.data.get('erro')
        erro = int(erro_raw) if erro_raw not in [None, ''] else 0

        if not leitura or not id_prova or not arquivo:
            return Response({
                "erro": "leitura, id_prova e arquivo são obrigatórios"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            prova = Prova.objects.get(id_prova=id_prova)
        except Prova.DoesNotExist:
            return Response({"erro": "Prova não encontrada"}, status=status.HTTP_404_NOT_FOUND)

        # Cálculo seguro da nota
        try:
            acertos, total = comparar_leitura(leitura, prova.gabarito)
            acertos = max(0, int(acertos)) if acertos is not None else 0
            total = max(1, int(total)) if total is not None else 1  # Evita divisão por zero
            
            nota = round((10 * acertos / total), 2)  # Nota de 0 a 10
            nota = max(0.0, min(10.0, nota))  # Garante que está entre 0 e 10
        except Exception as e:
            print(f"Erro no cálculo: {str(e)}")
            acertos, total, nota = 0, 1, 0.0  # Valores padrão em caso de erro

        acertos_str = f'{acertos}/{total}'

        # Criação do resultado
        resultado = Resultado.objects.create(
            erro=erro,
            gabarito_res=leitura,
            acertos=acertos_str,
            nota=nota,  # Agora sempre tem valor
            id_prova=id_prova,
            id_aluno=id_aluno,
            arquivo=arquivo
        )
        
        serializer = ResultadoSerializer(resultado)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ParticipanteViewSet(viewsets.ModelViewSet):
    queryset = Participante.objects.all()
    serializer_class = ParticipanteSerializer


class ProvaViewSet(viewsets.ModelViewSet):
    queryset = Prova.objects.all()
    serializer_class = ProvaSerialiazer


class UploadViewSet(viewsets.ViewSet):
    serializer_class = UploadProvaSerializer

    @action(detail=False, methods=['post'])
    def upload(self, request):
        serializer = UploadProvaSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['image']
            file_type = os.path.splitext(uploaded_file.name)[1]
            file_data = uploaded_file.read()

            try:
                resultado = read_image_from_data(file_type, file_data)
                return Response(resultado, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"erro": "Não foi possível processar a imagem", "detalhe": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)