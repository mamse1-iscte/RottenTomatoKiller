from django.urls import include, path
from . import views





# (. significa que importa views da mesma directoria)

app_name = 'votacao'

urlpatterns = [
 path("", views.index, name="index"),
 path('criaConta', views.criaConta, name='criaConta'),
 path('HomePage', views.HomePage, name='HomePage'),
 path('fazerLogin', views.fazerLogin, name='fazerLogin'),
 path('mostrarFilmes', views.mostrarFilmes, name='mostrarFilmes'),
 path('mostrarSeries', views.mostrarSeries, name='mostrarSeries'),
 path('criarUser', views.criarUserButton, name='criarUserButton'),
 path('administradorPage', views.administradorPage, name='administradorPage'),

 path('criarFilme', views.criarFilme, name='criarFilme'),
path('informacaoPessoal', views.informacaoPessoal,name='informacaoPessoal'),

path('loginview', views.loginview,name='loginview'),
path('logoutview', views.logoutview, name='logoutview'),
path('mudarImagemPerfil', views.mudarImagemPerfil, name='mudarImagemPerfil'),
path('myList', views.myList, name='myList'),
path('pesquisaGeneroFilme', views.pesquisaGeneroFilme, name='pesquisaGeneroFilme'),
path('<int:filme_id>', views.filmePage, name='filmePage'),
path('teste', views.teste,name='teste'),

path('<int:filme_id>/apagarFilmeOuSerie', views.apagarFilmeOuSerie, name='apagarFilmeOuSerie'),

path('pesquisaGeneroSerie', views.pesquisaGeneroSerie, name='pesquisaGeneroSerie'),

path('<int:filme_id>/criarComentario', views.criarComentario, name='criarComentario'),

path('<int:filme_id>/addTolist', views.addTolist, name='addTolist'),

path('<int:filme_id>/delTolist', views.delTolist, name='delTolist'),

path('pesquisa', views.pesquisa, name='pesquisa'),
]