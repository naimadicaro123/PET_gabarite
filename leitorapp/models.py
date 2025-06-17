from django.db import models

class Participante(models.Model):
    id_aluno = models.AutoField(primary_key=True, blank=False)
    nome = models.CharField(max_length=100)
    escola = models.CharField(max_length=100)

    def __str__(self):
        ordering = ['id']
        return f'{self.nome} ({self.id_aluno})'


class Prova(models.Model):
    id_prova = models.AutoField(primary_key=True)
    gabarito = models.CharField(max_length=20)
    # modalidade = models.IntegerField()  # !!! definir as modalidades !!!

    def __str__(self):
        return f'Prova {self.id_prova}'
        

class Resultado(models.Model):
    id_resultado = models.AutoField(primary_key=True)
    erro = models.IntegerField(null=True, blank=True)
    gabarito_res = models.CharField(max_length=21)
    acertos = models.CharField(max_length=10) 
    nota = models.FloatField()
    id_prova = models.IntegerField()
    id_aluno = models.IntegerField()
    arquivo = models.FileField(upload_to='uploads/')

    def __str__(self):
        return f'Resultado {self.id_resultado} - Aluno {self.id_aluno}'

