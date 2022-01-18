from django.shortcuts import render, redirect
from django.contrib import messages
from app.forms import UserForm, LoginForm, DeseoForm
from app.models import User, Deseo
import bcrypt

def index(request):
    if 'usuario' not in request.session:
        return redirect('/login')
    
    usuario = User.objects.get(id=request.session['usuario']['id'])
    items = Deseo.objects.exclude(id__in=usuario.preferencias.all().values_list('id', flat=True))
    preferencias = usuario.preferencias.all()

    context = {
        'form': DeseoForm(),
        'items': items,
        'deseos_preferidos': preferencias
    }
    return render(request, 'app/index.html', context)

    # if 'usuario' in request.session:
    #     return render(request, 'app/index.html')

# una vez creada esta función principal lo ideal es enviar información, ya que al crear la visualización en el template de cada cita que se vaya agregando con la función inicialmente aparecerá el contenido template que se le está enviando, por lo tanto es necesario ponerle un contexto

def create(request):
    
    if 'usuario' not in request.session:
        return redirect('/login')
    
    print(request.POST)
    
    usuario = User.objects.get(id=request.session['usuario']['id'])
    items = Deseo.objects.exclude(id__in=usuario.preferencias.all().values_list('id', flat=True))
    preferencias = usuario.preferencias.all()
    

    if request.method=='POST':
        form = DeseoForm(request.POST)
        if form.is_valid():
            deseo = form.save(commit=False)
            deseo.usuario = usuario
            deseo.save()
            messages.success(request, "Item agregado correctamente")
            return redirect('/')
        else:
            messages.error(request, "Formulario procesado con errroes.")
            return render(request, 'app/create.html', {'form':form, 'items': items})

    context = {
        'form': DeseoForm(),
        'items': items,
        'deseos_preferidos': preferencias,
    }
    return render(request, 'app/create.html', context)



def register(request):
    if 'usuario' in request.session:
        return redirect('/')
    
    if request.method == 'POST':
        #POST
        form = UserForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = bcrypt.hashpw(usuario.password.encode(), bcrypt.gensalt()).decode()
            usuario.save()            
            messages.success(request, "Usuario creado correctamente")
            return redirect('/')
        else:
            messages.error(request, "Formulario procesado con errroes.")
            return render(request, 'app/register.html', {'form':form })
    else:
        # GET
        context = {
            'form' : UserForm()
        }
        return render(request, 'app/register.html', context)


def login(request):
    if 'usuario' in request.session:
        return redirect('/')
    
    if request.method == 'POST':
        # POST
        user = User.objects.filter(username=request.POST['username'])
        
        if user:
            usuario_login = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(),  usuario_login.password.encode()):
                print("USUARIO CORRECTO")
                request.session['usuario'] = { 'nombre':usuario_login.name , 'username':usuario_login.username,'id':usuario_login.id}
                return redirect('/')
            else:
                print("USUARIO NO ES SU CONTRASEÑA")
                messages.error(request, "USUARIO NO ES SU CONTRASEÑA")

        else:
            messages.error(request, "Usuario no encontrado")
        return redirect('/login')

    else:
        # GET
        context = {
            'form' : LoginForm()
        }
        return render(request, 'app/login.html', context)


def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
        
    return redirect('/login')


def delete(request, id):
    if 'usuario' not in request.session:
        return redirect('/login')
    deseo = Deseo.objects.get(id=id)
    deseo.delete()
    messages.success(request, " el item ha sido eliminado de tu lista de deseos")
    return redirect('/')


def preferencias_add(request, id):
    if 'usuario' not in request.session:
        return redirect('/login')
    
    usuario = User.objects.get(id=request.session['usuario']['id'])
    deseo = Deseo.objects.get(id=id)

    usuario.preferencias.add(deseo)
    usuario.save()

    messages.success(request, "Item agregado a tu lista de preferencias")
    return redirect("/")


def preferencias_delete(request, id):
    if 'usuario' not in request.session:
        return redirect('/login')
    
    usuario = User.objects.get(id=request.session['usuario']['id'])
    deseo = Deseo.objects.get(id=id)

    usuario.preferencias.remove(deseo)
    usuario.save()

    messages.success(request, "Item removido a tu lista de preferencias")
    return redirect("/")