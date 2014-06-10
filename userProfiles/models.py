from django.db import models
from django.contrib.auth.models import User

class Tipo(models.Model):
	tipo = models.IntegerField()
	usuario = models.ForeignKey(User, unique=True)
	def __unicode__(self):
		return self.usuario.first_name