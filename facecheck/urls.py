from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login, LoginView, LogoutView
from inicio.views import Sesion, Logout,Seguridad
from seguridad.views import Registrar, Reconociendo, Reconocimiento, Registrar2, Users,Editar, Eliminar

urlpatterns = [
    path('admin/', admin.site.urls),
    # login y logout
    path('sesion/', Sesion, name="sesion"),
    path('inicio/', LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user = True), name="login"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('seguridad/', Seguridad, name='seguridad'),
    path('logout/', Logout, name='logout'),
    # seguridad
    path('registrar/', Registrar, name='registrar'),
    path('registro/', Registrar2, name='registro'),
    path('reconocimiento/', Reconocimiento, name='reconocimiento'),
    path('reconociendo/', Reconociendo, name="reconociendo"),
    path('users/', Users, name='users'),
    path("editar/<int:id>/", Editar, name='editar'),
    path("eliminar/<int:id>/", Eliminar, name='eliminar'),
]