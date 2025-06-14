from rest_framework import serializers
from .models import Participante, Prova, Resultado


class UploadProvaSerializer(serializers.Serializer):
    arquivo_prova = serializers.ImageField()


    class Meta:

        pass

class ResultadoSerializer(serializers.ModelSerializer):


    class Meta:
        model = Resultado
        fields = '__all__' 