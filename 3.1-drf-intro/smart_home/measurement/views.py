from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView

from .serializers import SensorSerializer, AllSensorsSerializer, MeasurementAddSerializer
from .models import Sensor, Measurement


class AllSensorsView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = AllSensorsSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SensorView(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class MeasurementView(CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementAddSerializer
