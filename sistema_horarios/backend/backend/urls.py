from django.contrib import admin
from django.urls import path, include  # <--- 1. Asegúrate de importar 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 2. Agrega esta línea. 
    # Cambia 'nombre_de_tu_app' por el nombre real de la carpeta donde tienes tus views.py
    path('api/', include('escuela.urls')), 
]