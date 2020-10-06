import json

from dependency.django_models import DjangoModels
from services.serializers import MQTTPayloadSerializer


class Collector:
    models = DjangoModels()
    serializer = MQTTPayloadSerializer

    def insert_data_from_mqtt(self, payload):
        if isinstance(payload, str):
            payload = json.loads(payload.replace("'", '"'))
        else:
            raise ValueError("Payload serialization failed")

        print(F"Started data insertion to user: {payload['user']} "
              F"device: {payload['device']} "
              F"sensor: {payload['sensor']}")

        serializer = MQTTPayloadSerializer(data=payload, models_providers=self.models)

        validation = serializer.is_valid()
        if not validation:
            print(f"Payload is not valid, erros: {serializer.errors}")
            # raise ValueError(f"Payload is not valid, error: {serializer.errors}")
            return None

        try:
            instance = serializer.save()
            instance.save()
            print(F"Finished insertion for {instance}")

        except Exception as e:
            print(F"Insertion failed: {e}")
            return None
