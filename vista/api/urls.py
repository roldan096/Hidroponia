from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from .views import ZonasInvernaderoApiView

app_name = 'admin_app'
apiviews_patterns = ([
    path('zonas-invernadero/', ZonasInvernaderoApiView.as_view(), name='zonas-invernadero'), 
],"viewsapi")
