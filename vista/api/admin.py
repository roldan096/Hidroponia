from django.contrib import admin

# Register your models here.
from .models import Invernadero,Nutriente,Solucion,Horario,Tratamiento,Zona,Tanque,Sensor,Planta
# Register your models here.

class invernaderoAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

class nutrienteAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

class solucionAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

class horarioAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

class tratamientoAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

class zonaAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

class tanqueAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

class sensorAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

class plantaAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)



admin.site.register(Invernadero,invernaderoAdmin)
admin.site.register(Nutriente,nutrienteAdmin)
admin.site.register(Solucion,solucionAdmin)
admin.site.register(Horario,horarioAdmin)
admin.site.register(Tratamiento,tratamientoAdmin)
admin.site.register(Zona,zonaAdmin)
admin.site.register(Tanque,tanqueAdmin)
admin.site.register(Sensor,sensorAdmin)
admin.site.register(Planta,plantaAdmin)
