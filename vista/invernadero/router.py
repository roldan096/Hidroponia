from api.viewsets import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('invernadero',InvernaderoViewset)
router.register('zona',ZonaViewset)
router.register('tratamiento',TratamientoViewset)
router.register('horario',HorarioViewset)
router.register('solucion',SolucionViewset)
router.register('nutriente',NutrienteViewset)
router.register('planta',PlantaViewset)
router.register('tanque',TanqueViewset)
router.register('sensor',SensorViewset)
