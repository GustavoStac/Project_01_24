from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Noticia, Categoria
from .forms import NoticiaForm, ComentarioForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def ListarNoticias(request):
    contexto = {}
    id_categoria = request.GET.get("id", None)
    antiguedad = request.GET.get("antiguedad", None)
    orden = request.GET.get("orden", None)

    n = Noticia.objects.all()

    if id_categoria:
        n = n.filter(categoria_noticia=id_categoria)

    if antiguedad == "asc":
        n = n.order_by('fecha_publicacion')
    elif antiguedad == "desc":
        n = n.order_by('-fecha_publicacion')

    if orden == "asc":
        n = n.order_by('titulo')
    elif orden == "desc":
        n = n.order_by('-titulo')

    contexto = {
        'noticias': n,
        'categorias': Categoria.objects.all(),
    }

    return render(request, 'noticias/listar.html', contexto)


    '''contexto = {}
    id_categoria = request.GET.get("id", None)

    if id_categoria:
        n = Noticia.objects.filter(categoria_noticia = id_categoria)
    else:    
        n = Noticia.objects.all() # SELECT * FROM NOTICIAS
    
    # filtrar por antiguedad asc
        antiguedad_asc = request.GET.get("antiguedad_asc")
        if antiguedad_asc:
            n = Noticia.objects.all().order_by('fecha_publicacion') #ordena por fecha

    # filtrar por antiguedad desc
        antiguedad_desc = request.GET.get("antiguedad_desc")
        if antiguedad_desc:
            n = Noticia.objects.all().order_by('-fecha_publicacion') #ordena por fecha

    # filtrar por orden alfabetico asc
        orden_asc = request.GET.get("orden_asc")
        if orden_asc:
            n = Noticia.objects.all().order_by('titulo') #ordena por titulo

     # filtrar por orden alfabetico desc
        orden_desc = request.GET.get("orden_desc")
        if orden_desc:
         n = Noticia.objects.all().order_by('-titulo') #ordena por titulo


    cat = Categoria.objects.all().order_by('nombre') #ORDENA POR NOMBRE
    contexto['noticias'] = n
    contexto['categorias'] = cat

    return render (request, 'noticias/listar.html', contexto)'''

'''def DetalleNoticia(request, pk):
    contexto = {}

    n = Noticia.objects.get(pk = pk) # SELECT * FROM NOTICIAS WHERE id = 1
    contexto['noticias'] = n

    #BORRAR NOTICIA
    if request.method == 'POST' and 'delete_noticia' in request.POST:
        n.delete()
        return redirect('noticias:listar')
    
    return render (request, 'noticias/detalle.html', contexto)'''

#DETALE NOTICIAS CON COMENTARIOS INCLUIDOS

def DetalleNoticia(request, pk):
    contexto = {}

    n = Noticia.objects.get(pk = pk) # SELECT * FROM NOTICIAS WHERE id = 1
    contexto['noticias'] = n

    c = n.comentarios.all()
    contexto['comentarios'] = c

    #BORRAR NOTICIA
    if request.method == 'POST' and 'delete_noticia' in request.POST:
        n.delete()
        return redirect('noticias:listar')
    
    #CREAR COMENTARIO
    if request.method == 'POST' and 'add_comentario' in request.POST:
       form = ComentarioForm(request.POST)
       if form.is_valid():
                comentario = form.save(commit=False)
                comentario.usuario = request.user
                form.save()
                return redirect('noticia:detalle', pk=pk)
    else:
        form = NoticiaForm()


    return render (request, 'noticias/detalle.html', contexto)

    

@login_required
def AddNoticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST or None, request.FILES) ##Request files es para las imagenes

        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.autor = request.user
            form.save()
            return redirect('home')
    else:
        form = NoticiaForm()
    
    return render (request, 'noticias/addNoticia.html', {'form':form})