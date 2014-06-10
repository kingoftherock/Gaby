from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'home.views.home', name='home'),
    
    url(r'^Gaby/$', 'home.views.gaby', name='gaby'),
    url(r'^gaby/$', 'home.views.gabyGeneral', name='gabyGeneral'),
    url(r'^GABY/$', 'home.views.gabyGeneral', name='gabyGeneral'),
    
    url(r'^Gaby/AccesoAdmins', 'userProfiles.views.loginAdmins', name='loginAdmins'),
    url(r'^registrar$', 'userProfiles.views.registrar', name='registrar'),
    url(r'^registrarProfe$', 'userProfiles.views.registrarProfe', name='registrarProfe'),
    url(r'^entrado$', 'userProfiles.views.entrado', name='entrado'),
    url(r'^salir$', 'userProfiles.views.salir', name='salir'),
    
    url(r'^Gaby/AccesoAlumnos', 'home.views.loginAlumnos', name='loginAlumnos'),
    url(r'^Gaby/Alumno/$', 'home.views.alumno', name='alumno'),
    url(r'^Gaby/Academia/$', 'home.views.academia', name='academia'),
    url(r'^Gaby/Academia/Configuracion', 'home.views.academiaConfiguracion', name='academiaConfiguracion'),

    
    url(r'^Gaby/Academia/Cuestionarios/$', 'home.views.cuestionariosAcademia', name='cuestionariosAcademia'),
    url(r'^Gaby/Academia/Cuestionarios/Borrar', 'home.views.borrar_cuestionario', name='borrar_cuestionario'),
    url(r'^Gaby/Academia/Cuestionarios/Nuevo', 'home.views.cuestionariosAcademiaNuevo', name='cuestionariosAcademiaNuevo'),
    url(r'^Gaby/Academia/Cuestionarios/Cuestionario/(\d+)/', 'home.views.academiaCuestionario', name='academiaCuestionario'),

    
    url(r'^Gaby/Academia/Maestros/$', 'home.views.maestrosAcademia', name='maestrosAcademia'),
    url(r'^Gaby/Academia/Maestros/Registrar/', 'userProfiles.views.maestrosRegistrar', name='maestrosRegistrar'),

    
    url(r'^Gaby/Academia/Estadisticas/$', 'home.views.estadisticasAcademia', name='estadisticasAcademia'),
    url(r'^Gaby/Academia/Estadisticas/Alumno/(\d+)/$', 'home.views.estadisticasAcademiaAlumno', name='estadisticasAcademiaAlumno'),
    url(r'^Gaby/Academia/Estadisticas/Grupo/$', 'home.views.estadisticasAcademiaGrupo', name='estadisticasAcademiaGrupo'),
    url(r'^Gaby/Academia/Estadisticas/Maestro/$', 'home.views.estadisticasAcademiaMaestro', name='estadisticasAcademiaMaestro'),
    url(r'^Gaby/Academia/Estadisticas/Cuestionario/$', 'home.views.estadisticasAcademiaCuestionario', name='estadisticasAcademiaCuestionario'),
    
    url(r'^Gaby/Academia/Material/$', 'home.views.materialAcademia', name='materialAcademia'),

    
    url(r'^Gaby/Academia/Alumnos/$', 'home.views.alumnosAcademia', name='alumnosAcademia'),
    url(r'^Gaby/Academia/Alumnos/Grupo/(\d+)/$', 'home.views.alumnosAcademiaGrupo', name='alumnosAcademiaGrupo'),

    url(r'^Gaby/Profesor/$', 'home.views.profesor', name='profesor'),
    url(r'^Gaby/Profesor/Cuestionarios/$', 'home.views.cuestionariosProfesor', name='cuestionariosProfesor'),
    url(r'^Gaby/Profesor/Cuestionarios/Cuestionario/(\d+)', 'home.views.profesorCuestionario', name='profesorCuestionario'),

    url(r'^Gaby/Profesor/Grupos/$', 'home.views.profesorGrupos', name='profesorGrupos'),
    url(r'^Gaby/Profesor/Grupos/Nuevo/', 'home.views.profesorGruposNuevo', name='profesorGruposNuevo'),
    url(r'^Gaby/Profesor/Grupos/Grupo/(\d+)/$', 'home.views.profesorGrupo', name='profesorGrupo'),
    url(r'^Gaby/Profesor/Grupos/Grupo/(\d+)/Alumnos/$', 'home.views.profesorGrupoAlumnos', name='profesorGrupoAlumnos'),
    url(r'^Gaby/Profesor/Grupos/Grupo/(\d+)/Cuestionarios/$', 'home.views.profesorGrupoCuestionarios', name='profesorGrupoCuestionarios'),

    url(r'^Gaby/Profesor/Estadisticas/$', 'home.views.profesorEstadisticas', name='profesorEstadisticas'),
    url(r'^Gaby/Profesor/Estadisticas/Grupo/$', 'home.views.profesorEstadisticasGrupo', name='profesorEstadisticasGrupo'),
    url(r'^Gaby/Profesor/Estadisticas/Cuestionario/$', 'home.views.profesorEstadisticasCuestionario', name='profesorEstadisticasCuestionario'),

    url(r'^Gaby/Profesor/Material$', 'home.views.materialProfesor', name='materialProfesor'),
    
    url(r'^Gaby/Alumno/Inscribirse/$', 'home.views.alumnoInscripcionAcademia', name='alumnoInscripcionAcademia'),
    url(r'^Gaby/Alumno/Inscribirse/Academia/(\d+)/$', 'home.views.alumnoInscripcionAcademiaEspecifico', name='alumnoInscripcionAcademiaEspecifico'),
    url(r'^Gaby/Alumno/Academia/(\d+)/$', 'home.views.alumnoAcademiaHome', name='alumnoAcademiaHome'),
    url(r'^Gaby/Cuestionario/', 'home.views.alumnoCuestionario', name='alumnoCuestionario'),
    url(r'^Gaby/Alumno/Cuestionario/(\d+)/$', 'home.views.alumnoAcademiaResolverCuestionario', name='alumnoAcademiaResolverCuestionario'),
    #url(r'^Gaby/Alumno/Home', 'home.views.InicioAcademia', name='InicioAcademia'),


    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logOut/$', 'home.views.logOut', name='logOut'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)