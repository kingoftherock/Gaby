#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

class ContactoAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombre', 'email',)
	list_filter = ('nombre',)
	search_fields = ('nombre', 'email', 'id')

class CuestionarioAdmin(admin.ModelAdmin):
	list_display = ('id', 'titulo','fecha_Creacion', 'academia')
	list_filter = ('id', 'titulo',)
	search_fields = ('id', 'titulo','fecha_Creacion')

class PreguntaAdmin(admin.ModelAdmin):
	list_display = ('id','cuestionario','pregunta','respuestaCorrecta','respuestaIncorrecta1', 'respuestaIncorrecta2', 'respuestaIncorrecta3')
	search_fields = ('id','pregunta',)

class AcademiaAdmin(admin.ModelAdmin):
	list_display = ('id','academia','estado')
	search_fields = ('academia',)

class ProfesorAdmin(admin.ModelAdmin):
	list_display = ('id','profesor',)
	search_fields = ('id' ,'profesor',)

class AcademiaProfesorAdmin(admin.ModelAdmin):
	list_display = ('id','profesor', 'academia')

class GrupoAlumnoAdmin(admin.ModelAdmin):
	list_display = ('id','grupo', 'alumno', 'nombreRelacion')

class GrupoAdmin(admin.ModelAdmin):
	list_display = ('id','nombre', 'academia_profesor',)

class Alumno_CuestionarioAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombreRelacion', 'alumno', 'cuestionario', 'fechaResolucion', 'fechaConclusion', 'contestado', 'calificacion')

class Alumno_Cuestionario_PreguntaAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombreRelacion', 'alumno_cuestionario', 'pregunta', 'respuesta', 'contestado', 'correcto')

class Alumno_Academia_PromedioAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombreRelacion', 'alumno', 'academia', 'calificacion',)

class DocumentoAdmin(admin.ModelAdmin):
	list_display = ('id', 'nombreRelacion', 'titulo', 'docfile', 'academia',)

admin.site.register(Contacto, ContactoAdmin)
admin.site.register(Cuestionario, CuestionarioAdmin)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(Academia, AcademiaAdmin)
admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(Alumno)
admin.site.register(Academia_Profesor, AcademiaProfesorAdmin)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Cuestionario_Profesor_Grupo)
admin.site.register(Grupo_Alumno, GrupoAlumnoAdmin)
admin.site.register(Alumno_Cuestionario, Alumno_CuestionarioAdmin)
admin.site.register(Alumnos_Cuestionario_Pregunta, Alumno_Cuestionario_PreguntaAdmin)
admin.site.register(Alumno_Academia_Promedio, Alumno_Academia_PromedioAdmin)
admin.site.register(Documento, DocumentoAdmin)