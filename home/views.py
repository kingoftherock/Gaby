# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, render_to_response, RequestContext, get_object_or_404
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from models import *
from forms import contactosForm, cuestionariosForm, preguntaForm, grupoForm, documentoForm
from django.db.models import Q
import random
from random import shuffle
from datetime import datetime
from decimal import * 

mensaje = ''
caracteres_validos_Usuarios = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyzÁÉÍÓÚáéíóúÄËÏÖÜäëïöü-_¿?0123456789!¡'

def mostrarTipo(usuario):
    tipo = Tipo.objects.get(usuario=usuario)
    return tipo.tipo

@login_required(login_url='/Gaby/AccesoAdmins')
def academia(request):
    tipo = mostrarTipo(request.user)
    if tipo != 1:
        if tipo == 2:
            return redirect('/Gaby/Profesor')
        else:
            return redirect('/Gaby/AccesoAlumnos')   
    return redirect('cuestionariosAcademia')

@login_required(login_url='/Gaby/AccesoAdmins')
def academiaConfiguracion(request):
    return render(request, 'academiaConfiguracion.html')    

@login_required(login_url='/Gaby/AccesoAdmins')
def profesor(request):
    tipo = mostrarTipo(request.user)
    if tipo != 2:
        if tipo == 1:
            return redirect('/Gaby/Academia')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    return redirect('/Gaby/Profesor/Cuestionarios')

class cuestionarios_activoClase():
    def inicializar(self, cuestionarioObtenido, activoObtenido):
        self.cuestionario = cuestionarioObtenido
        self.activo =  activoObtenido

@login_required(login_url='/Gaby/AccesoAdmins')
def cuestionariosProfesor(request):
    tipo = mostrarTipo(request.user)
    if tipo != 2:
        if tipo == 1:
            return redirect('/Gaby/Academia')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    profesor = Profesor.objects.get(profesor__exact=request.user)
    academia = Academia_Profesor.objects.get(profesor__exact=profesor)
    cuestionarios = Cuestionario.objects.filter(academia__exact=academia.academia.academia)

    contador = 0
    resultados_cuestionarios = []
    for x in cuestionarios:
        contador = 0
        RelacionCuestionario_profesor_grupo = Cuestionario_Profesor_Grupo.objects.filter(cuestionario=x)
        for y in RelacionCuestionario_profesor_grupo:
            if y.activo:
                objetoClase = cuestionarios_activoClase()
                objetoClase.inicializar(x, y.activo)
                resultados_cuestionarios.append(objetoClase)
                break
            contador += 1
        if contador == len(RelacionCuestionario_profesor_grupo):
            objetoClase = cuestionarios_activoClase()
            objetoClase.inicializar(x, False)
            resultados_cuestionarios.append(objetoClase)



    return render(request, 'profesorCuestionarios.html', {'cuestionarios':resultados_cuestionarios})

@login_required(login_url='/Gaby/AccesoAlumnos')
def alumno(request):

    template = 'alumnoIndex.html'
    tipos = Tipo.objects.filter(usuario=request.user)
    alumnos = Alumno.objects.filter(alumno=request.user)
    if len(tipos) == 0 and len(alumnos) == 0:
        nuevoAlumno = Alumno(alumno=request.user)
        nuevoAlumno.save()
        nuevoUsuario = Tipo(tipo=3, usuario=request.user)
        nuevoUsuario.save()
    
    alumno = Alumno.objects.get(alumno=request.user)
    relacionConGrupo = Grupo_Alumno.objects.filter(alumno=alumno)
    grupos = []
    for elementoRelacionGrupo in relacionConGrupo:
        grupos.append(elementoRelacionGrupo.grupo)
    academias = []
    for elementoGrupos in grupos:
        if elementoGrupos.academia_profesor.academia in academias:
            pass
        else:
            academias.append(elementoGrupos.academia_profesor.academia)

    diccionario = {
        'user': request.user,
        'academias': academias,
    }

    tipo = mostrarTipo(request.user)
    if tipo != 3:
        if tipo == 1:
            return redirect('/Gaby/Academia')
        else:
            return redirect('/Gaby/Profesor')
    return render(request, template, diccionario)

@login_required(login_url='/Gaby/AccesoAlumnos')
def alumnoInscripcionAcademia(request):
    tipo = mostrarTipo(request.user)
    if tipo != 3:
        if tipo == 1:
            return redirect('/Gaby/Academia')
        else:
            return redirect('/Gaby/Profesor')

    template = 'alumnoInscripcionAcademia.html'
    
    academias = Academia.objects.filter(estado=True)


    alumnoObtenido = Alumno.objects.get(alumno=request.user)
    GruposAlumnoRegistrado = Grupo_Alumno.objects.filter(alumno=alumnoObtenido)
    grupos = []
    for relacionGrupos in GruposAlumnoRegistrado:
        grupos.append(relacionGrupos.grupo)
    relacionesAcademiaProfesor = []
    for elementoGrupo in grupos:
        relacionesAcademiaProfesor.append(elementoGrupo.academia_profesor)
    academiasSuscritas = []
    for elementoAcademia in relacionesAcademiaProfesor:
        academiasSuscritas.append(elementoAcademia.academia)


    results = []

    if request.method == 'GET':
        nombre = request.GET.get("nombre", "")
        if nombre != '' and nombre != ' ':
            posibles = User.objects.filter(Q(username__icontains=nombre) | Q(first_name__icontains=nombre) | Q(last_name__icontains=nombre) | Q(email__icontains=nombre))
            for x in posibles:
                try:
                    Es_Academia = Academia.objects.get(academia=x)
                    if Es_Academia in academias:
                        results.append(Es_Academia)
                except:
                    pass

    if request.method == 'POST':
        academiaFormulario = request.POST.get('academia','')
        url = '/Gaby/Alumno/Inscribirse/Academia/' + academiaFormulario
        return redirect(url)

    diccionario = {
        'user': request.user,
        'academias': academias,
        'resultados': results,
        'academiasSuscritas': academiasSuscritas
    }


    return render(request, template, diccionario)

@login_required(login_url='/Gaby/AccesoAlumnos')
def alumnoInscripcionAcademiaEspecifico(request, id_Academia):
    tipo = mostrarTipo(request.user)
    if tipo != 3:
        if tipo == 1:
            return redirect('/Gaby/Academia')
        else:
            return redirect('/Gaby/Profesor')
    template = 'alumnoInscripcionAcademiaEspecifico.html'

    academia = get_object_or_404(Academia, id=int(id_Academia))
    relacionAcademia = Academia_Profesor.objects.filter(academia=academia)
    grupos = Grupo.objects.filter(academia_profesor=relacionAcademia)
    alumnoObtenido = Alumno.objects.get(alumno=request.user)

    gruposSuscritos1 = []
    for elementoGrupo in grupos:
        try:
            relacionIterada = elementoGrupo.nombre + alumnoObtenido.alumno.username
            grupoSuscrito = Grupo_Alumno.objects.get(nombreRelacion=relacionIterada)
            gruposSuscritos1.append(grupoSuscrito)
        except:
            pass

    gruposSuscritos = []
    for elementoGrupoSuscrito in gruposSuscritos1:
        gruposSuscritos.append(elementoGrupoSuscrito.grupo)

    if request.method == 'POST':
        grupoObtenido = request.POST.get('grupo','')
        grupo = Grupo.objects.get(nombre=grupoObtenido, academia_profesor=relacionAcademia)
        nombreRelacion = 'grupo' + str(grupo.id) + 'alumno' + str(alumnoObtenido.alumno.id) + 'academia' + str(academia.id)
        relacionGrupoAlumnoExistente = Grupo_Alumno.objects.filter(nombreRelacion=nombreRelacion)
        if len(relacionGrupoAlumnoExistente) == 0:
            nuevaRelacionAlumnoGrupo = Grupo_Alumno(grupo=grupo, alumno=alumnoObtenido, nombreRelacion=nombreRelacion)
            nuevaRelacionAlumnoGrupo.save()
        try:
            alumno = Alumno.objects.get(alumno=request.user)
            nuevoNombreRelacionAcademiaAlumno = 'alumno' + str(alumno.id) + 'academia' + str(academia.id)
            nuevaRelacionAlumnoAcademiaCali = Alumno_Academia_Promedio(nombreRelacion=nuevoNombreRelacionAcademiaAlumno, alumno=alumno, academia=academia)
            nuevaRelacionAlumnoAcademiaCali.save()
        except:
            pass
        return redirect('/Gaby/Alumno')

    diccionario = {
        'academia': academia,
        'grupos': grupos,
        'gruposSuscritos': gruposSuscritos,
    }


    return render(request, template, diccionario)

class cuestionariosContestadosClase():
    def inicializar(self, relacionObtenido, alumno_cuestionarioObtenido):
        self.relacion = relacionObtenido
        self.alumno_cuestionario =  alumno_cuestionarioObtenido

@login_required(login_url='/Gaby/AccesoAlumnos')
def alumnoAcademiaHome(request, id_Academia):
    tipo = mostrarTipo(request.user)
    if tipo != 3:
        if tipo == 1:
            return redirect('/Gaby/Academia')
        else:
            return redirect('/Gaby/Profesor')
    template = 'alumnoAcademiaHome.html'
    alumno = Alumno.objects.get(alumno=request.user)
    academia = get_object_or_404(Academia, id=int(id_Academia))
    academiasProfes = Academia_Profesor.objects.filter(academia=academia)
    gruposPosibles = []
    for x in academiasProfes:
        try:
            grupoObjetosAhora = Grupo.objects.filter(academia_profesor=x)
            for y in grupoObjetosAhora:
                gruposPosibles.append(y)
        except:
            pass

    gruposPosibles2 = []
    for y in gruposPosibles:
        try:
            Grupos_del_alumno = Grupo_Alumno.objects.get(alumno=alumno, grupo=y)
            gruposPosibles2.append(y)
        except:
            pass

    gruposFinal = []
    for elementoGruposPosibles in gruposPosibles2:
        porAhora = Cuestionario_Profesor_Grupo.objects.filter(grupo=elementoGruposPosibles)
        if len(porAhora) > 0:
            gruposFinal.append(porAhora)

    gruposFinalFinal = []
    for elemento2 in gruposFinal:
        for y in elemento2:
            gruposFinalFinal.append(y)

    if request.method == 'POST':
        idCuestionarioParaContestar = request.POST.get('id','')
        cuestionarioParaContestar = Cuestionario_Profesor_Grupo.objects.get(id=int(idCuestionarioParaContestar))
        
        cuestionarioObetenido = cuestionarioParaContestar.cuestionario

        preguntasAMostrar = cuestionarioParaContestar.numeroPreguntas
        preguntasTodas = Pregunta.objects.filter(cuestionario=cuestionarioObetenido)

        preguntasAContestar = random.sample(preguntasTodas, preguntasAMostrar)

        listaFinal = []
        for preguntaObjeto in preguntasAContestar:
            listaPreguntas = [preguntaObjeto.respuestaCorrecta, preguntaObjeto.respuestaIncorrecta1, preguntaObjeto.respuestaIncorrecta2, preguntaObjeto.respuestaIncorrecta3]
            listaPreguntas = random.sample(listaPreguntas, 4)
            objetoClasesitas = objetoPreguntasClase()
            objetoClasesitas.inicializar(preguntaObjeto.pregunta, listaPreguntas)
            listaFinal.append(objetoClasesitas)

    cuestionariosContestados = []
    for a in gruposFinalFinal:
        try:
            alumnosCuestionariosContestados = Alumno_Cuestionario.objects.filter(cuestionario=a.cuestionario, alumno=alumno, contestado=True)
            for y in alumnosCuestionariosContestados:
                cuestionariosContestados.append(y)
        except:
            pass
    cuestionariosContestados_final = []
    for i in cuestionariosContestados:
        for y in gruposFinalFinal:
            if i.cuestionario == y.cuestionario and i.grupo == y.grupo:
                gruposFinalFinal.remove(y)
                cuestionariosContestadosObjeto = cuestionariosContestadosClase()
                alumnosCuestionariosContestados2 = Alumno_Cuestionario.objects.get(grupo=i.grupo, cuestionario=i.cuestionario, alumno=alumno)
                cuestionariosContestadosObjeto.inicializar(y, alumnosCuestionariosContestados2)
                cuestionariosContestados_final.append(cuestionariosContestadosObjeto)

    documentos = Documento.objects.filter(academia=academia)

    diccionario = {
        'CuestionariosActivos': gruposFinalFinal,
        'CuestionariosContestados': cuestionariosContestados_final,
        'documentos' : documentos
    }

    return render(request, template, diccionario)

@login_required(login_url='/Gaby/AccesoAlumnos')
def alumnoCuestionario(request):
    tipo = mostrarTipo(request.user)
    if tipo != 3:
        if tipo == 1:
            return redirect('/Gaby/Academia')
        else:
            return redirect('/Gaby/Profesor')

    id_dela_relacion = request.POST.get('id_cuestionario', '')
    try:
        id_dela_relacion = int(id_dela_relacion)
        cuestionarioContest = Cuestionario_Profesor_Grupo.objects.get(id=id_dela_relacion)
        cuestionarioObetenido = cuestionarioContest.cuestionario
        grupo = cuestionarioContest.grupo
        preguntasAMostrar = cuestionarioContest.numeroPreguntas
        preguntasTodas = Pregunta.objects.filter(cuestionario=cuestionarioObetenido)

        preguntasAContestar = random.sample(preguntasTodas, preguntasAMostrar)

        nuevoNombreRelacionCuestionario = 'grup' + str(grupo.id) + 'cuest' + str(cuestionarioObetenido.id) + 'alum' + str(request.user.id)
        alumno = Alumno.objects.get(alumno=request.user)
        NuevoAlumno_Cuestionario = Alumno_Cuestionario(nombreRelacion=nuevoNombreRelacionCuestionario, alumno=alumno, grupo=grupo, cuestionario=cuestionarioObetenido, fechaResolucion=datetime.now(), fechaConclusion=datetime.now())



        try:
            NuevoAlumno_Cuestionario.save()
        except:
            NuevoAlumno_Cuestionario = Alumno_Cuestionario.objects.get(nombreRelacion=nuevoNombreRelacionCuestionario)

        listaFinal = []
        for preguntaObjeto in preguntasAContestar:
            listaRespuestas = [preguntaObjeto.respuestaCorrecta, preguntaObjeto.respuestaIncorrecta1, preguntaObjeto.respuestaIncorrecta2, preguntaObjeto.respuestaIncorrecta3]
            listaRespuestas = random.sample(listaRespuestas, 4)
            NombreRelacionPreguntas = 'AlumnCuest' + str(NuevoAlumno_Cuestionario.id) + 'Pregu' + str(preguntaObjeto.id)
            NUevoRelacion_con_Preguntas = Alumnos_Cuestionario_Pregunta(nombreRelacion=NombreRelacionPreguntas, alumno_cuestionario=NuevoAlumno_Cuestionario, pregunta=preguntaObjeto)
            try:
                NUevoRelacion_con_Preguntas.save()
            except:
                pass
    except:
        return redirect('/Gaby/Alumno')
    return redirect('/Gaby/Alumno/Cuestionario/'+str(id_dela_relacion))

class objetoPreguntasClase():
    def inicializar(self, preguntaObtenido, respuestasObtenido):
        self.pregunta = preguntaObtenido
        self.respuesta1 = respuestasObtenido[0]
        self.respuesta2 = respuestasObtenido[1]
        self.respuesta3 = respuestasObtenido[2]
        self.respuesta4 = respuestasObtenido[3]

@login_required(login_url='/Gaby/AccesoAlumnos')
def alumnoAcademiaResolverCuestionario(request, idCuestionarioContestar):
    global mensaje
    tipo = mostrarTipo(request.user)
    if tipo != 3:
        if tipo == 1:
            return redirect('/Gaby/Academia')
        else:
            return redirect('/Gaby/Profesor')
    template = 'alumnoAcademiaResolverCuestionario.html'

    cuestionarioContestProfGrupo = get_object_or_404(Cuestionario_Profesor_Grupo, id=int(idCuestionarioContestar))
    cuestionarioObetenido = cuestionarioContestProfGrupo.cuestionario
    numero_de_preguntas_totales = cuestionarioContestProfGrupo.numeroPreguntas
    usuario = request.user
    alumno = Alumno.objects.get(alumno=usuario)

    valor_por_pregunta = Decimal(10.0 / numero_de_preguntas_totales)

    cuestionarioContest = Alumno_Cuestionario.objects.get(cuestionario=cuestionarioObetenido, alumno=alumno, grupo=cuestionarioContestProfGrupo.grupo)

    alumnos_cuestionario_pregunta = Alumnos_Cuestionario_Pregunta.objects.filter(alumno_cuestionario=cuestionarioContest)

    alumnos_cuestionario_pregunta_NOcontestadas = []

    academiaUsuario = cuestionarioContestProfGrupo.cuestionario.academia
    academia = Academia.objects.get(academia=academiaUsuario)
    ObjetoAlumnoAcademiaPromedio = Alumno_Academia_Promedio.objects.get(alumno=alumno, academia=academia)
    todosLosCuestionariosAcademiaAlumno = Alumno_Cuestionario.objects.filter(alumno=alumno)
    listaCuestionariosAcademiaAlumno = []
    sumaCalificaciones = 0
    for e in todosLosCuestionariosAcademiaAlumno:
        academiaPorAhora = Academia.objects.get(academia=e.cuestionario.academia)
        if academiaPorAhora == academia:
            listaCuestionariosAcademiaAlumno.append(e)
            sumaCalificaciones += e.calificacion

    promedio = sumaCalificaciones / len(listaCuestionariosAcademiaAlumno)
    ObjetoAlumnoAcademiaPromedio.calificacion = Decimal(promedio)
    ObjetoAlumnoAcademiaPromedio.save()

    for a in alumnos_cuestionario_pregunta:
        if a.contestado == False:
            alumnos_cuestionario_pregunta_NOcontestadas.append(a)

    if len(alumnos_cuestionario_pregunta_NOcontestadas) == 0:
        cuestionarioContest.fechaConclusion = datetime.now()
        cuestionarioContest.contestado = True
        cuestionarioContest.save()
        mensaje = 'Ya no tienes preguntas por resolver, Felicidades!'
        return render(request, template, {'mensaje':mensaje})

    listaPreguntas = []
    for y in alumnos_cuestionario_pregunta:
        if y.contestado == False:
            listaPreguntas.append(y.pregunta)

    listaFinal = []
    for preguntaObjeto in listaPreguntas:
        listaRespuestas = [preguntaObjeto.respuestaCorrecta, preguntaObjeto.respuestaIncorrecta1, preguntaObjeto.respuestaIncorrecta2, preguntaObjeto.respuestaIncorrecta3]
        listaRespuestas = random.sample(listaRespuestas, 4)
        objetoClasesitas = objetoPreguntasClase()
        objetoClasesitas.inicializar(preguntaObjeto, listaRespuestas)
        listaFinal.append(objetoClasesitas)

    diccionario = {
        'preguntillas': listaFinal,        
    }

    if request.method == 'POST':
        respuesta = request.POST.get('respuesta', '')
        id_dela_pregunta = request.POST.get('id', '')
        pregunta_contestada = Pregunta.objects.get(id=id_dela_pregunta)
    
        Alumnos_cuestionario_pregunta_D = Alumnos_Cuestionario_Pregunta.objects.get(alumno_cuestionario=cuestionarioContest, pregunta=pregunta_contestada)
        if respuesta == "":
            pass
        else:
            Alumnos_cuestionario_pregunta_D.respuesta = respuesta
            if pregunta_contestada.respuestaCorrecta == respuesta:
                if Alumnos_cuestionario_pregunta_D.contestado == False:
                    Alumnos_cuestionario_pregunta_D.correcto = True
                    Alumnos_cuestionario_pregunta_D.contestado = True
                    cuestionarioContest.calificacion = cuestionarioContest.calificacion + valor_por_pregunta
                    cuestionarioContest.save()
            else:
                Alumnos_cuestionario_pregunta_D.contestado = True
            Alumnos_cuestionario_pregunta_D.save()

        Todas_las_preguntas = Alumnos_Cuestionario_Pregunta.objects.filter(alumno_cuestionario=cuestionarioContest)
        contador_preguntas = 0
        for x in Todas_las_preguntas:
            if x.correcto:
                contador_preguntas += 1
        if contador_preguntas == len(Todas_las_preguntas):
            cuestionarioContest.calificacion = Decimal(10)
            cuestionarioContest.save()



        return redirect('/Gaby/Alumno/Cuestionario/'+idCuestionarioContestar)
    return render(request, template, diccionario)


@login_required(login_url='/Gaby/AccesoAdmins')
def alumnosAcademia(request):
    tipo = mostrarTipo(request.user)
    if tipo != 1:
        if tipo == 2:
            return redirect('/Gaby/Profesor')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    academia = Academia.objects.get(academia=request.user)

    if request.method == 'POST':
        estado = request.POST.get('estado','')
        if estado == '':
            academia.estado = False
            academia.save()
        if estado == 'on':
            academia.estado = True
            academia.save()
        return redirect('/Gaby/Academia/Alumnos/')


    gruposObtenido = Grupo.objects.all()
    grupos = []
    for grupo in gruposObtenido:
        try:
            if grupo.academia_profesor.academia == academia:
                grupos.append(grupo)
        except:
            pass


    diccionario = {
        'academia':academia,
        'grupos': grupos,
    }

    return render(request, 'academiaAlumnos.html', diccionario)

class Alumno_PromedioClase():
    def inicializar(self, alumnoObtenido, promedioObtenido):
        self.alumno = alumnoObtenido
        self.promedio = promedioObtenido

@login_required(login_url='/Gaby/AccesoAdmins')
def alumnosAcademiaGrupo(request, id_grupo):
    tipo = mostrarTipo(request.user)
    if tipo != 1:
        if tipo == 2:
            return redirect('/Gaby/Profesor')
        else:
            return redirect('/Gaby/AccesoAlumnos')
    grupo = get_object_or_404(Grupo, id=int(id_grupo))
    academia = Academia.objects.get(academia=request.user)
    RelacionAcademia_Profesor = Academia_Profesor.objects.filter(academia=academia)

    grupos_posibles = []
    for x in RelacionAcademia_Profesor:
        try:
            grupo_ahora = Grupo.objects.filter(academia_profesor=x)
            for y in grupo_ahora:
                grupos_posibles.append(y)
        except:
            pass

    correcto = False
    for x in grupos_posibles:
        if grupo == x:
            correcto = True
            break
    if correcto == False:
        return redirect("/Gaby/Academia/Alumnos/")

    Grupo_Alumno_Ahora = Grupo_Alumno.objects.filter(grupo = grupo)
    Alumnos_ahora = []

    for x in Grupo_Alumno_Ahora:
        ahora = x.alumno
        objetoAlumno_Promedio = Alumno_PromedioClase()
        promedio_ahora = Alumno_Academia_Promedio.objects.get(alumno=ahora, academia=academia)
        objetoAlumno_Promedio.inicializar(x.alumno, promedio_ahora.calificacion)
        Alumnos_ahora.append(objetoAlumno_Promedio)

    Alumnos_final = sorted(Alumnos_ahora, key=lambda Alumno_PromedioClase: Alumno_PromedioClase.alumno.alumno.last_name)

    diccionario = {
        'Grupo' : grupo,
        'Alumnos' : Alumnos_final,
    }


    return render(request, "academiaAlumnosGrupo.html", diccionario)


class estadoAcademiaCuestionarios():
    def inicializar(self, cuestionarioObtenido, estadoObtenido):
        self.cuestionario = cuestionarioObtenido
        self.estado = estadoObtenido

@login_required(login_url='/Gaby/AccesoAdmins')
def cuestionariosAcademia(request):
    tipo = mostrarTipo(request.user)
    if tipo != 1:
        if tipo == 2:
            return redirect('/Gaby/Profesor')
        else:
            return redirect('/Gaby/AccesoAlumnos')
    cuestionarios = Cuestionario.objects.filter(academia=request.user)

    miOtraLista = []

    for i in cuestionarios:
        try:
            porAhora = Cuestionario_Profesor_Grupo.objects.filter(cuestionario=i)
            activo = False
            for elemento in porAhora:
                if elemento.activo:
                    activo = True
                    break
            estado_cuestionarioObjeto = estadoAcademiaCuestionarios()
            estado_cuestionarioObjeto.inicializar(i, activo)
        except:
            estado_cuestionarioObjeto = estadoAcademiaCuestionarios()
            estado_cuestionarioObjeto.inicializar(i, False)

        miOtraLista.append(estado_cuestionarioObjeto)


    diccionario = {
        'cuestionarios': miOtraLista,
    }

    return render(request, 'academiaCuestionarios.html', diccionario)

@login_required(login_url='/Gaby/AccesoAdmins')
def cuestionariosAcademiaNuevo(request):
    global mensaje
    tipo = mostrarTipo(request.user)
    if tipo != 1:
        if tipo == 2:
            return redirect('/Gaby/Profesor')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    form = cuestionariosForm(request.POST or None)
    if form.is_valid():
        nuevoCuestionario = request.POST.get("titulo", "")
        if len(nuevoCuestionario) < 5:
            mensaje = "Ponga un nombre de mas de 5 caracteres al cuestionario"
            render(request, 'academiaCuestionariosNuevo.html', {'mensaje':mensaje})
        else:
            form.save()
            return redirect('/Gaby/Academia/Cuestionarios/')

    return render(request, 'academiaCuestionariosNuevo.html',{'form':form, 'usuario':request.user,})

@login_required(login_url='/Gaby/AccesoAdmins')
def borrar_cuestionario(request):
    if request.method == 'POST':
        try:
            id_cuestionario_borrar = request.POST.get('cuestionario')
            objeto_cuestionario = Cuestionario.objects.get(id=id_cuestionario_borrar)
            objetos_preguntas = Pregunta.objects.filter(cuestionario=objeto_cuestionario)

            if len(objetos_preguntas) > 0:
                objetos_preguntas.delete()

            objeto_cuestionario.delete()
        except:
            pass

    return redirect('/Gaby/Academia/Cuestionarios/')

@login_required(login_url='/Gaby/AccesoAdmins')
def academiaCuestionario(request, id_Cuestionario):
    tipo = mostrarTipo(request.user)
    if tipo != 1:
        if tipo == 2:
            return redirect('/Gaby/Profesor')
        else:
            return redirect('/Gaby/AccesoAlumnos')
    cuestionarioId = get_object_or_404(Cuestionario, id=id_Cuestionario)
    cuestionario = Cuestionario.objects.get(id=int(id_Cuestionario))

    preguntas = Pregunta.objects.filter(cuestionario=int(id_Cuestionario))

    tamanioCuestionario = len(preguntas)


    url = '/Gaby/Academia/Cuestionarios/Cuestionario/' + id_Cuestionario

    
    if request.method == 'GET':
        nombre = request.GET.get("nombre", "")
        if nombre != '' and nombre != ' ':
            results = Pregunta.objects.filter(pregunta__icontains=nombre, cuestionario=int(id_Cuestionario))
        else:
            results = None


    form = preguntaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(url)

    if request.method == 'POST':
        cambio = request.POST.get('input_cambio_titulo', '')
        if cambio != None:
            cuestionario_cambio = Cuestionario.objects.get(id = id_Cuestionario)
            cuestionario_cambio.titulo = cambio
            cuestionario_cambio.save();
            return HttpResponseRedirect('../%s' %(id_Cuestionario))

    diccionario = {
        'cuestionario':cuestionario,
        'preguntas':preguntas,
        'tamanio': tamanioCuestionario,
        'resultado': results,
    }

    return render(request, 'academiaCuestionario.html', diccionario)

@login_required(login_url='/Gaby/AccesoAdmins')
def profesorCuestionario(request, id_Cuestionario):
    tipo = mostrarTipo(request.user)
    if tipo != 2:
        if tipo == 1:
            return redirect('/Gaby/Academia')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    cuestionarioId = get_object_or_404(Cuestionario, id=id_Cuestionario)
    cuestionario = Cuestionario.objects.get(id=int(id_Cuestionario))

    preguntas = Pregunta.objects.filter(cuestionario=int(id_Cuestionario))

    tamanioCuestionario = len(preguntas)

    diccionario = {
        'cuestionario':cuestionario,
        'preguntas':preguntas,
        'tamanio': tamanioCuestionario,
    }

    return render(request, 'profesorCuestionario.html', diccionario)

@login_required(login_url='/Gaby/AccesoAdmins')
def profesorGruposNuevo(request):
    tipo = mostrarTipo(request.user)
    if tipo != 2:
        if tipo == 1:
            return redirect('/Gaby/Academia')
        else:
            return redirect('/Gaby/AccesoAlumnos')


    profesor = Profesor.objects.get(profesor__exact=request.user)
    relacionAcademia = Academia_Profesor.objects.get(profesor__exact=profesor)

    diccionario = {
        'ralacionAcademia': relacionAcademia,    
    }
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre','')
        nuevoGrupo = Grupo(nombre=nombre, academia_profesor=relacionAcademia)
        nuevoGrupo.save()
        return redirect('/Gaby/Profesor/Grupos')

    return render(request, 'profesorGruposNuevo.html', diccionario)

@login_required(login_url='/Gaby/AccesoAdmins')
def profesorGrupos(request):
    tipo = mostrarTipo(request.user)
    if tipo != 2:
        if tipo == 1:
            return redirect('/Gaby/Academia')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    profesor = Profesor.objects.get(profesor__exact=request.user)
    relacionAcademia = Academia_Profesor.objects.get(profesor__exact=profesor)

    grupos = Grupo.objects.filter(academia_profesor=relacionAcademia)

    diccionario = {
        'grupos': grupos,
    }

    return render(request, 'profesorGrupos.html', diccionario)

@login_required(login_url='/Gaby/AccesoAdmins')
def profesorGrupo(request, id_Grupo):
    tipo = mostrarTipo(request.user)
    if tipo != 2:
        if tipo == 1:
            return redirect('/Gaby/Academia')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    grupo = get_object_or_404(Grupo, id=id_Grupo)

    diccionario = {
        'grupo': grupo,
    }

    return render(request, 'profesorGrupo.html', diccionario)

class objetoAlumno_PromedioClase():
    def inicializar(self, alumnoObtenido, promedioObtenido):
        self.alumno = alumnoObtenido
        self.promedio = promedioObtenido

@login_required(login_url='/Gaby/AccesoAdmins')
def profesorGrupoAlumnos(request, id_grupo):
    tipo = mostrarTipo(request.user)
    if tipo != 2:
        if tipo == 1:
            return redirect('/Gaby/Academia')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    grupo = get_object_or_404(Grupo, id=int(id_grupo))
    academia = grupo.academia_profesor.academia
    Grupo_Alumno_Ahora = Grupo_Alumno.objects.filter(grupo = grupo)
    alumnos = []
    for i in Grupo_Alumno_Ahora:
        alumnos.append(i.alumno)

    clases = []
    for i in alumnos:
        RelacionAlumno_academia_promedio = Alumno_Academia_Promedio.objects.get(alumno=i, academia=academia)
        clase = objetoAlumno_PromedioClase()
        clase.inicializar(i, RelacionAlumno_academia_promedio.calificacion)
        clases.append(clase)

    Alumnos_final = sorted(clases, key=lambda alumno: alumno.alumno.alumno.last_name)

    diccionario = {
        'grupo': grupo,
        'Alumnos': Alumnos_final,
    }

    return render(request, 'profesorGrupoAlumnos.html', diccionario)

class profesorGrupoCuestionariosClase():
    def inicializar(self, cuestionarioObtenido, apliObtenido):
        self.cuestionario = cuestionarioObtenido
        


@login_required(login_url='/Gaby/AccesoAdmins')
def profesorGrupoCuestionarios(request, id_Grupo):
    global mensaje
    tipo = mostrarTipo(request.user)
    if tipo != 2:
        if tipo == 1:
            return redirect('/Gaby/Academia')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    grupo = get_object_or_404(Grupo, id=id_Grupo)
    academia = grupo.academia_profesor.academia.academia
    cuestionarios = Cuestionario.objects.filter(academia=academia)

    todos_Cuestionario_profesor = Cuestionario_Profesor_Grupo.objects.filter(grupo=grupo)
    
    Final_cuestionarios = []
    for x in cuestionarios:
        PGCClass = profesorGrupoCuestionariosClase()
        relacionNombre = 'cuest' + str(x.id) + 'grupo' + str(grupo.id) + 'prof' + str(request.user.id)
        nuevoCuestionarioProfesorGrupo = Cuestionario_Profesor_Grupo(nombreRelacion=relacionNombre, cuestionario=x, grupo=grupo)
        try:
            nuevoCuestionarioProfesorGrupo.save()
        except:
            pass


    if request.method == 'POST':
        try:
            estado = request.POST.get('estado','')
            nuevoNombreRelacion = request.POST.get('nombreRelacion','')
            nuevoNombreRelacion = int(nuevoNombreRelacion)
            cuestionarioActual = Cuestionario.objects.get(id=nuevoNombreRelacion)
            if estado == '':
                activo = False
            elif estado == 'on':
                activo = True
            cuestionarioEnUso = Cuestionario_Profesor_Grupo.objects.get(cuestionario=cuestionarioActual, grupo=grupo.id)
            if cuestionarioEnUso.numeroPreguntas > 0:
                cuestionarioEnUso.activo = activo
                cuestionarioEnUso.save()
                return redirect("/Gaby/Profesor/Grupos/Grupo/"+ id_Grupo +"/Cuestionarios/")
            else:
                mensaje = 'No haz ingresado número de preguntas a aplicar'
            return render(request, 'profesorGrupoCuestionarios.html', {'grupo': grupo,'Cuestionarios': todos_Cuestionario_profesor,'mensaje':mensaje})
        except:
            cambio_pregunta = request.POST.get('input_cambio_preguntas','')
            idCuestionarioSeleccionado = request.POST.get('preguntas_input2','')
            try:
                idCuestionarioSeleccionado = int(idCuestionarioSeleccionado)
                cuestionarioActual = Cuestionario.objects.get(id=idCuestionarioSeleccionado)
                relacionNombre = 'cuest' + str(cuestionarioActual.id) + 'grupo' + str(grupo.id) + 'prof' + str(request.user.id)
                Ahora_relacion = Cuestionario_Profesor_Grupo.objects.get(nombreRelacion=relacionNombre)
                preguntas = Pregunta.objects.filter(cuestionario=cuestionarioActual)
                if len(preguntas) >= int(cambio_pregunta):
                    Ahora_relacion.numeroPreguntas = int(cambio_pregunta)
                    if int(cambio_pregunta) == 0:
                        Ahora_relacion.activo = False
                    Ahora_relacion.save()

                    return redirect('/Gaby/Profesor/Grupos/Grupo/'+id_Grupo+'/Cuestionarios/')
                else:
                    mensaje = 'El número ingresado es mayor al número de preguntas existentes'
                    return render(request, 'profesorGrupoCuestionarios.html', {'grupo': grupo,'Cuestionarios': todos_Cuestionario_profesor,'mensaje':mensaje})
            except:
                mensaje = 'Ingrese un número'
                return render(request, 'profesorGrupoCuestionarios.html', {'grupo': grupo,'Cuestionarios': todos_Cuestionario_profesor,'mensaje':mensaje})

            

    diccionario = {
        'grupo': grupo,
        'Cuestionarios': todos_Cuestionario_profesor,
    }

    return render(request, 'profesorGrupoCuestionarios.html', diccionario)

@login_required(login_url='/Gaby/AccesoAdmins')
def profesorEstadisticas(request):
    tipo = mostrarTipo(request.user)
    if tipo != 2:
        if tipo == 1:
            return redirect('/Gaby/Academia')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    profesor = Profesor.objects.get(profesor=request.user)
    academia_profesor_relacion = Academia_Profesor.objects.get(profesor=profesor)    
    grupos = Grupo.objects.filter(academia_profesor=academia_profesor_relacion)
    aprobados = 0
    reprobados = 0
    for x in grupos:
        ahora_alumno_cuestionario = Alumno_Cuestionario.objects.filter(grupo=x)
        for y in ahora_alumno_cuestionario:
            if y.calificacion <= 5:
                reprobados += 1
            else:
                aprobados +=1



    diccionario = {
        'aprobados' : aprobados,
        'reprobados' : reprobados,
    }

    return render(request, 'profesorEstadisticas.html', diccionario)

class grupoProfesorEstadisticasClase():
    def inicializar(self, grupoObtenido, promedioGrupoObtenido):
        self.grupo = grupoObtenido
        self.promedio = promedioGrupoObtenido

@login_required(login_url='/Gaby/AccesoAdmins')
def profesorEstadisticasGrupo(request):
    tipo = mostrarTipo(request.user)
    if tipo != 2:
        if tipo == 1:
            return redirect('/Gaby/Academia')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    profesor = Profesor.objects.get(profesor=request.user)
    academia_profesor_relacion = Academia_Profesor.objects.get(profesor=profesor)    
    grupos = Grupo.objects.filter(academia_profesor=academia_profesor_relacion)

    lista_grupos_promedio = []

    for x in grupos:
        ahora_alumno_cuestionario = Alumno_Cuestionario.objects.filter(grupo=x)
        print ahora_alumno_cuestionario
        suma_por_grupo = 0
        for y in ahora_alumno_cuestionario:
            suma_por_grupo += y.calificacion
        if len(ahora_alumno_cuestionario) != 0:
            promedio = suma_por_grupo / len(ahora_alumno_cuestionario)
        else:
            promedio = 0
        clase = grupoProfesorEstadisticasClase()
        clase.inicializar(x, promedio)
        lista_grupos_promedio.append(clase)


    for x in lista_grupos_promedio:
        print x.grupo
        print x.promedio

    diccionario = {
        'Lista' : lista_grupos_promedio,
    }

    return render(request, 'profesorEstadisticasGrupo.html', diccionario)

class ProfesorCuestionarioEstadisticasClase():
    def inicializar(self, cuestionarioObtenido, aprobadosObtenido, reprobadosObtenido):
        self.cuestionario = cuestionarioObtenido
        self.aprobados = aprobadosObtenido
        self.reprobados = reprobadosObtenido

@login_required(login_url='/Gaby/AccesoAdmins')
def profesorEstadisticasCuestionario(request):
    tipo = mostrarTipo(request.user)
    if tipo != 2:
        if tipo == 1:
            return redirect('/Gaby/Academia')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    profesor = Profesor.objects.get(profesor=request.user)
    academia_profesor_relacion = Academia_Profesor.objects.get(profesor=profesor)    
    grupos = Grupo.objects.filter(academia_profesor=academia_profesor_relacion)

    cuestionarios_promedios = []
    cuestionarios = Cuestionario.objects.filter(academia=academia_profesor_relacion.academia.academia)
    for x in cuestionarios:
        suma_por_cuestionario = 0
        aprobados = 0
        reprobados = 0
        for y in grupos:
            ahora = Alumno_Cuestionario.objects.filter(cuestionario=x, grupo=y)
            for z in ahora:
                if z.calificacion <= 5:
                    reprobados += 1
                else:
                    aprobados += 1
        clase = ProfesorCuestionarioEstadisticasClase()
        clase.inicializar(x, aprobados, reprobados)
        cuestionarios_promedios.append(clase)

    diccionario = {
        'Lista' : cuestionarios_promedios,
    }
    return render(request, 'profesorEstadisticasCuestionarios.html', diccionario)

@login_required(login_url='/Gaby/AccesoAdmins')
def estadisticasAcademia(request):
    tipo = mostrarTipo(request.user)
    if tipo != 1:
        if tipo == 2:
            return redirect('/Gaby/Profesor')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    academia = Academia.objects.get(academia=request.user)
    ObjetosAlumnoAcademiaPromedio = Alumno_Academia_Promedio.objects.filter(academia=academia)
    aprobados = 0
    reprobados = 0
    for elemento in ObjetosAlumnoAcademiaPromedio:
        if elemento.calificacion >= 6.0:
            aprobados += 1
        else:
            reprobados +=1

    busqueda = ""
    if request.method == 'GET':
        busqueda = request.GET.get("busqueda", "")
        results = []
        if busqueda != '' and busqueda != ' ':
            posibles = User.objects.filter(Q(username__icontains=busqueda) | Q(first_name__icontains=busqueda) | Q(last_name__icontains=busqueda) | Q(email__icontains=busqueda))
            for x in posibles:
                try:
                    Es_alumno = Alumno.objects.get(alumno=x)
                    try:
                        resultado_ahora = Alumno_Academia_Promedio.objects.get(alumno=Es_alumno, academia=academia)
                        results.append(resultado_ahora)
                    except:
                        pass
                except:
                    pass

    diccionario = {
        'aprobados': aprobados,
        'reprobados': reprobados,
        'resultados': results,
        'busqueda': busqueda,
    }
    return render(request, 'academiaEstadisticas.html', diccionario)

def home(request):
    if request.method == "POST":
        form = contactosForm(request.POST)
        if form.is_valid():
            nuevo_idea = Contacto(
                nombre = request.POST.get('nombre',''),
                email = request.POST.get('email','')
            )
            nuevo_idea.save()
            if request.POST.get('texto','') != '':
                tema = "Nueva idea enviada por: %s" %nuevo_idea.nombre
                mensaje = request.POST.get('texto','') + "\n\n\n\nCorreo: " + nuevo_idea.email + "\n\nNombre: " + nuevo_idea.nombre
                sender = nuevo_idea.email
                send_mail(
                    tema, mensaje, sender, ['dreediMX@gmail.com'], fail_silently=False
                )
            
            return HttpResponseRedirect("/")
		
        else:
			form = contactosForm()
    
    
    return render(request, 'index.html')


def gaby(request):
	return render(request, 'gaby.html')

def gabyGeneral(request):
	return redirect('gaby')

def loginAdmins(request):
    return render(request, 'loginAdmins.html')

def loginAlumnos(request):
    return render(request, 'loginAlumnos.html')

@login_required(login_url='/Gaby/AccesoAdmins')
def logOut(request):
    logout(request)
    return redirect('gaby')

class grupoAcademiaClase():
    def inicializar(self, profesorObtenido, gruposObtenido):
        self.profesor = profesorObtenido
        self.grupos = gruposObtenido

@login_required(login_url='/Gaby/AccesoAdmins')
def maestrosAcademia(request):
    tipo = mostrarTipo(request.user)
    if tipo != 1:
        if tipo == 2:
            return redirect('/Gaby/Profesor')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    academia = Academia.objects.get(academia=request.user)

    profesores = Academia_Profesor.objects.filter(academia=academia)
    results = None

    grupoProfesor = []
    grupoAcademia = []
    for elementoProfesor in profesores:
        grupoProfesor = Grupo.objects.filter(academia_profesor=elementoProfesor)
        variableClase = grupoAcademiaClase()
        variableClase.inicializar(elementoProfesor, grupoProfesor)
        grupoAcademia.append(variableClase)

    grupoAcademiaBusqueda = []
    if request.method == 'GET':
        nombre = request.GET.get("nombre", "")
        results = []
        if nombre != '' and nombre != ' ':
            posibles = User.objects.filter(Q(username__icontains=nombre) | Q(first_name__icontains=nombre) | Q(last_name__icontains=nombre) | Q(email__icontains=nombre))
            for x in posibles:
                try:
                    Es_profe = Profesor.objects.get(profesor=x)
                    try:
                        Academia_Profesor_PorAhora = Academia_Profesor.objects.get(profesor=Es_profe, academia=academia)
                        results.append(Academia_Profesor_PorAhora)
                    except:
                        pass
                except:
                    pass

            for y in results:
                grupoProfesor = Grupo.objects.filter(academia_profesor=y)
                variableClase = grupoAcademiaClase()
                variableClase.inicializar(y, grupoProfesor)
                grupoAcademiaBusqueda.append(variableClase) 

    diccionario = {
        'resultado': grupoAcademiaBusqueda,
        'grupoAcademia': grupoAcademia,
    }

    return render(request, 'academiaMaestros.html', diccionario)

@login_required(login_url='/Gaby/AccesoAdmins')
def estadisticasAcademiaAlumno(request, idAlumno):
    tipo = mostrarTipo(request.user)
    if tipo != 1:
        if tipo == 2:
            return redirect('/Gaby/Profesor')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    academia = Academia.objects.get(academia=request.user)
    alumnoUsuario = User.objects.get(id=int(idAlumno))
    alumno = Alumno.objects.get(alumno=alumnoUsuario)

    alumnoAcademia = Alumno_Academia_Promedio.objects.get(alumno=alumno)

    alumnoCuestionario = Alumno_Cuestionario.objects.filter(alumno=alumno)

    listaPaEnviar = []

    for a in alumnoCuestionario:
        academiaPorAhora = Academia.objects.get(academia=a.cuestionario.academia)
        if academia == academiaPorAhora:
            listaPaEnviar.append(a)

    diccionario = {
        'alumno':alumno,
        'alumnoAcademia': alumnoAcademia,
        'cuestionarios': listaPaEnviar,
    }
    return render(request, 'academiaEstadisticasAlumno.html', diccionario)


class grupoEstadisticasClase():
    def inicializar(self, grupoObtenido, promedioGrupoObtenido):
        self.grupo = grupoObtenido
        self.promedio = promedioGrupoObtenido

@login_required(login_url='/Gaby/AccesoAdmins')
def estadisticasAcademiaGrupo(request):
    tipo = mostrarTipo(request.user)
    if tipo != 1:
        if tipo == 2:
            return redirect('/Gaby/Profesor')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    academia = Academia.objects.get(academia=request.user)
    RelacionAcademia_Profesor = Academia_Profesor.objects.filter(academia=academia)
    
    Grupos = []
    for x in RelacionAcademia_Profesor:
        grupo = Grupo.objects.filter(academia_profesor=x)
        for y in grupo:
            Grupos.append(y)

    lista_final = []
    for x in Grupos:
        suma_calificacion_por_grupo = 0
        Ahora = Alumno_Cuestionario.objects.filter(grupo=x)
        for y in Ahora:
            suma_calificacion_por_grupo = suma_calificacion_por_grupo + y.calificacion
        if len(Ahora) == 0:
            calificacion_total_por_grupo = 0
        else:
            calificacion_total_por_grupo = suma_calificacion_por_grupo / len(Ahora)  
        ObjetogrupoEstadisticas = grupoEstadisticasClase()
        ObjetogrupoEstadisticas.inicializar(x, calificacion_total_por_grupo)
        lista_final.append(ObjetogrupoEstadisticas)

    busqueda = ""
    if request.method == 'GET':
        busqueda = request.GET.get("busqueda", "")
        results = []
        if busqueda != '' and busqueda != ' ':
            for x in lista_final:
                if busqueda.lower() in x.grupo.nombre.lower():
                    results.append(x)
                

    diccionario = {
        'resultados': results,
        'Lista_final': lista_final,
    }
    return render(request, 'academiaEstadisticasGrupo.html', diccionario)

class ProfesorEstadisticasClase():
    def inicializar(self, profesorObtenido, promedioObtenido):
        self.profesor = profesorObtenido
        self.promedio = promedioObtenido


@login_required(login_url='/Gaby/AccesoAdmins')
def estadisticasAcademiaMaestro(request):
    tipo = mostrarTipo(request.user)
    if tipo != 1:
        if tipo == 2:
            return redirect('/Gaby/Profesor')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    academia = Academia.objects.get(academia=request.user)
    RelacionAcademia_Profesor = Academia_Profesor.objects.filter(academia=academia)
    
    Grupos = []
    for x in RelacionAcademia_Profesor:
        grupo = Grupo.objects.filter(academia_profesor=x)
        for y in grupo:
            Grupos.append(y)

    lista_final = []
    for x in Grupos:
        suma_calificacion_por_grupo = 0
        Ahora = Alumno_Cuestionario.objects.filter(grupo=x)
        for y in Ahora:
            suma_calificacion_por_grupo = suma_calificacion_por_grupo + y.calificacion
        if len(Ahora) == 0:
            calificacion_total_por_grupo = 0
        else:
            calificacion_total_por_grupo = suma_calificacion_por_grupo / len(Ahora)  
        ObjetogrupoEstadisticas = grupoEstadisticasClase()
        ObjetogrupoEstadisticas.inicializar(x, calificacion_total_por_grupo)
        lista_final.append(ObjetogrupoEstadisticas)

    busqueda = ""
    if request.method == 'GET':
        busqueda = request.GET.get("busqueda", "")
        results = []
        if busqueda != '' and busqueda != ' ':
            for x in lista_final:
                if busqueda.lower() in x.grupo.nombre.lower():
                    results.append(x)

    listaProfesoresAcademia = []
    for x in RelacionAcademia_Profesor:
        listaProfesoresAcademia.append(x.profesor)

    listaFinalFinal = []
    for x in listaProfesoresAcademia:
        listaProfesorAhora = []
        suma = 0
        for y in lista_final:
            if y.grupo.academia_profesor.profesor == x:
                listaProfesorAhora.append(y.promedio)
        for z in listaProfesorAhora:
            suma = suma + z

        promedio = 0
        if len(listaProfesorAhora) != 0:
            promedio = suma / len(listaProfesorAhora)
        
        objetoClase = ProfesorEstadisticasClase()
        objetoClase.inicializar(x, promedio)
        listaFinalFinal.append(objetoClase)


    diccionario = {
        'resultados': results,
        'Lista_final': listaFinalFinal,
    }
    return render(request, 'academiaEstadisticasMaestro.html', diccionario)

class CuestionarioEstadisticasClase():
    def inicializar(self, cuestionarioObtenido, aprobadosObtenido, reprobadosObtenido):
        self.cuestionario = cuestionarioObtenido
        self.aprobados = aprobadosObtenido
        self.reprobados = reprobadosObtenido

@login_required(login_url='/Gaby/AccesoAdmins')
def estadisticasAcademiaCuestionario(request):
    tipo = mostrarTipo(request.user)
    if tipo != 1:
        if tipo == 2:
            return redirect('/Gaby/Profesor')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    academia = Academia.objects.get(academia=request.user)
    Todos_los_cuestionarios = Cuestionario.objects.filter(academia=request.user)

    Cuestionarios_mandar = []

    for x in Todos_los_cuestionarios:
        los_alumnos = Alumno_Cuestionario.objects.filter(cuestionario=x)
        suma_por_cuestionario = 0
        aprobados = 0
        reprobados = 0
        for y in los_alumnos:  
            if y.calificacion <= 5:
                reprobados += 1
            else:
                aprobados += 1
        clase = CuestionarioEstadisticasClase()
        clase.inicializar(x, aprobados, reprobados)
        Cuestionarios_mandar.append(clase)
        


    diccionario = {
        'Cuestionarios': Cuestionarios_mandar,
    }
    return render(request, 'academiaEstadisticasCuestionario.html', diccionario)

@login_required(login_url='/Gaby/AccesoAdmins')
def materialAcademia(request):
    tipo = mostrarTipo(request.user)
    if tipo != 1:
        if tipo == 2:
            return redirect('/Gaby/Profesor')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    academia = Academia.objects.get(academia=request.user)

    if request.method == 'POST':
        form = documentoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_recibido = request.FILES['docfile']
            nombreRelacion = 'Aca' + str(academia.id) + 'Doc' + str(archivo_recibido)
            titulo = request.POST.get('Titulo', '')
            nuevo_documento = Documento(nombreRelacion=nombreRelacion, docfile=archivo_recibido, titulo=titulo, academia=academia)
            try:
                nuevo_documento.save()
            except:
                pass
            return HttpResponseRedirect(reverse('materialAcademia'))

    else:
        form = documentoForm()
        print form

    documentos = Documento.objects.filter(academia=academia)
    

    diccionario = {
        'documentos' : documentos,
        'form' : form,
    }
    return render(request, 'academiaMateriales.html', diccionario)

@login_required(login_url='/Gaby/AccesoAdmins')
def materialProfesor(request):
    tipo = mostrarTipo(request.user)
    if tipo != 2:
        if tipo == 1:
            return redirect('/Gaby/Academia')
        else:
            return redirect('/Gaby/AccesoAlumnos')

    profesor = Profesor.objects.get(profesor=request.user)
    relacion_profesor_academia = Academia_Profesor.objects.get(profesor=profesor)
    academia = relacion_profesor_academia.academia

    if request.method == 'POST':
        form = documentoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_recibido = request.FILES['docfile']
            nombreRelacion = 'Aca' + str(academia.id) + 'Doc' + str(archivo_recibido)
            titulo = request.POST.get('Titulo', '')
            nuevo_documento = Documento(nombreRelacion=nombreRelacion, docfile=archivo_recibido, titulo=titulo, academia=academia)
            try:
                nuevo_documento.save()
            except:
                pass
            nombreRelacion2 = 'Documento' + str(nuevo_documento) + 'Profesor' + str(profesor.id) 
            nuevo_documento_profe = Documento_Profesor(nombreRelacion=nombreRelacion2, profesor=profesor, documento=nuevo_documento)
            try:
                nuevo_documento_profe.save()
            except:
                pass
            return HttpResponseRedirect(reverse('materialProfesor'))

    else:
        form = documentoForm()
        print form

    documentos = Documento.objects.filter(academia=academia)
    

    diccionario = {
        'documentos' : documentos,
        'form' : form,
    }
    return render(request, 'profesorMateriales.html', diccionario)