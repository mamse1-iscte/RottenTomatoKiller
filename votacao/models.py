from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User




from django.db import models
from django.utils import timezone
from six import string_types
import datetime

# Create your models here.

class Genero(models.Model):
    genero=models.CharField(max_length=100)

    def __str__(self):
        return self.genero

class Subgenero(models.Model):
    genero = models.CharField(max_length=100)

    def __str__(self):
        return self.genero

class Subgenero2(models.Model):
    genero = models.CharField(max_length=100)
    def __str__(self):
        return self.genero


class Filme_ou_serie(models.Model):
    filme_texto = models.CharField(max_length=200) #nome
    filme_ranking_critica = models.IntegerField(default=0)
    genero_id = models.ForeignKey(Genero,on_delete=models.CASCADE,default=0)
    subgenero_id = models.ForeignKey(Subgenero, on_delete=models.CASCADE,default=0)
    subgenero2_id = models.ForeignKey(Subgenero2, on_delete=models.CASCADE,default=0)
    filme_descricao = models.CharField(max_length=3000)
    is_filme = models.IntegerField(default=0) # se estiver a 1 é um filme se estiver a 0 é uma série
    imagem = models.CharField(max_length=300, default='0000000')
    release_year = models.IntegerField(default=0)
    pub_data = models.DateTimeField('data de publicacao')
    trailer = models.CharField(max_length=3000,default=0)
    atores = models.CharField(max_length=3000, default=0)

    def __str__(self):
        return self.filme_texto

    def foi_publicada_recentemente(self):
        return self.pub_data >= timezone.now() -datetime.timedelta(days=15)

class Comentario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    identificador_conteudo = models.ForeignKey(Filme_ou_serie, on_delete=models.CASCADE)
    comentario_texto = models.CharField(max_length=1500)
    rating = models.IntegerField(default=0) # 0-100
    pub_data = models.DateTimeField('data de publicacao')

    def __str__(self):
        return self.comentario_texto

    def foi_publicada_recentemente_comentario(self):
        return self.pub_data >= timezone.now() -datetime.timedelta(days=15)


class Critico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    marca = models.CharField(max_length=100)
    imagem = models.CharField(max_length=300, default='0000000')


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    identificador_conteudo = models.ForeignKey(Filme_ou_serie, on_delete=models.CASCADE)
    like= models.IntegerField(default=0)

