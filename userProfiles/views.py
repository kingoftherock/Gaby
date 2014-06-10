# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import *
from django.contrib.auth.models import User
from models import Tipo
from home.models import Academia_Profesor, Academia, Profesor
from home.views import *

mensaje = ''
caracteres_validos_Usuarios = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_?0123456789!'
caracter_espacio = ' '
# Create your views here.
def loginAdmins(request):
	global mensaje
	diccionario = {'mensaje' : mensaje}
	mensaje = ''
	return render(request, 'loginAdmins.html', diccionario)

def entrado(request):
	global mensaje
	username = request.POST.get('usuario', '')
	password = request.POST.get('contrasenna', '')
	user = authenticate(username=username, password=password)
	caracteres = ["'", '"']
	for caracter in caracteres:
		if caracter in username or caracter in password:
			mensaje = "SQL injection tu puta madre"
			return HttpResponseRedirect("/Gaby/AccesoAdmins", {'mensaje':mensaje})
	if user is not None:
		if user.is_active:
			login(request, user)
			tipo = Tipo.objects.get(usuario=user)
			if tipo.tipo == 1:
				return HttpResponseRedirect("/Gaby/Academia")
			elif tipo.tipo == 2:
				return HttpResponseRedirect("/Gaby/Profesor")
			elif tipo.tipo == 3:
				return HttpResponseRedirect("/Gaby/AccesoAlumnos")
		else:
			diccionario = {'mensaje' : "NO estas activo"}          
			return HttpResponseRedirect("/Gaby/Academia", diccionario)
	else:
		mensaje = 'Usuario y contraseña incorrectos'
		return HttpResponseRedirect("/Gaby/AccesoAdmins", {'mensaje':mensaje})
	
	return HttpResponseRedirect("/Gaby/AccesoAdmins", {'mensaje':mensaje})



def registrar(request):
	global mensaje
	usuario1 = request.POST.get('username', '')
	usuarios = User.objects.all()
	bueno = False
	for x in usuario1:
		if x in caracteres_validos_Usuarios:
			bueno = True
		if x in caracter_espacio:
			bueno = False
			break

	if bueno and len(usuario1)>=5:
		caracteres = ["'", '"']
		for usuario in usuarios:
			if usuario.username == usuario1:
				mensaje = "El usuario ya existe"
				return HttpResponseRedirect("/Gaby/AccesoAdmins", {'mensaje':mensaje})
		contrasenna1 = request.POST.get('password', '')
		contrasenna = request.POST.get('password1', '')

		if contrasenna1 != contrasenna:
			mensaje = 'Las contraseñas no coinciden'
			return HttpResponseRedirect("/Gaby/AccesoAdmins", {'mensaje':mensaje})

		if len(contrasenna1) >= 6:
			for caracter in caracteres:
				if caracter in usuario1 or caracter in contrasenna:
					mensaje = "Por favor no incluyas " + '" ' + "ó" + "' " + "en tu nombre de usuario"
					return HttpResponseRedirect("/Gaby/AccesoAdmins", {'mensaje':mensaje})

			correo1 = request.POST.get('email', '')
			nombre1 = request.POST.get('first_name', '')
			bueno2 = False
			for y in nombre1:
				if y in caracteres_validos_Usuarios:
					bueno2 = True

			if bueno2:
				user = User.objects.create_user(usuario1, correo1, contrasenna1, first_name=nombre1)
				tipo = 1
				un_poco_mas = Tipo(tipo = tipo, usuario = user)
				un_poco_mas.save()

				academiaNueva = Academia(academia=user)
				academiaNueva.save()

				mensaje = 'Usuario creado exitosamente'
				return HttpResponseRedirect("/Gaby/AccesoAdmins", {'mensaje':mensaje})
			else:
				mensaje = 'Nombre de academia invalido'
				return HttpResponseRedirect("/Gaby/AccesoAdmins", {'mensaje':mensaje})
		else:
			mensaje = 'La contraseña debe tener al menos 6 caracteres'
			return HttpResponseRedirect("/Gaby/AccesoAdmins", {'mensaje':mensaje})
	else:
		if len(usuario1) < 5:
			mensaje = 'El nombre de usuario debe tener al menos 5 caracteres'
		else:
			mensaje = 'Nombre de usuario invalido'
		return HttpResponseRedirect("/Gaby/AccesoAdmins", {'mensaje':mensaje})

def salir(request):
	logout(request)
	return HttpResponseRedirect("/Gaby")

@login_required(login_url='/Gaby/AccesoAdmins')
def registrarProfe(request):
	tipo = mostrarTipo(request.user)
	if tipo != 1:
		if tipo == 2:
			return redirect('/Gaby/Profesor')
		else:
			return redirect('/Gaby/AccesoAlumnos') 
	global mensaje
	usuario = request.POST.get('username', '')
	usuarios = User.objects.all()
	for elemento in usuarios:
		if elemento.username == usuario:
			mensaje = "El usuario ya existe"
			return HttpResponseRedirect('/Gaby/Academia/Maestros/Registrar/', {'mensaje':mensaje})

	contrasenna = 'dreediGaby'

	correo = request.POST.get('email', '')
	nombre = request.POST.get('first_name', '')
	apellido = request.POST.get('last_name', '')
	user = User.objects.create_user(usuario, correo, contrasenna, first_name=nombre, last_name=apellido)
	tipo = 2
	un_poco_mas = Tipo(tipo = tipo, usuario = user)
	un_poco_mas.save()

	profesorNuevo = Profesor(profesor=user)
	profesorNuevo.save()

	academia = Academia.objects.get(academia=request.user.id)

	relacionProfeAcademia = Academia_Profesor(academia=academia, profesor=profesorNuevo)
	relacionProfeAcademia.save()

	mensaje = 'Profesor registrado exitosamente'
	return HttpResponseRedirect('/Gaby/Academia/Maestros/Registrar/', {'mensaje':mensaje})

@login_required(login_url='/Gaby/AccesoAdmins')
def maestrosRegistrar(request):
	global mensaje
	tipo = mostrarTipo(request.user)
	if tipo != 1:
		if tipo == 2:
			return redirect('/Gaby/Profesor')
		else:
			return redirect('/Gaby/AccesoAlumnos')  
	diccionario = {
		'mensaje': mensaje,
	}
	mensaje = ''
	return render(request, 'academiaMaestrosRegistrar.html',diccionario)