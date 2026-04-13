from rest_framework import serializers
from tienda_app.models import Libro, Orden

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'precio']

class OrdenInputSerializer(serializers.Serializer):
    """
    Serializer para VALIDAR la entrada de datos.
    Actua como un DTO (Data Transfer Object).
    """
    libro_id = serializers.IntegerField()
    direccion_envio = serializers.CharField(max_length=200)