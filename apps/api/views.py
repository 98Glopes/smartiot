from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets

from apps.api.filters import ReadFilter
from apps.api.models import Device, Sensor, Read
from apps.api.serializers import UserDetailSerializer, UserSerializer, DeviceCreateSerializer, \
    DeviceSerializer, SensorSerializer, SensorCreateSerializer, ListReadSerializer


class UsersQuerySet:
    @property
    def device(self):
        qs = Device.objects.all()
        qs = qs.filter(user=self.request.user)
        return get_object_or_404(qs, id=self.kwargs['device'])

    @property
    def sensor(self):
        qs = Sensor.objects.all()
        qs = qs.filter(device=self.device)
        return get_object_or_404(qs, id=self.kwargs['sensor'])


class MyUserDetailView(viewsets.ModelViewSet):
    """
    API endpoint that get user information
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated]

    # def get_object(self):
    #     pk = self.kwargs.get('pk')
    #
    #     if pk == "current":
    #         return self.request.user
    #
    #     return super(MyUserDetailView, self).get_object()

    def get_queryset(self):
        qs = User.objects.get(id=self.request.user.id)
        return [qs]


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = []


class DeviceListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        qs = Device.objects.filter(user=self.request.user)
        return qs

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DeviceCreateSerializer
        return DeviceSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeviceRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self, *args, **kwargs):
        qs = Device.objects.all().filter(user=self.request.user)
        return qs

    def get_object(self):
        qs = self.get_queryset()
        obj = get_object_or_404(qs, pk=self.kwargs['device'])
        return obj

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return DeviceCreateSerializer
        else:
            return DeviceSerializer


class SensorListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        qs = Sensor.objects.all().filter(device=self.device)
        return qs

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SensorCreateSerializer
        else:
            return SensorSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "device": self.device
            }
        )
        return context

    def perform_create(self, serializer):
        serializer.save(device=self.device)

    @property
    def device(self):
        qs = Device.objects.all(). \
            filter(user=self.request.user)
        return get_object_or_404(qs, id=self.kwargs['device'])


class SensorRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SensorSerializer

    def get_queryset(self):
        qs = Sensor.objects.filter(device=self.device)
        return qs

    def get_object(self):
        qs = self.get_queryset()
        return get_object_or_404(qs, id=self.kwargs['sensor'])

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return SensorCreateSerializer
        return SensorSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "device": self.device
            }
        )
        return context

    @property
    def device(self):
        qs = Device.objects.all(). \
            filter(user=self.request.user)
        return get_object_or_404(qs, id=self.kwargs['device'])


class ReadListView(generics.ListAPIView, UsersQuerySet):
    serializer_class = ListReadSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = ReadFilter

    def get_queryset(self):
        qs = Read.objects.all().filter(sensor=self.sensor).order_by('-timestamp')
        return qs


