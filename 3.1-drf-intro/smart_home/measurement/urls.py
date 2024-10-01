from django.urls import path

from measurement.views import SensorView, AllSensorsView, MeasurementView

urlpatterns = [
    path("sensors/", AllSensorsView.as_view()),
    path("sensors/<int:pk>/", SensorView.as_view()),
    path("measurements/", MeasurementView.as_view()),
]
