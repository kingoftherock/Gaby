#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from userProfiles.models import Tipo
from django.contrib.auth.models import User

# Create your models here.
class Academia(models.Model):
	academia = models.ForeignKey(User)
	estado = models.BooleanField(default=False)

	def __unicode__(self):
		return self.academia.first_name

class Profesor(models.Model):
	profesor = models.ForeignKey(User)

	def __unicode__(self):
		return self.profesor.first_name

class Alumno(models.Model):
	alumno = models.ForeignKey(User)
	nombre = models.CharField(max_length=100)
	apellido = models.CharField(max_length=100)

	def __unicode__(self):
		return self.alumno.first_name

class Contacto(models.Model):
    nombre = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    def __unicode__(self):
		return self.email

class Cuestionario(models.Model):
	titulo = models.CharField(max_length=255)
	fecha_Creacion = models.DateField(auto_now=True)
	academia = models.ForeignKey(User)

	def __unicode__(self):
		return self.titulo

class Pregunta(models.Model):
	cuestionario = models.ForeignKey(Cuestionario)
	pregunta =models.CharField(max_length=255, unique=True)
	respuestaCorrecta = models.CharField(max_length=255)
	respuestaIncorrecta1 = models.CharField(max_length=255)
	respuestaIncorrecta2 = models.CharField(max_length=255)
	respuestaIncorrecta3 = models.CharField(max_length=255)

	def __unicode__(self):
		return self.pregunta

class Academia_Profesor(models.Model):
	academia = models.ForeignKey(Academia)
	profesor = models.ForeignKey(Profesor)

	def __unicode__(self):
		return self.profesor.profesor.first_name

class Grupo(models.Model):
	nombre = models.CharField(max_length=255)
	academia_profesor = models.ForeignKey(Academia_Profesor)

	def __unicode__(self):
		return self.nombre

class Grupo_Alumno(models.Model):
	nombreRelacion = models.CharField(max_length=255, unique=True)
	grupo = models.ForeignKey(Grupo)
	alumno = models.ForeignKey(Alumno)	

class Cuestionario_Profesor_Grupo(models.Model):
	nombreRelacion = models.CharField(max_length=255, unique=True)
	cuestionario = models.ForeignKey(Cuestionario)
	activo = models.BooleanField(default=False)
	grupo = models.ForeignKey(Grupo)
	numeroPreguntas = models.IntegerField(default=0)

	def __unicode__(self):
		return self.nombreRelacion

class Alumno_Cuestionario(models.Model):
	nombreRelacion = models.CharField(max_length=255, unique=True)
	alumno = models.ForeignKey(Alumno)
	cuestionario = models.ForeignKey(Cuestionario)
	grupo = models.ForeignKey(Grupo)
	fechaResolucion = models.DateTimeField()
	fechaConclusion = models.DateTimeField()
	contestado = models.BooleanField(default=False)
	calificacion = models.DecimalField(default=0.0, max_digits=4, decimal_places=2)
	def __unicode__(self):
		return self.nombreRelacion

class Alumnos_Cuestionario_Pregunta(models.Model):
	nombreRelacion = models.CharField(max_length=255, unique=True)
	alumno_cuestionario = models.ForeignKey(Alumno_Cuestionario)
	pregunta = models.ForeignKey(Pregunta)
	respuesta = models.CharField(max_length=255, default="No ha contestado")
	contestado = models.BooleanField(default = False)
	correcto = models.BooleanField(default = False)
	def __unicode__(self):
		return self.nombreRelacion

class Alumno_Academia_Promedio(models.Model):
	nombreRelacion = models.CharField(max_length=255, unique=True)
	alumno = models.ForeignKey(Alumno)
	academia = models.ForeignKey(Academia)
	calificacion = models.DecimalField(default=0.0, max_digits=4, decimal_places=2)

class Documento(models.Model):
	nombreRelacion = models.CharField(max_length=255, unique=True)
	docfile = models.FileField(upload_to = 'documents/%Y/%m/%d')
	titulo = models.CharField(max_length=255)
	academia = models.ForeignKey(Academia)
	def __unicode__(self):
		return self.titulo

class Documento_Profesor(models.Model):
	nombreRelacion = models.CharField(max_length=255, unique=True)
	profesor = models.ForeignKey(Profesor)
	documento = models.ForeignKey(Documento)
	def __unicode__(self):
		return self.nombreRelacion