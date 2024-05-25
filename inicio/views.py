from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from inicio import models
from django.contrib import messages

def Sesion(request):
    if request.method=='POST':
        id = request.POST['id']
        nombre = request.POST['nombre']
        contraseña = request.POST['contraseña']
        
        try:
            info = models.User.objects.get(id = id) 
            if info.contraseña == contraseña and info.nombre == nombre:
                return redirect('login')
            else:
                messages.error(request, 'Contraseña o usuario invalidos')
        except AttributeError and models.User.DoesNotExist:
            messages.error(request, 'Contraseña o usuario invalidos')
            return redirect('sesion')
        
    return render(request, 'registro.html')

def Logout(request):
    return render(request, 'registration/logout.html')


@login_required
def Seguridad(request):
    return render(request, 'registration/login.html')
