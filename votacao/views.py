# Create your views here.

from .models import Filme_ou_serie, Genero, Comentario, Critico, Subgenero, WatchList, Subgenero2

from django.utils import timezone
from django.db.models import Sum

from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from django.contrib.auth import logout

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required


from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.views.decorators import staff_member_required



def index(request):
   # latest_question_list =Filme_ou_serie.objects.order_by('-pub_data')[:5]
   # context = {'latest_question_list':latest_question_list}
   return render(request, 'votacao/HomePage.html')



def fazerLogin(request):
    return render(request, 'votacao/fazerLogin.html')





def criarUserButton(request):
    uploaded_file_url=''

    filepath = request.FILES.get('myfile', False)
    if request.method == 'POST' and filepath:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)



    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['psw']
    imagem=uploaded_file_url

    if User.objects.filter(username=username).exists():
        return HttpResponseRedirect(reverse('votacao:criaConta'))



    omeuuser = User.objects.create_user(username,email,password)
    ut = Critico(user=omeuuser,imagem=imagem)
    omeuuser.save()
    ut.save()
    user = authenticate(username=username, password=password)
    login(request, user)


    return HttpResponseRedirect(reverse('votacao:HomePage'))



def loginview(request):
 username = request.POST['username']
 password = request.POST['psw']
 user = authenticate(username=username,
 password=password)




 if user is not None:
    login(request, user)
    if user.is_staff==1:
        return HttpResponseRedirect(reverse('votacao:HomePage'))
    #paginaSucesso
    return HttpResponseRedirect(reverse('votacao:HomePage'))
 else:
    # paginaInsucesso(request)
     #paginaInsucesso
     return HttpResponseRedirect(reverse('votacao:fazerLogin'))


@login_required(login_url='/votacao/HomePage')
def informacaoPessoal(request):
    return render(request, 'votacao/informacaoPessoal.html')


@login_required(login_url='/votacao/HomePage')
def mudarImagemPerfil(request):
    current_user = request.user

    filepath = request.FILES.get('myfile', False)
    if request.method == 'POST' and filepath:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        Critico.objects.filter(user_id=current_user.id).update(imagem=uploaded_file_url)
    return render(request, 'votacao/informacaoPessoal.html')





def criaConta(request):
    return render(request, 'votacao/criaConta.html')

def mostrarSeries(request):
    latest_movies_list = Filme_ou_serie.objects.filter(is_filme = 0).order_by('-pub_data')[:5]
    best_movies_list = Filme_ou_serie.objects.filter(is_filme = 0).order_by('-filme_ranking_critica')[:5]
    teste = 0
    context = {'latest_movies_list':latest_movies_list, 'teste':teste, 'best_movies_list':best_movies_list}
    return render(request, 'votacao/mostrarSeries.html',context)


def mostrarFilmes(request):
    latest_movies_list = Filme_ou_serie.objects.filter(is_filme = 1).order_by('-pub_data')[:5]
    best_movies_list = Filme_ou_serie.objects.filter(is_filme = 1).order_by('-filme_ranking_critica')[:5]
    teste = 1
    context = {'latest_movies_list':latest_movies_list, 'teste':teste, 'best_movies_list':best_movies_list}
    return render(request, 'votacao/mostrarFilmes.html',context)

@login_required(login_url='/votacao/HomePage')
def myList(request):
    latest_movies_list = WatchList.objects.filter(user = request.user)[:5]
    teste = 2
    context = {'latest_movies_list':latest_movies_list, 'teste':teste}
    return render(request, 'votacao/myList.html',context)



def HomePage(request):
    best_movies_list = Filme_ou_serie.objects.order_by('-filme_ranking_critica')[:5]
    latest_movies_list = Filme_ou_serie.objects.order_by('-pub_data')[:5]
    context = {'latest_movies_list': latest_movies_list,'best_movies_list':best_movies_list }
    return render(request, 'votacao/HomePage.html', context)

@login_required(login_url='/votacao/HomePage')
def administradorPage(request):
    return render(request, 'votacao/administradorPage.html')



@staff_member_required
def criarFilme(request):
    imagem=''

    filepath = request.FILES.get('myfile', False)
    if request.method == 'POST' and filepath:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        imagem = uploaded_file_url

    if request.method == 'POST' :

        # se a invocação veio do form, isto é, está no 2º passo

        filme_texto = request.POST['nome_filme']
        genero = request.POST['genero']
        subgenero= request.POST['subgenero']
        subgenero2 = request.POST['subgenero2']
        filme_descricao = request.POST['filme_descricao']
        is_filme = request.POST['is_filme']
        anoLancamento= request.POST['anoLancamento']
        trailer = request.POST['trailer']
        atores= request.POST['atores']

        if filme_texto:
            # se a questao_texto está preenchida,
            # então vai instanciar a Questão e depois volta ao detalhe
            generoObject=Genero.objects.get(pk=genero)
            generoObject1 = Subgenero.objects.get(pk=subgenero)
            generoObject2 = Subgenero2.objects.get(pk=subgenero2)
            filme = Filme_ou_serie(filme_texto = filme_texto, filme_ranking_critica = 0, filme_descricao = filme_descricao,is_filme = is_filme, pub_data=timezone.now(), genero_id = generoObject ,release_year = anoLancamento, imagem = imagem,  subgenero2_id = generoObject2, subgenero_id = generoObject1 , trailer = trailer, atores=atores)
            filme.save()
            return HttpResponseRedirect(reverse('votacao:HomePage'))
        else:
            # se a questao_texto não está preenchida, volta ao form
            return HttpResponseRedirect(reverse('votacao:HomePage'))
    else:
         # se a invocação não veio do form, isto é, o 1º passo
        return render(request,'votacao/criarFilme.html')

@login_required(login_url='/votacao/HomePage')
def criarComentario(request, filme_id):
    filme = get_object_or_404(Filme_ou_serie, pk=filme_id)

    if request.method == 'POST' :

        # se a invocação veio do form, isto é, está no 2º passo

        comentario_texto = request.POST['comentario_texto']

        rating = request.POST.get('rating', 0);
        print("rating",rating)
        #rating = request.POST['rating']
        latest_coments_movie_list = Comentario.objects.filter(identificador_conteudo=filme_id)
        latest_movies_list = latest_coments_movie_list.order_by('-pub_data')[:5]
        context = {'latest_movies_list': latest_movies_list, 'filme': filme}

        if comentario_texto and rating != 0:
            # se a questao_texto está preenchida,
            # então vai instanciar a Questão e depois volta ao detalhe
            print("user id ",request.user)
            comentario = Comentario(user= request.user, identificador_conteudo = filme, comentario_texto = comentario_texto, rating = rating, pub_data=timezone.now())
            comentario.save()

            comentarios = Comentario.objects.filter(identificador_conteudo=filme_id)

            nfilmes = comentarios.count()

            totalRating = Comentario.objects.filter(identificador_conteudo=filme_id).aggregate(Sum('rating'))

            totalR = totalRating['rating__sum']
            score = int((totalR / nfilmes)*10)

            print("nfilmes", nfilmes, "totalRating", totalRating, "totalR", totalR, "score", score)
            Filme_ou_serie.objects.filter(pk=filme_id).update(filme_ranking_critica=score)

            return HttpResponseRedirect(reverse('votacao:filmePage',args=(filme_id,)))
        else:
   # se a questao_texto não está preenchida, volta ao form
            return HttpResponseRedirect(reverse('votacao:filmePage',args=(filme_id,)))
    else:
         # se a invocação não veio do form, isto é, o 1º passo
        return HttpResponseRedirect(reverse('votacao:filmePage',args=(filme_id,)))


@login_required(login_url='/votacao/HomePage')
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('votacao:HomePage'))



def pesquisaGeneroFilme(request):
    #latest_movies_list = Filme_ou_serie.objects.filter(is_filme=filme_id)
    genero=request.POST.get('genero')
    genero=int(genero)

    latest_movies_list1 = Filme_ou_serie.objects.filter(is_filme=1, genero_id=genero).order_by('-pub_data')[:5]
    latest_movies_list2 = Filme_ou_serie.objects.filter(is_filme=1, subgenero_id=genero).order_by('-pub_data')[:5]
    latest_movies_list3 = Filme_ou_serie.objects.filter(is_filme=1, subgenero2_id=genero).order_by('-pub_data')[:5]
    latest_movies_list = (latest_movies_list1 | latest_movies_list2 | latest_movies_list3).order_by('-pub_data')[:5]


    if genero==90:
        latest_movies_list = Filme_ou_serie.objects.filter(filme_ranking_critica__gte=genero).order_by('-pub_data')[:5]
        context = {'latest_movies_list': latest_movies_list,'genero': genero}
        return render(request, 'votacao/pesquisa.html', context)
    if genero == 70:
        latest_movies_list = Filme_ou_serie.objects.filter(filme_ranking_critica__gte=genero).order_by('-pub_data')[:5]
        context = {'latest_movies_list': latest_movies_list,'genero': genero}
        return render(request, 'votacao/pesquisa.html', context)
    if genero == 50:
        latest_movies_list = Filme_ou_serie.objects.filter(filme_ranking_critica__gte=genero).order_by('-pub_data')[:5]
        context = {'latest_movies_list': latest_movies_list,'genero': genero}
        return render(request, 'votacao/pesquisa.html', context)


    context = {'latest_movies_list': latest_movies_list,'genero': genero}
    return render(request, 'votacao/genero.html',context)

def pesquisaGeneroSerie(request):
    #latest_movies_list = Filme_ou_serie.objects.filter(is_filme=filme_id)
    genero=request.POST.get('genero')
    genero=int(genero)
    latest_movies_list1 = Filme_ou_serie.objects.filter(is_filme=0, genero_id=genero).order_by('-pub_data')[:5]
    latest_movies_list2 = Filme_ou_serie.objects.filter(is_filme=0, subgenero_id=genero).order_by('-pub_data')[:5]
    latest_movies_list3 = Filme_ou_serie.objects.filter(is_filme=0, subgenero2_id=genero).order_by('-pub_data')[:5]
    latest_movies_list=(latest_movies_list1 | latest_movies_list2 |latest_movies_list3).order_by('-pub_data')[:5]
    #mydata = Members.objects.filter(firstname='Emil').values() | Members.objects.filter(firstname='Tobias').values()

    if genero==90:
        latest_movies_list = Filme_ou_serie.objects.filter(filme_ranking_critica__gte=genero).order_by('-pub_data')[:5]
        context = {'latest_movies_list': latest_movies_list,'genero': genero}
        return render(request, 'votacao/pesquisaSerie.html', context)
    if genero == 70:
        latest_movies_list = Filme_ou_serie.objects.filter(filme_ranking_critica__gte=genero).order_by('-pub_data')[:5]
        context = {'latest_movies_list': latest_movies_list,'genero': genero}
        return render(request, 'votacao/pesquisaSerie.html', context)
    if genero == 50:
        latest_movies_list = Filme_ou_serie.objects.filter(filme_ranking_critica__gte=genero).order_by('-pub_data')[:5]
        context = {'latest_movies_list': latest_movies_list,'genero': genero}
        return render(request, 'votacao/pesquisaSerie.html', context)


    context = {'latest_movies_list': latest_movies_list,'genero': genero}
    return render(request, 'votacao/generoSerie.html',context)





def filmePage(request, filme_id):
    #objeto se não dá erro 404
    filme = get_object_or_404(Filme_ou_serie, pk = filme_id)
    latest_coments_movie_list = Comentario.objects.filter(identificador_conteudo = filme_id )
    latest_movies_list =latest_coments_movie_list.order_by('-pub_data')[:5]
    if request.user.is_authenticated:
        watchList = WatchList.objects.all()
        watchList = WatchList.objects.filter(identificador_conteudo=filme_id,user_id=request.user)
        context = {'latest_movies_list':latest_movies_list,'filme': filme,'watchList':watchList}
        return render(request, 'votacao/filmePage.html', context)
    else:
        context = {'latest_movies_list':latest_movies_list,'filme': filme}
        return render(request, 'votacao/filmePage.html', context)





def teste(request):
    return render(request, 'votacao/teste.html')



def pesquisa(request):
    if 'q' in request.GET:
        q=request.GET['q']
        latest_movies_list = Filme_ou_serie.objects.filter(filme_texto__icontains=q)[:5]
    else:
        latest_movies_list = Filme_ou_serie.objects.all()[:5]
    context={'latest_movies_list':latest_movies_list, 'pesquisa':q}
    return render(request, 'votacao/pesquisa.html',context)







@login_required(login_url='/votacao/HomePage')
def addTolist(request, filme_id):
    print("ola")
    filme = get_object_or_404(Filme_ou_serie, pk=filme_id)
    w = WatchList(user=request.user, identificador_conteudo=filme, like = 1)
    latest_coments_movie_list = Comentario.objects.filter(identificador_conteudo = filme_id )
    latest_movies_list =latest_coments_movie_list.order_by('-pub_data')[:5]
    watchList = WatchList.objects.all()
    watchList = WatchList.objects.filter(identificador_conteudo=filme_id)
    context = {'latest_movies_list':latest_movies_list,'filme': filme, 'watchList':watchList}
    try:
        wInList = WatchList.objects.get(identificador_conteudo=filme, user=request.user, like=1)
        return render(request, 'votacao/filmePage.html', context)
    except WatchList.DoesNotExist:
        w.save()
        return render(request, 'votacao/filmePage.html', context)


@login_required(login_url='/votacao/HomePage')
def delTolist(request, filme_id):
    filme = get_object_or_404(Filme_ou_serie, pk=filme_id)
    latest_coments_movie_list = Comentario.objects.filter(identificador_conteudo = filme_id )
    latest_movies_list =latest_coments_movie_list.order_by('-pub_data')[:5]
    watchList = WatchList.objects.all()
    watchList = WatchList.objects.filter(identificador_conteudo=filme_id)
    context = {'latest_movies_list':latest_movies_list,'filme': filme,'watchList':watchList}
    try:
        wInList = WatchList.objects.get(identificador_conteudo=filme, user=request.user, like=1)
        wInList.delete()
        return render(request, 'votacao/filmePage.html', context)
    except WatchList.DoesNotExist:
        return render(request, 'votacao/filmePage.html', context)


@staff_member_required
def apagarFilmeOuSerie(request, filme_id):
    filmeOuSerie = get_object_or_404(Filme_ou_serie, pk=filme_id)
    filmeOuSerie.delete()
    return HttpResponseRedirect(reverse('votacao:HomePage'))


