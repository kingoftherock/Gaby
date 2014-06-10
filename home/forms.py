from django import forms
from django.forms import ModelForm
from models import Contacto, Cuestionario, Pregunta, Grupo, Documento_Profesor, Documento

class contactosForm(ModelForm):
	class Meta:
		model = Contacto

class cuestionariosForm(ModelForm):
	class Meta:
		model = Cuestionario

class grupoForm(ModelForm):
	class Meta:
		model = Grupo

class preguntaForm(ModelForm):
	class Meta:
		model = Pregunta
		fields = ('cuestionario', 'pregunta', 'respuestaCorrecta', 'respuestaIncorrecta1', 'respuestaIncorrecta2', 'respuestaIncorrecta3')

class documentoForm(forms.Form):
	docfile = forms.FileField(
		label = 'Seleccione un archivo'
	)
