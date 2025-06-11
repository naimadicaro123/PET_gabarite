from django.db import models

class Participante(models.Model):
    id_aluno = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)
    escola = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    data = models.DateField()  # *** caso necessario alterar para CharField ***

    def __str__(self):
        return f'{self.nome} ({self.id_aluno})'


class Prova(models.Model):
    id_prova = models.IntegerField(primary_key=True)
    gabarito = models.CharField(max_length=100)
    modalidade = models.IntegerField()  # !!! definir as modalidades !!!

    def __str__(self):
        return f'Prova {self.id_prova}'


class Resultado(models.Model):
    id_resultado = models.AutoField(primary_key=True)
    erro = models.IntegerField()
    gabarito_res = models.CharField(max_length=100)
    acertos = models.CharField(max_length=100)  
    nota = models.FloatField()
    id_prova = models.ForeignKey(Prova, on_delete=models.CASCADE)
    id_aluno = models.ForeignKey(Participante, on_delete=models.CASCADE)
    arquivo = models.CharField(max_length=200) 

    def __str__(self):
        return f'Resultado {self.id_resultado} - Aluno {self.id_aluno.id_aluno}'

