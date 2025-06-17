from rest_framework import serializers
from .models import Participante, Prova, Resultado


class UploadProvaSerializer(serializers.Serializer):
    image = serializers.ImageField()


    class Meta:
        pass


class ParticipanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participante
        fields = '__all__'


class ResultadoSerializer(serializers.ModelSerializer):
    acertos = serializers.CharField(read_only=True)
    nota = serializers.FloatField(read_only=True)
    id_aluno = serializers.IntegerField(read_only=True)

    class Meta:
        model = Resultado
        fields = '__all__'   


class ProvaSerialiazer(serializers.ModelSerializer):

    class Meta:
        model = Prova
        fields = '__all__'