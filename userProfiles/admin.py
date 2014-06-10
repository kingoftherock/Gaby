from django.contrib import admin
from models import Tipo
from django.contrib.auth.models import User

class TipoAdmin(admin.ModelAdmin):
	list_display = ('id' ,'tipo', 'usuario')
	list_filter = ('id' ,'tipo', 'usuario')
	search_fields = ('id' ,'tipo', 'usuario')

admin.site.register(Tipo, TipoAdmin)
