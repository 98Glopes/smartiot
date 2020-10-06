from rest_framework import serializers


class MQTTPayloadSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=4)
    device = serializers.CharField(max_length=4)
    sensor = serializers.CharField(max_length=4)

    raw_value = serializers.CharField(max_length=30)
    gateway_id = serializers.CharField(max_length=30)
    rssi = serializers.FloatField()
    snr = serializers.FloatField()
    timestamp = serializers.DateTimeField()

    read_fields = ['raw_value', 'gateway_id', 'gateway_id', 'rssi', 'snr', 'timestamp', 'sensor']

    def __init__(self, *args, models_providers=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.models = models_providers
        self.model = models_providers.Read

        self.fields['user'].validators = [IdExist(self.models.User.objects.all())]

        device_queryset = self.models.Device.objects.filter(user=kwargs['data']['user'])
        self.fields['device'].validators = [BelongTo(device_queryset, 'id')]
        
        sensor_queryset = self.models.Sensor.objects.filter(device=kwargs['data']['device'])
        self.fields['sensor'].validators = [BelongTo(sensor_queryset, 'id')]

    def create(self, validated_data):
        read_data = {field: validated_data[field] for field in self.read_fields}
        read_data['sensor'] = self.models.Sensor.objects.get(id=read_data['sensor'])

        return self.model(**read_data)


class IdExist:

    def __init__(self, queryset):
        self.queryset = queryset

    def __call__(self, value):
        items = self.queryset.filter(id=value)
        if len(items) == 0:
            raise serializers.ValidationError("Access Denied")
        else:
            return True


class BelongTo:

    def __init__(self, queryset, filter_word):
        """
        Example:
            This device belong to this user?
            So:
                models.Device.filter(user=<str:user_id>).filter(id=<str:value>)
            general:
                queryset = models.Model.filter(owner=<str:owner_id> # External queryset
                in __call_() ->
                items = self.queryset.filter(self.filter_word=value)

        :param queryset: django.queryset
        :param filter_word: str: kwarg to filter the queryset  (queryset.filter(filter_word=value)
        """
        self.queryset = queryset
        self.filter_word = filter_word

    def __call__(self, value):
        filter_set = {self.filter_word: value}
        items = self.queryset.filter(**filter_set)

        if len(items) == 0:
            raise serializers.ValidationError("Access Denied")
        else:
            return True
