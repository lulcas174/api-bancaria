from drf_yasg import openapi

MENSAGEM_RESPONSE = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'mensagem': openapi.Schema(
            type=openapi.TYPE_STRING
        )
    }
)