from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrdenInputSerializer
from tienda_app.services import CompraService
from tienda_app.infra.factories import PaymentFactory

class CompraAPIView(APIView):
    """
    Endpoint para procesar compras via JSON.
    POST /api/v1/comprar/
    Payload: { "libro_id": 1, "direccion_envio": "Calle 123" }
    """
    def post(self, request):
        # 1. Validacion de entrada (Adapter)
        serializer = OrdenInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        datos = serializer.validated_data

        try:
            # 2. Inyeccion de Dependencias (Factory)
            gateway = PaymentFactory.get_processor()

            # 3. Logica de Negocio (Service Layer) — reutilizada sin cambios
            servicio = CompraService(procesador_pago=gateway)
            resultado = servicio.ejecutar_compra(
                libro_id=datos['libro_id'],
                direccion=datos['direccion_envio'],
                usuario=None
            )
            return Response({
                "estado": "exito",
                "mensaje": f"Orden creada. Total: {resultado}"
            }, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({"error": "Error interno"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)