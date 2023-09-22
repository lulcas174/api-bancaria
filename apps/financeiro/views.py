from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import date
from drf_yasg.utils import swagger_auto_schema
from apps.base.schema import MENSAGEM_RESPONSE
from drf_yasg import openapi


from apps.financeiro.models import ContaBancaria, Extrato, Transacao
from apps.financeiro.serializers import SaldoContaBancariaSerializer

ENDPOINT_TAGS_CONSULTA=['Consulta-financeiro']
ENDPOINT_TAGS_OPERACAO=['Operacao-financeiro']
CONSULTAR_SALDO = 'Operação para consultar saldo'
CONSULTAR_EXTRATO_MES = 'Operação para consultar o status do mês'
TRANSFERENCIA_CONTA_CORRENTE_POUPANCA = 'Operação para realizar a transferência entre contas'


@swagger_auto_schema(
    method='get',
    responses={
        status.HTTP_200_OK: openapi.Response('', SaldoContaBancariaSerializer),
        status.HTTP_500_INTERNAL_SERVER_ERROR: MENSAGEM_RESPONSE,
        status.HTTP_400_BAD_REQUEST: MENSAGEM_RESPONSE,
    },
    operation_description=CONSULTAR_SALDO,
    operation_summary=CONSULTAR_SALDO,
    tags=ENDPOINT_TAGS_CONSULTA
)
@api_view(["GET"])
def consultar_saldo(request, id_conta):
    try:
        conta = ContaBancaria.objects.get(id=id_conta)
        serializer = SaldoContaBancariaSerializer(conta)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    except ContaBancaria.DoesNotExist:
        return Response(
            {"error": "Conta não encontrada."},
            status=status.HTTP_404_NOT_FOUND
        )


@swagger_auto_schema(
    method='get',
    responses={
        status.HTTP_200_OK: openapi.Response(
            description='', 
            examples={
                'application/json': {
                    "data": "DD/MM/YYYY",
                    "descricao": "string",
                    "saldo": 0
                }
            }
            ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: MENSAGEM_RESPONSE,
        status.HTTP_400_BAD_REQUEST: MENSAGEM_RESPONSE,
    },
    operation_description=CONSULTAR_SALDO,
    operation_summary=CONSULTAR_SALDO,
    tags=ENDPOINT_TAGS_CONSULTA
)
@api_view(["GET"])
def consultar_extrato_mes(request, id_conta):
    data_hoje = date.today()
    try:
        extrato = Extrato.objects.filter(data__month=data_hoje.month, conta_id=id_conta).first()
        data = {
            'data': extrato.data.strftime("%d/%m/%Y"),
            'descricao': extrato.descricao,
            'saldo': extrato.conta.saldo,
        }
        return  Response(data, status=status.HTTP_200_OK)
    except Extrato.DoesNotExist:
        return Response(
            {"error": "Extrato não encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['valor'],
        properties={
            'valor': openapi.Schema(type=openapi.TYPE_NUMBER),  
        }
    ),
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description='Criado',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'data': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                    'descricao': openapi.Schema(type=openapi.TYPE_STRING),
                    'saldo_atual': openapi.Schema(type=openapi.TYPE_NUMBER),
            }
        )
        ),
        status.HTTP_404_NOT_FOUND: 'Conta bancária não encontrada',
    },
    operation_description=TRANSFERENCIA_CONTA_CORRENTE_POUPANCA,
    operation_summary=TRANSFERENCIA_CONTA_CORRENTE_POUPANCA,
    tags=ENDPOINT_TAGS_OPERACAO
)
@api_view(["POST"])
def transferencia_conta_corrente(request,id_conta_corrente, id_conta_poupanca):
    try:
        conta_corrente = ContaBancaria.objects.get(id=id_conta_corrente, tipo_conta='corrente')
    except ContaBancaria.DoesNotExist:
        return Response(
            {"error": "Conta corrente não encontrada."},
            status=status.HTTP_404_NOT_FOUND
        )
    try:
        conta_poupanca = ContaBancaria.objects.get(id=id_conta_poupanca, tipo_conta='poupanca')
    except ContaBancaria.DoesNotExist:
        return Response(
            {"error": "Conta poupança não encontrada."},
            status=status.HTTP_404_NOT_FOUND
        )
    if conta_corrente.titular != conta_poupanca.titular:
        return Response(
            {"error": "Titular das contas diferentes."},
            status=status.HTTP_400_BAD_REQUEST
        )
    if conta_corrente.saldo <= 0:
        return Response(
            {"error": "Saldo insuficiente."},
            status=status.HTTP_400_BAD_REQUEST
        )
    conta_corrente.saldo -= request.data['valor']
    conta_corrente.save()
    conta_poupanca.saldo += request.data['valor']
    conta_poupanca.save()
    
    transacao = Transacao.objects.create(
        conta_origem=conta_corrente,
        conta_destino=conta_poupanca,
        valor=request.data['valor'],
        descricao=request.data['descricao']
    )
    data = Extrato.objects.get(conta__id=transacao.conta_origem.id)
    novo_extrato = {
        'data': data.data.strftime("%d/%m/%Y"),
        'descricao': data.descricao,
        'saldo_atual': data.conta.saldo,
    }
    return Response(
        novo_extrato,
        status=status.HTTP_201_CREATED
    )


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['valor'],
        properties={
            'valor': openapi.Schema(type=openapi.TYPE_NUMBER),  
        }
    ),
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description='Criado',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'data': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                    'descricao': openapi.Schema(type=openapi.TYPE_STRING),
                    'saldo_atual': openapi.Schema(type=openapi.TYPE_NUMBER),
            }
        )
        ),
        status.HTTP_404_NOT_FOUND: 'Conta bancária não encontrada',
    },
    operation_description=TRANSFERENCIA_CONTA_CORRENTE_POUPANCA,
    operation_summary=TRANSFERENCIA_CONTA_CORRENTE_POUPANCA,
    tags=ENDPOINT_TAGS_OPERACAO
)
@api_view(["POST"])
def resgate_poupanca(request, id_conta_corrente, id_conta_poupanca):
    try:
        conta_corrente = ContaBancaria.objects.get(id=id_conta_corrente, tipo_conta='corrente')
    except ContaBancaria.DoesNotExist:
        return Response(
            {"error": "Conta corrente não encontrada."},
            status=status.HTTP_404_NOT_FOUND
        )
    try:
        conta_poupanca = ContaBancaria.objects.get(id=id_conta_poupanca, tipo_conta='poupanca')
    except ContaBancaria.DoesNotExist:
        return Response(
            {"error": "Conta poupança não encontrada."},
            status=status.HTTP_404_NOT_FOUND
        )
    if conta_corrente.titular != conta_poupanca.titular:
        return Response(
            {"error": "Titular das contas diferentes."},
            status=status.HTTP_400_BAD_REQUEST
        )
    if conta_poupanca.saldo <= 0 or conta_poupanca.saldo < request.data['valor']:
        return Response(
            {"error": "Saldo insuficiente."},
            status=status.HTTP_400_BAD_REQUEST
        )
    conta_poupanca.saldo -= request.data['valor']
    conta_poupanca.save()
    conta_corrente.saldo += request.data['valor']
    conta_corrente.save()
    
    transacao = Transacao.objects.create(
        conta_origem=conta_corrente,
        conta_destino=conta_poupanca,
        valor=request.data['valor'],
        descricao=request.data['descricao']
    )
    data = Extrato.objects.get(conta__id=transacao.conta_origem.id)
    novo_extrato = {
        'data': data.data.strftime("%d/%m/%Y"),
        'descricao': data.descricao,
        'saldo_atual_resgate': data.conta.saldo,
    }
    return Response(
        novo_extrato,
        status=status.HTTP_201_CREATED
    )